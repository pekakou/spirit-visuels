# icônes vectorielles (supersampling x4) pour « Le Décryptage SPIRIT »
import math
from PIL import Image, ImageDraw
SS = 4
def _new(s):
    S = int(s * SS); im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); return im, ImageDraw.Draw(im), S
def _out(im, s): return im.resize((int(s), int(s)), Image.LANCZOS)
def bank(s, c):
    im, d, S = _new(s); u = S / 100
    d.polygon([(50*u, 12*u), (90*u, 36*u), (10*u, 36*u)], fill=c)
    for x in (20, 38, 56, 74): d.rounded_rectangle((x*u, 42*u, (x+9)*u, 76*u), radius=2*u, fill=c)
    d.rounded_rectangle((10*u, 80*u, 90*u, 90*u), radius=3*u, fill=c); return _out(im, s)
def bolt(s, c):
    im, d, S = _new(s); u = S / 100
    d.polygon([(58*u, 6*u), (22*u, 56*u), (46*u, 56*u), (38*u, 94*u), (78*u, 40*u), (54*u, 40*u)], fill=c); return _out(im, s)
def globe(s, c):
    im, d, S = _new(s); u = S / 100; w = int(6*u)
    d.ellipse((10*u, 10*u, 90*u, 90*u), outline=c, width=w)
    d.ellipse((32*u, 10*u, 68*u, 90*u), outline=c, width=int(5*u))
    d.line((10*u, 50*u, 90*u, 50*u), fill=c, width=int(5*u))
    d.arc((14*u, 22*u, 86*u, 78*u), 200, 340, fill=c, width=int(4*u)); return _out(im, s)
def crane(s, c):
    im, d, S = _new(s); u = S / 100
    d.rectangle((26*u, 14*u, 33*u, 92*u), fill=c)
    for y in range(20, 90, 12): d.line((26*u, y*u, 33*u, (y+10)*u), fill=c, width=int(2.5*u)); d.line((33*u, y*u, 26*u, (y+10)*u), fill=c, width=int(2.5*u))
    d.rectangle((8*u, 12*u, 90*u, 19*u), fill=c)
    d.polygon([(30*u, 6*u), (22*u, 14*u), (38*u, 14*u)], fill=c)
    d.line((78*u, 19*u, 78*u, 52*u), fill=c, width=int(3*u)); d.rounded_rectangle((70*u, 52*u, 86*u, 64*u), radius=3*u, fill=c)
    d.rectangle((8*u, 19*u, 20*u, 30*u), fill=c); d.rectangle((14*u, 90*u, 46*u, 96*u), fill=c); return _out(im, s)
def people(s, c):
    im, d, S = _new(s); u = S / 100
    for cx, sc in ((34, 1.0), (68, 0.82)):
        r = 12 * sc; cy = 34 + (1 - sc) * 14
        d.ellipse(((cx-r)*u, (cy-r)*u, (cx+r)*u, (cy+r)*u), fill=c)
        d.pieslice(((cx-24*sc)*u, (cy+16*sc)*u, (cx+24*sc)*u, (cy+16*sc+50*sc)*u), 180, 360, fill=c)
    return _out(im, s)
def coin(s, c):
    im, d, S = _new(s); u = S / 100
    d.ellipse((8*u, 8*u, 92*u, 92*u), outline=c, width=int(7*u)); d.ellipse((24*u, 24*u, 76*u, 76*u), outline=c, width=int(4*u))
    d.rounded_rectangle((46*u, 34*u, 54*u, 66*u), radius=2*u, fill=c); d.rounded_rectangle((38*u, 44*u, 62*u, 51*u), radius=2*u, fill=c); return _out(im, s)
def trend(s, c, down=False):
    im, d, S = _new(s); u = S / 100
    pts = [(10, 70), (36, 46), (54, 58), (88, 22)] if not down else [(10, 24), (36, 48), (54, 36), (88, 74)]
    d.line([(x*u, y*u) for x, y in pts], fill=c, width=int(8*u), joint='curve')
    ex, ey = pts[-1]; a = math.atan2(pts[-1][1]-pts[-2][1], pts[-1][0]-pts[-2][0])
    p = [(ex, ey), (ex - 20*math.cos(a-0.5), ey - 20*math.sin(a-0.5)), (ex - 20*math.cos(a+0.5), ey - 20*math.sin(a+0.5))]
    d.polygon([(x*u, y*u) for x, y in p], fill=c); return _out(im, s)
def arrow(s, c):
    im, d, S = _new(s); u = S / 100
    d.line((8*u, 50*u, 70*u, 50*u), fill=c, width=int(9*u)); d.polygon([(66*u, 26*u), (94*u, 50*u), (66*u, 74*u)], fill=c); return _out(im, s)
def check(s, c):
    im, d, S = _new(s); u = S / 100
    d.ellipse((8*u, 8*u, 92*u, 92*u), outline=c, width=int(7*u)); d.line([(28*u, 52*u), (44*u, 68*u), (74*u, 34*u)], fill=c, width=int(9*u), joint='curve'); return _out(im, s)
def bubble(s, c):
    im, d, S = _new(s); u = S / 100
    d.rounded_rectangle((8*u, 12*u, 92*u, 70*u), radius=16*u, outline=c, width=int(7*u))
    d.polygon([(30*u, 68*u), (30*u, 92*u), (52*u, 68*u)], fill=c)
    for x in (30, 50, 70): d.ellipse(((x-4)*u, 38*u, (x+4)*u, 46*u), fill=c)
    return _out(im, s)
def megaphone(s, c):
    im, d, S = _new(s); u = S / 100
    d.polygon([(14*u, 40*u), (60*u, 18*u), (60*u, 82*u), (14*u, 60*u)], fill=c); d.rounded_rectangle((6*u, 38*u, 22*u, 62*u), radius=4*u, fill=c)
    d.arc((52*u, 30*u, 86*u, 70*u), -60, 60, fill=c, width=int(6*u)); d.rectangle((22*u, 60*u, 34*u, 82*u), fill=c); return _out(im, s)
ICONS = dict(bank=bank, bolt=bolt, globe=globe, crane=crane, people=people, coin=coin, arrow=arrow, check=check, bubble=bubble, megaphone=megaphone)
def get(name, s, c):
    if name == 'up': return trend(s, c, False)
    if name == 'down': return trend(s, c, True)
    return ICONS[name](s, c)
