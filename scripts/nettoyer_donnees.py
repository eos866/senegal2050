import json,re
d=json.load(open('src/os.json'))
def clean(s):
    s=re.sub(r'(\w)- (\w)',lambda m:m.group(1)+m.group(2) if m.group(2).islower() else m.group(0),s)
    s=s.replace('æ','').replace(' ,',',').replace(' .','.')
    return re.sub(r'\s+',' ',s).strip(' ;.')
for o in d:
    o['titre']=clean(o['titre']).rstrip('|').strip()
    if o['titre'].isupper(): o['titre']=o['titre'].capitalize()
    o['programmes']=[p for p in o['programmes'] if p['nom'].strip() not in ('Programme','Programmes')]
    for p in o['programmes']:
        p['nom']=clean(p['nom']); p['projets']=[clean(x) for x in p['projets'] if len(clean(x))>3]; p['reformes']=[clean(x) for x in p['reformes'] if len(clean(x))>3]
    for ob in o['objectifs']:
        ob['nom']=clean(ob['nom']); ob['resultats']=[clean(x) for x in ob['resultats']]
    o['objectifs']=[ob for ob in o['objectifs'] if ob['nom'] or ob['resultats']]
    o['indicateurs']=[[clean(r[0])]+[c.strip() for c in r[1:3]] for r in o['impact']+o['activites'] if r and r[0].strip() and len(r)>=3]
    del o['impact'],o['activites']
# drop copy of 1.1 agro rows in 1.3
o13=d[2]; o13['indicateurs']=[r for r in o13['indicateurs'] if not re.search(r'insécurité alimentaire|agroalimentaire|Contribution du secteur \(\*\)|Emplois formels et informels',r[0])]
# dedupe indicators
for o in d:
    seen=set(); o['indicateurs']=[r for r in o['indicateurs'] if not (tuple(r) in seen or seen.add(tuple(r)))]
places={'Dakar':['Dakar','Diamniadio','Bargny','Rufisque','Yoff','Pikine','Guédiawaye'],'Thiès':['Thiès','Ndayane','Mbour','Tivaouane','Kayar','Joal','Mboro','Saly'],'Diourbel':['Diourbel','Touba','Mbacké','Bambey'],'Fatick':['Fatick','Sangomar','Foundiougne','Saloum'],'Kaolack':['Kaolack','Nioro','Dakhonga'],'Kaffrine':['Kaffrine'],'Louga':['Louga','Linguère','Kébémer'],'Saint-Louis':['Saint-Louis','Podor','Dagana','Richard-Toll','Grand Tortue','GTA'],'Matam':['Matam','Ourossogui','Kanel'],'Tambacounda':['Tambacounda','Bakel','Niokolo','Kidira'],'Kédougou':['Kédougou','Saraya','Sabodala'],'Kolda':['Kolda','Anambé','Vélingara'],'Sédhiou':['Sédhiou'],'Ziguinchor':['Ziguinchor','Cap Skirring','Bignona','Oussouye']}
loc=[]
for o in d:
  for p in o['programmes']:
    for kind in ('projets','reformes'):
      for it in p[kind]:
        regs=[r for r,ks in places.items() if any(re.search(r'\b'+re.escape(k)+r'\b',it) for k in ks)]
        cas='Casamance' in it
        if regs or cas: loc.append({'os':o['id'],'txt':it,'regions':regs,'casamance':cas})
json.dump(d,open('src/os_clean.json','w'),ensure_ascii=False)
json.dump(loc,open('src/loc.json','w'),ensure_ascii=False,indent=0)
print(len(loc)); from collections import Counter; c=Counter(r for l in loc for r in l['regions']); print(c, sum(l['casamance'] for l in loc))
print(sum(len(p['projets']) for o in d for p in o['programmes']),sum(len(p['reformes']) for o in d for p in o['programmes']),sum(len(o['programmes']) for o in d),sum(len(o['indicateurs']) for o in d))
for l in loc: print(l['os'],l['regions'],l['txt'][:110])
