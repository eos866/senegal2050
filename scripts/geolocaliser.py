import json,re
d=json.load(open('src/os_clean.json'))
G=json.load(open('eos866/observatoire-territoires-senegal/data/geodata.json'))
CODES={'SN-DK':'Dakar','SN-KD':'Kolda','SN-MT':'Matam','SN-KA':'Kaffrine','SN-KE':'Kédougou','SN-SE':'Sédhiou','SN-ZG':'Ziguinchor','SN-DB':'Diourbel','SN-SL':'Saint-Louis','SN-TC':'Tambacounda','SN-KL':'Kaolack','SN-TH':'Thiès','SN-LG':'Louga','SN-FK':'Fatick'}
# lieu: (regex, région, lon, lat)  — coordonnées OSM (lieux habités) ou approximatives (≈) pour les sites
GAZ=[('Dakar',r'\bDakar\b(?!-Kidira)','Dakar',-17.448,14.693),
 ('Diamniadio',r'Diamniadio','Dakar',-17.184,14.720),('Diass',r'\bDiass\b','Thiès',-17.084,14.642),
 ('Bargny / Sendou',r'Sendou|Bargny','Dakar',-17.217,14.682),('Yoff',r'\bYoff\b','Dakar',-17.475,14.752),
 ('Gorée',r'Gorée','Dakar',-17.398,14.667),('Ndayane',r'Ndayane','Thiès',-17.075,14.535),
 ('Thiès',r'\bThiès\b','Thiès',-16.926,14.792),('Touba',r'\bTouba\b','Diourbel',-15.876,14.865),
 ('Delta du Saloum',r'Saloum','Fatick',-16.55,13.90),('Sangomar',r'Sangomar','Fatick',-16.765,13.835),
 ('Foundiougne',r'Foundiougne','Fatick',-16.468,14.126),('Toubacouta',r'Toubacouta','Fatick',-16.475,13.784),
 ('Fatick',r'\bFatick\b','Fatick',-16.404,14.334),('Kaolack',r'\bKaolack\b','Kaolack',-16.076,14.139),
 ('Louga',r'\bLouga\b','Louga',-16.223,15.612),('Saint-Louis',r'Saint-Louis','Saint-Louis',-16.505,16.028),
 ('Matam',r'\bMatam\b','Matam',-13.256,15.657),('Lacs de Bakel',r'Bakel','Tambacounda',-12.457,14.905),
 ('Kidira',r'Kidira','Tambacounda',-12.214,14.457),('Kédougou',r'Kédougou','Kédougou',-12.186,12.557),
 ('Bassin de l’Anambé',r'Anambé','Kolda',-14.172,12.942),('Ziguinchor',r'Ziguinchor','Ziguinchor',-16.273,12.564),
 ('Casamance',r'Casamance','Ziguinchor',-16.15,12.72)]
LINES=[('Dakar-Kidira',r'Dakar-Kidira',[[-17.448,14.693],[-16.926,14.792],[-15.876,14.865],[-15.548,14.102],[-13.668,13.769],[-12.214,14.457]])]
loc=[]
for o in d:
  for p in o['programmes']:
    for kind in ('projets','reformes'):
      for it in p[kind]:
        pl=[]
        for nm,rx,rg,x,y in GAZ:
          if re.search(rx,it) and not (nm=='Delta du Saloum' and 'Sangomar' in it):
            pl.append({'n':nm,'r':rg,'x':x,'y':y})
        # régions « dans les régions de Fatick et Kaolack »
        ln=[l[2] for l in LINES if re.search(l[1],it)]
        if ln: pl=[q for q in pl if q['n'] not in('Dakar',)]+[{'n':'Dakar','r':'Dakar','x':-17.448,'y':14.693}]
        if pl or ln:
          regs=sorted({q['r'] for q in pl}|({'Tambacounda','Dakar'} if ln else set()))
          loc.append({'os':o['id'],'k':'projet' if kind=='projets' else 'réforme','txt':it,'regions':regs,'places':pl,'line':ln[0] if ln else None})
geo={'reg':{CODES[k]:v[0] for k,v in G['reg'].items()},'dep':[{'n':n,'r':CODES[v['reg']],'g':v['rings']} for n,v in G['dep'].items()]}
json.dump(loc,open('src/loc2.json','w'),ensure_ascii=False)
json.dump(geo,open('src/geo.json','w'),separators=(',',':'),ensure_ascii=False)
from collections import Counter
print(len(loc),Counter(r for l in loc for r in l['regions']))
for l in loc: print(l['os'],[q['n'] for q in l['places']],l['txt'][:80])
