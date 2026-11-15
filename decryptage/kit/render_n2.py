# « Le Décryptage SPIRIT » — habillage motion design 4:5 (1080x1350, 25 i/s)
import os, sys, os, math, subprocess, random, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import icons
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = '/home/claude/kit_minute_conseil/assets/'
W, H, FPS = 1080, 1350, 25
INTRO, DUR, OUTRO = 7.3, 83.0, 5.94
TOTAL = INTRO + DUR + OUTRO
RED, GOLD, WHITE, INK, GREY = (216, 51, 63), (190, 150, 70), (255, 255, 255), (24, 23, 28), (170, 168, 172)
def font(w, px): return ImageFont.truetype(KIT + 'fonts/Poppins-' + w + '.ttf', int(px))
def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def eio(x): x = max(0.0, min(1.0, x)); return 0.5 - 0.5 * math.cos(math.pi * x)
def fit_w(im, w): return im.resize((w, max(1, int(im.height * w / im.width))), Image.LANCZOS)
def rgba(c, a): return tuple(c) + (int(max(0, min(255, a))),)
def spaced(d, cx, y, tx, f, fill, sp=0.0, left=False):
    ws = [d.textlength(c, font=f) for c in tx]; tw = sum(ws) + sp * (len(tx) - 1); x = cx if left else cx - tw / 2
    for c, w_ in zip(tx, ws): d.text((x, y), c, font=f, fill=fill); x += w_ + sp
    return tw
def ctext(d, cx, y, tx, f, fill): d.text((cx - d.textlength(tx, font=f) / 2, y), tx, font=f, fill=fill)
def fmt(v, dec=1): return f'{v:.{dec}f}'.replace('.', ',')

LOGO = Image.open(KIT + 'logo_spirit.png').convert('RGBA'); LOGO = LOGO.crop(LOGO.getbbox())
def logo_white(w):
    l = fit_w(LOGO, w); wl = Image.new('RGBA', l.size, (255, 255, 255, 255)); wl.putalpha(l.getchannel('A')); return wl
LOGO_S = logo_white(170)

