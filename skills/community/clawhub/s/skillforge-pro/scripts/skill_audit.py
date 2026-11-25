# -*- coding: utf-8 -*-
"""SkillForge audit: deterministic metrics plus a first-pass six-dimension score.

Standard library only (Python 3.8+). No third-party dependency, no network access.

Usage
-----
    python skill_audit.py <skill_dir | path/to/SKILL.md>
    python skill_audit.py <skill_dir> --profile generic --json card.json --fail-under 75
    python skill_audit.py --scan <library_root> --depth 3 --json queue.json

Output is one JSON document on stdout (UTF-8). The first-pass score is a
mechanical baseline: re-score by hand against references/audit-rubric.md before
reporting. Exit codes: 0 = score >= fail_under, 1 = score < fail_under,
2 = usage error or unreadable target.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys

TOOL_VERSION = "1.0.0"
SCHEMA_CARD = "skillforge.audit.v1"
SCHEMA_BATCH = "skillforge.audit.batch.v1"

WEIGHTS = [
    ("trigger", "触发准确性", 20),
    ("boundary", "边界清晰度", 15),
    ("workflow", "流程可执行性", 25),
    ("acceptance", "验收可检验性", 20),
    ("token", "token 经济性", 10),
    ("safety", "安全合规", 10),
]

HOUSE_FIELDS = [
    "name", "display_name", "display_name_en", "description", "description_en",
    "version", "category", "sub_categories", "tags", "tags_en", "icon",
    "platforms", "trigger_keywords", "author", "license", "pay_skill", "price_cny",
]
GENERIC_FIELDS = ["name", "description"]

EXCLUDE_DIRS = {
    ".git", "__pycache__", "node_modules", "dist", ".pay_cache", ".archive",
    "_done", ".venv", "venv", ".idea", ".vscode", "build",
}

# --- filler phrases -------------------------------------------------------
# strong: genuinely undecidable in a spec; weak: soft words that only matter
# in bulk and are reported separately so the score stays defensible.
STRONG_FILLER = [
    "根据实际情况", "视情况而定", "视具体情况", "酌情", "灵活处理", "灵活把握",
    "适当", "尽可能", "尽量", "等等", "若干", "差不多", "大概", "大致",
    "as appropriate", "as needed", "where appropriate", "and so on",
]
WEAK_FILLER = [
    "一般来说", "通常情况下", "原则上", "如有必要", "必要时", "建议考虑",
    "可以考虑", "需要注意的是", "值得注意的是", "综合来看", "总体来说",
    "保证效果", "高质量", "专业水准", "确保", "努力",
    "in general", "if necessary", "try to", "ensure",
]
VOICE_TRACES = [
    "我的经验", "我之前", "我遇到", "我踩过", "踩过的坑", "某用户", "本人经验",
    "in my experience", "from my own", "a user once",
]

# --- risk patterns --------------------------------------------------------
RX_WIN_PATH = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]")
RX_POSIX_HOME = re.compile(r"(?<![\w.])/(?:home|root|Users|opt|mnt)/")
RX_TILDE = re.compile(r"(?<![\w])~/")
RX_KEYLIKE = re.compile(
    r"(?i)\b(?:sk|pk|rk|ghp|gho|ghs|glpat|xox[abprs])[-_][A-Za-z0-9_-]{16,}")
RX_SECRET_ASSIGN = re.compile(
    r"(?i)(?:api[_-]?key|secret|token|password|passwd|access[_-]?key)\s*[:=]\s*"
    r"[\"'][^\"'\s]{8,}[\"']")
RX_PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
RX_INTERNAL_IP = re.compile(
    r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")
RX_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[A-Za-z]{2,}\b")
RX_PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
RX_LINK = re.compile(r"https?://[^\s<>\)\]\"']+")
DANGER_WORDS = ["删除", "覆盖", "清空", "发送", "推送", "发布", "部署", "上线",
                "rm -rf", "DROP TABLE", "git push", "force push", "delete", "overwrite"]
CONFIRM_WORDS = ["确认", "先询问", "预览", "试运行", "回滚", "备份", "dry-run",
                 "confirm", "preview", "rollback", "backup"]

RX_FENCE = re.compile(r"^\s*(```+|~~~+)")
RX_H2 = re.compile(r"^##\s+(.+?)\s*$")
RX_H1 = re.compile(r"^#\s+(.+?)\s*$")
RX_H3 = re.compile(r"^###\s+")
RX_CHECKBOX = re.compile(r"^\s*[-*]\s+\[[ xX]\]")
RX_NUMBERED = re.compile(r"^\s*\d+[.)]\s+")
RX_H3_STEP = re.compile(r"^###\s+\d+[.)、]?\s")
RX_BULLET = re.compile(r"^\s*[-*+]\s+")
RX_TABLE = re.compile(r"^\s*\|")
RX_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")
RX_CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


# --------------------------------------------------------------------------
# reading
# --------------------------------------------------------------------------
def read_text(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(enc).replace("\r\n", "\n").replace("\r", "\n"), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8/replace"


def split_frontmatter(text):
    """Return (fm_lines or None, body, reason)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text, "no-frontmatter"
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            return lines[1:i], "\n".join(lines[i + 1:]), "ok"
    return None, text, "unterminated-frontmatter"


