# -*- coding: utf-8 -*-
"""semantic_stream.py — 长书稿 → 固定栏位的语义化内容分配（reading-notes-master v2.14）

解决三个真实故障（2026-11-10 四刊合璧 40 页实跑）：
  1. 单一游标顺序消费 → 40 页只用了 20 万字中的 6525 字（3.2%），且开头是版权页/献词。
  2. 按字数硬切 → 只有 7.1% 片段以标点收尾，读起来断章。
  3. 只取完整短语 → 栏宽尾差浪费，中文掉到 4276 字（−34%）。

四步管线：剥离前置 matter → 中文标点短语化 → 全书 N 等分 → 栏宽尾差补足。
另附 WCAG 相对亮度文字色择优（替代「亮度>0.55」二值阈值）。

纯标准库，无第三方依赖。可作为库 import，也可 CLI 自检：

    python3 semantic_stream.py --self-test
    python3 semantic_stream.py --file book.txt --pages 40 --cap 18 --json stream.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import deque

__version__ = "2.14.0"

PUNCT = "。！？；，、："
CJK = re.compile(r"[\u4e00-\u9fff]")
DARK = (0.13, 0.11, 0.12)
INK = (0.0, 0.0, 0.0)          # 中灰底兜底：纯黑可达 5.28:1（深墨仅 4.22、白仅 3.98）
WHITE = (1.0, 1.0, 1.0)


# ── 1) 前置 matter / 附录剥离 ───────────────────────────────
def strip_front_matter(text: str, start_marker: str = "前言",
                       end_marker: str = "Table of Contents"):
    """返回 (body, start, end)。找不到标记时退化为全文，绝不抛异常阻塞交付。

    电子书 txt 常见结构：版权信息 → 书名/作者 → 献词 → 前言(正文起点) …
    → 致谢/译者后记 → 书末目录(Table of Contents)。
    若书稿结构不同，显式传 start_marker / end_marker，或先手工指定 body。
    """
    start = text.find(start_marker)
    start = max(0, start)
    end = text.rfind(end_marker)
    if end <= start:
        end = len(text)
    return text[start:end], start, end


# ── 2) 中文标点短语化 ──────────────────────────────────────
def build_fragments(text: str, maxlen: int = 10):
    """按中文标点切成完整语义短语；超长段再均分。

    中文之间的空白直接删除，英文词之间保留单空格（避免 RobertCialdini）。
    短语尽量以标点收尾，这是「不切在句中」的可度量代理指标。
    """
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.findall(r"[^%s]+[%s]?" % (PUNCT, PUNCT), text)
    out = []
    for part in parts:
        part = part.strip()
        while len(part) > maxlen:
            out.append(part[:maxlen])
            part = part[maxlen:]
        if part:
            out.append(part)
    return out


# ── 3) 全书 N 等分队列 ────────────────────────────────────
def page_queues(frags, npages: int):
    """每页取全书的 1/N 连续片段；页内连续、页间跨全书。

    返回 list[deque]，索引 0..N-1 对应第 1..N 页。
    """
    n = len(frags)
    return [deque(frags[int(i * n / npages):int((i + 1) * n / npages)])
            for i in range(npages)]


# ── 4) 栏宽尾差补足 ───────────────────────────────────────
def take_frags(q, cap: int, stats: dict | None = None):
    """取 ≤cap 字：优先完整短语，尾差用下一短语前缀补足，剩余留队首。

    - 不切在成对符号或英文单词中间。
    - 剩余部分 appendleft 回队首 → 下一个槽位接着读，跨槽位文本连续。
    - stats 可累计 sem_full / sem_chars，用于计算 semantic_char_pct。
    """
    buf, full = "", 0
    while q and len(buf) + len(q[0]) <= cap:
        seg = q.popleft()
        buf += seg
        full += len(seg)
    if q and len(buf) < cap:
        seg = q[0]
        need = cap - len(buf)
        if need >= 2 and len(seg) > need:
            cut = need
            if seg[cut - 1] in "（《「‘“" or (
                    seg[cut - 1].isalnum() and seg[cut:cut + 1].isalnum()):
                cut = max(1, cut - 1)
            buf += seg[:cut]
            q.popleft()
            q.appendleft(seg[cut:])
        elif len(seg) <= need:
            buf += q.popleft()
            full += len(seg)
    if not buf and q:
        seg = q.popleft()
        buf = seg[:cap]
        full += min(cap, len(seg))
        if seg[cap:]:
            q.appendleft(seg[cap:])
    if stats is not None:
        stats["sem_full"] = stats.get("sem_full", 0) + full
        stats["sem_chars"] = stats.get("sem_chars", 0) + len(buf)
    return buf


# ── WCAG 相对亮度与文字色择优 ──────────────────────────────
def _lum(c):
    v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def contrast(a, b):
    """a/b 为 0–1 的 RGB 三元组，返回 WCAG 2.x 对比度（1–21）。"""
    l1, l2 = sorted((_lum(a), _lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def text_color(bg, dark=DARK, white=WHITE, min_contrast=4.5):
    """中灰底不再失读：取与底色对比度更高的文字色，并做纯黑/纯白兜底。

    实测（40 页 / 530 槽）：二值阈值方案 13.7% 槽位 <4.5；
    两色择优方案 1.1%（中位 16.79）；加入纯黑兜底后中灰底也能达标。
    注意 (0.5,0.5,0.5) 中灰下 DARK 仅 4.22、WHITE 仅 3.98，两者都不过 4.5，
    故当最优仍不达标时在 (纯黑, 纯白) 中再择优。
    """
    best = max((dark, white), key=lambda c: contrast(bg, c))
    if contrast(bg, best) < min_contrast:
        best = max((INK, white), key=lambda c: contrast(bg, c))
    return best


def sampled_positions(frags, npages: int, body_len: int):
    """各页首段在正文中的相对位置（0–1），用于验证「跨全书」而非只取开头。"""
    out = []
    n = len(frags)
    acc = 0
    for i in range(npages):
        a = int(i * n / npages)
        acc = sum(len(f) for f in frags[:a])
        out.append(round(acc / max(1, body_len), 4))
    return out


def self_test():
    text = ("版权信息本书纸版由北京联合出版公司于2017年9月出版。"
            "前言来到行为科学的黄金时代1946年，伟大的诗人奥登发表了一首诗作。"
            "行为经济学提升了社会心理学的公众地位，因为前者继承了后者的核心特征。"
            "Table of Contents书名页版权信息目录导言")
    body, s, e = strip_front_matter(text)
    assert "版权信息本书纸版" not in body, "前置 matter 未剥离"
    assert "Table of Contents" not in body, "书末附录未剥离"
    frags = build_fragments(body, maxlen=10)
    assert frags and all(len(f) <= 10 for f in frags), "短语超长"
    qs = page_queues(frags, 4)
    assert len(qs) == 4 and all(qs), "空页队列"
    stats = {}
    outs = []
    for q in qs:
        for _ in range(12):
            outs.append(take_frags(q, 18, stats))
    assert all(len(t) <= 18 for t in outs), "栏宽溢出"
    assert stats["sem_chars"] > 0
    semantic_pct = 100 * stats["sem_full"] / stats["sem_chars"]
    # 文字色择优：中灰底必须给出对比度更高的那一个
    mid = (0.5, 0.5, 0.5)
    chosen = text_color(mid)
    assert contrast(mid, chosen) >= 4.5, "纯黑兜底未生效"
    assert chosen == INK, "中灰底应触发纯黑兜底"
    assert contrast(mid, DARK) < 4.5 and contrast(mid, WHITE) < 4.5, "边界前提已变化"
    # 同一把尺：采样位置单调递增
    pos = sampled_positions(frags, 4, len(body))
    assert pos == sorted(pos), "采样位置非单调"
    return dict(ok=True, body_chars=len(body), fragments=len(frags),
                semantic_char_pct=round(semantic_pct, 1),
                sampled_positions=pos,
                mid_gray_contrast=round(contrast(mid, chosen), 2),
                mid_gray_ink_fallback=True,
                mid_gray_before=dict(dark=round(contrast(mid, DARK), 2),
                                     white=round(contrast(mid, WHITE), 2)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="书稿 txt（UTF-8）")
    ap.add_argument("--pages", type=int, default=40, help="成品页数 / 采样窗口数")
    ap.add_argument("--maxlen", type=int, default=10, help="单短语最大字数")
    ap.add_argument("--cap", type=int, default=18, help="单槽位字数上限（演示用）")
    ap.add_argument("--start-marker", default="前言")
    ap.add_argument("--end-marker", default="Table of Contents")
    ap.add_argument("--json", help="输出摘要 JSON")
    ap.add_argument("--self-test", action="store_true", help="运行内置自检")
    a = ap.parse_args()

    if a.self_test:
        res = self_test()
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    if not a.file:
        ap.error("需要 --file 或 --self-test")

    raw = open(a.file, encoding="utf-8").read()
    body, s, e = strip_front_matter(raw, a.start_marker, a.end_marker)
    frags = build_fragments(body, a.maxlen)
    qs = page_queues(frags, a.pages)
    stats = {}
    samples = []
    for i, q in enumerate(qs):
        for _ in range(6):
            t = take_frags(q, a.cap, stats)
            if t:
                samples.append(dict(page=i + 1, text=t))
    res = dict(version=__version__, raw_chars=len(raw), body_chars=len(body),
               body_span=[s, e], fragments=len(frags), pages=a.pages,
               semantic_char_pct=round(100 * stats["sem_full"] /
                                       max(1, stats["sem_chars"]), 1),
               sampled_positions=sampled_positions(frags, a.pages, len(body)),
               samples=samples[:8])
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if a.json:
        json.dump(res, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
