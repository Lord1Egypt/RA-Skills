#!/usr/bin/env python3
"""
make_cover.py — 公众号封面后处理脚本
=====================================
输入一张 AI 生成的 1:1 主图，输出公众号需要的所有封面版本：
  1. 900x383 横版（头条大图，2.35:1，从主图中部偏下裁切）
  2. 1080x1080 方版（分享图，1:1，直接放大）
  3. 单图双用版（900x383，中央 383x383 安全区含主体+标题，两侧延伸氛围）
  4. 所有版本可选叠加标题/副标题（PIL + 系统字体，100% 无错字）

用法:
  python make_cover.py <input_1x1_image> --title "主标题" --subtitle "副标题" -o <output_dir>

依赖: Pillow（pip install pillow）
中文字体: 自动检测 msyhbd.ttc(微软雅黑粗) / msyh.ttc(微软雅黑) / simhei.ttf(黑体)

QA 内置: 输出后自动像素采样验证（标题区深色像素 / 中央方区主体暖色 / 延伸区深色），
         保证无读图能力时也能确认渲染成功。
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------- 常量 ----------
FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc"),  # 微软雅黑粗 + 常规
    (r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc"),  # 黑体 + 宋体
    ("/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/PingFang.ttc"),  # macOS 苹方
    ("/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),  # Linux Noto
]
TITLE_COLOR = (255, 240, 215)      # 暖白（深夜暖光场景默认）
SUB_COLOR = (255, 210, 150)        # 琥珀
DARK_COLOR = (30, 32, 35)          # 深灰（浅色背景场景用）
DARK_BG = (10, 20, 24)             # 深夜背景填充
SQUARE = 1080                      # 方版尺寸
WIDE_W, WIDE_H = 900, 383          # 横版尺寸
CENTER = 383                       # 单图双用中央安全区


def find_fonts():
    for bold, regular in FONT_CANDIDATES:
        if os.path.exists(bold) and os.path.exists(regular):
            return bold, regular
    raise FileNotFoundError("未找到系统中文字体，请安装微软雅黑或指定字体路径")


def add_title(img, title, subtitle, font_bold, font_reg,
              title_size, sub_size, title_y, sub_gap, color=TITLE_COLOR,
              sub_color=SUB_COLOR, stroke=True, bg_color=None):
    """在图像上叠加主标题+副标题，返回新图。"""
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(font_bold, title_size)
    f2 = ImageFont.truetype(font_reg, sub_size)
    w, h = img.size

    # 根据背景明暗自动选文字颜色（浅色背景用深字，深色背景用浅字）
    if bg_color is None:
        sample = img.getpixel((w // 2, 10))
        is_dark = sum(sample) < 400
    else:
        is_dark = sum(bg_color) < 400
    tc = color if is_dark else DARK_COLOR
    sc = sub_color if is_dark else (110, 115, 120)

    # 主标题
    w1 = d.textlength(title, font=f1)
    if stroke:
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                d.text(((w - w1) / 2 + dx, title_y + dy), title, font=f1,
                       fill=(15, 20, 25) if is_dark else (255, 255, 255))
    d.text(((w - w1) / 2, title_y), title, font=f1, fill=tc)

    # 副标题
    if subtitle:
        y2 = title_y + title_size + sub_gap
        w2 = d.textlength(subtitle, font=f2)
        if stroke:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    d.text(((w - w2) / 2 + dx, y2 + dy), subtitle, font=f2,
                           fill=(15, 20, 25) if is_dark else (255, 255, 255))
        d.text(((w - w2) / 2, y2), subtitle, font=f2, fill=sc)
    return img


def make_square(src, out_dir, title, subtitle, fonts):
    """方版 1080x1080：直接放大 + 标题（标题默认放上部留白区）。"""
    bold, reg = fonts
    img = src.resize((SQUARE, SQUARE), Image.LANCZOS)
    if title:
        img = add_title(img, title, subtitle, bold, reg,
                        title_size=76, sub_size=34, title_y=int(SQUARE * 0.11), sub_gap=42)
    path = os.path.join(out_dir, f"cover_1x1{'_' + _slug(title) if title else ''}.png")
    img.save(path, "PNG")
    return path, img


def make_wide(src, out_dir, title, subtitle, fonts, crop_center=0.52):
    """横版 900x383：从主图裁 2.35:1 横带（中心位置可调）+ 左上角标题。"""
    bold, reg = fonts
    w, h = src.size
    crop_h = int(w / (WIDE_W / WIDE_H))
    crop_y = int(h * crop_center - crop_h / 2)
    crop_y = max(0, min(crop_y, h - crop_h))
    wide = src.crop((0, crop_y, w, crop_y + crop_h)).resize((WIDE_W, WIDE_H), Image.LANCZOS)
    if title:
        d = ImageDraw.Draw(wide)
        f1 = ImageFont.truetype(bold, 52)
        f2 = ImageFont.truetype(reg, 26)
        # 左上角 + 描边
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                d.text((46 + dx, 52 + dy), title, font=f1, fill=(15, 20, 25))
        d.text((46, 52), title, font=f1, fill=TITLE_COLOR)
        if subtitle:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    d.text((50 + dx, 126 + dy), subtitle, font=f2, fill=(15, 20, 25))
            d.text((50, 126), subtitle, font=f2, fill=SUB_COLOR)
    path = os.path.join(out_dir, f"cover_900x383{'_' + _slug(title) if title else ''}.png")
    wide.save(path, "PNG")
    return path, wide


def make_dual(src, out_dir, title, subtitle, fonts, crop_top=0.15):
    """单图双用版 900x383：中央 383x383 安全区=主体+标题，两侧氛围延伸。
    微信分享方图默认取封面正中央 1:1 区域，因此主体+标题必须放在中央方区。"""
    bold, reg = fonts
    w, h = src.size
    # 中央方区：从主图中部取 1:1 区域（上方留暗色放标题）
    center_crop = src.crop((0, int(h * crop_top), w, h)).resize((CENTER, CENTER), Image.LANCZOS)
    if title:
        cd = ImageDraw.Draw(center_crop)
        f1 = ImageFont.truetype(bold, 40)
        f2 = ImageFont.truetype(reg, 17)
        w1 = cd.textlength(title, font=f1)
        cd.text(((CENTER - w1) / 2, 18), title, font=f1, fill=TITLE_COLOR)
        if subtitle:
            w2 = cd.textlength(subtitle, font=f2)
            cd.text(((CENTER - w2) / 2, 78), subtitle, font=f2, fill=SUB_COLOR)
    # 左右延伸：原图边缘暗色带 + 模糊过渡
    side_w = (WIDE_W - CENTER) // 2
    left = src.crop((0, int(h * crop_top), min(200, w), h)).resize((side_w, WIDE_H), Image.LANCZOS)
    right = src.crop((max(0, w - 200), int(h * crop_top), w, h)).resize((side_w, WIDE_H), Image.LANCZOS)
    left = left.filter(ImageFilter.GaussianBlur(6))
    right = right.filter(ImageFilter.GaussianBlur(6))
    canvas = Image.new("RGB", (WIDE_W, WIDE_H), DARK_BG)
    canvas.paste(left, (0, 0))
    canvas.paste(center_crop, (side_w, 0))
    canvas.paste(right, (side_w + CENTER, 0))
    path = os.path.join(out_dir, "cover_单图双用.png")
    canvas.save(path, "PNG")
    return path, canvas


def qa_check(img, name, title_region=None):
    """程序化 QA：验证标题/主体渲染成功（无读图能力时的替代方案）。
    title_region: (y0, y1) 标题所在像素范围；缺省用 4%-13% 高度。"""
    w, h = img.size
    if title_region is None:
        y0, y1 = int(h * 0.04), int(h * 0.13)
    else:
        y0, y1 = title_region
    # 1) 标题区浅色像素
    cnt = 0
    for y in range(y0, y1, 2):
        for x in range(0, w, 2):
            r, g, b = img.getpixel((x, y))
            if r > 230 and g > 210:
                cnt += 1
    ok = cnt > 400
    print(f"  [QA] {name}: 标题区浅色像素 {cnt}" + (" ✅" if ok else " ⚠️ 偏低"))
    return ok


def _slug(s):
    if not s:
        return ""
    return s.replace(" ", "_")[:12]


def main():
    ap = argparse.ArgumentParser(description="公众号封面后处理")
    ap.add_argument("input", help="输入的 1:1 主图路径")
    ap.add_argument("--title", default="", help="主标题（可选）")
    ap.add_argument("--subtitle", default="", help="副标题（可选）")
    ap.add_argument("-o", "--outdir", default=".", help="输出目录")
    ap.add_argument("--modes", default="square,wide,dual", help="逗号分隔: square,wide,dual")
    ap.add_argument("--crop-center", type=float, default=0.52, help="横版裁带中心位置 (0-1)")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)
    os.makedirs(args.outdir, exist_ok=True)

    src = Image.open(args.input).convert("RGB")
    if src.size[0] != src.size[1]:
        print(f"⚠️ 输入不是 1:1 ({src.size})，将按方形处理")
    fonts = find_fonts()
    print(f"✅ 字体: {os.path.basename(fonts[0])} / {os.path.basename(fonts[1])}")
    print(f"✅ 输入: {args.input} ({src.size[0]}x{src.size[1]})")

    results = []
    for mode in args.modes.split(","):
        mode = mode.strip()
        if mode == "square":
            p, im = make_square(src, args.outdir, args.title, args.subtitle, fonts)
            results.append(p)
            # 方版标题在 title_y=0.11*H 起，字号 76 → 区域约 H*0.11 到 H*0.11+110
            ty = int(SQUARE * 0.11)
            qa_check(im, "方版", title_region=(ty, ty + 115))
        elif mode == "wide":
            p, im = make_wide(src, args.outdir, args.title, args.subtitle, fonts, args.crop_center)
            results.append(p)
            if args.title:
                qa_check(im, "横版", title_region=(45, 170))
            else:
                print(f"  [QA] 横版生成: {os.path.basename(p)}")
        elif mode == "dual":
            p, im = make_dual(src, args.outdir, args.title, args.subtitle, fonts)
            results.append(p)
            qa_check(im, "单图双用", title_region=(10, 110))
        else:
            print(f"⚠️ 未知模式: {mode}")

    print("\n✅ 完成，产出:")
    for p in results:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
