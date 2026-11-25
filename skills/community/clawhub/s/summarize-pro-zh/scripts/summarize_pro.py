#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""summarize-pro 本地工具链（零依赖、纯标准库、不联网）。

它做三件事，且只做这三件事：
  1. extract    把 txt/md/docx 读成纯文本，抽取可核验的事实线索（日期/数字/人名/待办句/决策句/条件句），
                并按指定的格式族生成「骨架」Markdown。不做语义总结 —— 那是 Agent 的工作。
  2. citecheck  把一份「输出」逐句抽事实 token，回原文比对，列出无法溯源的清单。
                这是把「忠实性纪律」从口号变成可跑断言的核心。
  3. selfcheck  检查一份输出是否满足格式族的机器可判要素（如纪要必须有待办区且含责任人或期限列）。

错误码（固定，便于上层脚本判断）：
  S001 输入文件不存在   S002 编码不可读   S003 内容为空
  S004 未知输出格式     S005 输出目录不可写 S006 原文过短（<50 字，按边界规则不套格式族）

退出码：0 成功；1 业务失败（带错误码）；2 参数错误。

用法：
  python summarize_pro.py extract  --file demo/sample_transcript.md --format minutes --out demo_out
  python summarize_pro.py citecheck --file demo_out/sample_transcript.minutes.md --source demo/sample_transcript.md
  python summarize_pro.py selfcheck --file demo_out/sample_transcript.minutes.md --format minutes
  （任意子命令加 --json 输出机读结果，字段固定 ok/error_id/data）
"""
import argparse
import json
import os
import re
import sys
import zipfile

FORMATS = ("minutes", "compare", "timeline", "bullets", "card")

# ---------- 事实抽取规则（全部可解释、可复核） ----------
DATE_PATTERNS = [
    r"\d{4}-\d{2}-\d{2}",
    r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*[日号]",
    r"\d{4}\s*年\s*\d{1,2}\s*月",
    r"\d{1,2}\s*月\s*\d{1,2}\s*[日号]",
    r"\d{1,2}\s*月",
]
NUM_PATTERN = r"(?<![\w-])\d+(?:\.\d+)?(?:%|％|万|亿|元|美元|人|天|小时|分钟|个|份|页|条|台|次|版)?"
NEGOTIABLE = re.compile(r"要|需|必须|应当|负责|跟进|截止|前完成|待办|下一步|行动项|TODO"
                        r"|出初稿|由我|我来|我来发|我发|我写|我出|我看看|回头说|再说"
                        r"|跟.{0,8}对接|对接|谁去|下次会|挂到")
DECISION = re.compile(r"决定|确定|定了|结论|批准|同意|一致认为|拍板|裁定"
                      r"|改为|改到|写死|定为|释放|退回|不做|只做|先行|定\s*\d"
                      r"|建议|提议|暂定|暂时|先按|初步|可以考虑")
CONDITION = re.compile(r"如果|若|一旦|在.{0,12}条件下|以.{0,12}为前提|前提是|除非")
SPEAKER = re.compile(r"^\s*([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9·\.\-_]{1,11})\s*[:：]\s*")
SPK_INLINE = re.compile(r"([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9·\.\-_]{1,7})[：:]")
NO_NAME = {"结论", "决定", "备注", "议题", "待办", "注意", "说明", "要点", "时间", "地点",
           "参会", "记录", "摘要", "原则", "口径", "结果", "问题", "原因", "方案", "风险",
           "下一步", "决议", "行动", "建议", "分工", "目标", "背景", "现状", "进展", "遗留",
           "主题", "事项", "会议", "内容", "目的", "范围", "版本", "日期", "负责人"}


def is_name(word):
    return bool(word) and word not in NO_NAME
OWNER_HINT = re.compile(r"([\u4e00-\u9fa5]{2,3}|[A-Z][a-z]{2,15})\s*(负责|跟进|来|牵头|owner)", re.I)


def log(msg):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(msg)


def die(code, msg, as_json=False):
    if as_json:
        log(json.dumps({"ok": False, "error_id": code, "error_msg": msg, "data": None},
                       ensure_ascii=False))
    else:
        log("[%s] %s" % (code, msg))
    sys.exit(1)


def read_any(path):
    """读 txt / md / docx（docx 用 zipfile + 正则取段落，不依赖 python-docx）。"""
    if not os.path.isfile(path):
        die("S001", "文件不存在：%s" % path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
        except Exception as e:
            die("S002", "docx 解析失败：%s" % e)
        paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
        lines = []
        for p in paras:
            txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
            lines.append(txt)
        text = "\n".join(lines)
    elif ext in (".txt", ".md", ".markdown"):
        raw = open(path, "rb").read()
        text = None
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            die("S002", "编码无法识别（试过 utf-8/gbk/gb18030）")
    else:
        die("S004", "不支持的输入格式：%s（支持 .txt/.md/.docx）" % ext)
    if not text.strip():
        die("S003", "内容为空")
    return text


def sentences(text):
    """按中文标点/换行切句，保留原始顺序（用于逐句溯源）。"""
    parts = re.split(r"(?<=[。！？；\n])", text)
    return [p.strip() for p in parts if p and p.strip()]


def find_all(pattern, text):
    return [m.group(0) for m in re.finditer(pattern, text)]


def speaker_sentences(text):
    """返回 (说话人, 句子) 列表。说话人可出现在行首或句中「X：」，非人名词一律排除。
    Markdown 标题行不计入句子流（否则「# 需求评审会转写」会被当成待办）。"""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        pos, cur = 0, None
        for m in SPK_INLINE.finditer(line):
            if not is_name(m.group(1)):
                continue
            seg = line[pos:m.start()].strip()
            if seg:
                for s in sentences(seg):
                    out.append((cur, s))
            cur = m.group(1)
            pos = m.end()
        seg = line[pos:].strip()
        if seg:
            for s in sentences(seg):
                out.append((cur, s))
    return out


