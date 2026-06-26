#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image, ImageDraw, ImageFont

SKILL_DIR = r"C:\Users\chenyuxin\.qclaw\workspace\skills\shampoo-recommender"
DIRS = [
    os.path.join(SKILL_DIR, "assets", "images"),
    os.path.join(SKILL_DIR, "assets", "templates"),
    os.path.join(SKILL_DIR, "assets", "mockups"),
]

def create_directories():
    print("=" * 50)
    print("Step 1: Creating directories...")
    print("=" * 50)
    for d in DIRS:
        try:
            os.makedirs(d, exist_ok=True)
            print("[OK] " + d)
        except Exception as e:
            print("[ERR] " + d + ": " + str(e))

def hex2rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def make_ad(name, color_hex, bg_hex, path):
    w, h = 1200, 628
    c = hex2rgb(color_hex)
    bg = hex2rgb(bg_hex)
    img = Image.new('RGB', (w, h), bg)
    draw = ImageDraw.Draw(img)
    try:
        ft = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 72)
        fs = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 36)
        fs2 = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
    except:
        ft = ImageFont.load_default()
        fs = ImageFont.load_default()
        fs2 = ImageFont.load_default()
    draw.rectangle([0, 0, w, 15], fill=c)
    draw.rectangle([0, 0, 15, h], fill=c)
    draw.text((50, 50), "NAKORURU", font=fs2, fill=(80, 80, 80))
    draw.line([(50, 85), (180, 85)], fill=c, width=3)
    draw.text((50, 130), name, font=ft, fill=c)
    draw.text((50, 220), "SHAMPOO", font=fs, fill=c)
    bx, by = 850, 120
    draw.rounded_rectangle([bx+35, by, bx+85, by+40], radius=5, fill=c)
    draw.rounded_rectangle([bx, by+40, bx+120, by+380], radius=25, fill=(255,255,255), outline=c, width=4)
    draw.rounded_rectangle([bx+15, by+140, bx+105, by+280], radius=10, fill=bg)
    draw.text((bx+30, by+200), "NAKO\nRURU", font=fs2, fill=c)
    draw.line([(50, 480), (1150, 480)], fill=(200,200,200), width=2)
    draw.text((50, 510), "Professional Hair Care - NAKORURU", font=fs2, fill=(150,150,150))
    img.save(path, "PNG")
    print("  [OK] " + os.path.basename(path))

def generate_ads():
    print("=" * 50)
    print("Step 2: Generating product ads...")
    print("=" * 50)
    products = [
        ("shencengziyangxiufu", "#8B5A2B", "#FFF8F0"),
        ("qingshuangkongyou", "#4682B4", "#F0F8FF"),
        ("quxiezhiyang", "#228B22", "#F0FFF0"),
        ("fangtuogufa", "#8B4513", "#FFF5EE"),
        ("anjisuanwenhe", "#9370DB", "#F8F8FF"),
        ("pengsongfengying", "#FF8C00", "#FFFAF0"),
        ("quluxiufu", "#008080", "#F0FFFF"),
    ]
    d = os.path.join(SKILL_DIR, "assets", "images")
    for name, color, bg in products:
        make_ad(name, color, bg, os.path.join(d, name + "_ad.png"))

def make_template(ttype, path):
    if ttype == "single":
        w, h = 800, 450
        img = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, w, 60], fill=(100, 100, 100))
        try:
            f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        except:
            f = ImageFont.load_default()
        draw.text((30, 15), "NAKORURU - Recommendation", font=f, fill=(255,255,255))
        draw.rectangle([50, 100, 400, 350], outline=(200,200,200), width=2)
        draw.rectangle([450, 100, 750, 350], outline=(200,200,200), width=2)
        draw.rectangle([0, 380, w, h], fill=(245, 245, 245))
    elif ttype == "double":
        w, h = 1000, 500
        img = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, w, 60], fill=(100, 100, 100))
        try:
            f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        except:
            f = ImageFont.load_default()
        draw.text((30, 15), "NAKORURU - Product Compare", font=f, fill=(255,255,255))
        draw.rectangle([50, 100, 480, 450], outline=(200,200,200), width=2)
        draw.rectangle([520, 100, 950, 450], outline=(200,200,200), width=2)
    else:
        w, h = 1200, 800
        img = Image.new('RGB', (w, h), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, w, 80], fill=(80, 80, 80))
        try:
            f = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
        except:
            f = ImageFont.load_default()
        draw.text((30, 25), "NAKORURU - Full Report", font=f, fill=(255,255,255))
        sections = [(100, 200), (320, 200), (540, 200), (760, 200)]
        for y, hh in sections:
            draw.rectangle([30, y, w-30, y+hh], fill=(255,255,255), outline=(200,200,200), width=1)
    img.save(path, "PNG")
    print("  [OK] " + os.path.basename(path))

def generate_templates():
    print("=" * 50)
    print("Step 3: Generating templates...")
    print("=" * 50)
    d = os.path.join(SKILL_DIR, "assets", "templates")
    make_template("single", os.path.join(d, "card_single.png"))
    make_template("double", os.path.join(d, "card_double.png"))
    make_template("report", os.path.join(d, "report_full.png"))

def make_mockup(mtype, path):
    if mtype == "front":
        w, h = 600, 800
        img = Image.new('RGB', (w, h), (245, 245, 245))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([150, 100, 450, 700], radius=30, fill=(255,255,255), outline=(150,150,150), width=3)
        draw.rounded_rectangle([220, 50, 380, 120], radius=10, fill=(100,100,100))
        draw.rounded_rectangle([180, 250, 420, 550], radius=15, fill=(240,240,255))
    elif mtype == "side":
        w, h = 400, 800
        img = Image.new('RGB', (w, h), (245, 245, 245))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([100, 100, 300, 700], radius=20, fill=(255,255,255), outline=(150,150,150), width=3)
        draw.rounded_rectangle([150, 50, 250, 120], radius=5, fill=(100,100,100))
    else:
        w, h = 1200, 800
        img = Image.new('RGB', (w, h), (200, 220, 240))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 500, w, h], fill=(180, 160, 140))
        draw.rectangle([0, 0, w, 300], fill=(150, 200, 230))
    img.save(path, "PNG")
    print("  [OK] " + os.path.basename(path))

def generate_mockups():
    print("=" * 50)
    print("Step 4: Generating mockups...")
    print("=" * 50)
    d = os.path.join(SKILL_DIR, "assets", "mockups")
    make_mockup("front", os.path.join(d, "bottle_front.png"))
    make_mockup("side", os.path.join(d, "bottle_side.png"))
    make_mockup("scene", os.path.join(d, "scene_usage.png"))

def main():
    print("\n" + "=" * 50)
    print("NAKORURU Shampoo Skill - Asset Generator")
    print("=" * 50 + "\n")
    create_directories()
    generate_ads()
    generate_templates()
    generate_mockups()
    print("=" * 50)
    print("[DONE] All assets generated!")
    print("=" * 50)
    print("\nFile tree:")
    for root, dirs, files in os.walk(SKILL_DIR):
        level = root.replace(SKILL_DIR, '').count(os.sep)
        indent = '  ' * level
        print(indent + os.path.basename(root) + "/")
        subindent = '  ' * (level + 1)
        for f in files:
            if f.endswith('.png'):
                print(subindent + f)

if __name__ == "__main__":
    main()
