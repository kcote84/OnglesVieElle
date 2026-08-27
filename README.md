# OnglesVieElle

Site vitrine d'**Ongles Vie-Elle** — salon d'ongles à Saint-Éloi (MRC des Basques, Bas-Saint-Laurent, Québec).

- **Site en ligne** : https://www.onglesvieelle.ca/ — domaine officiel actif, servi en HTTPS par GitHub Pages. La version sans `www` redirige vers `www`.
- **Page** : `index.html` — fichier unique, autonome (CSS + JS + images en base64), aucune dépendance obligatoire.
- **Partage social** : `og-image.jpg` (1200 × 630) — seul fichier externe, référencé par `og:image`.
- **Réservation** : https://dactyl.mobile/book/GKhDXe5cruTzijekcXE49rnb5Qv2
- **Facebook** : https://www.facebook.com/profile.php?id=61587640748664

## Domaine et référencement

`https://www.onglesvieelle.ca/` est l'URL canonique définitive : elle est utilisée par
`canonical`, `og:url`, `og:image`, `twitter:image` et le JSON-LD.

| Fichier (racine) | Rôle |
| --- | --- |
| `CNAME` | domaine personnalisé de GitHub Pages — contient exactement `www.onglesvieelle.ca` |
| `robots.txt` | autorise l'indexation complète et déclare le sitemap |
| `sitemap.xml` | site d'une seule page : ne contient que `https://www.onglesvieelle.ca/` |
| `favicon.ico` | 16 + 32 + 48 px — icône affichée par Google Search et les onglets |
| `favicon-48.png` | 48 × 48 — format préféré de Google Search |
| `apple-touch-icon.png` | 180 × 180 — écran d'accueil iOS |

`robots.txt`, `sitemap.xml` et `CNAME` sont **statiques** : ils sont versionnés tels quels à la racine et ne sont
pas générés par `_sources/build.py` (rien à y interpoler). `sitemap.xml` n'inclut pas de
`<lastmod>`, faute d'un processus qui pourrait le tenir à jour de façon fiable.

La page reste indexable (`<meta name="robots" content="index, follow, max-image-preview:large">`)
et aucune règle ne bloque Googlebot.

## Modifier le site

`index.html` n'est pas édité à la main : il est assemblé à partir de `_sources/`.

```bash
cd _sources
python build.py           # régénère ../index.html
python make_og_image.py   # régénère ../og-image.jpg
python make_favicon.py    # régénère ../favicon.ico, favicon-48.png, apple-touch-icon.png
```

| Fichier | Contenu |
| --- | --- |
| `_sources/part1_head.html` | `<head>`, métadonnées SEO, Open Graph, favicon |
| `_sources/part2_css.html` | feuille de style complète |
| `_sources/part3_body_a.html` | icônes SVG, en-tête, hero, services, techniques |
| `_sources/part4_body_b.html` | galerie, à propos, avis, zone desservie, FAQ, pied de page |
| `_sources/part5_tail.html` | JSON-LD (schema.org) et JavaScript |
| `_sources/asset_*.txt` | images encodées en data-URI (`{{LOGO}}`, `{{G1}}`…`{{SALON}}`) |
| `_sources/make_og_image.py` | génère `og-image.jpg` à partir de `asset_G1` + `asset_LOGO` |
| `_sources/make_favicon.py` | génère les trois favicons depuis la version simplifiée du logo |

## À finaliser

1. ~~Remplacer le domaine placeholder par le domaine officiel.~~ — fait : `https://www.onglesvieelle.ca/` est actif et utilisé partout (`canonical`, Open Graph, Twitter, JSON-LD, `CNAME`, `robots.txt`, `sitemap.xml`).
2. ~~Déposer une image de partage `og-image.jpg` (1200 × 630) à la racine du site.~~ — fait : déployée à la racine, elle répond en HTTP 200 (`og:image` la référence en URL absolue).
3. Confirmer la ville : elle est déduite du code postal G0L 2V0, Facebook ne l'affiche pas.
4. Ajouter les heures d'ouverture réelles (`openingHoursSpecification` dans le JSON-LD).
5. Remplacer le `geo` du JSON-LD (centroïde du code postal) par les coordonnées exactes du local.

Les hypothèses et les sources des données sont documentées en commentaire au début d'`index.html`.
