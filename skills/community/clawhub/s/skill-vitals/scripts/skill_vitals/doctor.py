"""Doctor diagnostics and terminal renderer."""

import json
from pathlib import Path

from . import __version__
from .lifecycle import (
    DEFAULT_DORMANT_DAYS,
    ZOMBIE_MIN_AGE_DAYS,
    human_last_used,
    human_tokens,
    lifecycle_status,
)
from .overlap import DEFAULT_OVERLAP_MIN, overlap_pairs
from .snapshots import save_snapshot
from .util import run_id

# ── doctor：诊断（PRODUCT §5.1、ARCHITECTURE §5）────────────
#
# 这一层做的是 **事实 → 原因 → 影响 → 行动**，扫描器只负责事实。
# 它**不重新测量任何东西**：所有数字都从 out 里取，否则同一个数会有两个
# 来源，而两个来源迟早会给出两个答案。

SEVERITY_RANK = {"critical": 0, "warning": 1, "info": 2}
SEVERITY_GLYPH = {"critical": "✕", "warning": "⚠", "info": "·"}

# 安全规则名 → 诊断码。**必须覆盖 SECURITY_PATTERNS 的每一条**：
# 扫描器里有、这张表里没有的规则会在 doctor 里**静默消失** —— 一条命中
# 了却不出现在诊断里的规则，比没有这条规则更糟。
# `test_doctor.py::TestEverySecurityRuleHasACode` 钉住这个全覆盖。
SECURITY_CODES = {
    "adversarial_instruction": ("SV501", "PROMPT_INJECTION_PATTERN"),
    "pipe_to_shell": ("SV502", "PIPE_TO_SHELL"),
    "base64_exec": ("SV503", "BASE64_EXEC"),
    "raw_ip_fetch": ("SV504", "RAW_IP_FETCH"),
    "hardcoded_secret": ("SV505", "HARDCODED_SECRET"),
    "credential_env_read": ("SV506", "CREDENTIAL_READ"),
    "obfuscated_exec": ("SV507", "OBFUSCATED_EXEC"),
    "password_archive": ("SV508", "PASSWORD_PROTECTED_ARCHIVE"),
}

# 安全命中的原始严重度 → 诊断严重度。
# critical 保持 critical；high/medium 都是 warning（「会造成损害」）。
# **info 不用于安全**：info 的定义是「仅供参考」，而任何一条安全命中都
# 需要人打开看一眼。
SECURITY_SEVERITY = {"critical": "critical", "high": "warning", "medium": "warning"}

# 本次**不评估**的诊断码，以及为什么。
#
# 这张表要打印出来。少一条诊断而不说，读者会把「没报」读成「没有」——
# 与 §7.2「缺一列的报告有价值，编一列的没有」是同一条规矩：缺的那一列
# 必须自报家门。
NOT_ASSESSED = [
    ("SV003", "DESCRIPTION_TOO_LONG", "There is no defensible threshold. What counts as long depends "
                                      "on the host and total skill count."),
    ("SV104", "PLUGIN_NOT_ENABLED", "A disabled plugin is normal, not a defect; it is counted under not loaded."),
    ("SV203", "ORPHANED_USAGE_RECORD", "Renaming breaks trigger history and cannot be distinguished from deletion "
                                       "(open PRODUCT §10 question)."),
    ("SV302", "HIGH_METADATA_COST", "Same as SV003: no defensible threshold."),
    ("SV402", "OVERLAP_CONFIRMED", "Requires an in-host or --judge semantic decision; not implemented yet."),
]


def _diag(code, name, severity, impact, recommendation, caveats,
          skill=None, evidence=None):
    """`caveats` 是**必填**的位置参数，不是可选项（ARCHITECTURE §5.1）。

    带已知系统性偏差的诊断，偏差必须与结论同屏；写成 `caveats=None` 默认值
    的话，忘记填就等于偏差消失了。没有 caveat 就显式传 `[]`。
    """
    return {"code": code, "name": name, "severity": severity, "skill": skill,
            "evidence": evidence or {}, "impact": impact,
            "recommendation": recommendation, "caveats": caveats}


