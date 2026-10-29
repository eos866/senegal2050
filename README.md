# Sénégal 2050

Application web de consultation de l'**Agenda national de transformation Sénégal 2050 – Masterplan 2025-2034**.

Son ergonomie reprend celle de l'application CAP 28 (plan stratégique du Département d'Eure-et-Loir). Elle comprend :

- **Accueil** : présentation, chiffres clés, accès direct aux 27 objectifs stratégiques par tuiles colorées selon l'axe, liste filtrable (axe, type de contenu, recherche plein texte) ;
- **Fiches objectif** (`#os-1-1` … `#os-4-4`) : objectifs spécifiques et résultats attendus, programmes avec projets et réformes, indicateurs (référence 2023 → cible 2034), projets localisés ;
- **Table des indicateurs** : les indicateurs du Masterplan, filtrables par axe ;
- **Territoires** : carte des 14 régions (aplats ou cercles proportionnels, limites départementales), lieux des projets colorés par axe, tracé de la ligne Dakar-Kidira, encart sur la presqu'île du Cap-Vert, puis cartogramme schématique des régions et 8 pôles de croissance ; un clic sur une région (carte ou cartogramme) ou sur un lieu filtre la liste et zoome la carte, un clic sur un projet de la liste l'affiche seul sur la carte ;
- **Masterplan 2025-2034** : chaîne de planification, 4 axes et impacts attendus, trajectoires économiques ;
- **Documents** et **Arborescence** (axes → objectifs → programmes).

## Charte graphique

Les jetons de la charte sont regroupés dans `charte.css` (également intégrés à `index.html`).

| Rôle | Clair | Sombre |
|---|---|---|
| Fond / surface | `#F3F6F1` / `#FFFFFF` | `#0E1511` / `#16201A` |
| Texte / texte secondaire | `#13201A` / `#56665C` | `#E6EDE8` / `#97A89D` |
| Accent (vert baobab) | `#0A6B3B` | `#4CC38A` |
| Drapeau | vert `#00853F` · or `#F2C230` · rouge `#D9262E` | identique |
| Axe 1 · Économie (ocre) | `#B87A06` | `#E3A83A` |
| Axe 2 · Capital humain (latérite) | `#BF3B28` | `#EA7560` |
| Axe 3 · Aménagement (vert) | `#277A4A` | `#5BC086` |
| Axe 4 · Gouvernance (bleu Atlantique) | `#1D5C88` | `#5EA9DD` |

Typographies (Google Fonts) : **Archivo** étroit et gras pour les titres et les chiffres, **IBM Plex Sans** pour le texte, **IBM Plex Mono** pour les étiquettes, codes et valeurs. Signes distinctifs : mini-drapeau dans l'en-tête, filet tricolore en pied de page, frise d'horizon 2025 → 2029 → 2034 → 2050, titres de section en capitales.

## Utilisation

L'application tient dans un seul fichier `index.html`, sans dépendance à installer. Ouvrez-le dans un navigateur ou publiez le dépôt avec GitHub Pages (Settings → Pages → branche `main`, dossier `/`).

## Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `index.html` | Application (données intégrées) |
| `charte.css` | Jetons et styles de la charte graphique |
| `data/objectifs.json` | Les 27 objectifs stratégiques : objectifs spécifiques, programmes, projets, réformes, indicateurs |
| `data/projets-localises.json` | Projets et réformes citant un lieu : lieux (coordonnées) et régions |
| `data/limites-regions-departements.json` | Limites simplifiées des 14 régions et 45 départements (GADM 4.1) |
| `scripts/geolocaliser.py` | Géolocalisation des projets par lieu (gazetier) |
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
- Limites administratives : GADM 4.1, licence **non commerciale**, reprises de l'Observatoire des territoires du Sénégal. Pour un usage commercial, les remplacer par les limites officielles (DTGC, ANAT) ou geoBoundaries (CC BY 4.0).
- Lieux : OpenStreetMap (ODbL) ; les sites hors agglomération (Sangomar, delta du Saloum, Casamance, Ndayane) sont positionnés de façon approchée.
- Application non officielle, réalisée à titre de démonstration. Elle ne remplace pas le document de référence.

## Source

Agenda national de transformation Sénégal 2050 – Masterplan 2025-2034, Gouvernement du Sénégal.
