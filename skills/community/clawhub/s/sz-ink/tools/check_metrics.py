# -*- coding: utf-8 -*-
"""sz-ink 体检脚本 check_metrics.py
用法: python check_metrics.py <文本文件> [--register colloquial_media|official_doc|explanatory]
输出: 九项指标 JSON（stdout）。阈值读 rules/metrics.yaml（单一事实源）。
状态: v0.1 骨架——rhythm_cv/cliche_density/modal_temp/hedge_density/para_breath 已实现；
     v0.2.0: 九项指标全部实现（pattern_entropy/lex_rotation/struct_regularity 已补）。
"""
import json
import math
import re
import sys
from pathlib import Path

# ---------- 分词工具 ----------

SENT_SPLIT = re.compile(r"[。！？；]")
BURST_SPLIT = re.compile(r"[，,、——…：:]")

# 词表路径（批次2填充后自动生效；当前为空表则指标计0）
LEX_DIR = Path(__file__).resolve().parent.parent / "assets" / "lexicon"


def load_words(name: str) -> list:
    f = LEX_DIR / name
    if f.exists():
        return [w.strip() for w in f.read_text(encoding="utf-8").splitlines() if w.strip() and not w.startswith("#")]
    return []


def split_sentences(text: str) -> list:
    return [p for p in (s.strip() for s in SENT_SPLIT.split(text)) if p]


def split_bursts(text: str) -> list:
    parts = re.split(r"[。！？；，,、——…：:]", text)
    return [p for p in (s.strip() for s in parts) if p]


# ---------- 指标实现 ----------

def m_rhythm_cv(text: str) -> float:
    lens = [len(s) for s in split_sentences(text)]
    if not lens:
        return 0.0
    mean = sum(lens) / len(lens)
    var = sum((l - mean) ** 2 for l in lens) / len(lens)
    return math.sqrt(var) / mean if mean else 0.0


def m_short_burst(text: str) -> float:
    bursts = split_bursts(text)
    if not bursts:
        return 0.0
    return sum(1 for b in bursts if len(b) <= 6) / len(bursts)


# 引用语境配对（豁免用）：成对引号内的内容视为"引用"而非"使用"
# 含 ASCII 直引号：实测语料（含本技能自身文档）中文引用常用 "..." 而非弯引号
QUOTE_PAIRS = [("\u201c", "\u201d"), ("\u2018", "\u2019"),
               ("\u300c", "\u300d"), ("\u300e", "\u300f"),
               ("\u0022", "\u0022")]


def strip_quoted(text: str) -> str:
    """删去成对引号内的内容（引用反例不计套话）。
    2026-10-28 博客自检教训：文章引用"赋能/闭环"当反例，被词表计数误判 3.18/千字。
    护栏：引号内容不跨行、≤80 字——防止不成对引号吞掉半个文档。"""
    out = text
    for l, r in QUOTE_PAIRS:
        pat = re.escape(l) + r"[^" + re.escape(r) + r"\n]{0,80}" + re.escape(r)
        out = re.sub(pat, "", out)
    return out


def cliche_hits(text: str, words: list) -> dict:
    """未豁免（引号外）的套话命中明细：word -> count。"""
    counted = strip_quoted(text)
    return {w: counted.count(w) for w in words if counted.count(w)}


def m_cliche(text: str, words: list) -> float:
    if not words:
        return 0.0
    counted = strip_quoted(text)
    n = len(text)  # 分母用原文字数：引用也是文面的一部分
    return sum(counted.count(w) for w in words) / n * 1000 if n else 0.0


def m_modal(text: str) -> float:
    words = load_words("modal_common.txt")
    return m_cliche(text, words)


def m_hedge(text: str) -> float:
    words = load_words("hedge_common.txt")
    return m_cliche(text, words)


def m_para_breath(text: str) -> dict:
    paras = [p.strip() for p in text.split("\n") if p.strip()]
    if len(paras) < 2:
        return {"cv": 0.0, "short_ratio": 0.0}
    lens = [len(p) for p in paras]
    mean = sum(lens) / len(lens)
    var = sum((l - mean) ** 2 for l in lens) / len(lens)
    cv = math.sqrt(var) / mean if mean else 0.0
    short = sum(1 for l in lens if l < 40) / len(lens)
    return {"cv": round(cv, 3), "short_ratio": round(short, 3)}


