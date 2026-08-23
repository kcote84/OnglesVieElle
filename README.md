# OnglesVieElle

Site vitrine d'**Ongles Vie-Elle** — salon d'ongles à Saint-Éloi (MRC des Basques, Bas-Saint-Laurent, Québec).

- **Page** : `index.html` — fichier unique, autonome (CSS + JS + images en base64), aucune dépendance obligatoire.
- **Réservation** : https://dactyl.mobile/book/GKhDXe5cruTzijekcXE49rnb5Qv2
- **Facebook** : https://www.facebook.com/profile.php?id=61587640748664

## Modifier le site

`index.html` n'est pas édité à la main : il est assemblé à partir de `_sources/`.

```bash
cd _sources
python build.py      # régénère ../index.html
```

| Fichier | Contenu |
| --- | --- |
| `_sources/part1_head.html` | `<head>`, métadonnées SEO, Open Graph, favicon |
| `_sources/part2_css.html` | feuille de style complète |
| `_sources/part3_body_a.html` | icônes SVG, en-tête, hero, services, techniques |
| `_sources/part4_body_b.html` | galerie, à propos, avis, zone desservie, FAQ, pied de page |
| `_sources/part5_tail.html` | JSON-LD (schema.org) et JavaScript |
| `_sources/asset_*.txt` | images encodées en data-URI (`{{LOGO}}`, `{{G1}}`…`{{SALON}}`) |

## À finaliser avant la mise en ligne

1. Remplacer le domaine placeholder `https://www.onglesvieelle.ca/` (balise `canonical`, `og:url`, `twitter:image`, `og:image` et champ `url` du JSON-LD).
2. Déposer une image de partage `og-image.jpg` (1200 × 630) à la racine du site.
3. Confirmer la ville : elle est déduite du code postal G0L 2V0, Facebook ne l'affiche pas.
4. Ajouter les heures d'ouverture réelles (`openingHoursSpecification` dans le JSON-LD).

Les hypothèses et les sources des données sont documentées en commentaire au début d'`index.html`.