# ---------- fonds ----------
def make_bg():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    a = np.zeros((H, W, 3), np.float32) + np.array([20, 19, 25], np.float32)
    a += np.exp(-(((x - W * 0.95) / (W * 0.5)) ** 2 + ((y + 50) / (H * 0.35)) ** 2))[:, :, None] * np.array([70, 8, 14], np.float32)
    a += np.exp(-(((x - W * 0.05) / (W * 0.5)) ** 2 + ((y - H * 1.05) / (H * 0.3)) ** 2))[:, :, None] * np.array([45, 8, 12], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGB').convert('RGBA')
BG = make_bg()
def make_intro_bg(fn='abidjan.png', base=0.50, peak=0.30, cy=0.50, sg=0.26):
    ph = Image.open(HERE + '/photos/' + fn).convert('RGB').resize((W, H), Image.LANCZOS)
    a = np.asarray(ph, np.float32)
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    dark = base + peak * np.exp(-(((y - cy) / sg) ** 2))
    a = a * (1 - dark)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a += np.exp(-(((xx - W * 0.95) / (W * 0.5)) ** 2 + ((yy + 50) / (H * 0.35)) ** 2))[:, :, None] * np.array([70, 8, 14], np.float32)
    a += np.exp(-(((xx - W * 0.05) / (W * 0.5)) ** 2 + ((yy - H * 1.05) / (H * 0.3)) ** 2))[:, :, None] * np.array([45, 8, 12], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGB').convert('RGBA')
def vgrad(h, top, bot, power=1.0):
    g = (np.linspace(0, 1, h) ** power); a = (top + (bot - top) * g) * 255
    im = Image.new('RGBA', (W, h), (12, 11, 15, 0)); im.putalpha(Image.fromarray(np.tile(a[:, None], (1, W)).astype('uint8'))); return im
GR_TOP, GR_BOT = vgrad(420, 0.78, 0.0, 1.0), vgrad(520, 0.0, 0.86, 1.3)
GR_PHOTO = Image.new('RGBA', (W, H), (12, 11, 15, 0)); GR_PHOTO.putalpha(Image.fromarray((np.tile(np.concatenate([np.linspace(0.50, 0.14, 520), np.linspace(0.14, 0.30, 300), np.linspace(0.30, 0.82, 530)])[:, None], (1, W)) * 255).astype('uint8')))

# ---------- photos (effet Ken Burns) ----------
PH = {}
for name, fy in (('chantier', 0.62), ('atelier', 0.72), ('port', 0.5), ('bureau', 0.55)):
    im = Image.open(HERE + f'/photos/{name}.png').convert('RGB'); im = im.resize((1300, int(im.height * 1300 / im.width)), Image.LANCZOS)
    y0 = int(fy * (im.height - 1625)); PH[name] = im.crop((0, y0, 1300, y0 + 1625))
def photo(name, k, drift=1):
    z = 1.0 + 0.10 * k; bw, bh = 1300 / z, 1625 / z; mx, my = 1300 - bw, 1625 - bh
    x0 = mx * (0.5 + drift * (0.5 - k) * 0.6); y0 = my * 0.5
    return PH[name].crop((int(x0), int(y0), int(x0 + bw), int(y0 + bh))).resize((W, H), Image.BILINEAR)

# ---------- images du consultant ----------
PF = HERE + '/pf/p%05d.jpg'; NPF = len(os.listdir(HERE + '/pf'))
def pframe(ts):
    i = max(1, min(NPF, int(round(ts * FPS)) + 1)); return Image.open(PF % i).convert('RGB')
def rmask(w, h, r):
    m = Image.new('L', (w * 3, h * 3), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w * 3 - 1, h * 3 - 1), radius=r * 3, fill=255); return m.resize((w, h), Image.LANCZOS)
PIP = (60, 880, 330)           # x, y, taille
SRC_FULL, SRC_PIP = (0, 0, 1080, 1350), (190, 30, 890, 730)
def lerp(a, b, k): return a + (b - a) * k
def consultant(ts, k):
    """k=0 plein cadre, k=1 vignette"""
    fr = pframe(ts); e = eio(k)
    sx = [lerp(SRC_FULL[i], SRC_PIP[i], e) for i in range(4)]
    dx = [lerp(0, PIP[0], e), lerp(0, PIP[1], e), lerp(W, PIP[0] + PIP[2], e), lerp(H, PIP[1] + PIP[2], e)]
    dw, dh = int(round(dx[2] - dx[0])), int(round(dx[3] - dx[1]))
    part = fr.crop(tuple(int(v) for v in sx)).resize((dw, dh), Image.LANCZOS).convert('RGBA')
    part.putalpha(rmask(dw, dh, int(lerp(0, 34, e)))); return part, (int(dx[0]), int(dx[1])), e

# ---------- ouverture ----------
ZONES = [('CÔTE D’IVOIRE', 'crane', 'chantier'), ('BÉNIN', 'bolt', 'atelier'), ('CEDEAO', 'globe', 'port'), ('CEMAC', 'bank', 'bureau')]
def chip(lay, cx, cy, size, ic, label, k, active=1.0, lab_sz=24):
    if k <= 0: return
    d = ImageDraw.Draw(lay); s = int(size * (0.8 + 0.2 * ease(k))); x0, y0 = cx - s // 2, cy - s // 2
    d.rounded_rectangle((x0, y0, x0 + s, y0 + s), radius=int(s * 0.2), fill=rgba((255, 255, 255), 22 * k), outline=rgba(RED if active >= 1 else (255, 255, 255), 255 * k * (1 if active >= 1 else 0.35)), width=3)
    icn = icons.get(ic, int(s * 0.5), rgba(WHITE, 255 * k * (1 if active >= 1 else 0.5))); lay.alpha_composite(icn, (cx - icn.width // 2, cy - icn.height // 2))
    if label: spaced(d, cx, y0 + s + 16, label, font('Medium', lab_sz), rgba(WHITE, 255 * k * (1 if active >= 1 else 0.6)), 2)

BGI = make_intro_bg()
BGO = make_intro_bg('afrique_nuit.png', 0.22, 0.38, 0.47, 0.22)
SCR = 'ABCDEFGHKMNRSTUVXZ0123456789#%&/'
def intro(t):
    im = BGI.copy(); lay = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(lay)
    # grille animée discrète
    for i in range(-1, 14):
        x = (i * 90 + t * 14) % (W + 90) - 45; d.line((x, 0, x, H), fill=rgba(WHITE, 9), width=1)
    for j in range(0, 16):
        y = (j * 90 - t * 10) % (H + 90) - 45; d.line((0, y, W, y), fill=rgba(WHITE, 9), width=1)
    sy = (t * 520) % (H + 300) - 150; d.rectangle((0, sy, W, sy + 3), fill=rgba(RED, 70))
    k = ease(t / 0.6); lg = logo_white(300); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * k))); lay.alpha_composite(lg, ((W - 300) // 2, int(120 - (1 - k) * 20)))
    # « décryptage » : lettres brouillées qui se résolvent
    tx = 'LE DÉCRYPTAGE'; f = font('Bold', 98); rnd = random.Random(int(t * 25)); ws = [d.textlength(c, font=f) for c in tx]; tw = sum(ws); x = (W - tw) / 2
    for i, c in enumerate(tx):
        r = 0.55 + i * 0.075
        if t >= r + 0.22 or c == ' ': ch, col = c, WHITE + (255,)
        elif t >= 0.5: ch, col = rnd.choice(SCR), rgba(RED, 230)
        else: ch, col = ' ', WHITE + (0,)
        if t >= 0.5: d.text((x, 405), ch, font=f, fill=col)
        x += ws[i]
    k2 = ease((t - 1.7) / 0.5)
    if k2 > 0:
        f2 = font('Bold', 118); ctext(d, W / 2, 512 + (1 - k2) * 26, 'ÉCONOMIQUE', f2, rgba(RED, 255 * k2))
        lw = 240 * ease((t - 2.1) / 0.5); d.rounded_rectangle((W / 2 - lw / 2, 668, W / 2 + lw / 2, 673), radius=2, fill=RED + (255,))
    k3 = ease((t - 2.5) / 0.6)
    if k3 > 0: spaced(d, W / 2, 702 + (1 - k3) * 12, 'L’ANALYSE STRATÉGIQUE DE LA SEMAINE', font('Medium', 29), rgba(GOLD, 255 * k3), 4)
    xs = [150, 400, 650, 900]
    for i, (nm, ic, _) in enumerate(ZONES):
        kk = ease((t - 3.0 - i * 0.4) / 0.5); chip(lay, xs[i] - 0 if False else [165, 415, 665, 915][i] - 0, 1000, 170, ic, nm, kk, 1.0, 21)
    k5 = ease((t - 5.2) / 0.6)
    if k5 > 0: spaced(d, W / 2, 1232, 'N° 2', font('Regular', 24), rgba(GREY, 255 * k5), 5)
    im.alpha_composite(lay); return im

def outro(t, last):
    im = BGO.copy(); lay = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(lay)
    if last is not None and t < 0.7:
        k = eio(t / 0.7); edge = int(W * (1 - k)); m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, 0, edge, H), fill=255)
        im.paste(last.convert('RGB'), (0, 0), m); d.rectangle((edge - 6, 0, edge + 6, H), fill=RED + (255,))
    for i in range(-1, 14):
        x = (i * 90 + t * 14) % (W + 90) - 45; d.line((x, 0, x, H), fill=rgba(WHITE, 9 if t > 0.7 else 0), width=1)
    k = ease((t - 0.7) / 0.6)
    if k > 0:
        lg = logo_white(560); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * k))); lay.alpha_composite(lg, ((W - 560) // 2, int(250 - (1 - k) * 24)))
    k2 = ease((t - 1.1) / 0.6)
    if k2 > 0:
        ctext(d, W / 2, 560 + (1 - k2) * 18, 'Rendez-vous la semaine prochaine', font('Medium', 50), rgba(WHITE, 255 * k2))
        ctext(d, W / 2, 628 + (1 - k2) * 18, 'pour un nouveau', font('Medium', 50), rgba(WHITE, 255 * k2))
        ctext(d, W / 2, 696 + (1 - k2) * 18, 'Décryptage économique', font('Bold', 56), rgba(RED, 255 * k2))
        lw = 240 * ease((t - 1.5) / 0.5); d.rounded_rectangle((W / 2 - lw / 2, 782, W / 2 + lw / 2, 787), radius=2, fill=RED + (255,))
    for i, (nm, ic, _) in enumerate(ZONES): chip(lay, [165, 415, 665, 915][i], 890, 130, ic, nm, ease((t - 1.8 - i * 0.2) / 0.5), 1.0, 20)
    k4 = ease((t - 2.6) / 0.6)
    if k4 > 0:
        ctext(d, W / 2, 1075 + (1 - k4) * 10, 'Cabinet expert en Intelligence Économique, Expérience Client', font('Light', 29), rgba(WHITE, 255 * k4))
        ctext(d, W / 2, 1118 + (1 - k4) * 10, 'et Transformation de la Performance', font('Light', 29), rgba(WHITE, 255 * k4))
        ctext(d, W / 2, 1215, os.environ.get('SITE', 'www.spirit-ci.com   ·   www.spirit-bj.com'), font('Regular', 30), rgba(GOLD, 255 * k4))
    im.alpha_composite(lay); return im

# ---------- corps : éléments communs ----------
def topbar(lay, ts):
    d = ImageDraw.Draw(lay); kb = ease((ts - 0.3) / 0.5)
    d.rectangle((0, 0, W, 7), fill=rgba(WHITE, 60)); d.rectangle((0, 0, int(W * min(1, ts / DUR)), 7), fill=RED + (255,))
    if kb > 0:
        f1, f2 = font('Bold', 27), font('Medium', 19); w = 560
        d.rounded_rectangle((36, 44, 36 + w, 144), radius=24, fill=rgba(INK, 205 * kb), outline=rgba(WHITE, 40 * kb), width=2)
        d.ellipse((62, 70, 78, 86), fill=rgba(RED, 255 * kb)); d.text((92, 58), 'LE DÉCRYPTAGE ÉCONOMIQUE', font=f1, fill=rgba(WHITE, 255 * kb))
        spaced(d, 64, 102, 'N° 2', f2, rgba(GOLD, 255 * kb), 3, True)
        lg = LOGO_S.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * kb))); lay.alpha_composite(lg, (W - lg.width - 40, 62))

