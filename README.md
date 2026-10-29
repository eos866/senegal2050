# Sénégal 2050

Application web de consultation de l'**Agenda national de transformation Sénégal 2050 – Masterplan 2025-2034**.

Elle présente :

- la vision et l'horizon de planification (2025 → 2029 → 2034 → 2050) ;
- la chaîne de planification (prospective, planification, programmation, budgétisation, suivi-évaluation) ;
- les 4 axes stratégiques et leurs impacts attendus en 2034 ;
- les trajectoires économiques et macroéconomiques (tableaux 1 et 2 du Masterplan) ;
- un explorateur des 27 objectifs stratégiques : programmes, projets, réformes, objectifs spécifiques et indicateurs (référence 2023 → cible 2034), avec recherche plein texte et filtre par axe ;
- une vue territoriale : les 8 pôles de croissance et les projets qui citent explicitement un lieu, par région.

## Utilisation

L'application tient dans un seul fichier `index.html`, sans dépendance à installer. Ouvrez-le dans un navigateur ou publiez le dépôt avec GitHub Pages (Settings → Pages → branche `main`, dossier `/`).

## Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `index.html` | Application (données intégrées) |
| `data/objectifs.json` | Les 27 objectifs stratégiques : objectifs spécifiques, programmes, projets, réformes, indicateurs |
| `data/projets-localises.json` | Projets et réformes citant un lieu, rattachés à leur région |
| `scripts/extraire_tableaux.py` | Extraction des tableaux du PDF (pdfplumber) |
| `scripts/nettoyer_donnees.py` | Nettoyage des données et géolocalisation par région |
| `scripts/template.html` | Gabarit de la page, dans lequel les données sont injectées |

### Régénérer les données

```bash
pip install pdfplumber
mkdir -p src
python3 scripts/extraire_tableaux.py agenda_de_transformation_2050.pdf   # écrit src/os.json
python3 scripts/nettoyer_donnees.py                                     # écrit src/os_clean.json et src/loc.json
python3 -c "t=open('scripts/template.html').read(); t=t.replace('/*OSDATA*/',open('src/os_clean.json').read()).replace('/*LOCDATA*/',open('src/loc.json').read()); open('page.html','w').write(t)"
```

## Limites

- Les données sont extraites automatiquement des tableaux du PDF ; quelques intitulés de projets ou de réformes peuvent être découpés imparfaitement.
- La vue territoriale est un cartogramme schématique des 14 régions, pas une carte géographique.
- Application non officielle, réalisée à titre de démonstration. Elle ne remplace pas le document de référence.

## Source

Agenda national de transformation Sénégal 2050 – Masterplan 2025-2034, Gouvernement du Sénégal.
