"""Draws entry.png: one front page that sums up the world's news of Friday 20 November 2026.

Run once on a machine with Pillow and the usual Windows fonts:  python render.py
The program the grader runs (main.py) only copies the finished entry.png, so it needs neither.
Every story below was reported on 20 November 2026 (see SOURCES.md).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = "C:/Windows/Fonts/"

PAPER = (247, 243, 234)
INK = (22, 24, 29)
NAVY = (18, 35, 66)
RED = (196, 30, 36)
GREY = (92, 96, 104)
RULE = (190, 182, 166)


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


SERIF_B = lambda s: font("georgiab.ttf", s)
SERIF = lambda s: font("georgia.ttf", s)
SANS_B = lambda s: font("arialbd.ttf", s)
SANS = lambda s: font("arial.ttf", s)
COND_B = lambda s: font("ARIALNB.TTF", s)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, xy, text, f, width, fill=INK, gap=4):
    x, y = xy
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + gap
    return y


# ---------- icons, each drawn inside a box (x, y, size) ----------

def star(d, cx, cy, r1, r2, fill, n=8):
    import math
    pts = []
    for i in range(n * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def icon_globe_oil(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], fill=(70, 140, 190))
    d.ellipse([x + s * 0.18, y + s * 0.2, x + s * 0.55, y + s * 0.55], fill=(90, 160, 90))
    d.ellipse([x + s * 0.5, y + s * 0.5, x + s * 0.85, y + s * 0.82], fill=(90, 160, 90))
    # a clock hand: talks run into overtime
    d.ellipse([x + s * 0.55, y - s * 0.05, x + s * 1.05, y + s * 0.45], fill=PAPER, outline=INK, width=4)
    cx, cy = x + s * 0.8, y + s * 0.2
    d.line([cx, cy, cx, cy - s * 0.17], fill=INK, width=4)
    d.line([cx, cy, cx + s * 0.13, cy + s * 0.05], fill=RED, width=4)


def icon_servers(d, x, y, s):
    for i in range(3):
        top = y + s * 0.12 + i * s * 0.28
        d.rounded_rectangle([x, top, x + s * 0.62, top + s * 0.22], radius=4, fill=NAVY)
        d.ellipse([x + s * 0.06, top + s * 0.07, x + s * 0.14, top + s * 0.15], fill=(120, 220, 140))
    d.ellipse([x + s * 0.5, y + s * 0.42, x + s * 1.02, y + s * 0.94], fill=RED)
    f = SANS_B(int(s * 0.36))
    d.text((x + s * 0.76, y + s * 0.68), "$", font=f, fill="white", anchor="mm")


def icon_border(d, x, y, s):
    d.rectangle([x, y + s * 0.3, x + s * 0.1, y + s], fill=INK)
    d.rectangle([x + s * 0.9, y + s * 0.3, x + s, y + s], fill=INK)
    for i in range(4):
        fill = RED if i % 2 == 0 else "white"
        d.rectangle([x + s * 0.1 + i * s * 0.2, y + s * 0.45, x + s * 0.3 + i * s * 0.2, y + s * 0.58], fill=fill, outline=INK)
    # Estonia's flag colours
    for i, c in enumerate([(0, 114, 206), (0, 0, 0), (255, 255, 255)]):
        d.rectangle([x + s * 0.3, y + i * s * 0.1, x + s * 0.7, y + (i + 1) * s * 0.1], fill=c, outline=INK)


def icon_gavel(d, x, y, s):
    d.polygon([(x + s * 0.2, y + s * 0.15), (x + s * 0.55, y - s * 0.0), (x + s * 0.7, y + s * 0.3), (x + s * 0.35, y + s * 0.45)], fill=NAVY)
    d.line([x + s * 0.52, y + s * 0.3, x + s * 0.95, y + s * 0.8], fill=(120, 80, 40), width=int(s * 0.1))
    d.rectangle([x, y + s * 0.85, x + s * 0.6, y + s], fill=NAVY)
    d.line([x + s * 0.05, y + s * 0.62, x + s * 0.55, y + s * 0.62], fill=RED, width=6)


def icon_troops(d, x, y, s):
    for i in range(3):
        cx = x + s * (0.18 + i * 0.32)
        d.ellipse([cx - s * 0.1, y + s * 0.2, cx + s * 0.1, y + s * 0.4], fill=(85, 95, 60))
        d.pieslice([cx - s * 0.14, y + s * 0.14, cx + s * 0.14, y + s * 0.34], 180, 360, fill=(60, 70, 40))
        d.rounded_rectangle([cx - s * 0.14, y + s * 0.42, cx + s * 0.14, y + s * 0.9], radius=6, fill=(85, 95, 60))
    d.rectangle([x, y + s * 0.92, x + s, y + s], fill=(180, 150, 100))


def icon_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(235, 238, 242), outline=INK, width=2)
    pts = [(x + s * 0.05, y + s * 0.3), (x + s * 0.25, y + s * 0.2), (x + s * 0.42, y + s * 0.35),
           (x + s * 0.6, y + s * 0.3), (x + s * 0.78, y + s * 0.62), (x + s * 0.95, y + s * 0.88)]
    d.line(pts, fill=RED, width=6, joint="curve")
    d.polygon([(x + s * 0.98, y + s * 0.95), (x + s * 0.8, y + s * 0.9), (x + s * 0.93, y + s * 0.76)], fill=RED)
    d.text((x + s * 0.3, y + s * 0.78), "AI", font=SANS_B(int(s * 0.3)), fill=NAVY, anchor="mm")


def lead_map(d, x, y, w, h):
    """Stylised map: Poland in the west, Ukraine in the middle, Russia's launch site in the east."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 236))
    pol = [(x + 10, y + 30), (x + w * 0.36, y + 18), (x + w * 0.4, y + h * 0.55), (x + w * 0.34, y + h - 12), (x + 14, y + h - 30)]
    ukr = [(x + w * 0.4, y + h * 0.3), (x + w * 0.8, y + h * 0.22), (x + w * 0.86, y + h * 0.75), (x + w * 0.42, y + h * 0.88), (x + w * 0.34, y + h - 12), (x + w * 0.4, y + h * 0.55)]
    rus = [(x + w * 0.8, y), (x + w, y), (x + w, y + h), (x + w * 0.86, y + h * 0.75), (x + w * 0.8, y + h * 0.22)]
    d.polygon(pol, fill=(236, 228, 210), outline=INK)
    d.polygon(ukr, fill=(250, 224, 120), outline=INK)
    d.polygon(rus, fill=(205, 190, 190), outline=INK)
    lab = SANS_B(22)
    d.text((x + w * 0.16, y + h * 0.5), "POLAND", font=lab, fill=INK, anchor="mm")
    d.text((x + w * 0.62, y + h * 0.6), "UKRAINE", font=lab, fill=INK, anchor="mm")
    d.text((x + w * 0.92, y + h * 0.12), "RUSSIA", font=SANS_B(18), fill=INK, anchor="mm")
    # Kyiv
    kx, ky = x + w * 0.62, y + h * 0.36
    d.ellipse([kx - 7, ky - 7, kx + 7, ky + 7], fill=INK)
    d.text((kx + 12, ky - 12), "Kyiv", font=SANS_B(18), fill=INK)
    star(d, kx, ky, 18, 8, RED)
    # missile tracks from the east, three of them landing inside Poland
    sx, sy = x + w * 0.96, y + h * 0.45
    for tx, ty in [(x + w * 0.24, y + h * 0.7), (x + w * 0.29, y + h * 0.82), (x + w * 0.2, y + h * 0.3)]:
        mx, my = (sx + tx) / 2, min(sy, ty) - h * 0.28
        pts = []
        for i in range(21):
            t = i / 20
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t ** 2 * tx
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t ** 2 * ty
            pts.append((px, py))
        for i in range(0, 20, 2):
            d.line([pts[i], pts[i + 1]], fill=RED, width=5)
        star(d, tx, ty, 14, 6, RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead: the date first, as large as it will go
    d.rectangle([0, 0, W, 130], fill=NAVY)
    d.text((W / 2, 22), "THE WORLD'S NEWS IN ONE PAGE", font=SANS_B(22), fill=(200, 210, 230), anchor="mt")
    d.text((W / 2, 52), "FRIDAY 20 NOVEMBER 2026", font=SERIF_B(62), fill="white", anchor="mt")

    # ---- lead story
    top = 148
    d.text((32, top), "RUSSIAN MISSILES CROSS INTO POLAND", font=COND_B(54), fill=RED)
    lead_map(d, 32, top + 66, 560, 300)
    y = top + 70
    y = text_block(d, (612, y), "Two missiles and a drone land in eastern Poland during one of Russia's largest attacks on Ukraine.", SERIF_B(25), 380, gap=6)
    y += 10
    y = text_block(d, (612, y), "NATO's Rutte: a \"grave violation\". Tusk: \"an intentional provocation\".", SERIF(22), 380, fill=GREY)
    y += 10
    text_block(d, (612, y), "Same night: strikes on Kyiv's bridges kill 8, a strike on Lviv's station kills 2.", SERIF(22), 380, fill=GREY)

    # ---- six more stories on a 3 by 2 grid
    grid_top = 540
    d.line([32, grid_top - 12, W - 32, grid_top - 12], fill=INK, width=3)
    stories = [
        (icon_globe_oil, "COP31 runs into overtime", "Antalya draft drops every mention of fossil fuels"),
        (icon_servers, "Trump: tax US firms' data centres abroad", "Hails Shenzhen summit with Xi and Putin"),
        (icon_border, "Estonia shuts its Russia border", "For 6 months at least. Moscow: a new \"Iron Curtain\""),
        (icon_gavel, "Myanmar rejects genocide ruling", "World Court found it guilty over the Rohingya"),
        (icon_troops, "Iraqi troops enter militia stronghold", "Jurf al-Sakhar, base of Kataib Hezbollah"),
        (icon_chart, "AI sell-off sinks Wall Street", "Nasdaq wipes out its 2026 gain, S&P 500 in correction"),
    ]
    cw, ch = (W - 64) / 3, 214
    for i, (icon, head, sub) in enumerate(stories):
        cx = 32 + (i % 3) * cw
        cy = grid_top + (i // 3) * ch
        icon(d, cx + 4, cy + 10, 72)
        yy = text_block(d, (cx + 92, cy + 2), head, SANS_B(27), cw - 100, gap=2)
        text_block(d, (cx + 4, max(yy, cy + 96) + 8), sub, SERIF(21), cw - 18, fill=GREY, gap=4)
        if i % 3:
            d.line([cx - 6, cy, cx - 6, cy + ch - 20], fill=RULE, width=2)
    d.line([32, grid_top + ch - 10, W - 32, grid_top + ch - 10], fill=RULE, width=2)

    # ---- footer
    d.rectangle([0, H - 44, W, H], fill=NAVY)
    d.text((W / 2, H - 22), "The day's world news as reported on 20 November 2026", font=SANS(19), fill=(200, 210, 230), anchor="mm")

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