def diagnose(out, split_threshold, overlap_min=DEFAULT_OVERLAP_MIN):
    """把扫描输出翻成诊断列表。纯函数：只读 out，不碰文件系统。"""
    ds = []
    skills = out.get("skills", [])
    loaded = [s for s in skills if s.get("loaded")]
    b = out.get("description_budget", {}) or {}
    t = out.get("trigger_data", {}) or {}
    trig = bool(t.get("available"))

    # ── 预算 ──────────────────────────────────────────────
    budget_caveats = [c for c in (b.get("note"), ) if c]
    if b.get("excludes_builtin_skills"):
        budget_caveats.append("This number excludes built-in skills bundled in the CLI without a SKILL.md on disk; "
                              "actual usage is higher.")
    if b.get("available"):
        if (b.get("over_by_chars") or 0) > 0:
            ds.append(_diag(
                "SV002", "DESCRIPTION_BUDGET_OVERFLOW", "critical",
                "The description budget is exceeded; some skills may be silently omitted without an error.",
                (("Immediate workaround: %s. " % b["workaround"]) if b.get("workaround") else "") +
                "Durable fix: shorten the longest descriptions or disable unneeded skills.",
                budget_caveats,
                evidence={"used_chars": b.get("used_chars"),
                          "budget_chars": b.get("budget_chars"),
                          "over_by_chars": b.get("over_by_chars"),
                          "scope": b.get("scope"),
                          "counted_skills": b.get("counted_skills"),
                          "skills_possibly_dropped": b.get("skills_possibly_dropped"),
                          "longest_descriptions": b.get("longest_descriptions", [])}))
        elif (b.get("pct_used") or 0) >= 85:
            ds.append(_diag(
                "SV001", "DESCRIPTION_BUDGET_WARNING", "warning",
                "The description budget is %.1f%% used and close to overflowing." % b["pct_used"],
                "Shorten the longest descriptions now, before troubleshooting an overflow.",
                budget_caveats,
                evidence={"used_chars": b.get("used_chars"),
                          "budget_chars": b.get("budget_chars"),
                          "pct_used": b.get("pct_used"),
                          "longest_descriptions": b.get("longest_descriptions", [])}))

    # ── 覆盖 ──────────────────────────────────────────────
    kinds = {
        "shadowed_newer": ("SV101", "SKILL_SHADOWED_NEWER", "critical",
                           "The copy you edited is not effective: the shadowed copy is newer than the active copy.",
                           "Move the change to the effective copy or remove the obsolete duplicate."),
        "intentional_override": ("SV103", "SKILL_SHADOWED_OVERRIDE", "warning",
                                 "Multiple copies share the same name; the higher-priority newer copy is effective.",
                                 "Confirm that this override is intentional; otherwise remove the extra copy."),
        "redundant": ("SV102", "SKILL_SHADOWED_REDUNDANT", "info",
                      "Multiple same-named copies have identical content and are redundant.",
                      "Remove any redundant copy without changing behavior."),
    }
    by_kind = {}
    for c in out.get("conflicts", []):
        by_kind.setdefault(c["kind"], []).append(c)
    for kind, (code, name, sev, impact, rec) in kinds.items():
        hits = by_kind.get(kind, [])
        if not hits:
            continue
        ds.append(_diag(code, name, sev, impact, rec,
                        [out.get("precedence_note")] if out.get("precedence_note") else [],
                        evidence={"count": len(hits), "conflicts": hits}))

    # ── frontmatter ──────────────────────────────────────
    missing = (out.get("structure", {}) or {}).get("missing_frontmatter", [])
    if missing:
        ds.append(_diag(
            "SV105", "INVALID_FRONTMATTER", "warning",
            "A skill missing name or description cannot be selected reliably.",
            "Add name and description to its frontmatter.",
            [], evidence={"count": len(missing), "skills": missing}))

    # ── 使用 ──────────────────────────────────────────────
    # **零触发的前提是「问得到」**。没有触发数据时这一整段不出现，
    # 而不是出现一个「0 个僵尸」—— 后者读起来像「查过了，很健康」。
    if trig:
        zc = t.get("zombie_candidates", [])
        too_new = t.get("too_new_to_judge", [])
        if zc:
            ds.append(_diag(
                "SV201", "ZERO_TRIGGER", "warning",
                "%d skills are at least %d days old and have zero lifetime triggers, consuming budget and startup context."
                % (len(zc), t.get("zombie_min_age_days")),
                "Use explain to see why each skill was not selected; disable it only after confirming it is unnecessary. "
                "This tool never deletes anything automatically.",
                ["Trigger counts are lifetime totals, not a rolling 30-day window.",
                 "Zero triggers can also mean budget pressure or poor selection; those are SV002 / SV401 issues, "
                 "not proof that a skill should be removed."] +
                (["Another %d skills are younger than %d days and are not judged due to insufficient evidence."
                  % (len(too_new), t.get("zombie_min_age_days"))] if too_new else []),
                evidence={"count": len(zc), "too_new_count": len(too_new),
                          "zombie_min_age_days": t.get("zombie_min_age_days"),
                          "skills": zc}))
        dormant = [s for s in loaded
                   if lifecycle_status(s, True, t.get("zombie_min_age_days",
                                                      ZOMBIE_MIN_AGE_DAYS)) == "dormant"]
        if dormant:
            dormant.sort(key=lambda s: -(s.get("last_used_days_ago") or 0))
            ds.append(_diag(
                "SV202", "DORMANT_SKILL", "warning",
                "%d skills were used before but have not triggered for more than %d days."
                % (len(dormant), DEFAULT_DORMANT_DAYS),
                "Prior use is evidence of value; check whether a newer skill is competing before removing it.",
                ["Dormant means not used recently. Seasonal tasks such as tax filing or releases can appear here normally."],
                evidence={"count": len(dormant), "dormant_days": DEFAULT_DORMANT_DAYS,
                          "skills": [{"name": s["name"],
                                      "last_used_days_ago": s.get("last_used_days_ago"),
                                      "usage_count": s.get("usage_count")}
                                     for s in dormant]}))

    # ── 成本 ──────────────────────────────────────────────
    oversized = (out.get("structure", {}) or {}).get("oversized", [])
    if oversized:
        ds.append(_diag(
            "SV301", "HIGH_TRIGGER_COST", "warning",
            "%d skills have SKILL.md bodies over %d tokens; this core is loaded on every trigger."
            % (len(oversized), split_threshold),
            "Move on-demand material to references/ and keep only the decision path in the core body.",
            ["The criterion is tier2_core_tokens, not line count; density can vary by more than 4x.",
             "Splitting lowers average core cost and can increase worst-case max cost; name the metric that improved."],
            evidence={"count": len(oversized),
                      "split_threshold_tokens": split_threshold,
                      "skills": oversized}))
        # 又大又没人用 —— 两个信号叠加才值得单独提一条
        if trig:
            zombie_names = {z["name"] for z in t.get("zombie_candidates", [])}
            both = [o for o in oversized if o["name"] in zombie_names]
            if both:
                ds.append(_diag(
                    "SV303", "EXPENSIVE_AND_UNUSED", "warning",
                    "%d skills exceed the split threshold and have zero lifetime triggers." % len(both),
                    "Review these first because they have the weakest measured cost-to-use ratio.",
                    ["As with SV201, zero triggers do not prove uselessness; the skill may never have been selected."],
                    evidence={"count": len(both), "skills": both}))

    # ── 路由 ──────────────────────────────────────────────
    pairs = overlap_pairs(out, overlap_min)
    if pairs:
        ds.append(_diag(
            "SV401", "OVERLAP_CANDIDATE", "warning",
            "%d skill pairs have highly overlapping wording and may compete for the same requests." % len(pairs),
            "Run `skill-vitals overlap` to inspect shared terms; for an actionable judgment, run /skill-vitals "
            "in Claude Code and let the model read the descriptions.",
            ["This is a lexical filter, not a verdict. Skills with different wording can still compete, "
             "so false negatives are more common than false positives."],
            evidence={"count": len(pairs), "min_jaccard": overlap_min,
                      "pairs": pairs[:10]}))

    # ── 安全 ──────────────────────────────────────────────
    # 按诊断码聚合，而不是按 skill：读者要的是「有没有 pipe_to_shell」，
    # 每一条命中都带 skill + 文件 + 行号，因为**打开那一行看一眼才是防线**。
    hits_by_code = {}
    for s in (out.get("security", {}) or {}).get("flagged", []):
        for f in s.get("findings", []):
            code, cname = SECURITY_CODES.get(
                f.get("rule"), ("SV500", "UNMAPPED_SECURITY_RULE"))
            hits_by_code.setdefault((code, cname), []).append(
                {"skill": s["name"], "path": s.get("path"), "loaded": s.get("loaded"),
                 "rule": f.get("rule"), "severity": f.get("severity"),
                 "cited": f.get("cited"), "where": f.get("where"), "line": f.get("line"),
                 "match": f.get("match")})
    for (code, cname), hits in sorted(hits_by_code.items()):
        worst = min((h["severity"] for h in hits),
                    key=lambda x: ("critical", "high", "medium").index(x)
                    if x in ("critical", "high", "medium") else 9)
        # cited 那段解释**只在真有 cited 命中时**出现。一段完全相同的三行
        # 说明在报告里重复五遍，读者会开始跳过它 —— 而它恰恰是不该被跳过的
        # 那一段。让它出现得少一点，是为了让它出现时还有人读。
        caveats = ["Heuristic rules: a match does not prove malware, and no match does not prove safety."]
        if any(h["cited"] for h in hits):
            caveats.append(
                "Findings marked as citation-like context are only sorted differently; severity is not reduced and "
                "reporting is not suppressed. 'For example,' or an unmatched quote can fool this hint, so it is not a safety verdict.")
        ds.append(_diag(
            code, cname, SECURITY_SEVERITY.get(worst, "warning"),
            "%d findings (highest severity: %s)." % (len(hits), worst),
            "Open every reported line and review it manually.",
            caveats,
            evidence={"count": len(hits), "hits": hits[:20]}))

    # ── 宿主能力 ──────────────────────────────────────────
    lacking = []
    if not b.get("available"):
        lacking.append("description budget")
    if not trig:
        lacking.append("trigger data")
    if not (out.get("plugin_state", {}) or {}).get("host_config_read"):
        lacking.append("load-state evidence")
    if lacking:
        ds.append(_diag(
            "SV901", "CAPABILITY_UNAVAILABLE", "info",
            "This host does not provide: %s. Related judgments are omitted rather than treated as zero." % ", ".join(lacking),
            "Only Claude Code provides these fields through ~/.claude.json; their absence on another host is not a failure.",
            ["Unavailable is not zero. Rendering the former as the latter would turn an unmeasured value into a decision."],
            evidence={"unavailable": lacking, "host_selection": out.get("host_selection")}))

    unreadable = out.get("unreadable_skills", [])
    if unreadable:
        ds.append(_diag(
            "SV902", "SKILL_UNREADABLE", "warning",
            "%d SKILL.md files are unreadable and are excluded from all statistics above." % len(unreadable),
            "Check permissions and encoding; the inventory is incomplete until these files can be read.",
            ["This directly affects the denominators for budget, conflict, and zombie analysis."],
            evidence={"count": len(unreadable), "skills": unreadable[:20]}))

    ds.sort(key=lambda d: (SEVERITY_RANK[d["severity"]], d["code"]))
    return ds


