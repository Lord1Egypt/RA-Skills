# -*- coding: utf-8 -*-
"""小红书「行测数量关系 · 每日1题」图片生成器（1080×1440，3:4）

用法：
    python scripts/make_cards.py days/day01.json
    python scripts/make_cards.py days/day01.json --no-preview

输出：JSON 的 days/ 上一级生成 dayNN/，共 3 张：
    01-题目.png   题干 + 四个选项
    02-答案.png   答案 + 分步解析 + 秒杀口诀
    03-考点.png   考点拆解 + 避坑 + 下期预告
另生成 preview.png 供自检（不上传）。

排版原则：所有折行、标点避头、数字/单位不断开都由脚本处理；
内容过长会打印 WARN，请回 JSON 改短，不要手改 PNG。
"""
import os
import re
import json
import argparse
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
M, RIGHT = 80, 1000
CW = RIGHT - M              # 920
TOP = 176

PAPER = (250, 246, 239)
CARD = (255, 255, 255)
INK = (32, 36, 46)
INK_MID = (62, 62, 70)
INK_SOFT = (128, 120, 108)
INK_FAINT = (168, 158, 145)
LINE = (231, 223, 210)
ACCENT = (198, 74, 48)       # 朱红：题目
GREEN = (14, 110, 101)       # 墨绿：答案
TINT = (243, 236, 226)
GREEN_TINT = (231, 242, 238)
SHADOW = (238, 231, 220)

BOLD_CANDIDATES = [
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
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

# 连写片段整体成块：比例 6∶5∶4、算式 15×16＝240、数字+单位 16天、英文 A。
TOKEN = re.compile(
    r"\d+(?:[.,]\d+)?(?:[∶:×÷＋+－\-=＝]\d+(?:[.,]\d+)?)+%?"
    r"|\d+(?:\.\d+)?[A-Za-z]?(?:%|℃|天|人|元|小时|分钟|千米|米)?"
    r"|[A-Za-z]+"
)


def pick_font(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise SystemExit("找不到中文字体，请修改脚本顶部的字体路径")


F_BOLD = pick_font(BOLD_CANDIDATES)
F_REG = pick_font(REG_CANDIDATES)

_cache = {}


def fb(size):
    return _cache.setdefault(("b", size), ImageFont.truetype(F_BOLD, size, index=0))


def fr(size):
    return _cache.setdefault(("r", size), ImageFont.truetype(F_REG, size, index=0))


def units(text):
    """把数字/算式/比例/英文词锁成不可拆的块，标点粘前字。"""
    out, i, n = [], 0, len(text)
    while i < n:
        m = TOKEN.match(text, i)
        if m and m.group(0):
            tok, i = m.group(0), m.end()
            while i < n and text[i] in NO_START:
                tok += text[i]
                i += 1
            out.append(tok)
        else:
            ch = text[i]
            i += 1
            if out and ch in NO_START:
                out[-1] += ch
            else:
                out.append(ch)
    return out


def wrap(draw, text, fnt, maxw):
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for u in units(para):
            if not cur or draw.textlength(cur + u, font=fnt) <= maxw:
                cur += u
            else:
                lines.append(cur)
                cur = u
        lines.append(cur)
    return lines


def paper(img):
    """极淡的点阵纸纹，给数学题一点“草稿纸”的感觉。"""
    d = ImageDraw.Draw(img)
    for y in range(24, H, 48):
        for x in range(24, W, 48):
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(240, 234, 223))


def deco(img, color):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([902, 214, 1000, 220], 3, fill=LINE)
    d.rounded_rectangle([916, 236, 1000, 242], 3, fill=LINE)
    d.rounded_rectangle([934, 258, 1000, 264], 3, fill=color)


def pill(img, x, y, text, fnt, fg, bg, padx=24, h=52, radius=None):
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=fnt) + padx * 2
    d.rounded_rectangle([x, y, x + w, y + h], radius or h / 2, fill=bg)
    d.text((x + padx, y + h / 2), text, font=fnt, fill=fg, anchor="lm")
    return x + w


def header(img, day, page, total):
    d = ImageDraw.Draw(img)
    pill(img, M, 64, "行测数量关系 · 每日1题", fb(26), CARD, ACCENT, h=56)
    d.text((RIGHT, 92), f"DAY {day:02d}", font=fb(26), fill=INK_SOFT, anchor="rm")
    d.text((RIGHT, 132), f"{page:02d} / {total:02d}", font=fr(22), fill=INK_FAINT, anchor="rm")
    d.line([M, TOP, RIGHT, TOP], fill=LINE, width=2)
    d.rounded_rectangle([M, TOP - 6, M + 68, TOP + 6], 6, fill=ACCENT)


