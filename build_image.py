#!/usr/bin/env python3
"""Build entry.png: a broadsheet front page summing up Wednesday 25 November 2026.

Authoring tool only. The entry program (main.py) just copies the finished
entry.png to /output/entry.png. Run: python3 build_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
M = 32                      # side margin
CW = W - 2 * M              # content width = 960

PAPER = (246, 241, 231)
INK = (22, 22, 22)
RED = (172, 32, 32)
NAVY = (26, 42, 74)
GREY = (96, 96, 96)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill, lh):
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def rule(draw, y, weight=1):
    draw.line([(M, y), (W - M, y)], fill=INK, width=weight)


def panel(draw, x, y, width, kicker, headline, summary, head_size=23):
    y = draw_wrapped(draw, x, y, kicker, F(SANS_B, 15), width, RED, 18)
    y += 3
    y = draw_wrapped(draw, x, y, headline, F(SERIF_B, head_size), width, INK, head_size + 5)
    y += 4
    y = draw_wrapped(draw, x, y, summary, F(SANS, 16), width, INK, 20)
    return y


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=2)

    # Masthead
    mast = F(SERIF_B, 52)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, 20), title, font=mast, fill=INK)

    # Double rule
    rule(d, 88, 2)
    rule(d, 93, 1)

    # Date band
    d.rectangle([M, 100, W - M, 138], fill=NAVY)
    date_font = F(SANS_B, 26)
    date_text = "WEDNESDAY  ·  25 NOVEMBER 2026"
    d.text(((W - d.textlength(date_text, font=date_font)) / 2, 106),
           date_text, font=date_font, fill=(255, 255, 255))

    # Hero image (lead story: Hormuz)
    hero = Image.open(os.path.join(HERE, "media-generation-hero-0-be76fd3b-6f28-4c4f-901a-43cddc655fed.jpg")).convert("RGB")
    target_w, target_h = CW, 290
    scale = target_w / hero.width
    hero = hero.resize((target_w, round(hero.height * scale)), Image.LANCZOS)
    top = (hero.height - target_h) // 2
    hero = hero.crop((0, top, target_w, top + target_h))
    page.paste(hero, (M, 148))

    y = 444
    y = draw_wrapped(d, M, y,
                     "Illustration: tankers burn in the Strait of Hormuz after hitting naval mines early on Wednesday.",
                     F(SANS, 15), CW, GREY, 19)
    y += 6

    # Lead story
    y = draw_wrapped(d, M, y, "STRAIT OF HORMUZ", F(SANS_B, 16), CW, RED, 19)
    y += 2
    y = draw_wrapped(d, M, y, "TANKERS HIT MINES IN STRAIT OF HORMUZ",
                     F(SERIF_B, 36), CW, INK, 40)
    y += 4
    y = draw_wrapped(d, M, y,
                     "Two tankers explode and catch fire early on Wednesday after striking naval mines "
                     "on what Iran calls an 'unauthorised' route. A container ship hit a mine a day earlier.",
                     F(SANS, 18), CW, INK, 22)
    y += 8
    rule(d, y, 1)
    y += 10

    # Row A: two stories
    col_w = (CW - 20) // 2
    y_a1 = panel(d, M, y, col_w,
                 "RIYADH",
                 "Houthi drone hits Riyadh's tallest tower again",
                 "Eleven people are hurt in a second strike in a week on the PIF Tower, "
                 "home of the Saudi sovereign wealth fund.")
    y_a2 = panel(d, M + col_w + 20, y, col_w,
                 "NEW YORK",
                 "Huawei guilty on 10 of 12 US charges",
                 "A Brooklyn jury convicts the Chinese tech giant of bank fraud, sanctions "
                 "violations and conspiring to steal trade secrets.")
    y = max(y_a1, y_a2) + 8
    rule(d, y, 1)
    y += 10

    # Row B: three stories
    col_w3 = (CW - 42) // 3
    y_b1 = panel(d, M, y, col_w3,
                 "WASHINGTON",
                 "CIA and spy chief's office hacked",
                 "Hackers breach an unclassified open-source intelligence system; officials "
                 "say no classified material was touched.", head_size=22)
    y_b2 = panel(d, M + col_w3 + 21, y, col_w3,
                 "MARKETS",
                 "Nvidia slides 7% as AI doubts return",
                 "Shares fall after lawmakers question Trump's role in the return of CEO Jensen "
                 "Huang; Japan's Nikkei drops 2.8%.", head_size=22)
    y_b3 = panel(d, M + 2 * (col_w3 + 21), y, col_w3,
                 "SPACE",
                 "Pakistan's first astronaut reaches China's station",
                 "Shenzhou-24 lifts off carrying Pakistan's first astronaut to the Chinese "
                 "space station.", head_size=22)
    y = max(y_b1, y_b2, y_b3) + 8
    rule(d, y, 1)
    y += 10

    # Also today strip
    y = draw_wrapped(d, M, y,
                     "ALSO TODAY: All hostages freed after a supermarket siege in Cartagena  ·  "
                     "Senegal regain the Africa Cup of Nations title",
                     F(SANS_B, 15), CW, INK, 19)
    print("bottom y:", y, "of", H)

    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