def m_pattern_entropy(text: str) -> float:
    """句类分布熵：陈述/疑问/感叹/祈使四类，熵低=句类单一。归一化到0-1。"""
    sents = split_sentences(text)
    if len(sents) < 4:
        return 0.0
    raw = text
    n = 0
    counts = {"q": 0, "ex": 0, "im": 0, "st": 0}
    # 按句末标点重分句（保留标点信息）
    parts = [p for p in re.split(r'(?<=[。！？!?])', raw) if p.strip()]
    for s in parts:
        s = s.strip()
        if not s:
            continue
        n += 1
        if s[-1] in "？?":
            counts["q"] += 1
        elif s[-1] in "！!":
            counts["ex"] += 1
        elif re.match(r'^(请|别|不要|记得|试试|来|走|去|给|帮|吧[，。])', s) or s.endswith("吧。") or s.endswith("吧！"):
            counts["im"] += 1
        else:
            counts["st"] += 1
    if n == 0:
        return 0.0
    import math as _m
    ent = 0.0
    for c in counts.values():
        if c:
            p = c / n
            ent -= p * _m.log2(p)
    return round(ent / 2.0, 3)  # 归一化（最大熵=log2(4)=2）


TOP_CONTENT_MIN = 2  # 词长下限


def m_lex_rotation(text: str) -> float:
    """词汇轮换代理：最高频实词的千字频次。值越高=一词到底越严重。
    完整同义组聚类需词表支撑，此为无词表代理版。"""
    words = re.findall(r'[\u4e00-\u9fff]{2,6}', text)
    stop = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '都', '一', '上',
            '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看',
            '好', '自己', '这', '那', '但', '还', '被', '把', '让', '可以', '我们',
            '他们', '一个', '什么', '怎么', '因为', '所以', '如果', '现在', '时候'}
    n_chars = len(text)
    if not words or n_chars == 0:
        return 0.0
    from collections import Counter
    top = Counter(w for w in words if w not in stop).most_common(1)
    if not top:
        return 0.0
    return round(top[0][1] / n_chars * 1000, 2)


LIST_MARK = re.compile(r'(一是|二是|三是|四是|首先|其次|再次|最后|第一[，、]|第二[，、]|第三[，、])')


def m_struct(text: str) -> dict:
    """结构规整度：段落字数CV + 并列骨架标记数。"""
    paras = [p.strip() for p in text.split('\n') if p.strip() and len(p.strip()) > 1]
    if len(paras) >= 3:
        lens = [len(p) for p in paras]
        mean = sum(lens) / len(lens)
        var = sum((x - mean) ** 2 for x in lens) / len(lens)
        cv = round(math.sqrt(var) / mean, 3) if mean else 0.0
    else:
        cv = None  # 段落太少，无结构信号
    markers = len(LIST_MARK.findall(text))
    return {"para_cv": cv, "list_markers": markers}


def sample_sufficiency(text: str) -> dict:
    """样本量提示（片段模式）：依赖样本量的指标在短文本上自动标注"不计分依据"，
    防止静默给 0 分被误读为达标。2026-10-28 v0.4.2：输入含任意文体/片段后新增。"""
    n_sents = len(split_sentences(text))
    n_paras = len([p for p in text.split("\n") if p.strip()])
    flags = {}
    if n_sents < 4:
        flags["pattern_entropy"] = f"句数{n_sents}<4，熵不计分"
    if n_paras < 3:
        flags["struct"] = f"段落数{n_paras}<3，para_cv不计分"
    if n_paras < 2:
        flags["para_breath"] = f"段落数{n_paras}<2，不计分"
    if len(text) < 300:
        flags["_mode"] = "片段模式：<300字，S4 只动词层/句层卡(01-24)，篇层/结构卡停用"
    return flags