def footer(img, left, color=INK_SOFT, size=24, right=None):
    d = ImageDraw.Draw(img)
    d.line([M, 1318, RIGHT, 1318], fill=LINE, width=2)
    d.text((M, 1348), left, font=fr(size), fill=color, anchor="lm")
    if right:
        d.text((RIGHT, 1348), right, font=fr(22), fill=INK_FAINT, anchor="rm")


def dots(img, current, total, color, y):
    d = ImageDraw.Draw(img)
    gap, r = 30, 7
    x = W / 2 - (total - 1) * gap / 2
    for i in range(total):
        if i + 1 == current:
            d.rounded_rectangle([x - 17, y - 8, x + 17, y + 8], 8, fill=color)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(226, 217, 204))
        x += gap


def shadow(d, box, radius, fill=CARD):
    d.rounded_rectangle([box[0], box[1] + 5, box[2], box[3] + 5], radius, fill=SHADOW)
    d.rounded_rectangle(box, radius, fill=fill, outline=LINE, width=2)


def card_question(data, warn):
    img = Image.new("RGB", (W, H), PAPER)
    paper(img)
    d = ImageDraw.Draw(img)
    deco(img, ACCENT)
    header(img, data["day"], 1, 3)

    # 钩子
    d.text((M, 206), data["hook"], font=fb(28), fill=ACCENT, anchor="la")

    # 标签
    tag_end = pill(img, M, 252, data["tag"], fb(25), GREEN, GREEN_TINT, padx=22, h=50)
    d.text((tag_end + 20, 277), data["subtag"], font=fr(23), fill=INK_SOFT, anchor="lm")

    # 题干：自动选字号；优先避免末行只剩一两个字（孤字）
    y = 336
    maxh = 470
    fallback = None
    chosen = None
    for size in (48, 46, 44, 42, 40, 38):
        fq, lh = fb(size), int(size * 1.58)
        groups = [wrap(d, p, fq, 888) for p in str(data["q"]).split("\n")]
        lines = [ln for g in groups for ln in g]
        if len(lines) * lh > maxh:
            continue
        if fallback is None:
            fallback = (fq, lh, lines)
        if not any(len(g) >= 2 and d.textlength(g[-1], font=fq) < 0.34 * 888
                   for g in groups):
            chosen = (fq, lh, lines)
            break
    pick = chosen or fallback
    if pick is None:
        fq, lh = fb(38), int(38 * 1.58)
        lines = wrap(d, data["q"], fq, 888)
    else:
        fq, lh, lines = pick
    d.rounded_rectangle([M, y + 10, M + 8, y + len(lines) * lh - 22], 4, fill=ACCENT)
    for ln in lines:
        d.text((M + 32, y), ln, font=fq, fill=INK, anchor="la")
        y += lh

    # 选项 2×2
    y += 44
    gap, th = 24, 152
    tw = (CW - gap) // 2
    for i, op in enumerate(data["options"]):
        x = M + (i % 2) * (tw + gap)
        ty = y + (i // 2) * (th + gap)
        shadow(d, [x, ty, x + tw, ty + th], 26)
        cx, cy = x + 62, ty + th // 2
        d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=TINT)
        d.text((cx, cy), "ABCD"[i], font=fb(32), fill=ACCENT, anchor="mm")
        d.text((x + 118, cy), op, font=fb(54), fill=INK, anchor="lm")
    bottom = y + 2 * th + gap

    if bottom > 1190:
        warn(f"题卡内容底边 {bottom}px 已压到进度点")

    # 限时提示
    pill(img, M, 1228, "建议用时 60 秒", fr(22), INK_SOFT, TINT, padx=20, h=44)

    dots(img, 1, 3, ACCENT, 1290)
    footer(img, "答案与秒杀思路见第2张 →", ACCENT, 26, right="第 1 张 / 共 3 张")
    return img