def extract_facts(text):
    dates, nums, speakers = [], [], []
    for p in DATE_PATTERNS:
        dates += find_all(p, text)
    nums = find_all(NUM_PATTERN, text)
    for line in text.splitlines():
        m = SPEAKER.match(line)
        if m and is_name(m.group(1)):
            speakers.append(m.group(1))
    todos, decisions, conditions, owners = [], [], [], []
    SELF_CLAIM = re.compile(r"我来|我负责|我跟|由我|我出|我发|我接")
    for who, s in speaker_sentences(text):
        is_cond = bool(CONDITION.search(s))
        is_dec = bool(DECISION.search(s))
        if is_cond:
            conditions.append(s)
        if is_cond and not is_dec:
            # 条件句只归入「条件」区，不列成待办：把「如果超过 2% 就要回滚」列成任务会误导执行
            pass
        elif NEGOTIABLE.search(s) and not is_dec:
            # 已定结论不再重复列入待办表，避免同一句既当结论又当任务
            todos.append(s)
        if is_dec:
            decisions.append(s)
        for m in OWNER_HINT.finditer(s):
            if is_name(m.group(1)):
                owners.append(m.group(1))
        if who and SELF_CLAIM.search(s):
            owners.append(who)
    def uniq(seq):
        seen, out = set(), []
        for x in seq:
            if x and x not in seen:
                seen.add(x)
                out.append(x)
        return out
    decisions_graded = grade_decisions(decisions)
    commitments_graded = grade_commitments(todos)
    return {
        "chars": len(text),
        "lines": len([l for l in text.splitlines() if l.strip()]),
        "dates": uniq(dates),
        "numbers": uniq(nums),
        "speakers": uniq(speakers),
        "owners_hint": uniq(owners),
        "todo_sentences": uniq(todos),
        "decision_sentences": uniq(decisions),
        "condition_sentences": uniq(conditions),
        "decision_items": decisions_graded,
        "commitment_items": commitments_graded,
        "strength_summary": summarize_strength(decisions_graded, commitments_graded),
    }


