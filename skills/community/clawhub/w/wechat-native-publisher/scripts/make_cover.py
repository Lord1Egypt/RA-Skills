# -*- coding: utf-8 -*-
"""
wechat-native-publisher 封面图生成 v3（双模式 + 主题取色）

模式一：插画合成（--cover <AI插画底图>，默认）
  底图自动裁白边 → 900x500 白底画布 → 左 40% 标题 / 右 60% 插画 → 底部品牌条。

模式二：几何占位（--no-art，无插画时降级）
  用主题色画几何构成封面：柔和圆/环 + 标题排版 + 品牌条。
  买家没 AI 画图也能一键出封面（纯本地，可发布级观感）。

主题取色：--theme signature/mono/paper → theme.hex_colors()（本地 PIL 用 hex，与微信 rgb 不冲突）

用法：
  python make_cover.py --cover assets/art.png --title "主标题" [--title2 "副标题"] \
      --author "名字" --slogan "签名语" --theme signature --out cover.png
  python make_cover.py --no-art --title "主标题" [--title2 "副标题"] \
      --author "名字" --slogan "签名语" --theme paper --out cover.png
"""
import os, sys, argparse
from PIL import Image, ImageDraw, ImageFont
from theme import hex_colors

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_BD = r"C:\Windows\Fonts\msyhbd.ttc"   # 粗体
FONT_RG = r"C:\Windows\Fonts\msyh.ttc"     # 常规

W, H = 900, 500
TEXT_W = 440            # 左侧文字区宽度
RIGHT_W = W - TEXT_W    # 右侧插画/几何区宽度
BANNER_H = 56           # 底部品牌条高度
BANNER_TOP = H - BANNER_H


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def hx(s, alpha=255):
    """#rrggbb → (r,g,b[,a])"""
    s = s.lstrip("#")
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    return (r, g, b, alpha) if alpha < 255 else (r, g, b)


def content_bbox(img, threshold=250, pad=18):
    """检测非白色内容边界 (left, top, right, bottom)，用于裁掉白边留白"""
    rgb = img.convert("RGB")
    px = rgb.load()
    w, h = rgb.size
    left, top, right, bottom = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if r < threshold or g < threshold or b < threshold:
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y
    if right <= left or bottom <= top:
        return 0, 0, w, h
    left = max(0, left - pad); top = max(0, top - pad)
    right = min(w, right + pad); bottom = min(h, bottom + pad)
    return left, top, right, bottom


def fit_to_region(img, region_w, region_h):
    """把图片 cover-fit 到指定区域（保持比例，居中，超出裁切）"""
    iw, ih = img.size
    scale = max(region_w / iw, region_h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - region_w) // 2
    top = (nh - region_h) // 2
    return img.crop((left, top, left + region_w, top + region_h))


def _banner(draw, c):
    """底部品牌条：主色横条 + 左右点缀 + 作者/签名白字"""
    draw.rectangle([(0, BANNER_TOP), (W, H)], fill=hx(c["GREEN"]))
    draw.rectangle([(0, BANNER_TOP), (10, H)], fill=hx(c["ORANGE_ACCENT"]))
    draw.rectangle([(W - 10, BANNER_TOP), (W, H)], fill=hx(c["ORANGE_ACCENT"]))
    return draw


def _banner_text(draw, author, slogan, c):
    f_author = load_font(FONT_BD, 22)
    if author:
        cy = H - (38 if slogan else 28)
        draw.text((W / 2, cy), author, fill="#ffffff", font=f_author, anchor="mm")
    if slogan:
        draw.text((W / 2, H - 14), slogan, fill="#ffffff",
                  font=load_font(FONT_RG, 13), anchor="mm")


def _wrap_title(draw, text, font, max_w, max_rows=3):
    """按像素宽度折行（CJK 优先按字符断行，不做词切分）"""
    lines = []
    cur = ""
    for ch in text:
        if draw.textlength(cur + ch, font=font) <= max_w or not cur:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines[:max_rows]


