# -*- coding: utf-8 -*-
"""Genere l'image de partage Open Graph (1200x630) a la racine du site.

    cd _sources && python make_og_image.py     # ecrit ../og-image.jpg

Sources : asset_G1.txt (photo heros) et asset_LOGO.txt (logo de la cliente),
les memes data-URI que celles embarquees dans index.html — l'image de partage
reste donc automatiquement coherente avec le site.
"""
import base64, io, os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, os.pardir, "og-image.jpg")

W, H = 1200, 630
PANEL = 660                      # largeur du panneau creme, la photo occupe le reste
PAD = 74

CREAM = (251, 246, 241)          # --cream
CREAM_2 = (244, 234, 224)        # --cream-2
INK = (46, 33, 27)               # --ink
GOLD_DP = (142, 103, 47)         # --gold-dp
GOLD = (185, 139, 78)            # --gold
GOLD_LT = (227, 198, 143)        # --gold-lt

SERIF = "C:/Windows/Fonts/georgia.ttf"        # substitut de Cormorant Garamond
SANS = "C:/Windows/Fonts/segoeuisl.ttf"       # Segoe UI Semilight, dans la pile --sans


def asset(token):
    """Decode _sources/asset_<token>.txt vers une image Pillow."""
    raw = io.open(os.path.join(HERE, "asset_%s.txt" % token), encoding="utf-8").read().strip()
    return Image.open(io.BytesIO(base64.b64decode(raw.split(",", 1)[1])))


def tracked(draw, xy, text, font, fill, tracking=0):
    """Dessine du texte avec un interlettrage, absent de Pillow."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x - xy[0] - tracking


def tracked_width(draw, text, font, tracking=0):
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)


def keyed_logo(img):
    """Detoure le fond quasi blanc du logo pour le poser sur le creme."""
    img = img.convert("RGBA")
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            m = min(r, g, b)
            if m >= 250:
                px[x, y] = (r, g, b, 0)
            elif m > 238:
                px[x, y] = (r, g, b, int(a * (250 - m) / 12.0))
    return img


def build():
    card = Image.new("RGB", (W, H), CREAM)

    # --- fond du panneau : degrade vertical creme tres doux, pour la profondeur
    grad = Image.new("RGB", (1, H))
    gd = grad.load()
    for y in range(H):
        t = y / float(H - 1)
        gd[0, y] = tuple(int(CREAM[i] + (CREAM_2[i] - CREAM[i]) * t) for i in range(3))
    card.paste(grad.resize((PANEL, H), Image.BILINEAR), (0, 0))

    # --- photo heros a droite, recadree sans agrandissement
    photo = asset("G1").convert("RGB")
    pw, ph = W - PANEL, H
    ratio = pw / float(ph)
    cw = min(photo.width, int(photo.height * ratio))
    ch = int(cw / ratio)
    left = (photo.width - cw) // 2
    top = max(0, int((photo.height - ch) * 0.34))          # garde les ongles dans le cadre
    photo = photo.crop((left, top, left + cw, top + ch)).resize((pw, ph), Image.LANCZOS)
    card.paste(photo, (PANEL, 0))

    # --- filet dore vertical a la jonction, en echo aux filets du site
    seam = Image.new("RGB", (1, H))
    sd = seam.load()
    for y in range(H):
        t = y / float(H - 1)
        a, b = (GOLD_LT, GOLD_DP) if t < .5 else (GOLD_DP, GOLD_LT)
        u = (t * 2) if t < .5 else (t - .5) * 2
        sd[0, y] = tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))
    card.paste(seam.resize((3, H), Image.BILINEAR), (PANEL - 1, 0))

    # --- ombre portee douce du panneau sur la photo
    sh = Image.new("L", (60, H), 0)
    shd = ImageDraw.Draw(sh)
    for x in range(60):
        shd.line([(x, 0), (x, H)], fill=int(46 * (1 - x / 59.0)))
    card.paste(Image.new("RGB", (60, H), (60, 42, 32)), (PANEL + 2, 0), sh)

    draw = ImageDraw.Draw(card)

    # --- logo de la cliente
    logo = keyed_logo(asset("LOGO"))
    lw = 322
    logo = logo.resize((lw, int(lw * logo.height / float(logo.width))), Image.LANCZOS)
    card.paste(logo, (PAD, 74), logo)

    # --- titre : mentionne Saint-Eloi
    f_ttl = ImageFont.truetype(SERIF, 55)
    draw.text((PAD, 320), "Pose d\u2019ongles", font=f_ttl, fill=INK)
    f_ttl_i = ImageFont.truetype("C:/Windows/Fonts/georgiai.ttf", 55)
    x = PAD
    draw.text((x, 386), "\u00e0 ", font=f_ttl, fill=INK)
    x += draw.textlength("\u00e0 ", font=f_ttl)
    draw.text((x, 386), "Saint-\u00c9loi", font=f_ttl_i, fill=GOLD_DP)

    # --- filet + ligne de service, en petites capitales espacees
    draw.rectangle([PAD, 481, PAD + 54, 482], fill=GOLD)
    f_sm = ImageFont.truetype(SANS, 20)
    tracked(draw, (PAD, 508), "R\u00c9SINE & POUDRE \u00b7 GEL \u00b7 SUR RENDEZ-VOUS",
            f_sm, GOLD_DP, tracking=2.4)

    # --- signature discrete en bas du panneau
    f_xs = ImageFont.truetype(SANS, 18)
    tracked(draw, (PAD, 552), "BAS-SAINT-LAURENT, QU\u00c9BEC", f_xs, (123, 106, 95), tracking=2.0)

    card = card.filter(ImageFilter.UnsharpMask(radius=.7, percent=42, threshold=3))

    best = None
    for q in range(90, 59, -1):
        buf = io.BytesIO()
        card.save(buf, "JPEG", quality=q, optimize=True, progressive=True, subsampling=1)
        best = (q, buf.getvalue())
        if len(best[1]) <= 190000:
            break
    q, data = best
    open(OUT, "wb").write(data)
    print("OK og-image.jpg  %dx%d  q%d  %.1f KB" % (W, H, q, len(data) / 1024.0))


if __name__ == "__main__":
    build()
