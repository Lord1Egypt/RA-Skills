# -*- coding: utf-8 -*-
"""signature 水印生成模板——skill-promo-video
方法论：图腾（从视频叙事母题取）+ 烟熏胶囊托底 + 1px 金框 + 衬线品牌名 + 文楷网站名。
换 skill：改 BRAND/SITE/MOTIF 三参数（MOTIF 需按新母题手绘几行 PIL 图元）。
⛔ 版本号不进水印（密集更新期，用户令）。
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, argparse

SERIF_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
WK = os.path.expanduser("~/.local/share/fonts/LXGWWenKai-Regular.ttf")
GOLD, PAPER = (212, 175, 105), (237, 230, 212)

def motif_scroll_lines(d, mx, my):
    """AF 母题示例：卷筒+纸带+金数据折线（新 skill 换成自己的母题图元）"""
    d.rounded_rectangle([mx, my, mx + 13, my + 62], 6, fill=(58, 92, 76, 255))
    d.line([(mx + 4, my + 6), (mx + 4, my + 56)], fill=(150, 190, 168, 220), width=2)
    d.rounded_rectangle([mx + 11, my + 9, mx + 128, my + 53], 4, fill=PAPER + (248,))
    pts = [(mx + 24, my + 42), (mx + 52, my + 30), (mx + 78, my + 36), (mx + 106, my + 18)]
    d.line(pts, fill=GOLD + (255,), width=3)
    for p in pts:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=GOLD + (255,))

def build(brand, site, motif_fn, W=640, H=150):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(base).rounded_rectangle([4, 4, W - 4, H - 4], 24, fill=(16, 22, 32, 168))
    im.alpha_composite(base.filter(ImageFilter.GaussianBlur(0.5)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([7, 7, W - 7, H - 7], 21, outline=GOLD + (150,), width=1)
    motif_fn(d, 34, 42)
    TX = 186
    f = ImageFont.truetype(SERIF_B, 46)
    d.text((TX + 2, 26 + 2), brand, font=f, fill=(0, 0, 0, 120))
    d.text((TX, 26), brand, font=f, fill=(242, 237, 224, 248))
    d.ellipse([TX + 108, 92, TX + 116, 100], fill=GOLD + (220,))
    d.text((TX + 128, 80), site, font=ImageFont.truetype(WK, 36), fill=GOLD + (248,))
    return im

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", default="your-brand")
    ap.add_argument("--site", default="example.com")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    build(a.brand, a.site, motif_scroll_lines).save(a.out)
    print("watermark ok ->", a.out)