def glass(lay, x, y, w, h, a=1.0, accent=True, r=28):
    sh = Image.new('RGBA', (w + 80, h + 80)); ImageDraw.Draw(sh).rounded_rectangle((40, 52, 40 + w, 52 + h), radius=r, fill=(0, 0, 0, int(110 * a)))
    lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (x - 40, y - 40))
    d = ImageDraw.Draw(lay); d.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=rgba(INK, 168 * a), outline=rgba(WHITE, 60 * a), width=2)
    if accent: d.rounded_rectangle((x, y + 24, x + 9, y + h - 24), radius=4, fill=rgba(RED, 255 * a))

def bignum(d, cx, cy, val, unit, size=190, a=1.0, dec=1, thousands=False):
    s = f'{val:,.0f}'.replace(',', ' ') if thousands else fmt(val, dec); f, fu = font('Bold', size), font('Bold', int(size * 0.42))
    tw, uw = d.textlength(s, font=f), d.textlength(' ' + unit, font=fu); x = cx - (tw + uw) / 2
    d.text((x, cy - size * 0.62), s, font=f, fill=rgba(WHITE, 255 * a)); d.text((x + tw, cy + size * 0.06), ' ' + unit, font=fu, fill=rgba(RED, 255 * a))

def label(d, cx, y, tx, a=1.0): spaced(d, cx, y, tx, font('Medium', 27), rgba(GOLD, 255 * a), 5)
def sub(d, cx, y, tx, a=1.0, sz=36, col=WHITE): ctext(d, cx, y, tx, font('Medium', sz), rgba(col, 235 * a))
def src(d, cx, y, tx, a=1.0): ctext(d, cx, y, tx, font('Light', 24), rgba(GREY, 255 * a))