# --- 结论强度 / 承诺强度分级（语义维度，可断言） ---
DECISION_FIRM = re.compile(r"决定|确定|定了|拍板|批准|同意|裁定|通过|结论是|已经定")
DECISION_PROVISIONAL = re.compile(r"暂定|暂时|临时|先按|初步|暂以|先这么")
DECISION_PROPOSAL = re.compile(r"建议|提议|可以考虑|要不|是不是可以|倾向")
DECISION_CONDITIONAL = re.compile(r"如果|若|一旦|前提是|除非|在.{0,12}条件下")

COMMIT_COMMITTED = re.compile(r"我来|我负责|我跟|由我|我出|我发|我接|我盯|交给我|我这边"
                              r"|由[\u4e00-\u9fa5A-Za-z]{1,8}(出|写|发|做|负责|跟进|主导)")
COMMIT_NAMED = re.compile(r"跟一下|对接|谁去|让.{1,8}来|需要.{1,8}确认|由.{1,8}负责|请.{1,8}支持")
COMMIT_INTENT = re.compile(r"我看看|我考虑|想想|再看|回头说|再说|有时间|尽量")


def grade_decisions(sentences):
    """把决策句分成四档：conditional > provisional > proposal > firm（按语义特异性）"""
    out = []
    for s in sentences:
        if DECISION_CONDITIONAL.search(s):
            level, why = "conditional", "含条件触发词"
        elif DECISION_PROVISIONAL.search(s):
            level, why = "provisional", "含暂定/临时/先按"
        elif DECISION_PROPOSAL.search(s):
            level, why = "proposal", "含建议/提议/可以考虑"
        else:
            level, why = "firm", "含决定/确定/拍板/批准"
        out.append({"text": s, "strength": level, "evidence": why})
    return out


def grade_commitments(sentences):
    """把待办句分成三档：intent_only > named_unconfirmed > committed"""
    out = []
    for s in sentences:
        if COMMIT_INTENT.search(s) and not COMMIT_COMMITTED.search(s):
            level, why = "intent_only", "仅表达意向（我看看/再说/尽量）"
        elif COMMIT_COMMITTED.search(s):
            level, why = "committed", "明确接活（我来/我负责/由我）"
        elif COMMIT_NAMED.search(s):
            level, why = "named_unconfirmed", "被点名但未明确确认"
        else:
            level, why = "unstated", "未标出责任人"
        out.append({"text": s, "strength": level, "evidence": why})
    return out


def summarize_strength(decisions, commitments):
    d, c = {}, {}
    for it in decisions:
        d[it["strength"]] = d.get(it["strength"], 0) + 1
    for it in commitments:
        c[it["strength"]] = c.get(it["strength"], 0) + 1
    firm = d.get("firm", 0)
    soft = d.get("provisional", 0) + d.get("proposal", 0) + d.get("conditional", 0)
    commit = c.get("committed", 0)
    unconfirmed = c.get("named_unconfirmed", 0) + c.get("intent_only", 0) + c.get("unstated", 0)
    return {
        "decisions": d,
        "commitments": c,
        "firm_decisions": firm,
        "soft_decisions": soft,
        "committed_owners": commit,
        "unconfirmed_owners": unconfirmed,
        "verdict": "clean" if (soft == 0 and unconfirmed == 0) else "needs_confirmation",
    }


SKELETONS = {
    "minutes": """# 纪要骨架（待填）

> 一句话总览：___

## 议题
{topics}

## 结论
{decisions}

## 待办
| 事项 | 责任人 | 期限 |
|---|---|---|
{todos}

## 强度判读
{strength_box}

## 待确认 / 原文未提及
{unknown}
""",
    "compare": """# 对比骨架（待填）

> 一句话总览：___

| 维度 | 对象 A | 对象 B |
|---|---|---|
| ___ | ___ | ___ |

> 只放原文事实，不写原文没有的优劣判断。
""",
    "timeline": """# 时间线骨架（待填）

{items}
""",
    "bullets": """# 要点骨架（待填）

{items}
""",
    "card": """# 卡片骨架（待填）

- 标题：___
- 一句话结论：___
- 关键字段 1：___
- 关键字段 2：___
- 关键字段 3：___
""",
}


