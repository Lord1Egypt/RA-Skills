#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧招采专家 · 评标办法价格分规则半自动抽取（深度节点 C 的上游工具）
================================================================

从《评标办法》中抽取「价格分计算规则」参数，产出 `price_score.py` 可直接读取的
`price_config.json` 草稿，并附一份带置信度与「需人工确认项」的审阅报告
`price_config.review.md`。

设计原则（与价格分引擎一致，半自动）：
  - 只「读」规则、不「定」报价：抽取的是评标办法里的算法与参数，不是投标报价；
  - 每个参数给出命中片段与置信度；对低置信或歧义项标 `needs_review`；
  - 绝不臆造评标基准价、绝不替用户决定报价策略；
  - `quotes`（各投标人报价）是投标时才有的数据，抽取稿留空，运行算分前由用户填入。

输入：
  - 评标办法 PDF（需 pypdf：`pip install pypdf`）—— 自动抽取文本；
  - 或粘贴的章节文本 .txt / .md（零依赖）—— 推荐用于快速校验与回归。
  脚本会自动定位「价格分 / 投标报价 / 报价得分」所在章节作为抽取上下文。

输出：
  - <out>/price_config.json       抽取草稿（仅规则参数，quotes=[] 待填）
  - <out>/price_config.review.md  审阅报告（命中片段 / 置信度 / 需人工确认项）

用法：
  python extract_price_rules.py 评标办法.pdf --out ./out
  python extract_price_rules.py 评标办法.pdf --method-hint benchmark
  python extract_price_rules.py 评标办法_价格分章节.txt --out ./out

