# -*- coding: utf-8 -*-
"""小红书「公基常识 · 每日5题」图片生成器（1080×1440，3:4）  v1.2.1

用法:
    python make_cards.py days/day04.json
    python make_cards.py days/day04.json --out ./day04
    python make_cards.py days/day04.json --no-preview

输出：JSON 的 days/ 上一级生成 dayNN/（10 张图，题→解析交替）+ preview.png。
每期 5 题固定含 1–2 道真题：item 带 "source" 时，题目卡与解析卡底部都印「真题出处」；
题目卡顶部把 tag 拆成两枚胶囊——板块（绿）+「真题 · 题源缩写」（红）。
首图不再印文章标题，题目卡开头就是标签与题干。
每次出题都会打印 WARN 行提示排版溢出，看到就回去缩短题干/解析。
"""
import os
import sys
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440

PAPER    = (250, 246, 239)
CARD     = (255, 255, 255)
INK      = (32, 36, 46)
INK_SOFT = (128, 120, 108)
LINE     = (231, 223, 210)
ACCENT   = (198, 74, 48)      # 朱红：题目
ACCENT_D = (14, 110, 101)     # 墨绿：答案
TINT     = (243, 236, 226)

# 依次尝试，取第一个存在的字体文件
BOLD_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",   # 微软雅黑 粗
    r"C:\Windows\Fonts\simhei.ttf",   # 黑体
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]
REG_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simsun.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

NO_START = "，。、；：？！）】》”’%,.;:?!)]}"


def pick_font(cands):
    for p in cands:
        if os.path.exists(p):
            return p
    raise SystemExit("找不到中文字体，请把 BOLD_CANDIDATES / REG_CANDIDATES 改成机器上已有的字体路径")


F_BOLD = pick_font(BOLD_CANDIDATES)
F_REG = pick_font(REG_CANDIDATES)


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def units(text):
    """结尾标点粘到前一个字；数字/英文/单位保持完整，避免“800”被拆成 8 / 00。"""
    out = []
    for ch in text:
        prev = out[-1] if out else ""
        if prev and ch in NO_START:
            out[-1] = prev + ch
        elif prev and (ch in "℃%°" or (ch.isascii() and ch.isalnum()
                                       and prev[-1].isascii() and prev[-1].isalnum())):
            out[-1] = prev + ch
        else:
            out.append(ch)
    return out


def wrap(draw, text, fnt, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for u in units(para):
            if draw.textlength(cur + u, font=fnt) <= maxw or not cur:
                cur += u
            else:
                lines.append(cur)
                cur = u
        lines.append(cur)
    return lines


def deco(img, color):
    """右上角装饰：三条右对齐细线，末条用主题色。"""
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([902, 214, 1000, 220], 3, fill=TINT)
    d.rounded_rectangle([916, 236, 1000, 242], 3, fill=TINT)
    d.rounded_rectangle([934, 258, 1000, 264], 3, fill=color)


def pill(img, x, y, text, fnt, fg, bg, padx=26, h=56, radius=None):
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=fnt) + padx * 2
    radius = radius or h // 2
    d.rounded_rectangle([x, y, x + w, y + h], radius, fill=bg)
    d.text((x + padx, y + h / 2), text, font=fnt, fill=fg, anchor="lm")
    return x + w


def header(img, day, page, total):
    d = ImageDraw.Draw(img)
    pill(img, 80, 64, "公基常识 · 每日5题", font(F_BOLD, 26), CARD, ACCENT, h=56)
    d.text((1000, 92), f"DAY {day:02d}", font=font(F_BOLD, 26), fill=INK_SOFT, anchor="rm")
    d.text((1000, 132), f"{page:02d} / {total:02d}", font=font(F_REG, 22),
           fill=(168, 158, 145), anchor="rm")
    d.line([80, 176, 1000, 176], fill=LINE, width=2)


def footer(img, left, color=INK_SOFT, size=24, right=None):
    d = ImageDraw.Draw(img)
    d.line([80, 1318, 1000, 1318], fill=LINE, width=2)
    d.text((80, 1348), left, font=font(F_REG, size), fill=color, anchor="lm")
    if right:
        d.text((1000, 1348), right, font=font(F_REG, 22), fill=(176, 166, 152), anchor="rm")