def run(text: str, register: str = "colloquial_media") -> dict:
    cliche_words = load_words("cliche_common.txt") + load_words(f"cliche_{register}.txt")
    result = {
        "register": register,
        "chars": len(text),
        "metrics": {
            "rhythm_cv": round(m_rhythm_cv(text), 3),
            "short_burst_ratio": round(m_short_burst(text), 3),
            "cliche_density": round(m_cliche(text, cliche_words), 2),
            "modal_temp": round(m_modal(text), 2),
            "hedge_density": round(m_hedge(text), 2),
            "para_breath": m_para_breath(text),
        },
        "extra_metrics": {
            "pattern_entropy": m_pattern_entropy(text),
            "lex_rotation_top": m_lex_rotation(text),
            "struct": m_struct(text),
            "cliche_detail": sorted(
                ({"word": w, "n": n} for w, n in cliche_hits(text, cliche_words).items()),
                key=lambda x: -x["n"]),
            "sample_sufficiency": sample_sufficiency(text),
        },
        "version": "0.2.2",
    }
    return result


SELF_TEST_SAMPLES = [
    # (文本, 语体, 断言函数名, 说明) —— 回归基线：改词表/改算法后必跑
    ("在当今数字化时代，我们要赋能传统产业，打造全新生态。值得注意的是，综上所述，"
     "需要系统性地加以推进，构建闭环，实现降本增效，助力高质量发展。", "colloquial_media",
     "ai_cliche", "AI腔：套话密度应远超红线"),
    ("这事我一开始也没当回事。朋友说试试呗，我就试了。结果用了一礼拜，发现还真省事——"
     "以前每天晚上对账要对半个多小时，现在几分钟搞定。当然毛病也有，识别偶尔抽风，"
     "数字一多就乱。不过总体来说挺值，一个月十几块钱，少熬的夜可不止这个数。", "colloquial_media",
     "human_clean", "人写：套话应为0、语气留白应为正"),
    ("他说要警惕\u201c赋能\u201d这类说法，也别迷信\u201c闭环\u201d。", "colloquial_media",
     "quote_only_zero", "引用语境豁免：引号内套话不计数（2026-10-28 自检假阳性教训）"),
    ("他说要警惕\u201c赋能\u201d这类说法。但全文通篇都在赋能。", "colloquial_media",
     "unquoted_counted", "引号外套话照抓：豁免只豁引用，不豁使用"),
    ("他说要警惕\u0022赋能\u0022这种说法，也别迷信\u0022闭环\u0022。", "colloquial_media",
     "ascii_quote_zero", "ASCII直引号同样豁免（语料实测主形态）"),
    ("赋能闭环抓手。", "colloquial_media",
     "fragment_flags", "片段模式：样本不足的指标必须标注，不许静默给0"),

]


def self_test() -> bool:
    """词表/算法回归：AI腔必须抓到，人写必须不误伤。一条命令跑完。"""
    ok = True
    for text, reg, case, desc in SELF_TEST_SAMPLES:
        m = run(text, reg)["metrics"]
        if case == "ai_cliche":
            passed = m["cliche_density"] > 20 and m["modal_temp"] == 0
        elif case == "fragment_flags":
            passed = "pattern_entropy" in run(text, reg)["extra_metrics"]["sample_sufficiency"]
        elif case in ("quote_only_zero", "ascii_quote_zero"):
            passed = m["cliche_density"] == 0
        elif case == "unquoted_counted":
            passed = m["cliche_density"] > 0
        else:  # human_clean
            passed = (m["cliche_density"] == 0
                      and m["modal_temp"] > 0 and m["hedge_density"] > 0)
        print(f"  [{'PASS' if passed else 'FAIL'}] {case}: {desc} "
              f"(套话={m['cliche_density']} 语气={m['modal_temp']} 留白={m['hedge_density']})")
        ok = ok and passed
    # 词表文件完整性：通用词表非空
    for f in ["cliche_common.txt", "modal_common.txt", "hedge_common.txt"]:
        n = len(load_words(f))
        passed = n > 0
        print(f"  [{'PASS' if passed else 'FAIL'}] 词表 {f}: {n} 词")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args:
        args.remove("--self-test")
        print("check_metrics 自检（AI腔必抓 / 人写必放 / 词表非空）:")
        sys.exit(0 if self_test() else 1)
    reg = "colloquial_media"
    if "--register" in args:
        i = args.index("--register")
        reg = args[i + 1]
        args = args[:i] + args[i + 2:]
    if not args:
        print("usage: check_metrics.py <file> [--register name] [--self-test]")
        sys.exit(1)
    text = Path(args[0]).read_text(encoding="utf-8")
    print(json.dumps(run(text, reg), ensure_ascii=False, indent=2))