def geometric_cover(title, subtitle, author, slogan, out, theme_id="signature",
                    title2=None, title_font=46):
    """
    几何占位封面：白底 + 右侧柔和圆/环（主题色）+ 左侧标题排版 + 底部品牌条。
    标题过长自动折行降字号；无 author/slogan 时品牌条只保留色块。
    """
    c = hex_colors(theme_id)
    subtitle = subtitle or title2 or ""

    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # ---- 右侧几何装饰（透明叠色，先画大后画小） ----
    # 大软圆（accent，低透明）
    draw.ellipse([(560, 30), (830, 300)], fill=hx(c["ORANGE_ACCENT"], 30))
    # 主色圆环
    lw = 3
    draw.ellipse([(660, 250), (840, 430)], outline=hx(c["GREEN"], 120), width=lw)
    # 浅色大圆环（更淡）
    draw.ellipse([(600, 60), (760, 220)], outline=hx(c["GREEN_LIGHT"], 90), width=lw)
    # 小实心点（accent 与主色）
    draw.ellipse([(530, 330), (548, 348)], fill=hx(c["ORANGE_ACCENT"], 200))
    draw.ellipse([(835, 130), (853, 148)], fill=hx(c["GREEN"], 200))
    draw.ellipse([(855, 320), (869, 334)], fill=hx(c["ORANGE_ACCENT"], 160))

    # ---- 左上装饰双条 ----
    draw.rectangle([(0, 0), (170, 6)], fill=hx(c["GREEN"]))
    draw.rectangle([(170, 0), (240, 6)], fill=hx(c["ORANGE_ACCENT"]))

    # ---- 左侧标题区 ----
    f_big = load_font(FONT_BD, title_font)
    max_w = TEXT_W - 64
    rows = _wrap_title(draw, title, f_big, max_w)
    if len(rows) > 2:                       # 行太多 → 降字号重排
        f_big = load_font(FONT_BD, 36)
        rows = _wrap_title(draw, title, f_big, max_w)
    line_h = int(title_font * 1.42) if len(rows) <= 2 else int(36 * 1.5)
    block_h = line_h * len(rows)
    y = 168 - (block_h // 2) if len(rows) > 1 else 196
    for r in rows:
        draw.text((TEXT_W - 44, y), r, fill=hx(c["BODY"]), font=f_big)
        y += line_h

    # 绿色短条 + 副标题（也折行限制宽度，避免压到右侧几何）
    if subtitle:
        draw.rectangle([(TEXT_W - 44, y + 2), (TEXT_W - 44 + 64, y + 6)], fill=hx(c["GREEN"]))
        f_sub = load_font(FONT_RG, 21)
        sub_rows = _wrap_title(draw, subtitle, f_sub, max_w)
        sy = y + 22
        for sr in sub_rows:
            draw.text((TEXT_W - 44, sy), sr, fill=hx(c["GRAY"]), font=f_sub)
            sy += 30

    # ---- 底部品牌条 ----
    _banner(draw, c)
    _banner_text(draw, author, slogan, c)

    canvas.convert("RGB").save(out, "PNG")
    print(f"saved: {out} ({W}x{H}, theme={theme_id}, no-art)")


def make(cover_path, out_path, title, title2, en, cn, author, theme_id="signature", slogan=""):
    """插画合成封面（v2 逻辑保留，默认模式）"""
    c = hex_colors(theme_id)
    cover = Image.open(cover_path).convert("RGB")
    l, t, r, b = content_bbox(cover)
    content = cover.crop((l, t, r, b))

    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    art = fit_to_region(content, RIGHT_W, H)
    canvas.paste(art, (TEXT_W, 0))

    # 左上装饰（绿+橙双条，主题取色）
    draw.rectangle([(0, 0), (150, 6)], fill=hx(c["GREEN"]))
    draw.rectangle([(150, 0), (200, 6)], fill=hx(c["ORANGE_ACCENT"]))

    # 左侧文字区
    f_part = load_font(FONT_BD, 26)
    f_small = load_font(FONT_RG, 20)
    f_title = load_font(FONT_BD, 40)
    f_author = load_font(FONT_BD, 22)

    draw.text((TEXT_W - 330, 92), "PART", fill=hx(c["GREEN"]), font=f_part)
    draw.text((TEXT_W - 330, 130), f"{en} · {cn}", fill=hx(c["GREEN_LIGHT"]), font=f_small)
    draw.text((TEXT_W - 330, 182), title, fill=hx(c["BODY"]), font=f_title)
    if title2:
        draw.text((TEXT_W - 330, 238), title2, fill=hx(c["BODY"]), font=f_title)
    draw.rectangle([(TEXT_W - 330, 306), (TEXT_W - 258, 310)], fill=hx(c["GREEN"]))

    # 底部品牌条
    _banner(draw, c)
    _banner_text(draw, author, slogan, c)

    canvas.save(out_path, "PNG", quality=95)
    print(f"saved: {out_path} ({W}x{H}, theme={theme_id}, art)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", default=None, help="AI 插画底图（--no-art 时忽略）")
    ap.add_argument("--no-art", action="store_true", help="几何占位封面（无插画降级链）")
    ap.add_argument("--title", required=True, help="主标题（可长，自动折行）")
    ap.add_argument("--title2", default=None, help="主标题第 2 行 / 副标题")
    ap.add_argument("--en", default="READ", help="英文小标（插画模式用）")
    ap.add_argument("--cn", default="阅读", help="中文小标（插画模式用）")
    ap.add_argument("--author", default="", help="品牌条作者名")
    ap.add_argument("--slogan", default="", help="品牌条签名语")
    ap.add_argument("--theme", default="signature", help="主题 id：signature/mono/paper/custom")
    ap.add_argument("--primary", default=None, help="custom 时结构主色 #RRGGBB")
    ap.add_argument("--accent", default=None, help="custom 时焦点强调色 #RRGGBB")
    ap.add_argument("--out", default=None, help="输出封面路径")
    args = ap.parse_args()
    out = args.out or os.path.join(os.getcwd(), "cover.png")

    if args.theme == "custom":
        if not (args.primary and args.accent):
            ap.error("--theme custom 需同时给 --primary 与 --accent（#RRGGBB，如 --primary #2456a6 --accent #ff6b4a）")
        import theme
        theme.apply_custom(args.primary, args.accent)   # 注入 THEMES['custom']，hex_colors 可取

    if args.no_art:
        geometric_cover(args.title, args.title2, args.author, args.slogan,
                        out, theme_id=args.theme)
    else:
        if not args.cover:
            ap.error("插画模式需 --cover <底图>；没有插画可用 --no-art 生成几何占位封面")
        make(args.cover, out, args.title, args.title2, args.en, args.cn,
             args.author, theme_id=args.theme, slogan=args.slogan)