依赖：pypdf（仅 PDF 输入需要）；纯文本输入无需任何第三方库。
"""

import argparse
import json
import os
import re
import sys

CONF_HIGH = 0.85
CONF_MID = 0.6
CONF_LOW = 0.4


# ============================================================
# 文本读取
# ============================================================
def read_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        try:
            import pypdf  # type: ignore
        except ImportError:
            sys.exit("[错误] 读取 PDF 需要 pypdf，请先 `pip install pypdf`；"
                     "或把价格分章节另存为 .txt 直接传入。")
        reader = pypdf.PdfReader(path)
        parts = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        return "\n".join(parts)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def locate_price_section(text: str) -> str:
    """定位价格分章节，返回该章节上下文（整段文本中相关窗口）。"""
    anchors = ["价格分", "投标报价", "报价得分", "价格评分", "报价评分办法"]
    idxs = []
    for a in anchors:
        i = text.find(a)
        if i >= 0:
            idxs.append(i)
    if not idxs:
        return text  # 找不到锚点就用全文
    start = max(0, min(idxs) - 200)
    end = min(len(text), max(idxs) + 1800)
    return text[start:end]


def snippet(text: str, pattern: str, width: int = 36) -> str:
    m = re.search(pattern, text)
    if not m:
        return ""
    s = max(0, m.start() - width)
    e = min(len(text), m.end() + width)
    return text[s:e].replace("\n", " ").strip()


def to_float(s):
    if s is None:
        return None
    try:
        return float(str(s).replace(",", "").replace("，", ""))
    except ValueError:
        return None


# ============================================================
# 抽取各参数
# ============================================================
def extract_full_score(text):
    # 优先「价格分 XX 分」等明确分值表述
    best = None
    for pat in [
        r'价格分[是为：:是\s]*?(\d+(?:\.\d+)?)\s*分',
        r'报价得分[^\n]{0,18}?(\d+(?:\.\d+)?)\s*分',
        r'投标报价[^\n]{0,18}?(\d+(?:\.\d+)?)\s*分',
        r'价格部分[^\n]{0,18}?(\d+(?:\.\d+)?)\s*分',
    ]:
        m = re.search(pat, text)
        if m:
            best = (to_float(m.group(1)), CONF_HIGH, snippet(text, pat))
            break
    if best:
        return best
    # 退而求其次：价格权重百分比（需人工换算为分值）
    mw = re.search(r'价格.*?权重[为是：:]?\s*(\d+(?:\.\d+)?)\s*%', text)
    if mw:
        v = to_float(mw.group(1))
        return (v, CONF_LOW,
                f"{snippet(text, r'价格.*?权重[为是：:]?\\s*\\d+(?:\\.\\d+)?\\s*%')}"
                f" —— 仅检出权重百分比，请确认满分总分制（如百分制即 {v} 分）")
    return (None, 0.0, "")


def extract_method(text, hint=None):
    sigs = {}

    # 基准价法：出现「评标基准价」且伴随偏差/扣分描述
    if re.search(r'评标基准价', text):
        c = CONF_MID
        if re.search(r'每高.{0,8}?评标基准价|每低.{0,8}?评标基准价|高于评标基准价|低于评标基准价|偏差', text):
            c = CONF_HIGH
        sigs["benchmark"] = c

    # 低价优先法
    if re.search(r'低价优先', text) or re.search(r'最低报价为评标基准价', text) \
            or re.search(r'满足招标文件要求.{0,12}?最低报价', text):
        sigs["low_price_first"] = CONF_HIGH

    # 区间法 / 限值法
    if re.search(r'区间', text) or re.search(r'限值', text) \
            or re.search(r'在.{0,30}?之间.{0,12}?得满分', text):
        sigs["interval"] = CONF_MID

    if not sigs:
        return (None, 0.0, "未在文本中识别到明确的算法关键词")

    if hint and hint in sigs:
        sigs[hint] = max(sigs[hint], 0.95)

    method = max(sigs, key=sigs.get)
    conf = sigs[method]
    others = [k for k in sigs if k != method]
    ev = f"识别到算法信号：{ '、'.join(f'{k}={sigs[k]:.2f}' for k, v in sigs.items()) }"
    if others:
        ev += f"；备选：{ '、'.join(others) }（请确认主算法是否确为 {method}）"
    return (method, conf, ev)


def extract_base_mode(text):
    """仅 benchmark 需要。返回 (mode, conf, extra_dict, evidence)。"""
    # fixed：以控制价/标底/最高限价作为基准价
    if re.search(r'(?:招标控制价|标底|最高投标限价)[^\n]{0,24}?评标基准价', text) \
            or re.search(r'评标基准价[^\n]{0,24}?(?:招标控制价|标底|最高投标限价)', text):
        mv = re.search(r'(?:招标控制价|标底|最高投标限价)[^\n]{0,18}?(\d[\d,]*(?:\.\d+)?)\s*(万元|元)?', text)
        extra = {}
        if mv:
            extra["value"] = to_float(mv.group(1))
            if mv.group(2):
                extra["unit"] = mv.group(2)
        return ("fixed", CONF_MID, extra,
                snippet(text, r'(?:招标控制价|标底|最高投标限价)[^\n]{0,24}?评标基准价'))

    # lowest_n_avg：最低 N 家平均 / 去掉最高最低平均
    mn = re.search(r'最低\s*(\d+)\s*家[^\n]{0,24}?平均', text)
    if mn:
        return ("lowest_n_avg", CONF_MID, {"lowest_n": int(mn.group(1))},
                snippet(text, r'最低\s*\d+\s*家[^\n]{0,24}?平均'))
    if re.search(r'去掉最高[^\n]{0,30}?最低[^\n]{0,12}?平均', text):
        return ("lowest_n_avg", CONF_LOW, {"lowest_n": 3},
                snippet(text, r'去掉最高[^\n]{0,30}?最低[^\n]{0,12}?平均'))

    # average_k：平均值下浮 K% / ×(1−K)
    if re.search(r'平均[^\n]{0,12}?下浮\s*\d+(?:\.\d+)?\s*%', text) \
            or re.search(r'×\s*\(?\s*1\s*[-−]\s*K', text) or re.search(r'下浮\s*K', text):
        kk = re.search(r'(?:下浮|降幅)\s*(\d+(?:\.\d+)?)\s*%', text)
        kk2 = re.search(r'[Kk]\s*[=＝]\s*(\d+(?:\.\d+)?)\s*%?', text)
        k = None
        if kk:
            k = 1 - float(kk.group(1)) / 100.0
        elif kk2:
            raw = to_float(kk2.group(1))
            k = raw / 100.0 if raw and raw > 1 else raw
        extra = {"k": round(k, 4)} if k is not None else {}
        return ("average_k", CONF_MID, extra,
                snippet(text, r'平均[^\n]{0,12}?下浮\s*\d+(?:\.\d+)?\s*%'))

    # median：中位数
    if re.search(r'中位', text):
        return ("median", CONF_LOW, {}, snippet(text, r'中位'))

    # weighted：加权
    if re.search(r'加权', text):
        return ("weighted", CONF_LOW, {"w": 0.6},
                snippet(text, r'加权'))

    # average：默认算术平均（兜底）
    if re.search(r'平均', text):
        return ("average", CONF_LOW, {}, snippet(text, r'平均'))

    return (None, 0.0, {}, "未识别到评标基准价计算方式")


def extract_deduction(text):
    above = below = None
    ev_above = ev_below = ""
    ma = re.search(r'每高[于]?\s*评标基准价\s*1%\s*[，,]?\s*扣\s*(\d+(?:\.\d+)?)\s*分', text)
    if ma:
        above = to_float(ma.group(1)); ev_above = snippet(text, r'每高[于]?\s*评标基准价\s*1%\s*[，,]?\s*扣\s*\d+(?:\.\d+)?\s*分')
    else:
        ma2 = re.search(r'高于评标基准价[^\n]{0,18}?(\d+(?:\.\d+)?)\s*分', text)
        if ma2:
            above = to_float(ma2.group(1)); ev_above = snippet(text, r'高于评标基准价[^\n]{0,18}?\d+(?:\.\d+)?\s*分')
    mb = re.search(r'每低[于]?\s*评标基准价\s*1%\s*[，,]?\s*扣\s*(\d+(?:\.\d+)?)\s*分', text)
    if mb:
        below = to_float(mb.group(1)); ev_below = snippet(text, r'每低[于]?\s*评标基准价\s*1%\s*[，,]?\s*扣\s*\d+(?:\.\d+)?\s*分')
    else:
        mb2 = re.search(r'低于评标基准价[^\n]{0,18}?(\d+(?:\.\d+)?)\s*分', text)
        if mb2:
            below = to_float(mb2.group(1)); ev_below = snippet(text, r'低于评标基准价[^\n]{0,18}?\d+(?:\.\d+)?\s*分')
    conf = CONF_HIGH if (above is not None and below is not None) else (CONF_MID if (above or below) else 0.0)
    return (above, below, conf, ev_above, ev_below)


def extract_interval(text):
    mi = re.search(
        r'(?:投标报价|报价)\s*(?:在|位于|为)?\s*'
        r'(\d[\d,]*(?:\.\d+)?)\s*(万元|元)?\s*'
        r'[-~～至到]\s*'
        r'(\d[\d,]*(?:\.\d+)?)\s*(万元|元)?',
        text)
    if not mi:
        return (None, None, None, 0.0, "")
    low = to_float(mi.group(1))
    high = to_float(mi.group(3))
    unit = mi.group(2) or mi.group(4)
    conf = CONF_MID if (low and high and low < high) else CONF_LOW
    return (low, high, unit, conf, snippet(text,
            r'(?:投标报价|报价)\s*(?:在|位于|为)?\s*\d[\d,]*(?:\.\d+)?\s*(?:万元|元)?\s*[-~～至到]\s*\d[\d,]*(?:\.\d+)?'))


# ============================================================
# 组装
# ============================================================
def build_config(sec, method_hint):
    full_score, fs_conf, fs_ev = extract_full_score(sec)
    method, m_conf, m_ev = extract_method(sec, hint=method_hint)

    config = {}
    review = {"fields": [], "needs_review": []}

    def add(field, value, conf, evidence, note=""):
        review["fields"].append({
            "field": field, "value": value, "confidence": round(conf, 2),
            "evidence": evidence, "note": note,
        })
        if conf < CONF_MID or value is None:
            review["needs_review"].append(f"{field}：置信度 {conf:.2f}，需人工确认（{evidence or note or '无命中'}）")

    config["method"] = method
    add("method", method, m_conf, m_ev, "主算法；如与招标文件不符请手改")
    config["full_score"] = full_score
    add("full_score", full_score, fs_conf, fs_ev,
        "满分分值；若原文为权重百分比需换算")

    if method == "benchmark":
        mode, b_conf, b_extra, b_ev = extract_base_mode(sec)
        config["base"] = {"mode": mode}
        if "k" in b_extra:
            config["base"]["k"] = b_extra["k"]
        if "lowest_n" in b_extra:
            config["base"]["lowest_n"] = b_extra["lowest_n"]
        if "value" in b_extra:
            config["base"]["value"] = b_extra["value"]
        add("base.mode", mode, b_conf, b_ev, "评标基准价计算方式")
        above, below, d_conf, ev_a, ev_b = extract_deduction(sec)
        config["deduction"] = {"above": above, "below": below}
        add("deduction.above", above, d_conf, ev_a, "高于基准价每1%扣分")
        add("deduction.below", below, d_conf, ev_b, "低于基准价每1%扣分")

    elif method == "interval":
        low, high, unit, i_conf, i_ev = extract_interval(sec)
        config["interval"] = {"low": low, "high": high, "deduction_per_pct": 1.0}
        if unit:
            config["interval"]["unit_note"] = unit
        add("interval.low", low, i_conf, i_ev, f"区间下限（单位：{unit or '需确认'}）")
        add("interval.high", high, i_conf, i_ev, f"区间上限（单位：{unit or '需确认'}）")
        add("interval.deduction_per_pct", 1.0, 0.3, "默认 1.0 分/%，请按原文修正")

    elif method == "low_price_first":
        pass  # 仅需 full_score

    elif method is None:
        review["needs_review"].append(
            "method 未识别：请手填 method（low_price_first / benchmark / interval）"
            " 及相应 base / deduction / interval 字段")

    config["quotes"] = []  # 投标人报价投标时才有，留空待填
    review["fields"].append({
        "field": "quotes", "value": "[]", "confidence": 1.0,
        "evidence": "抽取工具不负责任意报价；运行 price_score.py 前由用户填入各投标人报价",
        "note": "必填（运行算分前）",
    })
    review["needs_review"].append("quotes：运行 price_score.py 前必须填入各投标人报价（单位须与 interval 区间单位一致）")

    return config, review


def render_review(review: dict, src: str) -> str:
    lines = []
    lines.append("# 价格分规则抽取审阅报告")
    lines.append("")
    lines.append(f"- 来源文件：`{src}`")
    lines.append("- 工具：智能招采专家 · extract_price_rules.py（半自动）")
    lines.append("- 原则：本表为**抽取草稿**，运行算分前须人工复核以下各项。")
    lines.append("")
    lines.append("## 一、参数抽取结果")
    lines.append("")
    lines.append("| 字段 | 抽取值 | 置信度 | 命中片段 / 说明 |")
    lines.append("|---|---|---|---|")
    for f in review["fields"]:
        val = f["value"]
        if val is None:
            val = "（未识别）"
        lines.append(f"| {f['field']} | {val} | {f['confidence']:.2f} | {f['evidence'] or f['note'] or ''} |")
    lines.append("")
    lines.append("## 二、⚠️ 需人工确认项")
    lines.append("")
    if review["needs_review"]:
        for item in review["needs_review"]:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- 无（各项置信度均较高，仍建议通读原文复核）")
    lines.append("")
    lines.append("## 三、下一步")
    lines.append("")
    lines.append("1. 逐项核对上方「需人工确认项」，修正 `price_config.json`；")
    lines.append("2. 在 `price_config.json` 的 `quotes` 中填入各投标人报价（单位与区间一致）；")
    lines.append("3. 运行 `python scripts/price_score.py --config price_config.json` 算分；")
    lines.append("4. 算分结果同样标注「⚠️ 需人工复核」，不得直接作为定标依据。")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="智慧招采专家 · 评标办法价格分规则半自动抽取")
    ap.add_argument("source", help="评标办法 PDF / 价格分章节 .txt / .md")
    ap.add_argument("--out", default=".", help="输出目录（默认当前目录）")
    ap.add_argument("--method-hint", choices=["low_price_first", "benchmark", "interval"],
                    help="已知算法时给提示，提升该算法置信度")
    args = ap.parse_args()

    try:
        text = read_text(args.source)
    except Exception as e:
        sys.exit(f"[错误] 读取文件失败：{e}")

    if not text.strip():
        sys.exit("[错误] 未从源文件读取到任何文本。")

    section = locate_price_section(text)
    config, review = build_config(section, args.method_hint)

    os.makedirs(args.out, exist_ok=True)
    cfg_path = os.path.join(args.out, "price_config.json")
    rev_path = os.path.join(args.out, "price_config.review.md")

    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    with open(rev_path, "w", encoding="utf-8") as f:
        f.write(render_review(review, args.source))

    print(f"[OK] 抽取草稿 → {cfg_path}")
    print(f"[OK] 审阅报告 → {rev_path}")
    print(f"[摘要] method={config.get('method')}  full_score={config.get('full_score')}"
          f"  待确认项={len(review['needs_review'])}")
    if review["needs_review"]:
        print("[提示] 请先阅读 price_config.review.md 完成人工复核再运行 price_score.py")


if __name__ == "__main__":
    main()