PX, PY, PW, PH_ = 60, 300, 960, 540
def hchain(d, lay, items, tl, a):
    """chaîne horizontale d'icônes reliées par des flèches, qui se révèlent à tour de rôle"""
    n = len(items); step = PW / n
    for i, (ic, tx1, tx2) in enumerate(items):
        k = ease((tl - 0.3 - i * 0.55) / 0.5) * a; cx = int(PX + step * (i + 0.5))
        if k <= 0: continue
        icn = icons.get(ic, 150, rgba(RED if i == n - 1 else WHITE, 255 * k)); lay.alpha_composite(icn, (cx - 75, int(PY + 130 + (1 - k) * 20)))
        ctext(d, cx, PY + 310, tx1, font('Bold', 34 if n < 3 else 28), rgba(WHITE, 255 * k)); ctext(d, cx, PY + 354, tx2, font('Medium', 25), rgba(GREY, 255 * k))
        if i < n - 1:
            ka = ease((tl - 0.55 - i * 0.55) / 0.4) * a
            if ka > 0:
                ar = icons.get('arrow', 62, rgba(GOLD, 255 * ka)); lay.alpha_composite(ar, (int(PX + step * (i + 1)) - 31, PY + 176))

def bars(d, tl, a, items, base, maxv, hmax=250, bw=170):
    n = len(items); step = PW / n
    for i, (lab, v, col, vtxt) in enumerate(items):
        k = ease((tl - 0.2 - i * 0.45) / 0.8) * a; cx = int(PX + step * (i + 0.5)); h = int(hmax * v / maxv * k)
        d.rounded_rectangle((cx - bw // 2, base - h, cx + bw // 2, base), radius=14, fill=rgba(col, 255 * a))
        if k > 0.15: ctext(d, cx, base - h - 54, vtxt, font('Bold', 42), rgba(WHITE, 255 * min(1, (k - 0.15) * 3) * a))
        ctext(d, cx, base + 14, lab, font('Medium', 26), rgba(GREY, 255 * a))

# états : (début, fin, fonction)
def st(lay, d, tl, a, kind):
    cx = PX + PW // 2
    def pill(txt, k, y=405, w=460):
        if k > 0:
            d.rounded_rectangle((cx - w // 2, PY + y - (1 - k) * 12, cx + w // 2, PY + y + 50 - (1 - k) * 12), radius=25, fill=rgba(RED, 255 * k)); ctext(d, cx, PY + y + 6 - (1 - k) * 12, txt, font('Bold', 29), rgba(WHITE, 255 * k))
    if kind == 'ci0':
        icn = icons.get('megaphone', 120, rgba(WHITE, 255 * a)); lay.alpha_composite(icn, (cx - 60, PY + 42))
        label(d, cx, PY + 180, 'LANCEMENT · ABIDJAN', a)
        ctext(d, cx, PY + 235, '12', font('Bold', 150), rgba(WHITE, 255 * a)); sub(d, cx, PY + 410, 'NOVEMBRE 2026', a, 40, RED)
        src(d, cx, PY + 480, 'Programme national de réduction de l’informalité', a)
    elif kind == 'ci1':
        label(d, cx, PY + 50, 'PART DE L’INFORMALITÉ', a); bars(d, tl, a, [('2018', 91.9, GREY, '91,9 %'), ('2025', 82.3, RED, '82,3 %')], PY + 435, 100.0, 240, 190)
        src(d, cx, PY + 495, 'Agence nationale de la statistique', a)
    elif kind == 'ci2': hchain(d, lay, [('people', 'NOUVEAUX CLIENTS', 'un marché qui se structure'), ('check', 'CONCURRENTS', 'qui deviennent formels')], tl, a); label(d, cx, PY + 50, 'CE QUE CELA CHANGE', a)
    elif kind == 'bj0':
        label(d, cx, PY + 50, 'PROJET DE BUDGET 2027', a); bignum(d, cx, PY + 235, 4757 * ease(tl / 1.8), 'Mds FCFA', 150, a, 0, True)
        sub(d, cx, PY + 365, 'contre 4 148 Mds FCFA en 2026', a, 34); src(d, cx, PY + 470, 'Conseil des ministres du Bénin', a)
    elif kind == 'bj1':
        label(d, cx, PY + 50, 'BUDGET DE L’ÉTAT · MDS FCFA', a); bars(d, tl, a, [('2026', 4148, GREY, '4 148'), ('2027', 4757, RED, '4 757')], PY + 455, 4757.0, 230, 190)
        pill('+14,7 %', ease((tl - 1.6) / 0.5) * a, 96, 240)
    elif kind == 'bj2': hchain(d, lay, [('people', 'HÔPITAUX', 'et écoles'), ('bolt', 'ÉNERGIE', ''), ('globe', 'NUMÉRIQUE', '')], tl, a); label(d, cx, PY + 50, 'COMMANDE PUBLIQUE EN HAUSSE', a)
    elif kind == 'ce0':
        label(d, cx, PY + 50, 'TAUX DIRECTEUR BCEAO', a); bignum(d, cx, PY + 255, 3 * ease(tl / 1.6), '%', 210, a, 0)
        sub(d, cx, PY + 390, 'maintenu', a); src(d, cx, PY + 480, 'BCEAO · communiqué du 9 septembre 2026', a)
    elif kind == 'ce1':
        label(d, cx, PY + 50, 'CROISSANCE PRÉVUE 2026', a); bignum(d, cx, PY + 255, 6.1 * ease(tl / 1.6), '%', 210, a)
        icn = icons.get('up', 96, rgba(RED, 255 * a)); lay.alpha_composite(icn, (PX + 770, PY + 70)); src(d, cx, PY + 470, 'BCEAO · Union monétaire ouest-africaine', a)
    elif kind == 'ce2':
        icn = icons.get('coin', 150, rgba(RED, 255 * a)); lay.alpha_composite(icn, (cx - 75, PY + 50))
        ctext(d, cx, PY + 220, 'CRÉDIT ABORDABLE', font('Bold', 74), rgba(WHITE, 255 * a)); sub(d, cx, PY + 340, 'Le bon moment pour financer', a, 38)
        src(d, cx, PY + 420, 'un projet qui attend', a)
    elif kind == 'cm0':
        label(d, cx, PY + 50, 'CROISSANCE · CEMAC', a); bars(d, tl, a, [('2025', 3.7, GREY, '3,7 %'), ('2026', 3.0, RED, '3,0 %')], PY + 435, 4.0, 240, 190)
        src(d, cx, PY + 495, 'BEAC · prévision 2026', a)
    elif kind == 'cm1':
        label(d, cx, PY + 50, 'INFLATION · MOYENNE ANNUELLE', a); bignum(d, cx, PY + 255, 2.2 * ease(tl / 1.6), '%', 210, a)
        pill('sous le seuil de 3 %', ease((tl - 1.4) / 0.5) * a, 392, 440); src(d, cx, PY + 480, 'BEAC · réunion du 28 septembre 2026', a)
    elif kind == 'cm2': hchain(d, lay, [('down', 'VOLUMES', 'prudence'), ('coin', 'COÛTS', 'vigilance')], tl, a); label(d, cx, PY + 50, 'UN MARCHÉ QUI RALENTIT', a)
ZSTATES = {
 0: [(1.5, 8.3, 'ci0'), (8.4, 17.2, 'ci1'), (17.4, 23.6, 'ci2')],
 1: [(24.0, 33.2, 'bj0'), (33.3, 40.0, 'bj1'), (40.1, 48.1, 'bj2')],
 2: [(48.4, 53.3, 'ce0'), (53.4, 58.0, 'ce1'), (58.1, 62.2, 'ce2')],
 3: [(62.4, 69.9, 'cm0'), (70.2, 74.7, 'cm1'), (75.1, 80.2, 'cm2')]}
ZSPAN = [(1.3, 23.7), (23.7, 48.3), (48.3, 62.3), (62.3, 80.3)]
def zone_at(ts):
    for i, (a, b) in enumerate(ZSPAN):
        if a <= ts < b: return i
    return None

def identity_card(lay, zi, k):
    if k <= 0: return
    x, y, w, h = 410, 880, 610, 330; glass(lay, x, y, w, h, k, True); d = ImageDraw.Draw(lay)
    nm, ic, _ = ZONES[zi]; icn = icons.get(ic, 110, rgba(RED, 255 * k)); lay.alpha_composite(icn, (x + 44, y + 50))
    spaced(d, x + 190, y + 56, f'ZONE {zi + 1} / 4', font('Medium', 23), rgba(GOLD, 255 * k), 4, True)
    d.text((x + 190, y + 96), nm, font=font('Bold', 46 if len(nm) < 11 else 40), fill=rgba(WHITE, 255 * k))
    for i in range(4):
        cx = x + 56 + i * 134; d.rounded_rectangle((cx, y + 250, cx + 118, y + 262), radius=6, fill=rgba(RED if i <= zi else WHITE, 255 * k if i <= zi else 60 * k))
        ic2 = icons.get(ZONES[i][1], 36, rgba(WHITE, (255 if i == zi else 110) * k)); lay.alpha_composite(ic2, (cx + 41, y + 190))

def body(ts):
    # --- plan de fond
    zi = zone_at(ts); k_pip = 0.0
    if ts < 0.9: k_pip = 0.0
    elif ts < 1.5: k_pip = (ts - 0.9) / 0.6
    elif ts < 80.3: k_pip = 1.0
    elif ts < 80.9: k_pip = 1 - (ts - 80.3) / 0.6
    im = Image.new('RGBA', (W, H), (0, 0, 0, 255)); lay = Image.new('RGBA', (W, H))
    cons, pos, e = consultant(ts, k_pip)
    if k_pip > 0:
        # photo(s) de fond
        zz = zi if zi is not None else (0 if ts < 20 else 3)
        t0 = ZSPAN[zz][0]; k = (ts - t0) / (ZSPAN[zz][1] - t0 + 1e-6)
        ph = photo(ZONES[zz][2], max(0, min(1, k)))
        sw = ZSPAN[zz][0]
        if zz > 0 and ts < sw + 0.6:
            old = photo(ZONES[zz - 1][2], 1.0, -1); kk = eio((ts - sw) / 0.6); edge = int(W * kk)
            m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, 0, edge, H), fill=255); old.paste(ph, (0, 0), m); ph = old
            ImageDraw.Draw(lay).rectangle((edge - 7, 0, edge + 7, H), fill=RED + (255,))
        ph = ph.convert('RGBA'); ph.alpha_composite(GR_PHOTO)
        base = ph
        if k_pip < 1:  # fondu d'entrée / sortie de la photo
            base = Image.new('RGBA', (W, H), (0, 0, 0, 255)); base.alpha_composite(consultant(ts, 0.0)[0], (0, 0))
            tmp = ph.copy(); tmp.putalpha(int(255 * ease(k_pip * 1.2))); base.alpha_composite(tmp)
        im = base
    else:
        im.alpha_composite(cons, pos); im.alpha_composite(GR_BOT, (0, H - GR_BOT.height))
    if k_pip > 0:
        # vignette du consultant par-dessus
        d0 = ImageDraw.Draw(lay)
        if e < 1: pass
        im.alpha_composite(lay); lay = Image.new('RGBA', (W, H))
        im.alpha_composite(cons, pos)
        if e >= 0.98:
            ImageDraw.Draw(im).rounded_rectangle((PIP[0], PIP[1], PIP[0] + PIP[2], PIP[1] + PIP[2]), radius=34, outline=RED + (255,), width=5)
            ImageDraw.Draw(im).ellipse((PIP[0] + 22, PIP[1] + 22, PIP[0] + 38, PIP[1] + 38), fill=RED + (255,))
    # --- éléments de zone
    if zi is not None and ts >= ZSPAN[zi][0] + 0.3:
        kz = ease((ts - ZSPAN[zi][0] - 0.3) / 0.5)
        if ts > ZSPAN[zi][1] - 0.01 and zi == 3: kz = 1.0
        identity_card(lay, zi, kz)
        for (a, b, kind) in ZSTATES[zi]:
            if a - 0.05 <= ts < b + 0.05:
                al = min(ease((ts - a) / 0.45), 1 - ease((ts - (b - 0.3)) / 0.3)) if True else 1
                if kind == 'cm2' and ts > b - 0.4: al = 1 - ease((ts - (b - 0.15)) / 0.25)
                if al > 0.01:
                    glass(lay, PX, PY, PW, PH_, al, True); d = ImageDraw.Draw(lay); st(lay, d, ts - a, al, kind)
    topbar(lay, ts)
    # --- plein cadre : sommaire + titre
    if False:
        d = ImageDraw.Draw(lay)
        for i, (nm, ic, _) in enumerate(ZONES):
            kk = ease((ts - 3.6 - i * 0.45) / 0.5) * (1 - ease((ts - 9.2) / 0.5)); chip(lay, [165, 415, 665, 915][i], 1020, 140, ic, nm, kk, 1.0, 20)
    im.alpha_composite(lay)
    return im

# ---------- sous-titres ----------
SUBS = [(0.0, 0.9, 'Bonjour.'),
 (1.47, 2.4, 'En Côte d’Ivoire,'),
 (2.77, 7.9, 'le gouvernement a lancé le 12 novembre à Abidjan\\Nle Programme national de réduction de l’informalité.'),
 (8.4, 16.9, 'L’informalité est passée de 91,9 % en 2018 à 82,3 %\\Nen 2025, selon l’Agence nationale de la statistique.'),
 (17.41, 23.4, 'Pour vous, c’est un marché qui se structure :\\Nde nouveaux clients, mais aussi de nouveaux\\Nconcurrents qui deviennent formels.'),
 (23.96, 32.9, 'Au Bénin, le projet de budget 2027 atteint 4 757 milliards\\Nde francs CFA, contre 4 148 milliards en 2026,'),
 (33.45, 37.4, 'soit environ 14,7 % de plus,\\Nselon le Conseil des ministres.'),
 (37.97, 39.5, 'Les députés l’examinent cette semaine.'),
 (40.15, 43.2, 'Hôpitaux, écoles, énergie, numérique :'),
 (43.56, 45.0, 'la commande publique va grossir.'),
 (45.52, 48.0, 'Préparez vos offres dès maintenant.'),
 (48.5, 54.0, 'En Afrique de l’Ouest, la BCEAO maintient\\Nson taux directeur à 3 %,'),
 (54.1, 57.3, 'et prévoit 6,1 % de croissance en 2026,\\Nselon son communiqué du 9 septembre.'),
 (58.05, 59.2, 'Le crédit reste abordable.'),
 (59.64, 62.0, 'Si un projet attend,\\Nc’est le moment de le financer.'),
 (62.46, 66.7, 'En zone CEMAC, la BEAC prévoit 3 % de croissance\\Nen 2026,'),
 (67.18, 69.8, 'contre 3,7 % en 2025,'),
 (70.26, 72.4, 'avec une inflation à 2,2 %,'),
 (72.88, 74.6, 'selon sa réunion du 28 septembre.'),
 (75.17, 77.2, 'Le marché ralentit mais reste stable :'),
 (77.54, 80.0, 'prudence sur les volumes,\\Nvigilance sur les coûts.'),
 (80.5, 83.0, 'C’était le Décryptage SPIRIT,\\Nà très bientôt.')]
def tsf(x): x = max(0, x); return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'
def write_ass(path):
    hdr = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', 'WrapStyle: 0', 'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
           'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
           'Style: Sub,Poppins Medium,40,&H00FFFFFF,&H00FFFFFF,&H00141414,&H64141414,0,0,0,0,100,100,0,0,1,3.5,0,2,50,50,0,1', '', '[Events]',
           'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    ev = [f'Dialogue: 0,{tsf(INTRO + a)},{tsf(INTRO + b + 0.12)},Sub,,0,0,0,,{{\\an2\\pos(540,1318)}}{tx}' for a, b, tx in SUBS]
    open(path, 'w', encoding='utf-8').write('\n'.join(hdr + ev) + '\n')

# ---------- rendu ----------
LAST = None
def frame(n):
    global LAST
    t = n / FPS
    if t < INTRO:
        im = intro(t)
        if t > INTRO - 0.6:   # balayage rouge vers le corps
            kk = eio((t - (INTRO - 0.6)) / 0.6); edge = int(W * kk); b = body(0.0).convert('RGB'); m = Image.new('L', (W, H), 0)
            ImageDraw.Draw(m).rectangle((0, 0, edge, H), fill=255); out = im.convert('RGB'); out.paste(b, (0, 0), m); ImageDraw.Draw(out).rectangle((edge - 7, 0, edge + 7, H), fill=RED); return out
        return im.convert('RGB')
    if t < INTRO + DUR: return body(t - INTRO).convert('RGB')
    if LAST is None: LAST = body(DUR - 0.04)
    return outro(t - INTRO - DUR, LAST).convert('RGB')
def work(n): return frame(n).tobytes()

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        for t in [float(x) for x in sys.argv[2:]]: frame(int(round(t * FPS))).save(HERE + f'/still_{t:06.2f}.jpg', quality=88)
    else:
        import multiprocessing as mp
        OUT = sys.argv[2]; N = int(round(TOTAL * FPS)); N0 = int(round((INTRO + DUR) * FPS))
        if mode == 'main': rng, vf = range(0, N0), f'ass={HERE}/subs.ass:fontsdir={KIT}fonts,format=yuv420p'; write_ass(HERE + '/subs.ass')
        else: rng, vf = range(N0, N), 'format=yuv420p'
        pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                               '-vf', vf, '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', OUT], stdin=subprocess.PIPE)
        with mp.Pool(2) as p:
            for i, b in enumerate(p.imap(work, rng, chunksize=4)):
                pr.stdin.write(b)
                if i % 250 == 0: print(i, len(rng), flush=True)
        pr.stdin.close(); pr.wait(); print('ok', len(rng))