def parse_frontmatter(fm_lines):
    data, order = {}, []
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = RX_KEY.match(line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        i += 1
        if val in (">-", ">", "|", "|-", ">+", "|+"):
            buf = []
            while i < len(fm_lines) and (not fm_lines[i].strip()
                                         or fm_lines[i][:1] in (" ", "\t")):
                buf.append(fm_lines[i].strip())
                i += 1
            data[key] = " ".join(x for x in buf if x)
        elif val == "":
            items = []
            while i < len(fm_lines) and (not fm_lines[i].strip()
                                         or fm_lines[i][:1] in (" ", "\t")):
                s = fm_lines[i].strip()
                if s.startswith("- "):
                    items.append(s[2:].strip())
                elif s.startswith("-"):
                    items.append("")
                i += 1
            data[key] = [x.strip("\"'") for x in items] if items else ""
        elif val.startswith("[") and val.endswith("]"):
            data[key] = [x.strip().strip("\"'") for x in val[1:-1].split(",") if x.strip()]
        else:
            if len(val) > 1 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            data[key] = val
        order.append(key)
    return data, order


def count_items(value):
    if isinstance(value, list):
        return len([x for x in value if str(x).strip()])
    if isinstance(value, str) and value.strip():
        return len([x for x in re.split(r"[,，;；]", value) if x.strip()])
    return 0


# --------------------------------------------------------------------------
# body metrics
# --------------------------------------------------------------------------
def mask_fences(body):
    """Blank out fenced code so headings inside examples are not counted.

    Tracks the opening fence length so a nested ``` inside a ```` block does
    not close the outer block early.
    """
    out, fence_char, fence_len, blocks = [], None, 0, 0
    for line in body.split("\n"):
        m = RX_FENCE.match(line)
        if m:
            token = m.group(1).strip()
            ch, length = token[0], len(token)
            if fence_char is None:
                fence_char, fence_len = ch, length
                blocks += 1
                out.append("")
                continue
            if ch == fence_char and length >= fence_len:
                fence_char, fence_len = None, 0
                out.append("")
                continue
        out.append("" if fence_char else line)
    return out, blocks


def mask_inline_code(line):
    return re.sub(r"`[^`]*`", "``", line)


def body_metrics(body):
    raw = body.split("\n")
    if raw and raw[-1] == "":
        raw = raw[:-1]
    masked, blocks = mask_fences(body)
    h2, h1, h3 = [], 0, 0
    checkboxes = steps = bullets = table_rows = 0
    for line in masked:
        if RX_H1.match(line):
            h1 += 1
        elif RX_H2.match(line):
            h2.append(RX_H2.match(line).group(1))
        elif RX_H3.match(line):
            h3 += 1
        if RX_CHECKBOX.match(line):
            checkboxes += 1
        elif RX_NUMBERED.match(line):
            steps += 1
        elif RX_BULLET.match(line):
            bullets += 1
        if RX_TABLE.match(line):
            table_rows += 1
    return {
        "body_lines": len(raw),
        "body_content_lines": len([x for x in raw if x.strip()]),
        "h1_count": h1,
        "h2": h2,
        "h2_count": len(h2),
        "h3_count": h3,
        "code_blocks": blocks,
        "checkboxes": checkboxes,
        "numbered_steps": steps,
        "bullets": bullets,
        "table_rows": table_rows,
        "masked_lines": masked,
    }


def find_section(lines, keywords):
    """Return (start, end) of the first H2 whose title matches any keyword."""
    for idx, line in enumerate(lines):
        m = RX_H2.match(line)
        if not m:
            continue
        title = m.group(1).lower()
        if any(k.lower() in title for k in keywords):
            end = len(lines)
            for j in range(idx + 1, len(lines)):
                if RX_H2.match(lines[j]) or RX_H1.match(lines[j]):
                    end = j
                    break
            return idx, end
    return None


def scan_phrases(lines, phrases):
    hits = []
    for no, line in enumerate(lines, start=1):
        probe = mask_inline_code(line)
        low = probe.lower()
        for phrase in phrases:
            if phrase.lower() in low:
                hits.append({"phrase": phrase, "line": no})
    return hits


def find_all(rx, text):
    out = []
    for m in rx.finditer(text):
        start = max(0, m.start() - 40)
        out.append(text[start:m.end() + 40].replace("\n", " ").strip())
    return out


def estimate_tokens(body):
    cjk = len(RX_CJK.findall(body))
    other = max(0, len(body) - cjk)
    mid = cjk * 0.65 + other * 0.27
    low = cjk * 0.55 + other * 0.22
    high = cjk * 0.78 + other * 0.34
    if mid <= 1500:
        band = "lean"
    elif mid <= 4000:
        band = "standard"
    elif mid <= 8000:
        band = "heavy"
    else:
        band = "oversize"
    return {
        "cjk_chars": cjk,
        "other_chars": other,
        "est_tokens": int(round(mid)),
        "est_tokens_range": [int(round(low)), int(round(high))],
        "est_tokens_band": band,
    }


def dependency_links(body, base_dir):
    """Cite-vs-exists check for references/, scripts/, assets/ mentions."""
    cited, missing = [], []
    for m in re.finditer(r"(?:references|scripts|assets)/[A-Za-z0-9_.\-/]+", body):
        rel = m.group(0).rstrip(".,;:)")
        if rel in cited:
            continue
        cited.append(rel)
        if not os.path.exists(os.path.join(base_dir, rel)):
            missing.append(rel)
    return {"cited": cited, "missing": missing}


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------
def score_trigger(fm, sec_title_list, lines):
    ev, notes = [], []
    trig = fm.get("trigger_keywords") or fm.get("trigger") or fm.get("triggers")
    n = count_items(trig)
    has_scene = find_section(lines, ["适用场景", "使用场景", "when to use", "use cases"]) is not None
    has_counter = any(k in ("\n".join(lines)).lower() for k in
                      ("不要触发", "不适用", "请勿使用", "do not use", "don't use", "when not to"))
    if n == 0 and not has_scene:
        return 0, ["no trigger field and no scenario section"], ["D1 无触发词也无场景，技能几乎不可能被选中"]
    if n == 0:
        return 1, ["no trigger field; scenario section only"], ["D1 只有场景没有触发词，命中依赖语义偶合"]
    if n <= 5:
        score = 2
        ev.append("trigger count=%d (too narrow)" % n)
    elif n <= 12:
        score = 3
        ev.append("trigger count=%d (in range 6-12)" % n)
    else:
        score = 2
        ev.append("trigger count=%d (over 12, misfire risk)" % n)
    if has_counter:
        score += 1
        ev.append("counter-trigger clauses present")
    else:
        notes.append("D1 缺反触发（以下情况不要使用）")
    if 6 <= n <= 12 and has_scene:
        score += 1
        ev.append("triggers align with a scenario section")
    else:
        notes.append("D1 触发词与场景小节无法逐条对应")
    return min(score, 5), ev, notes


def score_boundary(lines):
    ev, notes = [], []
    span = find_section(lines, ["能力边界", "边界", "限制", "范围", "不适用",
                                "boundaries", "limitations", "scope", "not for"])
    if span is None:
        return 0, ["no boundary section"], ["D2 无边界小节，技能会在错误场景里硬做"]
    text = "\n".join(lines[span[0]:span[1]])
    items = [x for x in lines[span[0]:span[1]] if RX_BULLET.match(x)]
    has_action = any(k in text for k in ("拒答", "拒绝", "降级", "转人工", "跳过",
                                         "终止", "返回", "refuse", "decline", "degrade",
                                         "abort", "skip", "reject"))
    has_cond = any(k in text for k in ("若", "当", "超过", "为空", "不含", "if ", "when ", "exceed"))
    score = 0
    if len(items) >= 3:
        score += 2
        ev.append("boundary items=%d" % len(items))
    elif items:
        score += 1
        ev.append("boundary items=%d (fewer than 3)" % len(items))
    else:
        notes.append("D2 边界小节存在但没有条目，等同免责声明")
    if has_action:
        score += 1
        ev.append("explicit handling on the boundary")
    else:
        notes.append("D2 未说明碰到边界时是拒答、降级还是转人工")
    if has_cond:
        score += 1
        ev.append("boundary phrased as a checkable condition")
    return min(score, 5), ev, notes


def score_workflow(lines, metrics):
    ev, notes = [], []
    span = find_section(lines, ["工作流", "流程", "步骤", "workflow", "process", "steps", "procedure"])
    if span is None:
        return 0, ["no workflow section"], ["D3 无工作流小节，只有目标没有做法"]
    text = lines[span[0]:span[1]]
    steps = sum(1 for x in text if RX_NUMBERED.match(x) or RX_H3_STEP.match(x))
    crit = sum(1 for x in text if "判据" in x or "criterion" in x.lower()
               or "pass if" in x.lower())
    fail = sum(1 for x in text if "失败" in x or "if it fails" in x.lower()
               or "fallback" in x.lower() or "on failure" in x.lower())
    link = sum(1 for x in text if any(k in x for k in ("产物", "输出", "输入", "output", "input")))
    if 4 <= steps <= 8:
        score = 2
        ev.append("numbered steps=%d (in range 4-8)" % steps)
    elif 2 <= steps <= 12:
        score = 1
        ev.append("numbered steps=%d (outside 4-8)" % steps)
    else:
        return 0, ["workflow section has no numbered steps"], ["D3 工作流没有编号步骤，无法照做"]
    need = max(2, steps * 0.5)
    if crit >= need:
        score += 1
        ev.append("criteria mentions=%d" % crit)
    else:
        notes.append("D3 判据覆盖不足（%d/%d 步）" % (crit, steps))
    if fail >= need:
        score += 1
        ev.append("failure branches=%d" % fail)
    else:
        notes.append("D3 失败分支覆盖不足（%d/%d 步）" % (fail, steps))
    if link >= 2:
        score += 1
        ev.append("step-to-step artifacts referenced")
    return min(score, 5), ev, notes


def score_acceptance(lines):
    ev, notes = [], []
    span = find_section(lines, ["质量门槛", "验收", "检查清单", "checklist",
                                "quality gate", "acceptance", "quality"])
    if span is None:
        return 0, ["no acceptance section"], ["D4 无验收小节，交付好坏无法判定"]
    chunk = lines[span[0]:span[1]]
    text = "\n".join(chunk)
    boxes = sum(1 for x in chunk if RX_CHECKBOX.match(x))
    measurable = len(re.findall(r"\d+\s*(?:行|字|条|个|字段|节|文件|毫秒|秒|分钟|%|字以内|以内)" , text))
    measurable += len(re.findall(r"(?:≤|≥|<=|>=|不超过|至少|最多|不多于|不少于)", text))
    measurable += len(re.findall(
        r"\b\d+\s*(?:lines?|words?|items?|fields?|sections?|files?|rows?|entries?|ms|seconds?|minutes?|%)",
        text, re.I))
    measurable += len(re.findall(
        r"(?i)\b(?:at most|at least|no more than|no fewer than|up to|not exceed|capped at)\b",
        text))
    if boxes >= 6:
        score = 2
        ev.append("checklist items=%d" % boxes)
    elif boxes >= 3:
        score = 1
        ev.append("checklist items=%d (fewer than 6)" % boxes)
    else:
        notes.append("D4 清单条目不足 3 条")
        score = 0
    if measurable >= 3:
        score += 2
        ev.append("measurable thresholds=%d" % measurable)
    elif measurable >= 1:
        score += 1
        ev.append("measurable thresholds=%d" % measurable)
    else:
        notes.append("D4 无任何可测量阈值（行数/字数/字段数/时长）")
    vague = len(re.findall(r"(完整|专业|合理|清晰|易用|良好|高质量|快速)", text))
    if measurable == 0 and vague >= 2:
        score = max(0, score - 1)
        notes.append("D4 验收以形容词为主，无法打勾")
    return min(score, 5), ev, notes


def score_token(size, metrics, has_refs, dup_h2):
    ev, notes = [], []
    est = size["est_tokens"]
    lines_n = metrics["body_lines"]
    if est > 8000:
        score = 0
        notes.append("D5 估算 %d token 已超 8,000，必须拆分" % est)
    elif lines_n >= 500 and not has_refs:
        score = 0
        notes.append("D5 正文 %d 行且无 references，属未拆分" % lines_n)
    elif est > 4000:
        score = 3
        notes.append("D5 估算 %d token 落在 4,000-8,000，存在可下沉段落" % est)
    else:
        score = 5
        ev.append("est_tokens=%d within budget" % est)
    if score >= 3 and dup_h2 >= 2:
        score -= 1
        notes.append("D5 二级标题重复 %d 处，存在重复表述" % dup_h2)
    if score >= 4 and not has_refs and lines_n > 200:
        score -= 1
        notes.append("D5 正文偏长但没有任何 references 承接细则")
    return max(0, min(score, 5)), ev, notes


def score_safety(risks, voice_hits, danger_hits, confirm_hits):
    ev, notes = [], []
    hard = bool(risks["absolute_paths"] or risks["secrets"]
                or risks["internal_ips"] or risks["personal"])
    if hard:
        notes.append("D6 命中绝对路径/密钥/内部地址/个人信息，该维清零")
        return 0, ev, notes, True
    if danger_hits and not confirm_hits:
        notes.append("D6 出现高危动作（%s）但全文无确认、预览或回滚说明" % "、".join(sorted(set(danger_hits))[:4]))
        return 3, ev, notes, False
    if voice_hits:
        notes.append("D6 存在来源痕迹表述（%d 处），应改为中性陈述" % len(voice_hits))
        return 3, ev, notes, False
    ev.append("no path, secret, internal address or personal data found")
    return 5, ev, notes, False


def grade_of(total, veto):
    if veto:
        return "D"
    if total >= 90:
        return "S"
    if total >= 75:
        return "A"
    if total >= 60:
        return "B"
    if total >= 40:
        return "C"
    return "D"


def finding_level(dim, score):
    if dim == "safety" and score == 0:
        return "P0"
    if score <= 1:
        return "P0"
    if score == 2:
        return "P1"
    if score == 3:
        return "P2"
    return "P3"


# --------------------------------------------------------------------------
# single audit
# --------------------------------------------------------------------------
def audit_one(skill_md, profile="house", base_dir=None):
    text, encoding = read_text(skill_md)
    base_dir = base_dir or os.path.dirname(os.path.abspath(skill_md))
    fm_lines, body, fm_state = split_frontmatter(text)
    fm, order = parse_frontmatter(fm_lines) if fm_lines is not None else ({}, [])
    metrics = body_metrics(body)
    lines = metrics.pop("masked_lines")
    size = estimate_tokens(body)
    need = HOUSE_FIELDS if profile == "house" else GENERIC_FIELDS
    missing = [k for k in need if not fm.get(k)]
    completeness = round((len(need) - len(missing)) / float(len(need)), 3)

    has_refs = os.path.isdir(os.path.join(base_dir, "references"))
    dup_h2 = len(metrics["h2"]) - len(set(metrics["h2"]))

    strong = scan_phrases(lines, STRONG_FILLER)
    weak = scan_phrases(lines, WEAK_FILLER)
    voice = scan_phrases(lines, VOICE_TRACES)

    risks = {
        "absolute_paths": find_all(RX_WIN_PATH, body) + find_all(RX_POSIX_HOME, body)
                          + find_all(RX_TILDE, body),
        "secrets": find_all(RX_KEYLIKE, body) + find_all(RX_SECRET_ASSIGN, body)
                   + find_all(RX_PRIVATE_KEY, body),
        "internal_ips": find_all(RX_INTERNAL_IP, body),
        "personal": find_all(RX_EMAIL, body) + find_all(RX_PHONE, body),
        "links": find_all(RX_LINK, body)[:20],
    }
    lower = body.lower()
    danger_hits = [w for w in DANGER_WORDS if w.lower() in lower]
    confirm_hits = [w for w in CONFIRM_WORDS if w.lower() in lower]

    dims, notes_all = {}, []
    for key, scorer in (("trigger", None), ("boundary", None), ("workflow", None),
                        ("acceptance", None), ("token", None), ("safety", None)):
        if key == "trigger":
            s, ev, nt = score_trigger(fm, metrics["h2"], lines)
        elif key == "boundary":
            s, ev, nt = score_boundary(lines)
        elif key == "workflow":
            s, ev, nt = score_workflow(lines, metrics)
        elif key == "acceptance":
            s, ev, nt = score_acceptance(lines)
        elif key == "token":
            s, ev, nt = score_token(size, metrics, has_refs, dup_h2)
        else:
            s, ev, nt, veto = score_safety(risks, voice, danger_hits, confirm_hits)
        weight = dict((k, w) for k, _label, w in WEIGHTS)[key]
        dims[key] = {"score": s, "weight": weight,
                     "weighted": round(s / 5.0 * weight, 1),
                     "evidence": ev}
        for item in nt:
            notes_all.append({"dim": key, "level": finding_level(key, s) if not item.startswith("D5") else "P2",
                              "message": item})

    total = round(sum(d["weighted"] for d in dims.values()), 1)
    veto = dims["safety"]["score"] == 0
    grade = grade_of(total, veto)

    return {
        "schema": SCHEMA_CARD,
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "tool": {"name": "skill_audit.py", "version": TOOL_VERSION, "profile": profile},
        "skill": {
            "name": fm.get("name") or os.path.basename(base_dir),
            "dir": os.path.abspath(base_dir),
            "path": os.path.abspath(skill_md),
            "encoding": encoding,
            "frontmatter_state": fm_state,
            "parsed": fm_state == "ok" and bool(fm),
        },
        "frontmatter": {
            "present": fm_lines is not None,
            "field_count": len(order),
            "keys": order,
            "required_for_profile": need,
            "missing": missing,
            "completeness": completeness,
            "description_chars": len(str(fm.get("description", ""))),
        },
        "structure": {
            "total_lines": len(text.split("\n")) - (1 if text.endswith("\n") else 0),
            "body_lines": metrics["body_lines"],
            "body_content_lines": metrics["body_content_lines"],
            "chars": len(text),
            "body_chars": len(body),
            "h1_count": metrics["h1_count"],
            "h2_count": metrics["h2_count"],
            "h2": metrics["h2"],
            "h3_count": metrics["h3_count"],
            "code_blocks": metrics["code_blocks"],
            "table_rows": metrics["table_rows"],
            "checkboxes": metrics["checkboxes"],
            "numbered_steps": metrics["numbered_steps"],
            "bullets": metrics["bullets"],
        },
        "size": size,
        "filler": {
            "strong_count": len(strong),
            "weak_count": len(weak),
            "total": len(strong) + len(weak),
            "strong_hits": strong[:20],
            "weak_hits": weak[:20],
        },
        "voice": {"count": len(voice), "hits": voice[:10]},
        "risks": risks,
        "dependencies": dependency_links(body, base_dir),
        "duplicates": {"h2_repeats": dup_h2},
        "score": {"dimensions": dims, "total": total, "grade": grade, "veto": veto},
        "findings": notes_all[:20],
    }


# --------------------------------------------------------------------------
# batch
# --------------------------------------------------------------------------
def scan_root(root, max_depth):
    found = []
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in EXCLUDE_DIRS and not d.startswith("."))
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if depth > max_depth:
            dirnames[:] = []
            continue
        if "SKILL.md" in filenames:
            found.append(os.path.join(dirpath, "SKILL.md"))
    return found


