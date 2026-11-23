#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news image, 1024x1024 PNG.

Deterministic: solid colours + DejaVu fonts only, no randomness, no
network, no timestamps in the PNG. Re-running writes identical bytes.
Stories verified from AP / Reuters / AFP / Al Jazeera round-ups of
Sunday 22 November 2026. The ICJ Rohingya verdict (19 Nov) and the
20 Nov market fall are deliberately NOT shown as 22 Nov news.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W = H = 1024
NAVY = (15, 42, 68)
NAVY2 = (21, 58, 92)
CREAM = (247, 243, 232)
WHITE = (255, 255, 255)
INK = (20, 28, 38)
GREY = (90, 100, 112)
RED = (178, 34, 34)
ORANGE = (204, 85, 0)
TEAL = (0, 110, 110)
GOLD = (255, 193, 7)
BLUE = (30, 90, 160)
GREEN = (34, 120, 70)
PURPLE = (110, 60, 140)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_DATE = font("DejaVuSans-Bold", 52)
F_SUB = font("DejaVuSans-Bold", 30)
F_KICK = font("DejaVuSans-Bold", 24)
F_HEAD = font("DejaVuSans-Bold", 44)
F_HEAD2 = font("DejaVuSans-Bold", 36)
F_BODY = font("DejaVuSans", 26)
F_FOOT = font("DejaVuSans-Bold", 23)
F_FOOT2 = font("DejaVuSans", 23)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, text, fnt, x, y, max_w, fill, lh=None):
    lines = wrap(draw, text, fnt, max_w)
    h = lh or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += h
    return y

# ---- header ----
d.rectangle([0, 0, W, 168], fill=NAVY)
d.rectangle([0, 168, W, 176], fill=GOLD)
d.text((36, 22), "SUNDAY  •  22 NOVEMBER 2026", font=F_DATE, fill=WHITE)
d.text((38, 118), "THE WORLD IN ONE IMAGE", font=F_SUB, fill=GOLD)

# ---- lead: COP31 ----
d.rectangle([24, 196, W - 24, 398], fill=WHITE)
d.rectangle([24, 196, 36, 398], fill=RED)
d.text((56, 210), "CLIMATE  •  ANTALYA, TURKEY", font=F_KICK, fill=RED)
d.text((56, 244), "COP31 COLLAPSES", font=F_HEAD, fill=INK)
para(d, "UN climate talks end with no deal — the EU rejects a final text that omits fossil fuels.",
     F_BODY, 56, 300, W - 112, INK)

# ---- 2x2 grid ----
tiles = [
    ("GULF  •  STRAIT OF HORMUZ", ORANGE, "TANKERS HIT, GULF ON EDGE",
     "Two supertankers hit mines and catch fire; Iran strikes US bases in Bahrain."),
    ("UKRAINE  •  WAR", BLUE, "KRYVYI RIH STRUCK",
     "Russian missile kills a 7-year-old boy and a 20-year-old woman; 60 wounded."),
    ("MEXICO  •  SINALOA", GREEN, "‘EL CHAPO ISIDRO’ CAPTURED",
     "Special forces seize the cartel boss in a raid that kills 11, including 4 soldiers."),
    ("INDONESIA  •  CIKANDE", PURPLE, "FACTORY FIRE: 34 MISSING",
     "A candy factory burns; 3 workers are dead and rescuers search the ruins for 34 more."),
]
gx, gy, tw, th, gap = 24, 418, 476, 252, 24
for i, (kick, col, head, body) in enumerate(tiles):
    x = gx + (i % 2) * (tw + gap)
    y = gy + (i // 2) * (th + gap)
    d.rectangle([x, y, x + tw, y + th], fill=WHITE)
    d.rectangle([x, y, x + tw, y + 10], fill=col)
    d.text((x + 20, y + 26), kick, font=F_KICK, fill=col)
    # headline may wrap to 2 lines
    yy = para(d, head, F_HEAD2, x + 20, y + 62, tw - 40, INK, lh=42)
    para(d, body, F_BODY, x + 20, yy + 8, tw - 40, GREY)

# ---- footer ----
d.rectangle([0, 946, W, H], fill=NAVY2)
para(d, "ALSO ON 22 NOV:  Drone strikes kill 4 near Khartoum, damage a UN building  •  Protests across Europe enter a third day over living costs.",
     F_FOOT2, 36, 966, W - 72, WHITE, lh=28)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