# 终端折行宽度。**按显示列宽折，不按字符数。**
#
# 表格那边（render_list 的 pad）刻意按**字符数**对齐，因为两个实现的格式化
# 原语都按字符计，字符计才能让输出逐字节一致。但整段中文说明按字符折的话，
# 一行 75 个汉字会铺开 150 列 —— caveat 是最需要被读到的那几行，不能糊成一片。
#
# 所以这里改用显示列宽（CJK 记 2 列），并把区间写死：两个实现用同一张表，
# 一致性照样成立，只是口径换了一个。
DOCTOR_WIDTH = 88
_WIDE_RANGES = (
    (0x1100, 0x115F), (0x2E80, 0x303E), (0x3041, 0x33FF), (0x3400, 0x4DBF),
    (0x4E00, 0x9FFF), (0xA000, 0xA4CF), (0xAC00, 0xD7A3), (0xF900, 0xFAFF),
    (0xFE30, 0xFE4F), (0xFF00, 0xFF60), (0xFFE0, 0xFFE6),
)


# 不得出现在行首的字符（中日文排版的「禁则处理」）
_NO_LINE_START = set("」』）〉》”’、。，！？：；·…—")


def _cols(text):
    """显示列宽：CJK 与全角记 2，其余记 1。"""
    n = 0
    for ch in text:
        o = ord(ch)
        n += 2 if any(lo <= o <= hi for lo, hi in _WIDE_RANGES) else 1
    return n


