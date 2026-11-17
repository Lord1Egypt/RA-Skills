#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_humanize.py — YottaMeta 元真（yotta-humanize）：去 AI 味中文写作编辑引擎。

检测器引擎（24 类规则 + 词表 + 统计突发性）识别 AI 腔文本，并给出确定性改写。
纯 Python 3.8+ 标准库，零外部依赖，Windows + Linux + macOS 通用，跨智能体可用。

子命令：
  score     输出 AI 腔评分（0-100，越高越像 AI 写的）
  analyze   详细检测报告（文本）
  report    Markdown 检测报告
  suggest   按优先级分组的改写建议
  rewrite   确定性改写文本 + 修复清单
  version   打印版本

退出码（与元安 / 元审 / 元盾家族一致）：
  0 = 成功（评分低于阈值，或未启用 --gate）
  1 = score --gate 且评分 >= 阈值（检测到明显 AI 腔）
  4 = 用法错误 / 致命异常

用法示例：
  python3 yotta_humanize.py score -f article.md
  python3 yotta_humanize.py analyze -f article.md
  python3 yotta_humanize.py report -f article.md > report.md
  python3 yotta_humanize.py suggest -f article.md
  python3 yotta_humanize.py rewrite -f article.md
  echo "..." | python3 yotta_humanize.py score --stdin