def dots(img, current, total, color, y):
    """底部答题进度点。"""
    d = ImageDraw.Draw(img)
    gap, r = 30, 8
    x = W / 2 - (total - 1) * gap / 2
    for i in range(total):
        if i + 1 == current:
            d.rounded_rectangle([x - 17, y - 8, x + 17, y + 8], 8, fill=color)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(226, 217, 204))
        x += gap


def split_tag(tag):
    """把「板块 · 题源缩写」拆成两段；没有分隔符时整条都算板块。"""
    for sep in ("·", "・"):
        if sep in tag:
            cat, exam = tag.split(sep, 1)
            return cat.strip(), exam.strip()
    return tag.strip(), ""


def dedupe_repeat(s):
    """「法律常识法律常识…」这类整段重复收敛成一遍，避免标签印出多遍。"""
    if not s:
        return s
    n = len(s)
    for k in range(2, n // 2 + 1):
        if n % k == 0 and s[:k] * (n // k) == s:
            return s[:k]
    return s


def source_footnote(img, src, y=1258, warn=None, idx=""):
    """卡片底部印「真题出处」；超宽先缩字号，仍超就截断并 WARN。"""
    src = (src or "").strip()
    if not src:
        return
    d = ImageDraw.Draw(img)
    prefix = "真题出处："
    size = 22
    while size > 16 and d.textlength(prefix + src, font=font(F_REG, size)) > 900:
        size -= 1
    if size < 20 and warn is not None:
        warn(f"第{idx}题真题出处偏长（{len(src)}字），字号缩到 {size}px，建议压到 30 字内")
    fsrc = font(F_REG, size)
    line = prefix + src
    if d.textlength(line, font=fsrc) > 900:
        if warn is not None:
            warn(f"第{idx}题真题出处过长（{len(src)}字），已截断，建议压到 30 字内")
        while src and d.textlength(prefix + src + "…", font=fsrc) > 900:
            src = src[:-1]
        line = prefix + src + "…"
    px = d.textlength(prefix, font=fsrc)
    d.text((80, y), prefix, font=fsrc, fill=(170, 105, 78), anchor="la")
    d.text((80 + px, y), line[len(prefix):], font=fsrc,
           fill=(150, 140, 126), anchor="la")


def question_card(q, idx, day, total, warn=None):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    deco(img, ACCENT)
    header(img, day, 2 * idx - 1, total)

    y = 210
    src = (q.get("source") or "").strip()
    tag = q["tag"]
    cat, exam = split_tag(tag) if src else (tag, "")
    cat_fixed, exam_fixed = dedupe_repeat(cat), dedupe_repeat(exam)
    if (cat_fixed, exam_fixed) != (cat, exam) and warn is not None:
        fixed = f"{cat_fixed} · {exam_fixed}" if exam_fixed else cat_fixed
        warn(f"第{idx}题标签有重复段，已合并为「{fixed}」")
    cat, exam = cat_fixed, exam_fixed

    # 板块胶囊（有真题胶囊时给它留出位置）
    cat_limit = 560 if src else 920
    csize = 28
    while csize > 19 and d.textlength(cat, font=font(F_BOLD, csize)) + 52 > cat_limit:
        csize -= 1
    if d.textlength(cat, font=font(F_BOLD, csize)) + 52 > cat_limit:
        if warn is not None:
            warn(f"第{idx}题板块标签「{cat}」过长，已截断，请压到 13 字以内")
        while cat and d.textlength(cat + "…", font=font(F_BOLD, csize)) + 52 > cat_limit:
            cat = cat[:-1]
        cat += "…"
    if csize < 24 and warn is not None:
        warn(f"第{idx}题板块标签「{cat}」偏长，已缩到 {csize}px，建议压到 13 字以内")
    x = pill(img, 80, y, cat, font(F_BOLD, csize), ACCENT_D, (231, 242, 238), h=56)

    # 真题胶囊：真题 · 题源缩写
    if src:
        label = f"真题 · {exam}" if exam else "真题"
        esize = 26
        while esize > 17 and x + 12 + d.textlength(label, font=font(F_BOLD, esize)) + 40 > 920:
            esize -= 1
        if x + 12 + d.textlength(label, font=font(F_BOLD, esize)) + 40 > 920:
            if warn is not None:
                warn(f"第{idx}题真题题源「{exam}」过长，已截断，建议压到 10 字以内")
            while exam and x + 12 + d.textlength(f"真题 · {exam}…", font=font(F_BOLD, esize)) + 40 > 920:
                exam = exam[:-1]
            label = f"真题 · {exam}…" if exam else "真题…"
        if esize < 21 and warn is not None:
            warn(f"第{idx}题真题题源偏长，字号缩到 {esize}px，建议写成「2024国考」")
        pill(img, x + 12, y + 4, label, font(F_BOLD, esize), ACCENT, (250, 236, 230),
             padx=20, h=48)

    y += 96

    fq = font(F_BOLD, 56)
    qlines = wrap(d, q["q"], fq, 900)
    d.rounded_rectangle([80, y + 6, 88, y + 6 + len(qlines) * 88 - 16], 4, fill=ACCENT)
    ty = y
    for ln in qlines:
        d.text((112, ty), ln, font=fq, fill=INK, anchor="la")
        ty += 88
    y = ty + 46

    fo = font(F_REG, 38)
    for i, op in enumerate(q["options"]):
        d.rounded_rectangle([80, y, 1000, y + 118], 26, fill=CARD,
                            outline=(233, 225, 213), width=2)
        cx, cy = 154, y + 59
        d.ellipse([cx - 33, cy - 33, cx + 33, cy + 33], fill=TINT)
        d.text((cx, cy), "ABCD"[i], font=font(F_BOLD, 34), fill=ACCENT, anchor="mm")
        ols = wrap(d, op, fo, 700)
        oy = cy - (len(ols) - 1) * 28
        for ln in ols:
            d.text((cx + 58, oy), ln, font=fo, fill=(52, 56, 66), anchor="lm")
            oy += 56
        y += 142

    if y > 1210 and warn is not None:
        warn(f"第{idx}题题干/选项过长：内容底边 {y}px 压到进度点了")

    source_footnote(img, src, warn=warn, idx=idx)

    nq = total // 2
    dots(img, idx, nq, ACCENT, min(max(y + 34, 1148), 1210))
    footer(img, "答案在下一张 →", ACCENT, 26, right=f"第 {idx} 题 / 共 {nq} 题")
    return img.convert("RGB")


def answer_card(q, idx, day, total, warn=None):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    deco(img, ACCENT_D)
    header(img, day, 2 * idx, total)

    letter = "ABCD"[q["answer"]]
    d.text((80, 232), "正确答案", font=font(F_REG, 28), fill=INK_SOFT, anchor="la")
    d.rounded_rectangle([80, 276, 236, 432], 36, fill=ACCENT_D)
    d.text((158, 354), letter, font=font(F_BOLD, 150), fill=CARD, anchor="mm")

    fopt = font(F_BOLD, 40)
    ols = wrap(d, q["options"][q["answer"]], fopt, 700)
    oy = 354 - (len(ols) - 1) * 30
    for ln in ols:
        d.text((280, oy), ln, font=fopt, fill=INK, anchor="lm")
        oy += 60

    y = 500
    d.text((80, y), "解 析", font=font(F_BOLD, 34), fill=ACCENT_D, anchor="la")
    d.line([186, y + 24, 260, y + 24], fill=ACCENT_D, width=4)
    y += 76

    fb = font(F_REG, 33)
    for para in q["why"]:
        for ln in wrap(d, para, fb, 900):
            d.text((80, y), ln, font=fb, fill=(62, 62, 70), anchor="la")
            y += 58
        y += 16

    # 记一句
    y += 26
    ft = font(F_BOLD, 32)
    tlines = wrap(d, q["tip"], ft, 800)
    bh = 46 + len(tlines) * 52 + 30
    d.rounded_rectangle([80, y, 1000, y + bh], 28, fill=(235, 245, 242))
    d.rounded_rectangle([80, y, 92, y + bh], 6, fill=ACCENT_D)
    d.text((124, y + 26), "记一句", font=font(F_BOLD, 24), fill=ACCENT_D, anchor="la")
    ty = y + 70
    for ln in tlines:
        d.text((124, ty), ln, font=ft, fill=(20, 60, 56), anchor="la")
        ty += 52

    if y + bh > 1180 and warn is not None:
        warn(f"第{idx}题解析过长：内容底边 {y + bh}px 会撞到底部互动区")
    if len(tlines) > 1 and warn is not None:
        warn(f"第{idx}题“记一句”折成 {len(tlines)} 行，建议压到 24 字以内")

    # 真题出处：固定在进度点与页脚线之间；超宽先缩字号，仍超就截断并 WARN
    source_footnote(img, q.get("source"), warn=warn, idx=idx)

    nq = total // 2
    dy = min(max(y + bh + 96, 1148), 1206)
    d.text((W / 2, dy - 52), "答对了吗？评论区报个到",
           font=font(F_REG, 24), fill=(158, 148, 134), anchor="mm")
    dots(img, idx, nq, ACCENT_D, dy)
    footer(img, f"第 {idx} 题解析", INK_SOFT, 24, right=f"公基常识 · Day {day:02d}")
    return img.convert("RGB")


def make_preview(files, out_path, cols=5):
    """拼一张总览图，方便一眼检查 10 张成图。"""
    tw, th = 360, 480
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols + 10 * (cols + 1),
                              th * rows + 10 * (rows + 1)), (232, 228, 220))
    for i, f in enumerate(files):
        sheet.paste(Image.open(f).resize((tw, th)),
                    (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    sheet.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", nargs="?", default="days/day01.json", help="题库 JSON 路径")
    ap.add_argument("--out", default=None, help="输出目录，默认 JSON 所在 days/ 的上一级 dayNN/")
    ap.add_argument("--no-preview", action="store_true", help="不生成总览图")
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)

    # 文本规范化：去掉作者手写的换行，折行统一交给 wrap() 处理，
    # 否则每行长短不齐（冷启动实测出现过）。
    def _flat(s):
        return " ".join(str(s).split()) if False else "".join(str(s).split("\r\n")).replace("\n", "").replace("\r", "").strip()

    for q in data["items"]:
        for k in ("q", "tip", "tag", "source"):
            if isinstance(q.get(k), str):
                q[k] = _flat(q[k])
        q["options"] = [_flat(o) for o in q["options"]]
        q["why"] = [_flat(p) for p in q["why"]]

    day = int(data["day"])
    items = data["items"]
    total = len(items) * 2

    json_dir = os.path.dirname(os.path.abspath(args.json))
    parent = os.path.dirname(json_dir) if os.path.basename(json_dir).lower() == "days" else os.getcwd()
    out = args.out or data.get("out") or os.path.join(parent, f"day{day:02d}")
    os.makedirs(out, exist_ok=True)

    warnings = []
    n_src = sum(1 for q in items if (q.get("source") or "").strip())
    if not 1 <= n_src <= 2:
        warnings.append(f"本期 {n_src} 道题带真题出处（source），应保持 1–2 道")
    saved = []
    for i, q in enumerate(items, 1):
        qf = os.path.join(out, f"{2*i-1:02d}-第{i}题.png")
        af = os.path.join(out, f"{2*i:02d}-第{i}题解析.png")
        question_card(q, i, day, total, warn=warnings.append).save(qf)
        answer_card(q, i, day, total, warn=warnings.append).save(af)
        saved += [qf, af]
        print("ok", i, f"{2*i-1:02d}/{2*i:02d}", out)

    for w in warnings:
        print("WARN", w)
    if not args.no_preview:
        print("preview:", make_preview(saved, os.path.join(parent, "preview.png")))
    print(f"done: {len(saved)} 张 -> {out}")


if __name__ == "__main__":
    main()
