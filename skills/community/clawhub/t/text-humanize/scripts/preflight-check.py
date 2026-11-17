#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only text statistics and optional format constraints (Python stdlib).

Default: INFO / WARN are advisory. --strict only fails explicitly selected
--check constraints; rhythm, word frequency, sentence/paragraph length never
block delivery. Exit 0: no selected format failure; 1: selected format failure;
2: invalid arguments or unreadable input. No authorship or moderation inference.
"""

import argparse
import json
import pathlib
import re
import sys

CLICHE_METAPHOR = ["信使", "信笺", "叹息", "诗篇", "守望者", "耳语", "序章", "独白", "回响"]
FILLER_ADJ = ["温柔", "沉默", "浪漫", "治愈", "漫长", "细碎"]
GREET_WORDS = ["咱们", "大伙儿", "人家"]
SOFT_WORDS = ["确实", "自然", "实在", "其实", "恐怕", "大概"]
# Descriptive buckets, not quality thresholds. See style-patterns-cn.md.
TAIL_SENT_MAX = 20
TRIAD_SENT_MAX = 22
CHECKS = ("quotes", "punctuation", "spacing", "dashes", "numbered-headings")
FAIL, WARN, INFO = "FAIL", "WARN", "INFO"
MASK = "\ufffc"  # Protected characters must not become synthetic typography spaces.
HEADING_NUM_RE = re.compile(
    r"^[ \t]{0,6}(?:[0-9]{1,2}[、.．)）]|[一二三四五六七八九十]{1,3}[、.．]"
    r"|[一二三四五六七八九十]{1,3}[ \t]*$|0[0-9][ \t])", re.M
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
QUOTATION_RE = re.compile(
    r'"(?:\\.|[^"\\\n])*"'
    r"|(?<![A-Za-z])'(?:\\.|[^'\\\n])*'(?![A-Za-z])"
    r"|“[^”\n]*”|‘[^’\n]*’|「[^」\n]*」|『[^』\n]*』"
)
APPO_RE = re.compile(r"[，,][^，。！？；：]{2,14}的[^，。！？；：]{2,10}")


def is_cjk(ch):
    o = ord(ch)
    return 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0xF900 <= o <= 0xFAFF


def cjk_len(text):
    return sum(is_cjk(c) for c in text)


def cjk_ratio(text):
    cjk = cjk_len(text)
    total = cjk + len(re.findall(r"[A-Za-z]", text))
    return cjk / total if total else 0.0


def mask_text(text):
    """Keep boundaries without creating artificial whitespace violations."""
    return re.sub(r"[^\n]", MASK, text)


def blank(match):
    return mask_text(match.group())


def strip_code(text):
    """Mask backtick/tilde fences of any length, indented and inline code.

    A fence closes only with the same character and at least the opener length.
    Unterminated fences stay protected through EOF. Exact-length backtick runs
    delimit inline code, including spans containing shorter backtick runs.
    """
    lines, fence_char, fence_len = [], None, 0
    for line in text.splitlines(keepends=True):
        if fence_char:
            close = re.fullmatch(r" {0,3}" + re.escape(fence_char) +
                                 r"{" + str(fence_len) + r",}[ \t]*(?:\r?\n)?", line)
            lines.append(mask_text(line))
            if close:
                fence_char = None
            continue
        opener = FENCE_RE.match(line)
        if opener and not (opener[1][0] == "`" and "`" in opener[2]):
            fence_char, fence_len = opener[1][0], len(opener[1])
            lines.append(mask_text(line))
        elif line.startswith(("    ", "\t")):
            lines.append(mask_text(line))
        else:
            lines.append(line)
    text = "".join(lines)
    # Scan runs instead of a fixed three-backtick regex.
    parts, start, pos = [], 0, 0
    while pos < len(text):
        opening = re.search(r"`+", text[pos:])
        if not opening:
            break
        left = pos + opening.start()
        run = opening.group()
        right = left + len(run)
        closing = re.search(r"(?<!`)" + re.escape(run) + r"(?!`)", text[right:])
        if closing:
            end = right + closing.end()
            parts.extend((text[start:left], mask_text(text[left:end])))
            start = pos = end
        else:
            pos = right
    parts.append(text[start:])
    return "".join(parts)


def strip_references(text):
    """Mask Markdown quotes (including lazy continuation), definitions and URLs.

    Link labels remain; targets and inline paired quotations are protected.
    This is a conservative heuristic, not a complete Markdown parser.
    """
    out, in_quote, in_definition = [], False, False
    for line in text.splitlines(keepends=True):
        s = line.strip()
        if not s:
            in_quote = in_definition = False
            out.append(line)
            continue
        if re.match(r"^ {0,3}>|^ {0,3}\[(?:\^)?[^\]]+\]:", line):
            in_quote = bool(re.match(r"^ {0,3}>", line))
            in_definition = not in_quote
            out.append(mask_text(line))
        elif in_quote and not re.match(r"^ {0,3}(?:#{1,6}\s|[-*+]\s|\d+[.)]\s)", line):
            out.append(mask_text(line))
        elif in_definition and line.startswith(("  ", "\t")):
            out.append(mask_text(line))
        else:
            in_quote = in_definition = False
            out.append(line)
    text = "".join(out)
    # Keep labels, mask destination including optional title; nested parentheses
    # beyond one level are intentionally left to manual review.
    text = re.sub(r"(!?\[[^\]\n]*\])\((?:[^()\n]|\([^()\n]*\))*\)",
                  lambda m: m[1] + MASK * (len(m[0]) - len(m[1])), text)
    text = re.sub(r"<[^<>\n]*(?:://|@)[^<>\n]*>", blank, text)
    text = re.sub(r"(?:https?://|www\.)[^\s<>\u3400-\u9fff，。！？；：]+", blank, text)
    return text


def prepare_text(raw):
    base = strip_references(strip_code(raw.replace("\r\n", "\n").replace("\r", "\n")))
    # All recognizable paired quotations are excluded, even in Chinese. Keep
    # their raw delimiter counts separately rather than propose changing quotes.
    return base, QUOTATION_RE.sub(blank, base)


def join_soft_lines(lines):
    text = "\n".join(line.strip() for line in lines)
    text = re.sub(r"(?<=[A-Za-z0-9])\n(?=[A-Za-z0-9])", " ", text)
    return text.replace("\n", "")


def body_paragraphs(text):
    """Blank-line paragraphs; headings, lists, quotes and tables are not prose."""
    out, current, list_block = [], [], False

    def flush():
        if current:
            out.append(join_soft_lines(current))
            current.clear()

    for line in text.splitlines():
        line = line.replace(MASK, "")
        s = line.strip()
        if not s:
            flush()
            list_block = False
        elif re.fullmatch(r"(?:=+|-+)", s) and current:
            # Setext heading: its preceding lines are a title, not a paragraph.
            current.clear()
        elif (s.startswith(("#", ">", "|")) or "|" in s or
              re.fullmatch(r"(?:[-*_]\s*){3,}", s) or
              re.match(r"^[-*+]\s|^\d+[.)、]\s", s) or HEADING_NUM_RE.match(s)):
            flush()
            list_block = bool(re.match(r"^[-*+]\s|^\d+[.)、]\s", s))
        elif list_block:
            continue
        else:
            current.append(s)
    flush()
    return out


def strip_md_markers(text):
    return re.sub(r"^[ \t]{0,3}#{1,6}[ \t]+", "", text, flags=re.M)


def baseline_note(text):
    half = text.count('"')
    curly = text.count("“") + text.count("”")
    if half:
        return (f"引号观察：半角双引号 {half} / 弯双引号 {curly}。仅凭数量不能判断作者来源、"
                "格式错误或转录污染；请对照原文件和引用语境，不要自动替换。")
    return None


def punctuation_view(text):
    """Mask recognizable English fragments before Chinese typography checks."""
    # At least one Latin letter; apostrophes, ASCII punctuation and dash forms
    # within an English fragment are legitimate. CJK text is never consumed.
    return re.sub(r"[A-Za-z][A-Za-z0-9 \t'’\".,;:!?()—–-]*", blank, text)


def sentences(paragraph):
    # Soft line wrapping has already been joined. Ellipses/delimiters are
    # approximations; this is not a syntactic sentence segmenter.
    return [s for s in re.split(r"[。！？!?]+", paragraph) if cjk_len(s) >= 2]


def collect(text, tier, para_max, lyrical):
    rows = []

    def add(level, scope, name, value, limit=None, check=None):
        rows.append(dict(level=level, scope=scope, name=name, value=value, limit=limit, check=check))

    punc = punctuation_view(strip_md_markers(text))
    add(WARN, "标点层", '未保护的半角双引号 "', punc.count('"'), 0, "quotes")
    add(WARN, "标点层", "未保护的半角单引号 '", punc.count("'"), 0, "quotes")
    add(WARN, "标点层", "中文后半角逗号/句点", len(re.findall(r"[\u3400-\u9fff][,.]", punc)), 0, "punctuation")
    add(WARN, "标点层", "三点省略号 ...", punc.count("..."), 0, "punctuation")
    add(WARN, "标点层", "非选定中文破折号形态 -- / 单 —",
        len(re.findall(r"(?<!-)--(?!-)|(?<!—)—(?!—)", punc)), 0, "dashes")
    add(WARN, "标点层", "破折号前后带空格", len(re.findall(r"[ \t]——|——[ \t]", punc)), 0, "spacing")
    add(WARN, "标点层", "标点周边空格",
        len(re.findall(r"[，。！？；：、）】”’][ \t]|[ \t][（【“‘]", punc)), 0, "spacing")
    add(INFO, "标点层", "标准破折号 ——(总量)", text.count("——"))
    add(INFO, "标点层", "中文省略号 ……", text.count("……"))
    if tier == "short":
        add(INFO, "风格提示", "短文本破折号(允许使用)", text.count("——"))
    add(WARN, "排版", "编号式小标题(可选体例)", len(HEADING_NUM_RE.findall(strip_md_markers(text))), 0, "numbered-headings")

    paras = body_paragraphs(text)
    lens = [cjk_len(p) for p in paras]
    add(WARN, "排版", f"超 {para_max} 字段落数(参考)", sum(n > para_max for n in lens), 0)
    add(INFO, "排版", "最长段落(字)", max(lens, default=0))
    add(INFO, "排版", "段落总数", len(paras))
    add(INFO, "人称", "「我们」", text.count("我们"))
    add(INFO, "人称", "「我」(不含我们)", len(re.findall(r"我(?!们)", text)))

    groups = [sentences(p) for p in paras]
    sent_lens = [cjk_len(s) for group in groups for s in group]
    add(INFO, "节奏", "句段数(粗计)", len(sent_lens))
    add(INFO, "节奏", "句段平均 CJK 字数", round(sum(sent_lens) / len(sent_lens), 2) if sent_lens else 0)

    if lyrical or tier == "literary":
        appo = longest = peak = 0
        for group in groups:
            run = count = 0
            for s in group:
                if APPO_RE.search(s):
                    appo += 1
                    count += 1
                    run += 1
                    longest = max(longest, run)
                else:
                    run = 0
            peak = max(peak, count)
        add(INFO, "R类", "同位语形态句数 X，Y的Z(粗计)", appo)
        add(INFO, "R类", "同位语最长连续句数(段内)", longest)
        add(INFO, "R类", "同位语单段峰值(粗计)", peak)
        add(INFO, "R类", "同位语形态句数占比%", round(appo * 100 / len(sent_lens), 2) if sent_lens else 0)
        add(INFO, "R类", "喻体词库命中", sum(text.count(w) for w in CLICHE_METAPHOR))
        add(INFO, "R类", "形容词词库命中", sum(text.count(w) for w in FILLER_ADJ))
        add(INFO, "R类", "词库命中明细", {w: text.count(w) for w in CLICHE_METAPHOR + FILLER_ADJ if text.count(w)})

    if tier in ("long", "literary"):
        tail = sum(bool(g) and cjk_len(g[-1]) <= TAIL_SENT_MAX for g in groups)
        add(INFO, "SS-CN8", f"段尾短句(≤{TAIL_SENT_MAX}字) / 段落数", f"{tail} / {len(paras)}")
        add(INFO, "SS-CN8", "段尾短句占比%(仅供人工参考)", round(tail * 100 / len(paras), 2) if paras else 0)
        add(INFO, "SS-CN8", "招呼式称谓(咱们/大伙儿/人家)", sum(text.count(w) for w in GREET_WORDS))
        add(INFO, "SS-CN8", "模糊限定词(确实/自然/实在/其实/恐怕/大概)", sum(text.count(w) for w in SOFT_WORDS))
        add(INFO, "SS-CN8", "词频明细", {w: text.count(w) for w in GREET_WORDS + SOFT_WORDS})
        triad = sum(s.count("，") + s.count("、") >= 2 and cjk_len(s) <= TRIAD_SENT_MAX for g in groups for s in g)
        add(INFO, "SS-CN8", "多逗号短句(粗计，非语法同构识别)", triad)
        add(INFO, "SS-CN8", "小标题节数", len(re.findall(r"^ {0,3}#{1,6}[ \t]+", text, re.M)))
    return rows


def apply_constraints(rows, zh_mode, strict, selected):
    for row in rows:
        if row["scope"] == "标点层" and not zh_mode:
            row.update(level=INFO, limit=None)
        elif strict and row["check"] in selected:
            row["level"] = FAIL
    return rows


def grade(row):
    level, value, limit = row["level"], row["value"], row["limit"]
    if level == INFO or limit is None:
        return "-", False
    bad = value > limit
    if level == FAIL:
        return ("FAIL" if bad else "OK"), bad
    return ("warn" if bad else "ok"), False


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("必须为正整数")
    return number


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path")
    ap.add_argument("--tier", choices=["short", "long", "literary"], default="long")
    ap.add_argument("--lyrical", action="store_true")
    ap.add_argument("--para-max", type=positive_int, default=70, help="段长参考值，不决定退出码")
    ap.add_argument("--strict", action="store_true", help="仅选定的 --check 格式约束决定退出码")
    ap.add_argument("--check", action="append", choices=CHECKS, default=[], help="显式选择格式约束，可重复")
    ap.add_argument("--cut", help="在首个字面标记处截断，未找到时保持原文并提示")
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto", help="auto: CJK >50%% 才启用中文格式检查")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        raw = pathlib.Path(a.path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        if a.json:
            print(json.dumps({"error": str(error), "file": a.path}, ensure_ascii=False))
        else:
            print(f"读取失败: {error}", file=sys.stderr)
        return 2
    notes = []
    cut_found = bool(a.cut and a.cut in raw)
    if cut_found:
        raw = raw.split(a.cut, 1)[0]
    elif a.cut:
        notes.append("未找到 --cut 标记；统计完整文件。")
    if a.strict and not a.check:
        notes.append("--strict 未选 --check；所有结果仅供参考，不因文风失败。")
    base, text = prepare_text(raw)
    ratio = cjk_ratio(text)
    zh_mode = a.lang == "zh" or (a.lang == "auto" and ratio > 0.5)
    rows = apply_constraints(collect(text, a.tier, a.para_max, a.lyrical), zh_mode, a.strict, set(a.check))
    rows.extend([
        dict(level=INFO, scope="引号原始统计", name='半角双引号 "(含行内引语)', value=base.count('"'), limit=None, check=None),
        dict(level=INFO, scope="引号原始统计", name="弯双引号 “ ”(含行内引语)", value=base.count("“") + base.count("”"), limit=None, check=None),
    ])
    graded = [(row, *grade(row)) for row in rows]
    fails = sum(mark == "FAIL" for _, mark, _ in graded)
    warns = sum(mark == "warn" for _, mark, _ in graded)
    lang_note = None
    if not zh_mode:
        reason = "显式指定 en" if a.lang == "en" else f"CJK 占比 {ratio:.1%}，未超过 50%"
        lang_note = f"{reason}；中文标点约束不适用，仅报统计。"
    out = dict(file=a.path, tier=a.tier, cjk=cjk_len(text), cjk_ratio=round(ratio, 6), zh_mode=zh_mode,
               strict=a.strict, checks=sorted(set(a.check)), cut_found=cut_found,
               rows=[dict(row, mark=mark) for row, mark, _ in graded], fail=fails, warn=warns, notes=notes)
    if lang_note:
        out["lang_note"] = lang_note
    if baseline_note(base):
        out["baseline_note"] = baseline_note(base)
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"文件: {a.path}\n档位: {a.tier}    可分析 CJK 字数: {cjk_len(text)}")
        for note in notes + [out[k] for k in ("lang_note", "baseline_note") if k in out]:
            print(f"提示: {note}")
        scope = None
        for row, mark, _ in graded:
            if row["scope"] != scope:
                scope = row["scope"]
                print(f"[{scope}]")
            value = json.dumps(row["value"], ensure_ascii=False) if isinstance(row["value"], dict) else row["value"]
            print(f"  {mark:4} {row['name']}: {value}")
        print(f"结果: 显式格式约束失败 {fails} 项；可选提示 {warns} 项。统计不代表质量或审核结论。")
    return int(bool(fails))


if __name__ == "__main__":
    sys.exit(main())