"""
import argparse
import json
import locale
import math
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import humanize_rules as HR  # noqa: E402

VERSION = "0.2.5"
TOOL_NAME = "yotta-humanize"
TOOL_CN = "元真"
DEFAULT_THRESHOLD = 45

# ── 中文文本统计 ────────────────────────────────────────────────────────────

_CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")
_ALNUM = re.compile(r"[0-9a-zA-Z]")
_SENT_SPLIT = re.compile(r"[。！？；!?;\n]+")
_INTENSIFIERS = re.compile(r"非常|十分|极其|特别|相当|无比|异常|格外")


def cjk_len(s):
    """CJK 字数 + 数字/英文单词数（标点与空格不计）。"""
    n = len(_CJK.findall(s))
    n += len(re.findall(r"[0-9a-zA-Z]+", s))
    return n


def split_sentences(text):
    """按中文句末标点切句，返回（句子列表，分隔符列表）。"""
    parts = _SENT_SPLIT.split(text)
    seps = _SENT_SPLIT.findall(text)
    sentences = []
    for p in parts:
        p = p.strip()
        if p:
            sentences.append(p)
    return sentences, seps


def bigrams(text):
    """把连续 CJK 字符切成双字单元，作为词汇多样性统计的伪词。"""
    runs = re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]+", text)
    out = []
    for run in runs:
        for i in range(len(run) - 1):
            out.append(run[i:i + 2])
    return out


def compute_stats(text):
    """计算中文风格统计量（突发性 / 句长均匀度 / 词汇多样性）。"""
    sentences, _ = split_sentences(text)
    lengths = [cjk_len(s) for s in sentences if cjk_len(s) > 0]
    n_sent = len(lengths)
    chars = cjk_len(text)
    toks = bigrams(text)
    n_tok = len(toks)
    uniq = len(set(toks))
    ttr = (uniq / n_tok) if n_tok else 0.0

    mean = 0.0
    std = 0.0
    cv = 0.0
    burst = 0.0
    if n_sent > 1:
        mean = sum(lengths) / n_sent
        var = sum((x - mean) ** 2 for x in lengths) / n_sent
        std = math.sqrt(var)
        cv = std / mean if mean else 0.0
        diffs = [abs(lengths[i] - lengths[i - 1]) for i in range(1, n_sent)]
        burst = (sum(diffs) / len(diffs)) / mean if mean else 0.0

    # 逗号密度（每 100 字的逗号数，过高说明一逗到底）
    comma_density = (text.count("，") + text.count(",")) / chars * 100 if chars else 0.0
    # 连接词密度（每 100 字）
    conj = sum(len(re.findall(w, text)) for w in
               ("然而", "但是", "同时", "此外", "另外", "更重要的是"))
    conj_density = conj / chars * 100 if chars else 0.0

    return {
        "char_count": chars,
        "sentence_count": n_sent,
        "avg_sentence_len": round(mean, 2),
        "sentence_std": round(std, 2),
        "cv": round(cv, 4),
        "burstiness": round(burst, 4),
        "type_token_ratio": round(ttr, 4),
        "comma_density": round(comma_density, 2),
        "conjunction_density": round(conj_density, 2),
    }


def _clamp01(x):
    return max(0.0, min(1.0, x))


def stats_score(stats):
    """统计量 → 0-100 的 AI 腔分数（句长越均匀 / 突发性越低 / 词汇越贫乏越像 AI）。"""
    if stats["char_count"] < 40 or stats["sentence_count"] < 3:
        return 0
    cv = stats["cv"]
    burst = stats["burstiness"]
    ttr = stats["type_token_ratio"]
    u = _clamp01((0.5 - cv) / 0.35)     # cv 高 = 句长变化大 = 人味 → 分低
    b = _clamp01((0.6 - burst) / 0.5)   # 突发性低 = 均匀 → 分高
    t = _clamp01((0.6 - ttr) / 0.35)    # 词汇多样性低 → 分高
    return round(100 * (0.4 * u + 0.35 * b + 0.25 * t))


# ── 规则检测 ────────────────────────────────────────────────────────────────

def find_all(text, pattern):
    """返回 pattern 在 text 中所有命中（match, start, end）。"""
    out = []
    for m in pattern.finditer(text):
        out.append((m.group(0), m.start(), m.end()))
    return out


def detect(text, only_ids=None, config=None):
    """运行全部（或指定）规则，返回 findings 列表。"""
    comp = HR.compiled()
    findings = []
    for rule in HR.RULES:
        rid = rule["id"]
        if only_ids is not None and rid not in only_ids:
            continue
        pats = comp[rid]
        seen = set()
        hits = []
        for p in pats:
            for match, start, end in find_all(text, p):
                key = (match, start)
                if key in seen:
                    continue
                seen.add(key)
                hits.append({"match": match, "start": start, "end": end})
        if not hits:
            continue
        findings.append({
            "rule_id": rid,
            "name": rule["name"],
            "group": rule["group"],
            "weight": rule["weight"],
            "matches": hits,
            "suggestion": rule["suggestion"],
        })
    return findings


def pattern_score(findings, char_count):
    """规则命中 → 0-100（密度 + 种类广度 + 分组多样性）。"""
    if not findings or char_count == 0:
        return 0
    weighted = sum(f["weight"] * len(f["matches"]) for f in findings)
    density = weighted / char_count * 100
    density_score = min(math.log2(density + 1) * 14, 60)
    breadth = min(len(findings) * 2, 20)
    groups = len(set(f["group"] for f in findings))
    cat = min(groups * 4, 16)
    return min(round(density_score + breadth + cat), 100)


def analyze(text, opts=None):
    """完整分析：{score, pattern_score, stats_score, total_matches, ...}。"""
    opts = opts or {}
    only_ids = opts.get("patterns")
    stats = compute_stats(text)
    findings = detect(text, only_ids=only_ids)
    total_matches = sum(len(f["matches"]) for f in findings)
    pscore = pattern_score(findings, stats["char_count"])
    sscore = stats_score(stats)
    if pscore == 0 and sscore == 0:
        score = 0
    elif not findings:
        score = min(round(sscore * 0.12), 12)
    else:
        score = min(round(pscore * 0.7 + sscore * 0.3), 100)

    categories = {}
    for g in HR.GROUPS:
        fs = [f for f in findings if f["group"] == g]
        categories[g] = {
            "label": HR.GROUP_LABELS[g],
            "matches": sum(len(f["matches"]) for f in fs),
            "rules": [f["name"] for f in fs],
        }
    return {
        "score": score,
        "pattern_score": pscore,
        "stats_score": sscore,
        "total_matches": total_matches,
        "rule_types": len(findings),
        "stats": stats,
        "categories": categories,
        "findings": findings,
        "summary": build_summary(score, total_matches, findings, stats),
    }


def build_summary(score, total_matches, findings, stats):
    level = "明显 AI 腔" if score >= 70 else (
        "中度 AI 腔" if score >= 45 else (
            "轻度 AI 痕迹" if score >= 20 else "基本像人写的"))
    top = sorted(findings, key=lambda f: f["weight"] * len(f["matches"]),
                 reverse=True)[:3]
    top_names = "、".join(f["name"] for f in top)
    msg = "评分 %d/100（%s）：命中 %d 处、%d 类规则。" % (
        score, level, total_matches, len(findings))
    if top_names:
        msg += " 主要问题：" + top_names + "。"
    if stats["sentence_count"] > 3 and stats["cv"] < 0.25:
        msg += " 句长过于均匀，节奏像机器。"
    if stats["char_count"] > 100 and stats["type_token_ratio"] < 0.4:
        msg += " 用词重复度偏高。"
    return msg


# ── 确定性改写 ─────────────────────────────────────────────────────────────

def _apply_fix(text, spec):
    """spec 形如 'pattern|replacement'（pattern 视为正则）。返回 (new_text, count)。"""
    if "|" not in spec:
        return text, 0
    pat, rep = spec.split("|", 1)
    if not pat:
        return text, 0
    new, n = re.subn(pat, rep, text)
    return new, n


def rewrite(text):
    """按规则 fix 映射做确定性机械改写，返回 {text, fixes, before, after}。"""
    out = text
    fixes = []
    before = analyze(text)
    for rule in HR.RULES:
        for spec in rule.get("fix", []):
            new, n = _apply_fix(out, spec)
            if n > 0:
                fixes.append({
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "count": n,
                    "detail": spec.split("|")[0],
                })
                out = new

    # 结构类修复（依赖计数，需单独处理）
    out, n1 = _limit_dash(out)
    if n1:
        fixes.append({"rule_id": "HZ-16", "name": "破折号滥用",
                      "count": n1, "detail": "多余破折号→逗号"})
    out, n2 = _limit_bang(out)
    if n2:
        fixes.append({"rule_id": "HZ-18", "name": "感叹号滥用",
                      "count": n2, "detail": "多余感叹号→句号"})
    out, n3 = _trim_blank(out)
    if n3:
        fixes.append({"rule_id": "HZ-22", "name": "废话填充",
                      "count": n3, "detail": "清理空壳标点"})
    after = analyze(out)
    return {
        "text": out,
        "fixes": fixes,
        "before": before["score"],
        "after": after["score"],
    }


def _limit_dash(text):
    """破折号超过 2 处时，把第 3 处起换成逗号。"""
    count = text.count("——")
    if count <= 2:
        return text, 0
    if count <= 2:
        return text, 0
    out = []
    seen = 0
    i = 0
    n = 0
    while i < len(text):
        if text.startswith("——", i):
            if seen >= 2:
                out.append("，")
                n += 1
            else:
                out.append("——")
            seen += 1
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out), n


def _limit_bang(text):
    """感叹号超过 2 个时，第 3 个起换成句号。"""
    if text.count("！") <= 2:
        return text, 0
    out = []
    seen = 0
    n = 0
    for ch in text:
        if ch == "！":
            if seen >= 2:
                out.append("。")
                n += 1
            else:
                out.append(ch)
            seen += 1
        else:
            out.append(ch)
    return "".join(out), n


def _trim_blank(text):
    """清理改写后产生的空壳标点（如“，，”“。。”“，。”）。"""
    before = text
    text = re.sub(r"[，,]{2,}", "，", text)
    text = re.sub(r"[。]{2,}", "。", text)
    text = re.sub(r"[，,][。]", "。", text)
    text = re.sub(r"^[，,。；;\s]+", "", text)
    return text, (0 if before == text else 1)


# ── 报告格式化 ─────────────────────────────────────────────────────────────

def _snippet(text, start, end, radius=14):
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    return text[lo:hi].replace("\n", " ")


def score_label(s):
    if s >= 70:
        return "明显 AI 腔"
    if s >= 45:
        return "中度 AI 腔"
    if s >= 20:
        return "轻度 AI 痕迹"
    return "基本像人写的"


def format_analyze(text, result):
    lines = []
    s = result
    lines.append("")
    lines.append("=" * 46)
    lines.append("  元真（yotta-humanize）AI 腔检测报告")
    lines.append("=" * 46)
    bar = "█" * round(s["score"] / 5) + "░" * (20 - round(s["score"] / 5))
    lines.append("  评分：%d/100 [%s]（%s）" % (s["score"], bar, score_label(s["score"])))
    lines.append("  字数 %d ｜ 句子 %d ｜ 命中 %d 处 / %d 类规则"
                 % (s["stats"]["char_count"], s["stats"]["sentence_count"],
                    s["total_matches"], s["rule_types"]))
    lines.append("  规则分 %d ｜ 统计分 %d" % (s["pattern_score"], s["stats_score"]))
    lines.append("  %s" % s["summary"])
    lines.append("")
    st = s["stats"]
    lines.append("── 文本统计 ───────────────────────────────────────")
    lines.append("  平均句长 %s 字 ｜ 句长波动 σ=%s（CV %s）"
                 % (st["avg_sentence_len"], st["sentence_std"], st["cv"]))
    lines.append("  突发性 %s ｜ 词汇多样性 %s ｜ 逗号密度 %s/百字"
                 % (st["burstiness"], st["type_token_ratio"], st["comma_density"]))
    lines.append("")
    if s["findings"]:
        lines.append("── 命中规则 ──────────────────────────────────────")
        for f in s["findings"]:
            lines.append("")
            lines.append("  [%s] %s（×%d，权重 %d）"
                         % (f["rule_id"], f["name"], len(f["matches"]), f["weight"]))
            for m in f["matches"][:5]:
                lines.append("    · %s" % _snippet(text, m["start"], m["end"]))
            if len(f["matches"]) > 5:
                lines.append("    … 还有 %d 处" % (len(f["matches"]) - 5))
            lines.append("    建议：%s" % f["suggestion"])
    lines.append("")
    lines.append("=" * 46)
    return "\n".join(lines)


def format_report(result):
    lines = []
    s = result
    lines.append("# AI 腔检测报告")
    lines.append("")
    lines.append("**评分：%d/100**（%s）" % (s["score"], score_label(s["score"])))
    lines.append("")
    lines.append("字数 %d ｜ 句子 %d ｜ 命中 %d 处 / %d 类规则 ｜ 规则分 %d ｜ 统计分 %d"
                 % (s["stats"]["char_count"], s["stats"]["sentence_count"],
                    s["total_matches"], s["rule_types"],
                    s["pattern_score"], s["stats_score"]))
    lines.append("")
    lines.append(s["summary"])
    lines.append("")
    st = s["stats"]
    lines.append("## 文本统计")
    lines.append("")
    lines.append("| 指标 | 数值 | 说明 |")
    lines.append("|---|---|---|")
    lines.append("| 平均句长 | %s 字 | %s |" % (
        st["avg_sentence_len"],
        "偏长" if st["avg_sentence_len"] > 30 else (
            "偏短" if st["avg_sentence_len"] < 10 else "适中")))
    lines.append("| 句长波动 CV | %s | %s |" % (
        st["cv"], "均匀（AI 味）" if st["cv"] < 0.25 else (
            "有起伏（人味）" if st["cv"] >= 0.45 else "中等")))
    lines.append("| 突发性 | %s | %s |" % (
        st["burstiness"],
        "低（节奏单调）" if st["burstiness"] < 0.3 else (
            "高（有起伏）" if st["burstiness"] >= 0.6 else "中等")))
    lines.append("| 词汇多样性 | %s | %s |" % (
        st["type_token_ratio"],
        "低（用词重复）" if st["type_token_ratio"] < 0.4 else (
            "高" if st["type_token_ratio"] >= 0.6 else "中等")))
    lines.append("| 逗号密度 | %s/百字 | %s |" % (
        st["comma_density"],
        "一逗到底" if st["comma_density"] > 12 else "正常"))
    lines.append("")
    if s["findings"]:
        lines.append("## 命中规则")
        lines.append("")
        for f in s["findings"]:
            lines.append("### %s. %s（×%d）" % (f["rule_id"], f["name"], len(f["matches"])))
            lines.append("")
            lines.append(f["suggestion"])
            lines.append("")
    return "\n".join(lines)


def format_suggest(text, result):
    levels = [
        (5, "高优先级（一眼 AI，必须改）"),
        (4, "中高优先级（明显 AI 腔）"),
        (3, "中优先级（有 AI 痕迹）"),
        (2, "低优先级（轻微）"),
    ]
    lines = []
    lines.append("按优先级分组的改写建议：")
    for w, label in levels:
        fs = [f for f in result["findings"] if f["weight"] == w]
        if not fs:
            continue
        lines.append("")
        lines.append("■ %s" % label)
        for f in fs:
            lines.append("  [%s] %s ×%d" % (f["rule_id"], f["name"], len(f["matches"])))
            lines.append("    " + f["suggestion"])
            for m in f["matches"][:3]:
                lines.append("    · %s" % _snippet(text, m["start"], m["end"]))
    if not result["findings"]:
        lines.append("  未命中规则；如需进一步，可关注统计分与句长节奏。")
    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────

def _read_stdin():
    """读 stdin 原始字节，优先按 UTF-8 解码，失败回退到本机编码。"""
    try:
        data = sys.stdin.buffer.read()
    except AttributeError:
        return sys.stdin.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        enc = locale.getpreferredencoding(False)
        return data.decode(enc, errors="replace")


def _read_text(args):
    if getattr(args, "file", None):
        p = Path(args.file)
        if not p.exists():
            raise SystemExit("文件不存在：%s\n修复建议：请检查文件路径是否正确、文件名是否拼错。" % p)
        try:
            return p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise SystemExit("无法读取文件：%s 不是 UTF-8 编码\n修复建议：请把文件另存为 UTF-8 编码后重试（记事本 → 另存为 → 编码选 UTF-8）。" % p)
        except OSError as e:
            raise SystemExit("无法读取文件：%s（%s）\n修复建议：请检查文件是否存在、是否有读取权限。" % (p, e))
    if getattr(args, "stdin", False):
        return _read_stdin()
    if getattr(args, "text", None):
        return " ".join(args.text)
    if not sys.stdin.isatty():
        return _read_stdin()
    raise SystemExit("缺少输入：用 -f 指定文件、--stdin 读管道，或直接传文本参数。")


def _add_input_args(ap):
    ap.add_argument("-f", "--file", help="输入文件（UTF-8）")
    ap.add_argument("--stdin", action="store_true", help="从 stdin 读取")
    ap.add_argument("text", nargs="*", help="直接传入的文本")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description="元真（yotta-humanize）：去 AI 味中文写作编辑引擎（24 类规则 + 词表 + 统计突发性）。")
    ap.add_argument("--version", action="version", version="%s %s" % (TOOL_NAME, VERSION))
    sub = ap.add_subparsers(dest="command", required=True)

    p_ver = sub.add_parser("version", help="打印版本")
    p_ver.set_defaults(cmd_version=True)

    p_score = sub.add_parser("score", help="输出 AI 腔评分（0-100）")
    _add_input_args(p_score)
    p_score.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                         help="--gate 判定阈值（默认 %d）" % DEFAULT_THRESHOLD)
    p_score.add_argument("--gate", action="store_true",
                         help="评分 >= 阈值时退出码 1（可用于 CI 拦截）")
    p_score.add_argument("--json", action="store_true", help="输出 JSON")

    p_an = sub.add_parser("analyze", help="详细检测报告（文本）")
    _add_input_args(p_an)
    p_an.add_argument("--json", action="store_true", help="输出 JSON")

    p_rep = sub.add_parser("report", help="Markdown 检测报告")
    _add_input_args(p_rep)

    p_sug = sub.add_parser("suggest", help="按优先级分组的改写建议")
    _add_input_args(p_sug)

    p_rw = sub.add_parser("rewrite", help="确定性改写文本")
    _add_input_args(p_rw)
    p_rw.add_argument("--json", action="store_true", help="输出 JSON")

    args = ap.parse_args(argv)
    try:
        if args.command == "version":
            print("%s %s" % (TOOL_NAME, VERSION))
            return 0
        text = _read_text(args)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 4

    try:
        if args.command == "score":
            res = analyze(text)
            if args.json:
                print(json.dumps({
                    "score": res["score"], "threshold": args.threshold,
                    "pattern_score": res["pattern_score"],
                    "stats_score": res["stats_score"],
                    "total_matches": res["total_matches"],
                    "summary": res["summary"],
                }, ensure_ascii=False, indent=2))
            else:
                print(res["score"])
            if args.gate and res["score"] >= args.threshold:
                return 1
            return 0
        if args.command == "analyze":
            res = analyze(text)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2,
                                 default=str))
            else:
                print(format_analyze(text, res))
            return 0
        if args.command == "report":
            print(format_report(analyze(text)))
            return 0
        if args.command == "suggest":
            print(format_suggest(text, analyze(text)))
            return 0
        if args.command == "rewrite":
            res = rewrite(text)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print("改写前评分：%d/100 → 改写后评分：%d/100" % (res["before"], res["after"]))
                if res["fixes"]:
                    print("修复 %d 处：" % len(res["fixes"]))
                    for fx in res["fixes"]:
                        print("  [%s] %s ×%d（%s）"
                              % (fx["rule_id"], fx["name"], fx["count"], fx["detail"]))
                else:
                    print("无需机械改写；如需人工润色，请运行 suggest 查看建议。")
                print("")
                print(res["text"])
            return 0
    except Exception as e:  # noqa: BLE001
        print("错误：%s\n修复建议：请检查输入是否为 UTF-8 编码、文件是否存在；若仍报错，请把上面的错误信息反馈给开发者。" % e, file=sys.stderr)
        return 4
    return 4


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