def severity_of(card):
    if card["score"]["veto"] or card["score"]["total"] < 60:
        return 3
    if card["score"]["total"] < 75:
        return 2
    return 1


def cost_of(card):
    lines = card["structure"]["body_lines"]
    est = card["size"]["est_tokens"]
    if lines <= 150 and est <= 3000:
        return 1
    if lines <= 400:
        return 2
    return 3


def top_issue(card):
    for finding in card.get("findings", []):
        if finding["level"] in ("P0", "P1"):
            return finding["message"]
    for dim in ("trigger", "workflow", "acceptance", "boundary", "token"):
        d = card["score"]["dimensions"][dim]
        if d["score"] <= 3 and d["evidence"]:
            return d["evidence"][0]
    return "minor polish only"


def audit_batch(root, profile, depth, impact):
    md_files = scan_root(root, depth)
    root_abs = os.path.abspath(root)
    cards, entries = [], []
    for md in md_files:
        try:
            card = audit_one(md, profile=profile)
        except Exception as exc:  # keep the batch alive on a single bad file
            cards.append({"schema": SCHEMA_CARD, "path": md, "error": repr(exc)})
            continue
        rel = os.path.relpath(os.path.dirname(md), root_abs).replace("\\", "/")
        card["rel_path"] = rel
        total = card["score"]["total"]
        s, c = severity_of(card), cost_of(card)
        priority = round(impact * s / float(c), 2)
        cards.append(card)
        entries.append({
            "name": card["skill"]["name"],
            "rel_path": rel,
            "total": total,
            "grade": card["score"]["grade"],
            "veto": card["score"]["veto"],
            "impact": impact,
            "severity": s,
            "cost": c,
            "priority": priority,
            "top_issue": top_issue(card),
        })
    entries.sort(key=lambda e: (-e["priority"], e["total"]))
    for idx, entry in enumerate(entries, start=1):
        entry["rank"] = idx
    audited = [c for c in cards if "score" in c]
    dist = {}
    for card in audited:
        g = card["score"]["grade"]
        dist[g] = dist.get(g, 0) + 1
    totals = [c["score"]["total"] for c in audited]
    return {
        "schema": SCHEMA_BATCH,
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "tool": {"name": "skill_audit.py", "version": TOOL_VERSION, "profile": profile},
        "root": root_abs,
        "count": len(md_files),
        "summary": {
            "audited": len(audited),
            "grade_distribution": dist,
            "mean": round(sum(totals) / len(totals), 1) if totals else 0,
            "min": min(totals) if totals else 0,
            "veto_count": sum(1 for c in audited if c["score"]["veto"]),
        },
        "queue": entries,
        "cards": [{k: c.get(k) for k in ("schema", "rel_path", "skill", "score",
                                         "size", "frontmatter", "findings")}
                  for c in cards],
    }


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------
def main(argv):
    parser = argparse.ArgumentParser(
        description="Audit one SKILL.md (or a whole library) and print a JSON scorecard.")
    parser.add_argument("target", nargs="?", help="skill directory or SKILL.md path")
    parser.add_argument("--scan", metavar="ROOT", help="audit every SKILL.md under ROOT")
    parser.add_argument("--depth", type=int, default=3,
                        help="max directory depth for --scan (default 3)")
    parser.add_argument("--profile", choices=("house", "generic"), default="house",
                        help="frontmatter profile to validate (default house)")
    parser.add_argument("--impact", type=int, choices=(1, 2, 3), default=2,
                        help="impact factor for the batch priority formula (default 2)")
    parser.add_argument("--json", metavar="PATH", help="also write the JSON document here")
    parser.add_argument("--fail-under", type=float, default=0.0,
                        help="exit 1 when the total score is below this value")
    args = parser.parse_args(argv)

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if args.scan:
        doc = audit_batch(args.scan, args.profile, args.depth, args.impact)
        total = doc["summary"]["mean"]
    else:
        if not args.target:
            print(json.dumps({"error": "usage", "detail": "give a skill dir, a SKILL.md, or --scan ROOT"},
                             ensure_ascii=False))
            return 2
        target = args.target
        if os.path.isdir(target):
            candidate = os.path.join(target, "SKILL.md")
        else:
            candidate = target
        if not os.path.isfile(candidate):
            print(json.dumps({"error": "not-found", "detail": candidate}, ensure_ascii=False))
            return 2
        doc = audit_one(candidate, profile=args.profile)
        total = doc["score"]["total"]

    payload = json.dumps(doc, ensure_ascii=False, indent=2)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(payload + "\n")
    print(payload)
    return 0 if total >= args.fail_under else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