def _wrap(text, prefix, width=DOCTOR_WIDTH, cont=None):
    """按列宽折行；续行缩进到 `cont`（默认与 prefix 等宽）。

    编号条目要传 `cont` 比 prefix 更深的缩进，否则续行会和下一条的编号顶齐，
    读起来像多了一条没编号的建议。

    CJK 之间没有空格，textwrap 折不动 —— 一整段中文会原样吐出一行。所以这里
    自己切：英文按词切（不劈开单词），CJK 逐字切。
    """
    room = max(20, width - _cols(prefix))
    # 切成「可换行的最小单位」：一个 CJK 字，或一段非空白的 ASCII 词
    units, buf = [], ""
    for ch in text:
        o = ord(ch)
        wide = any(lo <= o <= hi for lo, hi in _WIDE_RANGES)
        if wide or ch == " ":
            if buf:
                units.append(buf)
                buf = ""
            if wide:
                units.append(ch)
            else:
                units.append(" ")
        else:
            buf += ch
    if buf:
        units.append(buf)

    lines, cur = [], ""
    for u in units:
        if u == " " and not cur:
            continue                       # 行首不留空格
        # 禁则：闭引号、句读不能落在行首。宁可多出一两列，也不要让一行以
        # 「」时 开头 —— 那读起来像上一行被截断了。
        if cur and _cols(cur) + _cols(u) > room and u not in _NO_LINE_START:
            lines.append(cur.rstrip())
            cur = "" if u == " " else u
        else:
            cur += u
    if cur.strip():
        lines.append(cur.rstrip())
    pad_cont = cont if cont is not None else " " * _cols(prefix)
    return [(prefix if i == 0 else pad_cont) + ln for i, ln in enumerate(lines)] or [prefix.rstrip()]