def card_answer(data, warn):
    img = Image.new("RGB", (W, H), PAPER)
    paper(img)
    d = ImageDraw.Draw(img)
    deco(img, GREEN)
    header(img, data["day"], 2, 3)

    letter = "ABCD"[data["answer"]]
    d.text((M, 206), "正确答案", font=fr(26), fill=INK_SOFT, anchor="la")
    d.rounded_rectangle([M, 246, M + 220, 466], 36, fill=GREEN)
    d.text((M + 110, 356), letter, font=fb(138), fill=CARD, anchor="mm")
    d.text((M + 262, 316), data["answerText"], font=fb(66), fill=INK, anchor="lm")
    d.text((M + 264, 402), "选 " + letter, font=fr(26), fill=INK_SOFT, anchor="lm")

    y = 512
    d.line([M, y, RIGHT, y], fill=LINE, width=2)
    d.text((M, y + 26), "解析 · 整体法", font=fb(32), fill=GREEN, anchor="la")
    d.line([M + 250, y + 50, M + 330, y + 50], fill=GREEN, width=4)
    y += 96

    # 分步解析：字号自适应
    for size in (31, 30, 29, 28):
        fstep, lh = fr(size), int(size * 1.68)
        heights = [max(1, len(wrap(d, s, fstep, 830))) for s in data["steps"]]
        if sum(heights) * lh + 5 * 12 <= 430:
            break
    for i, step in enumerate(data["steps"]):
        lines = wrap(d, step, fstep, 830)
        d.ellipse([M, y + 2, M + 42, y + 44], fill=GREEN_TINT)
        d.text((M + 21, y + 23), str(i + 1), font=fb(21), fill=GREEN, anchor="mm")
        for ln in lines:
            d.text((M + 62, y), ln, font=fstep, fill=INK_MID, anchor="la")
            y += lh
        y += 12

    # 口诀
    y += 10
    tip_lines = wrap(d, data["tip"], fb(33), 790)
    bh = 44 + len(tip_lines) * 50 + 26
    d.rounded_rectangle([M, y, RIGHT, y + bh], 26, fill=GREEN_TINT)
    d.rounded_rectangle([M, y, M + 10, y + bh], 5, fill=GREEN)
    d.text((M + 34, y + 20), "秒杀口诀", font=fb(21), fill=GREEN, anchor="la")
    ty = y + 54
    for ln in tip_lines:
        d.text((M + 34, ty), ln, font=fb(33), fill=(20, 60, 56), anchor="la")
        ty += 50
    y += bh

    # 验证
    y += 24
    d.text((M, y + 2), "验证", font=fb(22), fill=GREEN, anchor="la")
    v_lines = wrap(d, data["verify"], fr(26), 772)
    vy = y
    for ln in v_lines:
        d.text((M + 86, vy), ln, font=fr(26), fill=(122, 114, 101), anchor="la")
        vy += 38
    y = max(vy, y + 42)

    # 另解
    y += 16
    alt_lines = wrap(d, data["alt"], fr(24), 900)
    for ln in alt_lines:
        d.text((M, y), ln, font=fr(24), fill=(150, 140, 126), anchor="la")
        y += 36

    if y > 1210:
        warn(f"答案卡内容底边 {y}px 会撞到底部互动区")
    if len(tip_lines) > 1:
        warn(f"口诀折成 {len(tip_lines)} 行，建议压到 20 字以内")

    dots(img, 2, 3, GREEN, 1290)
    footer(img, "第 2 张 · 答案解析", INK_SOFT, 24, right=f"行测数量关系 · Day {data['day']:02d}")
    return img


def card_point(data, warn):
    img = Image.new("RGB", (W, H), PAPER)
    paper(img)
    d = ImageDraw.Draw(img)
    deco(img, ACCENT)
    header(img, data["day"], 3, 3)

    d.text((M, 206), "这道题在考什么", font=fb(42), fill=INK, anchor="la")
    d.text((M, 268), f"{data['tag']} · {data['subtag']}", font=fr(24), fill=INK_SOFT, anchor="la")

    y = 336
    for i, p in enumerate(data["points"], 1):
        d.text((M, y), f"0{i}", font=fb(44), fill=(226, 190, 178), anchor="la")
        d.text((M + 92, y + 2), p["t"], font=fb(32), fill=ACCENT, anchor="la")
        body_lines = wrap(d, p["b"], fr(29), 800)
        by = y + 46
        for ln in body_lines:
            d.text((M + 92, by), ln, font=fr(29), fill=INK_MID, anchor="la")
            by += 46
        y = max(by + 26, y + 200)

    # 口诀
    y = max(y + 22, 920)
    tip_lines = wrap(d, data["tip"], fb(34), 800)
    bh = 46 + len(tip_lines) * 52 + 24
    shadow(d, [M, y, RIGHT, y + bh], 26, fill=(255, 250, 243))
    d.rounded_rectangle([M, y, M + 10, y + bh], 5, fill=ACCENT)
    d.text((M + 34, y + 20), "背下这一句", font=fb(21), fill=ACCENT, anchor="la")
    ty = y + 56
    for ln in tip_lines:
        d.text((M + 34, ty), ln, font=fb(34), fill=(92, 44, 30), anchor="la")
        ty += 52
    y += bh

    # 下期预告
    d.text((M, 1156), "下期预告", font=fb(21), fill=INK_FAINT, anchor="la")
    d.text((M, 1190), data["next"], font=fb(32), fill=GREEN, anchor="la")
    d.text((RIGHT, 1198), "关注我，每天1道数量关系", font=fr(22), fill=INK_SOFT, anchor="rm")

    if y > 1145:
        warn(f"考点卡口诀框底边 {y}px 压到下期预告")

    dots(img, 3, 3, ACCENT, 1290)
    footer(img, "先收藏，考前再刷一遍", INK_SOFT, 24, right=f"行测数量关系 · Day {data['day']:02d}")
    return img


