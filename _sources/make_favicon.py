# -*- coding: utf-8 -*-
"""
Genere les icones publiques du site a partir de la VERSION SIMPLIFIEE du logo
(le <symbol id="mark"> de part3_body_a.html) : pastille espresso, ongle amande
et coeur en degrade or. Le logo complet n'est PAS utilise : il est trop charge
pour 16-48 px.

    python make_favicon.py

Sorties (racine du site) :
    favicon.ico           16 + 32 + 48 px, chaque taille rendue separement
    favicon-48.png        48 x 48
    apple-touch-icon.png  180 x 180

Chaque taille est rasterisee depuis la geometrie vectorielle avec un
sur-echantillonnage x8 puis reduite en LANCZOS : le rendu reste net a 16 px.
"""
import io, os
from PIL import Image, ImageDraw

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ESPRESSO = (0x2E, 0x21, 0x1B)
GOLD = ((0xEB, 0xD3, 0xA2), (0xC0, 0x91, 0x3F), (0x8E, 0x67, 0x2F))

SS = 8  # sur-echantillonnage

# --- geometrie reprise telle quelle du <symbol id="mark"> (repere 64 x 64) ----
# Ongle amande : sommet en (32, 15.5), largeur maximale 16.8, hauteur 25.3.
NAIL = [
    ((32, 15.5), (37.9, 21.5), (40.4, 27.2), (40.4, 32)),
    ((40.4, 32), (40.4, 37.2), (36.7, 40.8), (32, 40.8)),
    ((32, 40.8), (27.3, 40.8), (23.6, 37.2), (23.6, 32)),
    ((23.6, 32), (23.6, 27.2), (26.1, 21.5), (32, 15.5)),
]
# Coeur : pointe basse en (32, 51.5), largeur 10, hauteur 8.3.
HEART = [
    ((32, 51.5), (29, 49.4), (27, 47.8), (27, 45.7)),
    ((27, 45.7), (27, 44.2), (28.1, 43.2), (29.5, 43.2)),
    ((29.5, 43.2), (30.4, 43.2), (31.3, 43.7), (32, 44.6)),
    ((32, 44.6), (32.7, 43.7), (33.6, 43.2), (34.5, 43.2)),
    ((34.5, 43.2), (35.9, 43.2), (37, 44.2), (37, 45.7)),
    ((37, 45.7), (37, 47.8), (35, 49.4), (32, 51.5)),
]


def flatten(curves, steps=160):
    """Convertit une suite de cubiques de Bezier en polygone."""
    pts = []
    for p0, p1, p2, p3 in curves:
        for i in range(steps):
            t = i / steps
            u = 1 - t
            pts.append((
                u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
                u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1],
            ))
    return pts


def place(pts, scale, cx, cy):
    """Recentre puis redimensionne un polygone autour de (cx, cy)."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ox = (min(xs) + max(xs)) / 2
    oy = (min(ys) + max(ys)) / 2
    return [((x - ox) * scale + cx, (y - oy) * scale + cy) for x, y in pts]


def gold_gradient(size, box):
    """Degrade or diagonal (haut-gauche -> bas-droite) sur la boite du motif."""
    x0, y0, x1, y1 = box
    span = max((x1 - x0) + (y1 - y0), 1e-6)
    grad = Image.new("RGB", (size, size), GOLD[1])
    px = grad.load()
    for y in range(size):
        for x in range(size):
            t = min(max(((x - x0) + (y - y0)) / span, 0.0), 1.0)
            if t < 0.5:
                a, b, k = GOLD[0], GOLD[1], t * 2
            else:
                a, b, k = GOLD[1], GOLD[2], (t - 0.5) * 2
            px[x, y] = (
                int(a[0] + (b[0] - a[0]) * k),
                int(a[1] + (b[1] - a[1]) * k),
                int(a[2] + (b[2] - a[2]) * k),
            )
    return grad


def render(size):
    """Rend l'icone a `size` px via un canevas sur-echantillonne.

    A 16 px le coeur evide se refermerait en une tache illisible : cette taille
    recoit donc l'ongle plein. Les tailles 32 px et plus portent le coeur.
    """
    big = size * SS
    k = big / 64.0

    nail = place(flatten(NAIL), 1.85, 32, 32)
    mask = Image.new("L", (big, big), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(x * k, y * k) for x, y in nail], fill=255)
    if size >= 32:
        heart = place(flatten(HEART), 1.8, 32, 37)
        md.polygon([(x * k, y * k) for x, y in heart], fill=0)

    xs = [x for x, _ in nail]
    ys = [y for _, y in nail]
    box = (min(xs) * k, min(ys) * k, max(xs) * k, max(ys) * k)

    canvas = Image.new("RGB", (big, big), ESPRESSO)
    canvas.paste(gold_gradient(big, box), (0, 0), mask)
    return canvas.resize((size, size), Image.LANCZOS)


def main():
    ico = [render(s) for s in (48, 32, 16)]
    ico[0].save(os.path.join(OUT, "favicon.ico"), format="ICO",
                sizes=[(48, 48), (32, 32), (16, 16)], append_images=ico[1:])
    render(48).save(os.path.join(OUT, "favicon-48.png"), format="PNG", optimize=True)
    render(180).save(os.path.join(OUT, "apple-touch-icon.png"), format="PNG", optimize=True)
    for f in ("favicon.ico", "favicon-48.png", "apple-touch-icon.png"):
        path = os.path.join(OUT, f)
        print("%-22s %6d o" % (f, os.path.getsize(path)))


if __name__ == "__main__":
    main()