def _doctor_not_loaded_breakdown(skills):
    """未加载的原因分布。

    未知的 reason **原样显示**，不并进「其他」—— 新增一种加载原因时，
    它应当在报告里跳出来，而不是被一个兜底桶吸收掉。
    """
    label = {
        "plugin-not-enabled": "plugin disabled",
        "plugin-state-unknown": "plugin state unknown",
        "unknown-location": "unclassified location",
        "openclaw-config-disabled": "disabled in config",
        "openclaw-config-enabled-runtime-unverified": "runtime unverified",
        "openclaw-discoverable-runtime-unverified": "runtime unverified",
        "openclaw-cli-not-eligible": "runtime ineligible",
    }
    counts = {}
    for s in skills:
        if s.get("loaded"):
            continue
        r = s.get("loaded_reason") or "unknown"
        key = label.get(r) or (
            "mode filtered" if r.startswith("workbuddy-mode-filtered") else r)
        counts[key] = counts.get(key, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def render_doctor(out, args):
    """`doctor` 的呈现。遵守 PRODUCT §5.1 的三条渲染纪律。"""
    ds = diagnose(out, args.split_threshold, args.min)

    if args.json:
        Path(args.json).write_text(json.dumps({
            "schema_version": out.get("schema_version"),
            "run": run_id(out),
            "host_selection": out.get("host_selection"),
            "diagnostics": ds,
            "not_assessed": [{"code": c, "name": n, "reason": why}
                             for c, n, why in NOT_ASSESSED],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Wrote %s: %d diagnostics" % (args.json, len(ds)))
        return

    b = out.get("description_budget", {}) or {}
    t = out.get("trigger_data", {}) or {}
    skills = out.get("skills", [])
    loaded_n = out.get("loaded_skills", 0)

    # run 标记与版本号同行：test_doctor 断言输出以 "Skill Vitals " 开头，
    # 另起一行会把那条断言变成检查一个不再存在的位置。
    print("Skill Vitals %s · run %s" % (__version__, run_id(out)))
    print("─" * 50)
    print("Host    %s" % out.get("host_selection", "?"))
    print("        trigger data %s · load evidence %s · description budget %s" % (
        "✓" if t.get("available") else "—",
        "✓" if (out.get("plugin_state", {}) or {}).get("host_config_read") else "—",
        "✓" if b.get("available") else "—"))
    print()
    print("Skills  %d on disk → %d loaded" % (out.get("total_skills_on_disk", 0), loaded_n))
    breakdown = _doctor_not_loaded_breakdown(skills)
    if breakdown:
        print("        not loaded: %s" % " · ".join("%s %d" % kv for kv in breakdown))

    # 变化段在结论**之前**（PRODUCT §5.1）。这是 diff 进入用户路径的方式。
    d = out.get("diff_vs_baseline")
    if d and not d.get("error"):
        print()
        print("Changes since %s" % d.get("baseline_file"))
        then, now = d.get("loaded_then_now", [0, 0])
        print("  loaded %d → %d  ·  + %d skills · − %d skills" % (
            then, now, len(d.get("added_skills", [])), len(d.get("removed_skills", []))))
        pt, pn = d.get("budget_pct_then_now", [None, None])
        if pt is not None and pn is not None:
            print("  description budget  %.1f%% → %.1f%%%s" % (
                pt, pn, "  ⚠ overflow" if (b.get("over_by_chars") or 0) > 0 else ""))
        if d.get("newly_judgeable"):
            print("  %d skills crossed the age gate and are judged for the first time" %
                  len(d["newly_judgeable"]))
        if d.get("new_security_findings"):
            print("  %d new security findings" % len(d["new_security_findings"]))
    elif d and d.get("error"):
        print()
        print("Changes  %s" % d["error"])

    for sev, title in (("critical", "CRITICAL"), ("warning", "WARNING"), ("info", "INFO")):
        group = [x for x in ds if x["severity"] == sev]
        if not group:
            continue
        print()
        print("%s — %d findings" % (title, len(group)))
        for x in group:
            print()
            for line in _wrap(x["impact"], "  %s %s  " % (SEVERITY_GLYPH[sev], x["code"])):
                print(line)
            if x["skill"]:
                print("           %s" % x["skill"])
            for line in _doctor_evidence_lines(x):
                print("           %s" % line)
            for line in _wrap(x["recommendation"], "           → "):
                print(line)
            for c in x["caveats"]:
                for line in _wrap(c, "           ! "):
                    print(line)

    # 纪律 1：描述预算（chars）与启动上下文（tokens）必须**分开两段**。
    # v0.1 把它们并排，用户第一眼读成「上下文用掉 91%」—— 虚报预算危机
    # 会让人去做无用功，比不报更糟。
    print()
    print("Description budget")
    if b.get("available"):
        # 纪律 3：没超就正常报一句百分比，不渲染成问题。
        print("  %s / %s chars (%.1f%%)  ·  %s, %d skills" % (
            "{:,}".format(b["used_chars"]), "{:,}".format(b["budget_chars"]),
            b["pct_used"], b["scope"], b["counted_skills"]))
        # 纪律 2：预算数字永远与「不含内置 skill」同屏。省掉这条 caveat，
        # 结论会从高估**翻转成低估**。
        if b.get("excludes_builtin_skills"):
            print("  ! Excludes built-in skills bundled in the CLI; actual usage is higher")
        print("  ! The threshold varies by host version; override it with --budget")
    else:
        print("  Unavailable — this host does not expose it, or its config is unreadable")
        print("  ! Unavailable does not mean zero characters used")

    print()
    print("Startup context (tier1)")
    print("  approx. %s tokens  ·  approx. %.2f%% of 200k   [estimated]" % (
        "{:,}".format(out.get("tier1_total_tokens", 0)),
        out.get("tier1_pct_of_200k", 0.0)))

    sec = out.get("security", {}) or {}
    print()
    print("Security")
    if sec.get("flagged_count"):
        print("  %d skills have findings · %d critical" % (
            sec["flagged_count"], sec.get("critical_count", 0)))
        if sec.get("all_cited_count"):
            print("  %d have findings only in citation-like context (sorting hint only; review required)"
                  % sec["all_cited_count"])
    else:
        print("  No rules matched.")
    # 「绝不输出「这个 skill 是安全的」。」没有命中只说明这几条正则没匹配上。
    print("  ! Heuristic rules: a match does not prove malware, and no match does not prove safety.")

    print()
    print("Not assessed")
    for code, name, why in NOT_ASSESSED:
        for line in _wrap("%s —— %s" % (name, why), "  %s " % code):
            print(line)

    print()
    print("Next steps")
    print("  skill-vitals list                 See which skills are actually in context")
    if any(x["code"] == "SV401" for x in ds):
        print("  skill-vitals overlap              Inspect potentially competing pairs")
    print("  Run /skill-vitals in Claude Code  Let the model judge descriptions semantically")


def _doctor_snapshot(out, enabled):
    """doctor 跑完之后存一份快照，并**在写成功之后**才说自己存了。

    这句话曾经被我刻意删掉：快照没实现之前打「✓ 已保存快照 → 下次运行会
    自动对比」，是承诺一件工具做不到的事。现在它能做到了，但那条纪律不变 ——
    **写失败就不能说写成功**。只读的 home、没权限的目录都会走到这条路上。
    """
    if not enabled:
        print()
        print("  No snapshot saved. To compare before and after:")
        print("    skill-vitals snapshot   then skill-vitals diff")
        return
    try:
        path = save_snapshot(out)
    except OSError as e:
        print()
        print("  ! Could not save snapshot: %s" % e)
        print("    Automatic comparison is unavailable; you can still save one manually with --json.")
        return
    print()
    print("  ✓ Snapshot saved → the next run will compare automatically")
    print("    %s" % path)


def _doctor_evidence_lines(d):
    """每条诊断的证据行。「只从 evidence 里取，不重新算。」"""
    e = d["evidence"]
    code = d["code"]
    if code in ("SV001", "SV002"):
        lines = ["%s / %s chars (%s%%)  ·  %s, %d skills" % (
            "{:,}".format(e["used_chars"]), "{:,}".format(e["budget_chars"]),
            e.get("pct_used", round(e["used_chars"] / e["budget_chars"] * 100, 1)),
            e["scope"] if e.get("scope") else "loaded-only", e["counted_skills"])]
        if e.get("skills_possibly_dropped"):
            lines.append("Descriptions for approx. %d skills may have been silently omitted" % e["skills_possibly_dropped"])
        lines += ["Longest: %s" % ", ".join("%s %d" % (x["name"], x["chars"])
                                        for x in e.get("longest_descriptions", [])[:3])]
        return [x for x in lines if x != "Longest: "]
    if code in ("SV101", "SV102", "SV103"):
        lines = []
        for c in e["conflicts"][:5]:
            lines.append("%s" % c["name"])
            lines.append("  active    %-10s %s" % (c["effective"]["level"], c["effective"]["path"]))
            for sh in c["shadowed"]:
                lines.append("  shadowed  %-10s %s" % (sh["level"], sh["path"]))
        if e["count"] > 5:
            lines.append("… and %d more" % (e["count"] - 5))
        return lines
    if code == "SV105":
        return ["%s (name=%s description=%s)" % (
            s["name"], "✓" if s["has_name"] else "✗",
            "✓" if s["has_description"] else "✗") for s in e["skills"][:5]]
    if code in ("SV201", "SV303"):
        return ["%s  installed %.0f days  tier1 %s" % (
            s["name"], s.get("installed_days_ago") or 0,
            human_tokens(s.get("tier1_tokens"))) for s in e["skills"][:5]]
    if code == "SV202":
        return ["%s  %s  %d uses total" % (s["name"], human_last_used(s["last_used_days_ago"]),
                                      s["usage_count"]) for s in e["skills"][:5]]
    if code == "SV301":
        return ["%s  core %s / max %s  (%d lines)" % (
            s["name"], human_tokens(s["tier2_core_tokens"]),
            human_tokens(s["tier2_max_tokens"]), s["body_lines"])
            for s in e["skills"][:5]]
    if code == "SV401":
        return ["%s ↔ %s  Jaccard %.2f" % (p["a"], p["b"], p["jaccard"])
                for p in e["pairs"][:5]]
    if code.startswith("SV5"):
        # 同一个 skill 在磁盘上有多份副本时，每份都会独立命中，打印出来是
        # 「一模一样的两行」，看着像重复输出的 bug。合并成 ×N，副本数不丢。
        seen, order = {}, []
        for h in e["hits"]:
            k = (h["skill"], h["where"], h["line"], h["severity"], h["cited"])
            if k not in seen:
                seen[k] = 0
                order.append(k)
            seen[k] += 1
        return ["%s  %s:%s  %s%s%s" % (
            k[0], k[1], k[2], k[3], " (citation-like context)" if k[4] else "",
            "  ×%d copies" % seen[k] if seen[k] > 1 else "") for k in order[:5]]
    if code == "SV902":
        return [s["path"] for s in e["skills"][:5]]
    return []