def write_copy(data, out):
    """有 titles/body/tags 时，同步生成可直接粘贴的小红书文案。"""
    titles = [str(t).strip() for t in data.get("titles", []) if str(t).strip()]
    body = [str(p).strip() for p in data.get("body", []) if str(p).strip()]
    tags = [str(t).strip() for t in data.get("tags", []) if str(t).strip()]
    if not (titles or body or tags):
        return None

    lines = [f"# Day {int(data['day']):02d} · {data['topic']}", ""]
    if titles:
        lines += ["## 标题（选 1）", ""]
        lines += [f"{i}. {t}" for i, t in enumerate(titles, 1)]
        lines.append("")
    if body:
        lines += ["## 正文", ""]
        for p in body:
            lines += [p, ""]
    if tags:
        lines += ["## 标签", "", " ".join(tags), ""]
    lines += ["## 发布", "",
              "- 图1 题目 → 图2 答案解析 → 图3 考点，按序号发。",
              "- 首图就是题，正文别剧透答案；答案可置顶评论区。"]

    path = os.path.join(out, "文案.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def make_preview(files, out_path):
    tw, th = 360, 480
    gap = 12
    sheet = Image.new("RGB", (tw * len(files) + gap * (len(files) + 1),
                              th + gap * 2), (232, 228, 220))
    for i, f in enumerate(files):
        sheet.paste(Image.open(f).resize((tw, th)),
                    (gap + i * (tw + gap), gap))
    sheet.save(out_path)
    return out_path


def flat(s):
    return "".join(str(s).split("\r\n")).replace("\n", "").replace("\r", "").strip()


def flat_keep_lines(s):
    """题干允许用换行分段（比如把“问：…”单独放一段），段内仍折叠空白。"""
    paras = ["".join(p.split()) for p in str(s).replace("\r", "").split("\n")]
    return "\n".join(p for p in paras if p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", nargs="?", default="days/day01.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-preview", action="store_true")
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as fh:
        data = json.load(fh)

    for k in ("hook", "tag", "subtag", "q", "answerText", "verify", "alt", "tip", "next"):
        if isinstance(data.get(k), str):
            data[k] = flat_keep_lines(data[k]) if k == "q" else flat(data[k])
    data["options"] = [flat(o) for o in data["options"]]
    data["steps"] = [flat(s) for s in data["steps"]]
    for p in data["points"]:
        p["t"], p["b"] = flat(p["t"]), flat(p["b"])

    json_dir = os.path.dirname(os.path.abspath(args.json))
    parent = os.path.dirname(json_dir) if os.path.basename(json_dir).lower() == "days" else os.getcwd()
    out = args.out or os.path.join(parent, f"day{int(data['day']):02d}")
    os.makedirs(out, exist_ok=True)

    warnings = []
    files = [
        (os.path.join(out, "01-题目.png"), card_question(data, warnings.append)),
        (os.path.join(out, "02-答案.png"), card_answer(data, warnings.append)),
        (os.path.join(out, "03-考点.png"), card_point(data, warnings.append)),
    ]
    for path, img in files:
        img.save(path)
        print("ok", os.path.basename(path))

    copy_path = write_copy(data, out)
    if copy_path:
        print("ok", os.path.basename(copy_path))

    for w in warnings:
        print("WARN", w)
    if not args.no_preview:
        print("preview:", make_preview([p for p, _ in files], os.path.join(parent, "preview.png")))
    print("done ->", out)


if __name__ == "__main__":
    main()
