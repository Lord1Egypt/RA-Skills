#!/usr/bin/env python3
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

PRESETS = {
    'pink': ((255, 228, 236), (255, 200, 220), (255, 242, 247)),
    'blue-purple': ((221, 229, 255), (167, 170, 255), (232, 221, 255)),
    'purple-blue': ((229, 220, 255), (151, 165, 255), (214, 235, 255)),
    'peach': ((255, 233, 220), (255, 198, 176), (255, 244, 235)),
    'mint': ((224, 248, 238), (173, 232, 214), (237, 252, 247)),
}

def make_bg(size, preset_name):
    c1, c2, c3 = PRESETS.get(preset_name, PRESETS['pink'])
    w, h = size
    bg = Image.new('RGBA', size, (*c1, 255))
    draw = ImageDraw.Draw(bg)
    for y in range(h):
        t = y / max(h - 1, 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(c1[i] * (1 - u) + c2[i] * u) for i in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(c2[i] * (1 - u) + c3[i] * u) for i in range(3))
        draw.line((0, y, w, y), fill=(*c, 255))

    blobs = [
        ((-80, int(h * 0.58), int(w * 0.40), int(h * 1.05)), (*c2, 90), 90),
        ((int(w * 0.66), -40, int(w * 1.05), int(h * 0.34)), (*c3, 80), 100),
        ((int(w * 0.08), int(h * 0.08), int(w * 0.92), int(h * 0.92)), (255, 255, 255, 120), 130),
    ]
    for box, color, blur in blobs:
        ov = Image.new('RGBA', size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.ellipse(box, fill=color)
        ov = ov.filter(ImageFilter.GaussianBlur(blur))
        bg = Image.alpha_composite(bg, ov)
    return bg

if len(sys.argv) not in (3, 4):
    print('usage: compose_pink_card.py <tweet_capture_png> <output_png> [preset]', file=sys.stderr)
    sys.exit(1)

src = Path(sys.argv[1]).expanduser().resolve()
out = Path(sys.argv[2]).expanduser().resolve()
preset = sys.argv[3].strip().lower() if len(sys.argv) == 4 else 'pink'
out.parent.mkdir(parents=True, exist_ok=True)

img = Image.open(src).convert('RGBA')
W = H = 1080
bg = make_bg((W, H), preset)
ratio = min(760 / img.size[0], 860 / img.size[1])
card = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.LANCZOS)
card_mask = Image.new('L', card.size, 0)
ImageDraw.Draw(card_mask).rounded_rectangle((0, 0, card.size[0], card.size[1]), radius=24, fill=255)
x = (W - card.size[0]) // 2
y = (H - card.size[1]) // 2
bg.paste(card, (x, y), card_mask)
bg.save(out)
print(str(out))
