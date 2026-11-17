# -*- coding: utf-8 -*-
"""小红书「判断推理 · 每日5题」图片生成器（1080×1440，3:4）

与公基版同一套视觉，但判断推理题干/选项普遍更长，所以：
  - 题干、选项字号按内容高度自适应（44→30 / 34→27）
  - 选项卡片高度随行数伸缩，不再固定 118px

用法:
    python make_cards.py ../days/day01.json
输出：days/ 上一级生成 dayNN/（10 张，题→解析交替）+ preview.png
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
HEADER_PILL = "判断推理 · 每日5题"

CONTENT_BOTTOM = 1200   # 内容底线（下方是进度点/页脚）
DOTS_Y_Q = 1250         # 题目卡进度点固定高度，避免压到选项卡片
DOTS_Y_A = 1252
BOX_L, BOX_R = 80, 1000
STEM_X, STEM_W = 112, 872
OPT_TEXT_X, OPT_TEXT_W = 214, 760


def pick_font(cands):
    for p in cands:
        if os.path.exists(p):
            return p
    raise SystemExit("找不到中文字体，请改 BOLD_CANDIDATES / REG_CANDIDATES")


F_BOLD = pick_font(BOLD_CANDIDATES)
F_REG = pick_font(REG_CANDIDATES)
_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def units(text):
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


def wrap(text, fnt, maxw):
    lines = []
    for para in str(text).split("\n"):
        cur = ""
        for u in units(para):
            if _MEASURE.textlength(cur + u, font=fnt) <= maxw or not cur:
                cur += u
            else:
                lines.append(cur)
                cur = u
        lines.append(cur)
    return lines


def wrap_clauses(text, fnt, maxw):
    """按逗号切句再拼行，避免把“脂肪”这类词从中间劈开。
    只在解析卡的正确选项上用：句子短、行数少，逗号断行最自然。"""
    text = str(text)
    parts = []
    buf = ""
    for ch in text:
        buf += ch
        if ch in "，；。":
            parts.append(buf)
            buf = ""
    if buf:
        parts.append(buf)
    if len(parts) == 1:
        return wrap(text, fnt, maxw)

    lines, cur = [], ""
    for p in parts:
        if _MEASURE.textlength(cur + p, font=fnt) <= maxw:
            cur += p
        else:
            if cur:
                lines.append(cur)
            while _MEASURE.textlength(p, font=fnt) > maxw:
                piece = ""
                for u in units(p):
                    if _MEASURE.textlength(piece + u, font=fnt) <= maxw or not piece:
                        piece += u
                    else:
                        lines.append(piece)
                        piece = u
                p = piece
            cur = p
    if cur:
        lines.append(cur)
    return lines


def deco(img, color):
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
    pill(img, 80, 64, HEADER_PILL, font(F_BOLD, 26), CARD, ACCENT, h=56)
    d.text((1000, 92), f"DAY {day:02d}", font=font(F_BOLD, 26), fill=INK_SOFT, anchor="rm")
    d.text((1000, 132), f"{page:02d} / {total:02d}", font=font(F_REG, 22),
           fill=(168, 158, 145), anchor="rm")
    d.line([80, 176, 1000, 176], fill=LINE, width=2)
    d.rounded_rectangle([80, 170, 148, 182], 6, fill=ACCENT)


def footer(img, left, color=INK_SOFT, size=24, right=None):
    d = ImageDraw.Draw(img)
    d.line([80, 1318, 1000, 1318], fill=LINE, width=2)
    d.text((80, 1348), left, font=font(F_REG, size), fill=color, anchor="lm")
    if right:
        d.text((1000, 1348), right, font=font(F_REG, 22), fill=(176, 166, 152), anchor="rm")


def dots(img, current, total, color, y):
    d = ImageDraw.Draw(img)
    gap, r = 30, 8
    x = W / 2 - (total - 1) * gap / 2
    for i in range(total):
        if i + 1 == current:
            d.rounded_rectangle([x - 17, y - 8, x + 17, y + 8], 8, fill=color)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(226, 217, 204))
        x += gap


# ---------------------------------------------------------------- 题目卡版面
def question_metrics(q, qs, osz, hook=None, shift=0):
    fq, fo = font(F_BOLD, qs), font(F_REG, osz)
    lh_q, lh_o = int(qs * 1.54), int(osz * 1.5)
    y = 210 + shift
    if hook:
        y += 62
    y += 56 + 30                       # 题型胶囊 + 间距
    stem_lines = wrap(q["q"], fq, STEM_W)
    stem_top = y
    y += len(stem_lines) * lh_q + 34
    boxes = []
    for op in q["options"]:
        lines = wrap(op, fo, OPT_TEXT_W)
        bh = len(lines) * lh_o + 34
        boxes.append({"y": y, "h": bh, "lines": lines})
        y += bh + 13
    return {"bottom": y - 13, "stem_top": stem_top, "stem_lines": stem_lines,
            "boxes": boxes, "lh_q": lh_q, "lh_o": lh_o, "qs": qs, "osz": osz,
            "shift": shift}


def pick_question_layout(q, hook=None, shift=0, limit=CONTENT_BOTTOM):
    """在字号阶梯里挑“最大且不溢出”的组合；短题会自动放大字号把版面撑起来。

    选项字号有 30px 下限（同系列内保持可读性一致），实在放不下才降到 28/27。
    """
    for ladder in ((38, 36, 34, 32, 30), (38, 36, 34, 32, 30, 28, 27)):
        best = None
        for qs in (52, 48, 44, 41, 38, 35, 32, 30):
            for osz in ladder:
                m = question_metrics(q, qs, osz, hook, shift)
                if m["bottom"] <= limit:
                    score = qs * 10 + osz
                    if best is None or score > best[0]:
                        best = (score, m)
        if best:
            return best[1]
    return question_metrics(q, 30, 27, hook, shift)


def question_card(q, idx, day, total, cover=False, hook=None, warn=None):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    deco(img, ACCENT)
    header(img, day, 2 * idx - 1, total)

    # 先按最小字号量一遍，给“内容偏短”的卡按比例整体下移，避免上半页挤、下半页空
    small = question_metrics(q, 30, 27, hook if cover else None)
    shift = int(min(max((1150 - small["bottom"]) * 0.38, 0), 124))
    m = pick_question_layout(q, hook if cover else None, shift, CONTENT_BOTTOM)

    y = 210 + m["shift"]
    if cover:
        d.text((80, y), hook or "今天这5题，能全对的不到三成",
               font=font(F_BOLD, 30), fill=ACCENT, anchor="la")
        y += 62
    pill(img, 80, y, q["tag"], font(F_BOLD, 28), ACCENT_D, (231, 242, 238), h=56)

    fq = font(F_BOLD, m["qs"])
    ty = m["stem_top"]
    d.rounded_rectangle([80, ty + 8, 89, ty + 8 + len(m["stem_lines"]) * m["lh_q"] - 22],
                        4, fill=ACCENT)
    for ln in m["stem_lines"]:
        d.text((STEM_X, ty), ln, font=fq, fill=INK, anchor="la")
        ty += m["lh_q"]

    fo = font(F_REG, m["osz"])
    for i, box in enumerate(m["boxes"]):
        d.rounded_rectangle([BOX_L, box["y"], BOX_R, box["y"] + box["h"]], 24, fill=CARD,
                            outline=(233, 225, 213), width=2)
        cy = box["y"] + box["h"] / 2
        cx = 152
        d.ellipse([cx - 31, cy - 31, cx + 31, cy + 31], fill=TINT)
        d.text((cx, cy), "ABCD"[i], font=font(F_BOLD, 32), fill=ACCENT, anchor="mm")
        oy = cy - (len(box["lines"]) - 1) * m["lh_o"] / 2
        for ln in box["lines"]:
            d.text((OPT_TEXT_X, oy), ln, font=fo, fill=(52, 56, 66), anchor="lm")
            oy += m["lh_o"]

    if m["bottom"] > CONTENT_BOTTOM and warn is not None:
        warn(f"第{idx}题过长：内容底边 {m['bottom']}px，已压到最小字号")

    nq = total // 2
    dots(img, idx, nq, ACCENT, DOTS_Y_Q)
    footer(img, "答案在下一张 →", ACCENT, 26, right=f"第 {idx} 题 / 共 {nq} 题")
    return img.convert("RGB"), m["qs"], m["osz"]


# ---------------------------------------------------------------- 解析卡版面
def answer_metrics(q, bs, dg):
    lh = int(bs * 1.72)
    y = 500 + 76
    paras = []
    for para in q["why"]:
        lines = wrap(para, dg, 900)
        paras.append((y, lines))
        y += len(lines) * lh + 16
    y += 26
    ft, tlh = dg, int(bs * 1.55)
    tlines = wrap(q["tip"], ft, 800)
    bh = 46 + len(tlines) * tlh + 30
    return {"paras": paras, "tip_y": y, "tip_h": bh, "tip_lines": tlines,
            "bottom": y + bh, "bs": bs, "lh": lh, "tlh": tlh}


def pick_answer_layout(q):
    best = None
    for bs in (34, 32, 30, 28, 27):
        m = answer_metrics(q, bs, font(F_REG, bs))
        if m["bottom"] <= 1186:
            if best is None:
                best = m
    if best:
        return best
    return answer_metrics(q, 27, font(F_REG, 27))


def answer_card(q, idx, day, total, warn=None):
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    deco(img, ACCENT_D)
    header(img, day, 2 * idx, total)

    letter = "ABCD"[q["answer"]]
    src = q.get("source") or ""
    d.text((80, 232), "正确答案", font=font(F_REG, 28), fill=INK_SOFT, anchor="la")
    d.rounded_rectangle([80, 276, 236, 432], 36, fill=ACCENT_D)
    d.text((158, 354), letter, font=font(F_BOLD, 150), fill=CARD, anchor="mm")

    fopt, ols = fit_answer_option(q["options"][q["answer"]], 700)
    oy = 354 - (len(ols) - 1) * 29
    for ln in ols:
        d.text((282, oy), ln, font=fopt, fill=INK, anchor="lm")
        oy += 58

    d.text((80, 500), "解 析", font=font(F_BOLD, 34), fill=ACCENT_D, anchor="la")
    d.line([186, 524, 260, 524], fill=ACCENT_D, width=4)

    m = pick_answer_layout(q)
    fb = font(F_REG, m["bs"])
    for y0, lines in m["paras"]:
        yy = y0
        for ln in lines:
            d.text((80, yy), ln, font=fb, fill=(62, 62, 70), anchor="la")
            yy += m["lh"]

    ft = font(F_BOLD, m["bs"] - 1)
    y = m["tip_y"]
    bh = m["tip_h"]
    d.rounded_rectangle([80, y, 1000, y + bh], 28, fill=(235, 245, 242))
    d.rounded_rectangle([80, y, 92, y + bh], 6, fill=ACCENT_D)
    d.text((124, y + 26), "记一句", font=font(F_BOLD, 24), fill=ACCENT_D, anchor="la")
    ty = y + 70
    for ln in m["tip_lines"]:
        d.text((124, ty), ln, font=ft, fill=(20, 60, 56), anchor="la")
        ty += m["tlh"]

    if m["bottom"] > 1186 and warn is not None:
        warn(f"第{idx}题解析过长：底边 {m['bottom']}px，已撞到互动区")
    if len(m["tip_lines"]) > 1 and warn is not None:
        warn(f"第{idx}题“记一句”折成 {len(m['tip_lines'])} 行，建议压到 24 字内")

    if src and m["bottom"] + 44 <= 1162:
        d.text((80, m["bottom"] + 44), "真题出处 · " + src,
               font=font(F_REG, 22), fill=(172, 162, 148), anchor="la")

    nq = total // 2
    d.text((W / 2, DOTS_Y_A - 44), "答对了吗？评论区报个到",
           font=font(F_REG, 24), fill=(158, 148, 134), anchor="mm")
    dots(img, idx, nq, ACCENT_D, DOTS_Y_A)
    footer(img, f"第 {idx} 题解析", INK_SOFT, 24, right=f"判断推理 · Day {day:02d}")
    return img.convert("RGB")


def fit_answer_option(text, maxw, max_lines=3):
    """解析卡右上「正确选项」大字：先 40px，超过 3 行就缩到 36/34。"""
    for sz in (40, 36, 34, 32):
        fnt = font(F_BOLD, sz)
        lines = wrap_clauses(text, fnt, maxw)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(F_BOLD, 32)
    return fnt, wrap_clauses(text, fnt, maxw)


def make_preview(files, out_path, cols=5):
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
    ap.add_argument("json", nargs="?", default="days/day01.json")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-preview", action="store_true")
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as f:
        data = json.load(f)

    def _flat(s):
        return "".join(str(s).split("\r\n")).replace("\n", "").replace("\r", "").strip()

    data["hook"] = _flat(data.get("hook") or "")
    for q in data["items"]:
        for k in ("q", "tip", "tag"):
            if isinstance(q.get(k), str):
                q[k] = _flat(q[k])
        q["options"] = [_flat(o) for o in q["options"]]
        q["why"] = [_flat(p) for p in q["why"]]

    day = int(data["day"])
    items = data["items"]
    total = len(items) * 2

    json_dir = os.path.dirname(os.path.abspath(args.json))
    # days/ 结构 → 输出到项目根；其它位置（如模板）→ 输出到 JSON 同级，避免写进 cwd
    if os.path.basename(json_dir).lower() == "days":
        parent = os.path.dirname(json_dir)
    else:
        parent = json_dir
    out = args.out or data.get("out") or os.path.join(parent, f"day{day:02d}")
    os.makedirs(out, exist_ok=True)

    warnings, saved = [], []
    for i, q in enumerate(items, 1):
        qf = os.path.join(out, f"{2*i-1:02d}-第{i}题.png")
        af = os.path.join(out, f"{2*i:02d}-第{i}题解析.png")
        cover = (i == 1 and data.get("cover_hook", True))
        img, qs, osz = question_card(q, i, day, total, cover=cover,
                                     hook=data.get("hook"), warn=warnings.append)
        img.save(qf)
        answer_card(q, i, day, total, warn=warnings.append).save(af)
        saved += [qf, af]
        print(f"ok {i}  题干{qs}px/选项{osz}px  {2*i-1:02d}/{2*i:02d}")

    for w in warnings:
        print("WARN", w)
    if not args.no_preview:
        print("preview:", make_preview(saved, os.path.join(parent, "preview.png")))
    print(f"done: {len(saved)} 张 -> {out}")


if __name__ == "__main__":
    main()
