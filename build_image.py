#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page, 1024x1024 PNG.

Newspaper style, like the entries leading this bounty's leaderboard:
35 stories, 7 regions, every one happened or first reported on
Sunday 22 November 2026 (UTC), with a date check at the foot.
Stories verified against AP / Reuters / AFP / Al Jazeera, the
Ukrainian Air Force, Hong Kong EAC, FIA, Cricinfo, ESA and ATP.

Deliberately LEFT OUT (earlier days, however big):
ICJ Rohingya verdict Thu 19 Nov; 'El Chapo Isidro' capture Fri 21 Nov;
Kryvyi Rih missile Sat 21 Nov; Denmark expels Russian attache Fri 20 Nov;
Sparta II drone strike Sat 21 Nov (its fire still burning on Sunday
is in the list, dated as such).

Deterministic: solid colours + DejaVu fonts only, no randomness,
no network, no timestamps. Re-running writes identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (245, 239, 224)
PAPER = (255, 252, 244)
NAVY = (16, 34, 56)
INK = (22, 26, 32)
GREY = (88, 92, 98)
RED = (172, 28, 28)
TEAL = (0, 102, 102)
GOLD = (214, 158, 0)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_SERIF = lambda s: font("DejaVuSerif-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)
F_SANSB = lambda s: font("DejaVuSans-Bold", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, max_w, fill, lh=None):
    h = lh or int(fnt.size * 1.28)
    for ln in wrap(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += h
    return y

def centre(text, fnt, y, fill, x0=0, x1=W):
    w = d.textlength(text, font=fnt)
    d.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)

# ---------- top bar ----------
d.rectangle([0, 0, W, 26], fill=NAVY)
centre("THE WORLD IN ONE DAY  •  35 STORIES  •  7 REGIONS  •  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
       F_SANSB(13), 5, (255, 255, 255))

# ---------- masthead ----------
d.text((24, 30), "Sunday 22 November 2026", font=F_SERIF(48), fill=INK)
d.text((24, 88), "COP31 ends with no deal  •  186 drones over Ukraine  •  Tankers hit in Hormuz",
       font=F_SERIF(18), fill=RED)
d.line([24, 118, W - 24, 118], fill=INK, width=2)

# ---------- numbers strip ----------
nums = [("186", "drones fired at Ukraine"),
        ("161", "downed or jammed"),
        ("98.79%", "Hong Kong turnout"),
        ("720/9", "India's record total"),
        ("2", "tankers hit in Hormuz"),
        ("36", "missing in Serang fire")]
x = 24
bw = (W - 48 - 5 * 8) / 6
for n, lab in nums:
    d.rectangle([x, 126, x + bw, 168], fill=PAPER, outline=(200, 190, 160))
    centre(n, F_SANSB(22), 129, RED, x, x + bw)
    centre(lab, F_SANS(10), 154, GREY, x, x + bw)
    x += bw + 8

# ---------- region bar ----------
regs = [("EUROPE", (30, 90, 160)), ("MIDDLE EAST", RED), ("ASIA-PACIFIC", (204, 120, 0)),
        ("AMERICAS", TEAL), ("AFRICA", (34, 120, 70)), ("OCEANIA", (110, 60, 140)),
        ("WORLD", (90, 90, 90))]
x = 24
rw = (W - 48) / 7
for name, col in regs:
    d.rectangle([x, 176, x + rw - 2, 196], fill=col)
    centre(name, F_SANSB(11), 181, (255, 255, 255), x, x + rw - 2)
    x += rw

# ---------- scenes (flat, drawn in code) ----------
def scene_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 122, 122))
    d.ellipse([x + w - 70, y + 8, x + w - 30, y + 48], fill=(255, 210, 90))
    for bx, bh in [(20, 55), (70, 75), (130, 60), (190, 80)]:
        d.rectangle([x + bx, y + h - bh - 28, x + bx + 42, y + h - 28], fill=(38, 70, 80))
        for wy in range(0, bh - 10, 14):
            d.rectangle([x + bx + 6, y + h - bh - 22 + wy, x + bx + 16, y + h - bh - 14 + wy], fill=(255, 210, 90))
    d.rectangle([x, y + h - 28, x + w, y + h], fill=(120, 70, 40))
    for i in range(6):
        cx = x + 30 + i * 48
        d.ellipse([cx, y + h - 48, cx + 18, y + h - 30], fill=(40, 40, 40))
        d.rectangle([cx + 2, y + h - 30, cx + 16, y + h - 28], fill=(40, 40, 40))