def build_skeleton(fmt, facts):
    if fmt == "minutes":
        topics = "\n".join("- (待填) %s" % s[:40] for s in facts["speakers"][:6]) or "- (待填)"
        dec = "\n".join("- [%s] %s" % (it["strength"], it["text"])
                        for it in facts["decision_items"][:8]) or "- 原文未提及"
        todo = "\n".join("| [%s] %s | %s | %s |" % (it["strength"], it["text"][:56], "待填", "原文未提及")
                         for it in facts["commitment_items"][:10]) or "| 原文未提及 | - | - |"
        ss = facts["strength_summary"]
        box = "\n".join([
            "- 已定（firm）%d 条；暂定/提案/条件（soft）%d 条" % (ss["firm_decisions"], ss["soft_decisions"]),
            "- 明确接活（committed）%d 条；被点名未确认或仅表意向 %d 条" % (ss["committed_owners"], ss["unconfirmed_owners"]),
            "- 判读：%s" % ("全部为已定且责任明确" if ss["verdict"] == "clean"
                          else "存在未定项或未确认责任，需在会后确认后再对外发布"),
        ])
        unknown = "- 责任人/期限未在原文出现的，已标「原文未提及」，不补全"
        return SKELETONS[fmt].format(topics=topics, decisions=dec, todos=todo,
                                     strength_box=box, unknown=unknown)
    if fmt == "timeline":
        items = "\n".join("%d. %s（日期待核对）" % (i + 1, d) for i, d in enumerate(facts["dates"][:12]))
        return SKELETONS[fmt].format(items=items or "1. (待填)")
    if fmt == "bullets":
        items = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(facts["decision_sentences"][:5]))
        if not items:
            items = "\n".join("%d. %s" % (i + 1, s[:80]) for i, s in enumerate(facts["todo_sentences"][:5]))
        return SKELETONS[fmt].format(items=items or "1. (待填)")
    return SKELETONS[fmt]


# ---------- 溯源校验 ----------
def fact_tokens(text):
    toks = []
    for p in DATE_PATTERNS:
        toks += find_all(p, text)
    toks += [n for n in find_all(NUM_PATTERN, text) if len(n) >= 2]
    return toks


def norm(t):
    """只归一化格式差异（空白、日期「日/号」写法），不做任何数值或语义归一。"""
    return re.sub(r"\s+", "", t).replace("日", "号")


def citecheck(output_text, source_text):
    src_norm = norm(source_text)
    missing = []
    checked = 0
    for s in sentences(output_text):
        if re.match(r"^\|[\s:\-|]+\|$", s):
            continue
        toks = fact_tokens(s)
        for t in toks:
            checked += 1
            if norm(t) not in src_norm:
                missing.append({"token": t, "sentence": s[:90]})
    return {"checked": checked, "missing": missing,
            "verdict": "PASS" if not missing else "FAIL"}


# ---------- 结构自检 ----------
def selfcheck(output_text, fmt):
    problems = []
    if fmt == "minutes":
        for need in ("## 议题", "## 结论", "## 待办", "## 待确认", "## 强度判读"):
            if need not in output_text:
                problems.append("缺少区块 %s" % need)
        if "| 事项 | 责任人 | 期限 |" not in output_text:
            problems.append("待办表缺表头（应为 事项/责任人/期限）")
        # 强度标注是 v2.0.2 起的强制项：结论与待办都必须带语义档位
        # （区块内确无内容、已标「原文未提及」时不强制，避免对空结论误报）
        dec_block = output_text.split("## 结论", 1)[-1].split("## 待办", 1)[0]
        if "原文未提及" not in dec_block and not re.search(
                r"\[(firm|provisional|proposal|conditional)\]", dec_block):
            problems.append("结论未标注语义档位（firm/provisional/proposal/conditional）")
        todo_block = output_text.split("## 待办", 1)[-1].split("## 强度判读", 1)[0]
        if "原文未提及" not in todo_block and not re.search(
                r"\[(committed|named_unconfirmed|intent_only|unstated)\]", todo_block):
            problems.append("待办未标注承诺状态（committed/named_unconfirmed/intent_only）")
    elif fmt == "compare":
        if output_text.count("|") < 4:
            problems.append("对比表结构不完整（需维度×对象两列以上）")
    elif fmt == "timeline":
        if not re.search(r"^\d+\.\s", output_text, re.M):
            problems.append("时间线需一行一事（数字编号行）")
    elif fmt == "bullets":
        n = len(re.findall(r"^\d+\.\s", output_text, re.M))
        if not (3 <= n <= 7):
            problems.append("要点族要求 3–7 条，实测 %d 条" % n)
    elif fmt == "card":
        for need in ("标题", "一句话结论"):
            if need not in output_text:
                problems.append("卡片缺字段：%s" % need)
    return {"verdict": "PASS" if not problems else "FAIL", "problems": problems}


