import pdfplumber,re,json,sys
P=sys.argv[1]
OS_ORDER=[f"1.{i}" for i in range(1,10)]+[f"2.{i}" for i in range(1,9)]+[f"3.{i}" for i in range(1,7)]+[f"4.{i}" for i in range(1,5)]
def items(cell):
    if not cell: return []
    lines=[l.strip() for l in cell.split('\n') if l.strip()]
    bul=sum(1 for l in lines if l[0] in '-•–')>=1
    out=[]
    for l in lines:
        t=re.sub(r'^[•\-–]\s*','',l)
        if re.match(r'^[A-ZÉ] [a-zé]',t): t=t[0]+t[2:]
        if bul: new = l[0] in '-•–' or not out
        else:
            prev=out[-1] if out else ''
            new = (not out) or (t[0].isupper() and prev.count('(')<=prev.count(')') and not re.search(r"(-|,| de| des| du| et| la| le| à| aux| en| d’| l’|:)$",prev))
        if new: out.append(t)
        else:
            out[-1]= out[-1][:-1]+t if re.search(r'\w-$',out[-1]) else out[-1]+' '+t
    return [re.sub(r'\s+',' ',o).strip(' ;') for o in out if len(o.strip())>1]
data={k:{"id":k,"objectifs":[],"programmes":[],"impact":[],"activites":[]} for k in OS_ORDER}
cur=None; mode=None; seen=[]; cad=[]
with pdfplumber.open(P) as pdf:
  for pn in range(12,128):
    for t in pdf.pages[pn].extract_tables():
      rows=[[c or '' for c in r] for r in t]
      if not rows: continue
      first=rows[0][0].replace('\n',' ')
      m=re.match(r'OS\.?\s*(\d\.\d)',first)
      hdr=' | '.join(' '.join(r) for r in rows[:2])
      if m:
        # determine OS by order: cadre tables advance
        if 'Objectifs spécifiques' in hdr:
            cur=OS_ORDER[len(cad)]; cad.append(cur); mode='obj'
            data[cur]['titre']=re.sub(r'^OS\.?\s*\d\.\d\.?\s*','',first).strip(' |æ')
        else:
            mid=m.group(1)
            if mid in data: cur=mid
            mode='prog'
        rows=[r for r in rows[1:] if not re.match(r'(Objectifs spécifiques|Programmes)',r[0].strip())]
      elif rows[0][0].startswith('Indicateurs d'):
        mode='impact' if 'impact' in rows[0][0] else 'activites'
        data[cur][mode]+= [[re.sub(r'\s+',' ',c).strip() for c in r] for r in rows[1:]]
        continue
      if cur is None: continue
      for r in rows:
        if mode=='obj' and len(r)>=2:
          name=re.sub(r'\s+',' ',r[0]).strip()
          res=items(r[-1])
          if name: data[cur]['objectifs'].append({"nom":name,"resultats":res})
          elif res and data[cur]['objectifs']: data[cur]['objectifs'][-1]['resultats']+=res
        elif mode=='prog' and len(r)>=3:
          name=re.sub(r'\s+',' ',r[0]).strip()
          pj=items(r[1]); rf=items(r[2])
          if name: data[cur]['programmes'].append({"nom":name,"projets":pj,"reformes":rf})
          elif data[cur]['programmes']:
              data[cur]['programmes'][-1]['projets']+=pj; data[cur]['programmes'][-1]['reformes']+=rf
json.dump(list(data.values()),open('src/os.json','w'),ensure_ascii=False,indent=1)
for d in data.values():
  print(d['id'],d.get('titre','??')[:60],len(d['objectifs']),len(d['programmes']),sum(len(p['projets']) for p in d['programmes']),sum(len(p['reformes']) for p in d['programmes']),len(d['impact']),len(d['activites']))