def scene_ukraine(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
    for sx, sy in [(20, 12), (70, 30), (140, 10), (210, 26), (270, 14), (110, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # apartment block, lit windows, one dark collapsed corner
    d.rectangle([x + 18, y + 30, x + 108, y + h], fill=(52, 58, 74))
    for r in range(4):
        for c in range(3):
            col = (255, 200, 80) if (r + c) % 2 else (30, 34, 48)
            d.rectangle([x + 28 + c * 28, y + 40 + r * 18, x + 44 + c * 28, y + 52 + r * 18], fill=col)
    d.polygon([(x + 108, y + 30), (x + 150, y + h), (x + 108, y + h)], fill=(30, 34, 48))
    # drones
    for dx, dy in [(190, 22), (240, 44), (280, 18)]:
        d.line([x + dx - 8, y + dy - 6, x + dx + 8, y + dy + 6], fill=(255, 180, 60), width=2)
        d.line([x + dx - 8, y + dy + 6, x + dx + 8, y + dy - 6], fill=(255, 180, 60), width=2)
    d.polygon([(x + 230, y + h), (x + 300, y + h), (x + 272, y + 40)], fill=(255, 220, 120))

def scene_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 44, 84))
    d.ellipse([x + w - 60, y + 10, x + w - 20, y + 50], fill=(240, 230, 200))
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(10, 30, 60))
    # tanker
    d.rectangle([x + 24, y + h - 66, x + 220, y + h - 42], fill=(90, 30, 30))
    d.rectangle([x + 150, y + h - 88, x + 190, y + h - 66], fill=(200, 200, 200))
    # fire + smoke
    for fx, fy, fs in [(60, 58, 22), (90, 50, 28), (120, 60, 20)]:
        d.polygon([(x + fx, y + h - fy - fs), (x + fx - fs // 2, y + h - fy),
                   (x + fx + fs // 2, y + h - fy)], fill=(255, 140, 0))
    for sx, sy, sr in [(70, 40, 9), (100, 32, 11), (130, 42, 8)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(90, 90, 90))
    # second tanker, small
    d.rectangle([x + 240, y + h - 54, x + w - 16, y + h - 42], fill=(60, 60, 60))

def scene_mini(x, y, w, h, kind):
    skies = {"vote": (200, 60, 60), "race": (20, 20, 60), "cricket": (40, 120, 60),
             "fire": (60, 30, 30), "sudan": (90, 70, 40), "gaza": (180, 170, 140)}
    d.rectangle([x, y, x + w, y + h], fill=skies[kind])
    if kind == "vote":
        d.rectangle([x + w // 2 - 22, y + 14, x + w // 2 + 22, y + h - 12], fill=(255, 255, 255))
        d.rectangle([x + w // 2 - 14, y + 20, x + w // 2 + 14, y + 30], fill=RED)
        d.line([x + w // 2 - 10, y + 40, x + w // 2 + 10, y + h - 20], fill=RED, width=3)
    elif kind == "race":
        d.rectangle([x, y + h - 18, x + w, y + h], fill=(40, 40, 40))
        d.rectangle([x + 18, y + 22, x + w - 18, y + 38], fill=(200, 0, 0))
        d.ellipse([x + 28, y + 36, x + 48, y + 52], fill=(10, 10, 10))
        d.ellipse([x + w - 48, y + 36, x + w - 28, y + 52], fill=(10, 10, 10))
        for i in range(5):
            d.rectangle([x + i * 26, y + 4, x + i * 26 + 13, y + 12], fill=(255, 255, 255))
    elif kind == "cricket":
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 160, 80))
        d.rectangle([x + w // 2 - 4, y + 8, x + w // 2 + 4, y + h - 16], fill=(220, 180, 120))
        d.ellipse([x + w - 30, y + 12, x + w - 16, y + 26], fill=(200, 30, 30))
    elif kind == "fire":
        d.polygon([(x + w // 2, y + 6), (x + w // 2 - 26, y + h - 8), (x + w // 2 + 26, y + h - 8)],
                  fill=(255, 140, 0))
        d.polygon([(x + w // 2, y + 24), (x + w // 2 - 12, y + h - 8), (x + w // 2 + 12, y + h - 8)],
                  fill=(255, 220, 0))
    elif kind == "sudan":
        d.rectangle([x, y + h - 20, x + w, y + h], fill=(140, 110, 70))
        for bx in (14, 54, 94):
            d.rectangle([x + bx, y + 22, x + bx + 28, y + h - 20], fill=(80, 60, 40))
        d.line([x + 20, y + 10, x + 60, y + 26], fill=(255, 200, 80), width=2)
        d.line([x + 60, y + 26, x + 100, y + 10], fill=(255, 200, 80), width=2)
    elif kind == "gaza":
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(120, 120, 120))
        d.rectangle([x + 16, y + 20, x + w - 16, y + 40], fill=(255, 255, 255))
        d.rectangle([x + 16, y + 20, x + w - 16, y + 28], fill=(220, 60, 60))
        d.ellipse([x + 30, y + 40, x + 46, y + 52], fill=(10, 10, 10))
        d.ellipse([x + w - 46, y + 40, x + w - 30, y + 52], fill=(10, 10, 10))

# ---------- top 3 panels ----------
top = [
    ("1  •  ANTALYA, TÜRKIYE  •  CLIMATE", "COP31 ends with no deal",
     "The EU rejects a final text that omits fossil fuels; COP president says there is no consensus, so nothing is adopted.", scene_cop31),
    ("2  •  UKRAINE  •  WAR", "186 drones in one night",
     "Russia fires 186 drones; air defences down 161. A drone hits a block in Dymer: at least 3 killed, 14 unaccounted for.", scene_ukraine),
    ("3  •  STRAIT OF HORMUZ  •  GULF", "Two tankers hit by mines",
     "Iran's navy says two supertankers hit mines and caught fire; Iran claims two US radars hit in Bahrain, Bahrain denies it.", scene_hormuz),
]
px, py, pw, ph, pgap = 24, 204, 312, 226, 16
for i, (kick, head, body, scene) in enumerate(top):
    x = px + i * (pw + pgap)
    d.rectangle([x, py, x + pw, py + ph], fill=PAPER, outline=(200, 190, 160))
    scene(x + 1, py + 1, pw - 2, 96)
    d.text((x + 10, py + 104), kick, font=F_SANSB(11), fill=RED)
    yy = para(head, F_SERIF(21), x + 10, py + 122, pw - 20, INK, lh=23)
    para(body, F_SANS(13), x + 10, yy + 4, pw - 20, GREY, lh=16)

# ---------- second row: 6 cards ----------
cards = [
    ("4  HONG KONG  •  ELECTION", "Record vote in Hong Kong",
     "856 candidates for 723 seats; turnout 98.79%, a record.", "vote"),
    ("5  LAS VEGAS  •  FORMULA 1", "Verstappen wins in Vegas",
     "Beats Norris by 0.639s after 35 lead changes; Piastri third.", "race"),
    ("6  WELLINGTON  •  CRICKET", "India declare on 720/9",
     "A record total in NZ: Rahul 136, Pant 128; lead of 352.", "cricket"),
    ("7  SERANG, INDONESIA  •  FIRE", "Candy-factory fire: 36 missing",
     "3 workers dead; 15 rescued alive as the blaze burns on.", "fire"),
    ("8  KHARTOUM  •  WAR", "Drones kill 4 near Khartoum",
     "Strikes blamed on the RSF damage a UN building; staff inside.", "sudan"),
    ("9  GAZA CITY  •  GAZA", "Three killed in food-van strike",
     "World Central Kitchen says the dead were not its team.", "gaza"),
]
cx, cy, cw, ch = 24, 442, 312, 146
for i, (kick, head, body, kind) in enumerate(cards):
    x = cx + (i % 3) * (cw + pgap)
    y = cy + (i // 3) * (ch + 10)
    d.rectangle([x, y, x + cw, y + ch], fill=PAPER, outline=(200, 190, 160))
    scene_mini(x + 1, y + 1, cw - 2, 48, kind)
    d.text((x + 10, y + 56), kick, font=F_SANSB(11), fill=RED)
    yy = para(head, F_SERIF(17), x + 10, y + 74, cw - 20, INK, lh=19)
    para(body, F_SANS(12), x + 10, yy + 3, cw - 20, GREY, lh=14)

# ---------- also list ----------
ly = 752
d.text((24, ly), "ALSO ON SUNDAY 22 NOVEMBER", font=F_SANSB(14), fill=INK)
d.line([24, ly + 20, W - 24, ly + 20], fill=INK, width=1)
also_left = [
    "10  Saudi Arabia intercepts a Houthi drone and missile.",
    "11  Iran unveils an underground missile city, dual launcher.",
    "12  Suspected drone strike hits Russian corvette Merkury.",
    "13  Sparta II still ablaze off Finland; 16 crew evacuated.",
    "14  Protests across Europe, 3rd day, over costs and housing.",
    "15  Settlers burn 12 vehicles in West Bank villages.",
    "16  Lebanon's Aoun demands Israeli withdrawal.",
    "17  Democrats win largest US House majority since 1992.",
    "18  Pezeshkian: Iran in a silent economic war; blockade at 130 days.",
    "19  Ex-Italian police chief found dead amid Sicily inquiry.",
    "20  BepiColombo enters Mercury orbit; thruster glitch reported.",
    "21  Turkey: Israel blocking container homes for Gaza.",
    "22  Hind Rajab Foundation urges Germany to arrest a soldier.",
]
also_right = [
    "23  Fidan: US-Israel war fallout threatens global markets.",
    "24  Displaced Palestinians protest as Israeli strikes continue.",
    "25  Zelenskyy urges US to release Patriot missiles.",
    "26  Alcaraz beats Zverev 6-2, 7-6 to win the ATP Finals.",
    "27  Liverpool rout Man Utd 4-0 at Anfield; Pochettino's debut.",
    "28  Wembanyama scores 50 as Spurs beat Pelicans 114-91.",
    "29  Nepal PM Balendra Shah lands in Delhi on first foreign trip.",
    "30  Chinese bomber turns back 170 km from Manila.",
    "31  Iran begins rationing electricity amid shortages.",
    "32  China eases margin rules; minimum ratio falls to 80%.",
    "33  NYT: China's spy agency ran a campaign to obtain AI chips.",
    "34  Delhi forum ends with no formal India-Pakistan talks.",
    "35  Cyclone Akvan weakens to a depression after Odisha landfall.",
]
y = ly + 28
for t in also_left:
    y = para(t, F_SANS(10), 24, y, 470, INK, lh=12) + 1
y = ly + 28
for t in also_right:
    y = para(t, F_SANS(10), 512, y, 488, INK, lh=12) + 1

# ---------- date check + footer ----------
d.rectangle([24, 962, W - 24, 998], fill=(255, 255, 255), outline=RED)
d.text((32, 968), "DATE CHECK", font=F_SANSB(12), fill=RED)
para("Every story here happened or was first reported on Sun 22 Nov 2026 (UTC). Left out: ICJ verdict (19 Nov), El Chapo capture, Kryvyi Rih missile, Denmark expulsion (20 Nov).",
     F_SANS(10), 128, 968, W - 152, INK, lh=13)
centre("Sources: Reuters  •  AP  •  AFP  •  Al Jazeera  •  Ukrainian Air Force  •  Hong Kong EAC  •  FIA  •  Cricinfo  •  ESA  •  ATP  —  Scenes are drawn illustrations, not photographs.",
       F_SANS(10), 1004, GREY)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