def main():
    ap = argparse.ArgumentParser(description="summarize-pro 本地工具链（零依赖）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="抽取事实线索并生成骨架")
    e.add_argument("--file", required=True)
    e.add_argument("--format", default="minutes", choices=FORMATS)
    e.add_argument("--out", default=".")
    e.add_argument("--json", action="store_true")

    c = sub.add_parser("citecheck", help="输出逐句回原文溯源")
    c.add_argument("--file", required=True, help="待核对输出")
    c.add_argument("--source", required=True, help="原文")
    c.add_argument("--json", action="store_true")

    s = sub.add_parser("selfcheck", help="格式族结构自检")
    s.add_argument("--file", required=True)
    s.add_argument("--format", default="minutes", choices=FORMATS)
    s.add_argument("--json", action="store_true")

    a = ap.parse_args()
    as_json = getattr(a, "json", False)

    if a.cmd == "extract":
        text = read_any(a.file)
        if len(text.strip()) < 50:
            die("S006", "原文仅 %d 字，按边界规则不套格式族（请直接一句话总览）" % len(text.strip()), as_json)
        facts = extract_facts(text)
        body = build_skeleton(a.format, facts)
        try:
            os.makedirs(a.out, exist_ok=True)
            stem = os.path.splitext(os.path.basename(a.file))[0]
            md_path = os.path.join(a.out, "%s.%s.md" % (stem, a.format))
            json_path = os.path.join(a.out, "%s.facts.json" % stem)
            open(md_path, "w", encoding="utf-8").write(body)
            open(json_path, "w", encoding="utf-8").write(
                json.dumps(facts, ensure_ascii=False, indent=1))
        except OSError as ex:
            die("S005", "输出目录不可写：%s" % ex, as_json)
        data = {"format": a.format, "chars": facts["chars"],
                "dates": len(facts["dates"]), "numbers": len(facts["numbers"]),
                "speakers": len(facts["speakers"]),
                "todo_sentences": len(facts["todo_sentences"]),
                "decision_sentences": len(facts["decision_sentences"]),
                "out_md": md_path, "out_json": json_path}
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": data}, ensure_ascii=False))
        else:
            log("已生成 %s\n事实线索：日期 %d / 数字 %d / 说话人 %d / 待办句 %d / 决策句 %d"
                % (md_path, data["dates"], data["numbers"], data["speakers"],
                   data["todo_sentences"], data["decision_sentences"]))
            log("说明：本工具只做抽取与骨架，语义总结由 Agent 完成。")

    elif a.cmd == "citecheck":
        out_text = read_any(a.file)
        src_text = read_any(a.source)
        r = citecheck(out_text, src_text)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": r}, ensure_ascii=False))
        else:
            log("核对事实 token：%d 个；不可溯源：%d 个；判定：%s"
                % (r["checked"], len(r["missing"]), r["verdict"]))
            for m in r["missing"][:20]:
                log("  ✗ %s  ←  %s" % (m["token"], m["sentence"]))
        sys.exit(0 if r["verdict"] == "PASS" else 1)

    else:
        out_text = read_any(a.file)
        r = selfcheck(out_text, a.format)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": r}, ensure_ascii=False))
        else:
            log("结构自检（%s）：%s" % (a.format, r["verdict"]))
            for p in r["problems"]:
                log("  ✗ %s" % p)
        sys.exit(0 if r["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
