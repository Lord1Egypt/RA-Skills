"""Per-Skill explanation funnel and renderer."""

import json
import sys
import time
from pathlib import Path

from .doctor import _wrap
from .lifecycle import ZOMBIE_MIN_AGE_DAYS, human_last_used, human_tokens
from .overlap import DEFAULT_OVERLAP_MIN, overlap_pairs

# ── explain：漏斗的 UI（PRODUCT §5.3、ARCHITECTURE §1）──────
#
# 这条命令回答的不是「有没有问题」，而是**「为什么」和「所以呢」**。
# 每一段输出都必须落到一个用户能执行的动作 —— 否则它只是把 doctor 的一条
# 诊断换了个排版重说一遍。

FUNNEL_GLYPH = {"true": "✓", "false": "✕", "at_risk": "⚠", "unknown": "?", "n/a": "·"}
FUNNEL_STAGES = ("Installed", "Enabled", "Loaded", "Discoverable", "Selected", "Triggered")


def find_skills(out, target):
    """按名字找 skill。**同名多份要全部返回。**

    只返回一份的话，`explain` 就永远讲不清 shadowing —— 而那正是它最该讲
    清楚的一件事（PRODUCT §5.3 的示例通篇在讲这个）。

    匹配顺序：完整的 `<namespace>:<name>` 优先，其次裸 name。反过来的话，
    一个插件叫 `github` 而你想问的是 `gh:github`，会被裸名匹配抢先。
    """
    skills = out.get("skills", [])
    exact_ns = [s for s in skills
                if s.get("namespace") and "%s:%s" % (s["namespace"], s["name"]) == target]
    if exact_ns:
        return exact_ns
    return [s for s in skills if s["name"] == target]


def _shadow_map(out):
    """path → (那份被谁盖了的 conflict, 是不是被盖的那一方)。"""
    m = {}
    for c in out.get("conflicts", []):
        m[c["effective"]["path"]] = (c, False)
        for sh in c["shadowed"]:
            m[sh["path"]] = (c, True)
    return m


def _enabled_stage(s):
    """Enabled：所属 plugin / host 配置是否启用。

    **拿不到宿主配置时是 unknown，不是 false。**把「问不到」渲染成「关着」，
    用户会去开一个本来就开着的开关，然后以为自己修好了。
    """
    reason = s.get("loaded_reason") or ""
    if s.get("enabled_state") is False:
        return "false", "explicitly disabled in host configuration"
    if reason == "plugin-not-enabled":
        return "false", "owning plugin is absent from enabledPlugins"
    if reason == "plugin-state-unknown":
        return "unknown", "host configuration is unreadable; plugin state is unknown"
    if reason.startswith("workbuddy-mode-filtered"):
        return "false", "filtered by welcome mode: %s" % reason.split(":", 1)[-1]
    if reason == "openclaw-config-disabled":
        return "false", "disabled in OpenClaw configuration"
    if s.get("enabled_state") is None and s["host_family"] in ("openclaw", "workbuddy"):
        return "unknown", "this host has no per-skill enablement interface"
    return "true", s.get("level") or reason or "—"


def funnel(s, out, budget_at_risk):
    """六级漏斗，每级 `(state, reason)`。

    一旦某一级是 false，**下游全部记 n/a**：上游已经断了，下游的判断没有
    意义。硬给一个 true/false 会让用户去修一个不存在的问题。
    """
    rows = [("Installed", "true", s["path"])]

    est, reason = _enabled_stage(s)
    rows.append(("Enabled", est, reason))
    if est == "false":
        return rows + [(n, "n/a", "not applicable (disabled)") for n in FUNNEL_STAGES[2:]]

    sh = _shadow_map(out).get(s["path"])
    if sh and sh[1]:
        c = sh[0]
        rows.append(("Loaded", "false", "shadowed by the %s level" % c["effective"]["level"]))
        return rows + [(n, "n/a", "not applicable (not loaded)") for n in FUNNEL_STAGES[3:]]
    if not s.get("loaded"):
        rows.append(("Loaded", "false", s.get("loaded_reason") or "—"))
        return rows + [(n, "n/a", "not applicable (not loaded)") for n in FUNNEL_STAGES[3:]]
    rows.append(("Loaded", "true", s.get("loaded_reason") or "—"))

    # Discoverable **永远不取 false**（ARCHITECTURE §1.2）：「超预算后从调用
    # 最少的开始丢弃」是传闻不是实测，我们没有资格断言某一条真的被丢了。
    #
    # 注意这与 skill 记录里的 `discoverable` 字段**不是一回事** —— 那个是
    # OpenClaw 的「文件系统候选」，同名不同义，不能拿来复用。
    b = out.get("description_budget", {}) or {}
    if not (s.get("has_name") and s.get("has_description")):
        miss = [k for k, ok in (("name", s.get("has_name")),
                                ("description", s.get("has_description"))) if not ok]
        rows.append(("Discoverable", "at_risk", "frontmatter is missing %s" % ", ".join(miss)))
    elif not b.get("available"):
        rows.append(("Discoverable", "unknown", "this host does not expose a description budget"))
    elif s["name"] in budget_at_risk:
        rows.append(("Discoverable", "at_risk",
                     "budget is exceeded by %d characters; this skill is in the estimated risk band" % b["over_by_chars"]))
    else:
        rows.append(("Discoverable", "true", "budget is within limit and frontmatter is complete"))

    # Selected 没有任何直接数据源。**能给的只有 candidates，不是结论。**
    rows.append(("Selected", "unknown", "host does not expose routing data; only overlap candidates are available"))

    t = out.get("trigger_data", {}) or {}
    if not t.get("available"):
        rows.append(("Triggered", "unknown", "this host does not expose trigger data"))
    elif (s.get("usage_count") or 0) > 0:
        rows.append(("Triggered", "true", "%d uses; most recent %s"
                     % (s["usage_count"], human_last_used(s.get("last_used_days_ago")))))
    else:
        age = s.get("installed_days_ago") or 0
        gate = t.get("zombie_min_age_days", ZOMBIE_MIN_AGE_DAYS)
        rows.append(("Triggered", "false", "zero lifetime triggers (installed %.0f days%s)"
                     % (age, "" if age >= gate else "; younger than %d days, insufficient evidence" % gate)))
    return rows


def _budget_at_risk_names(out):
    """预算溢出时，处于「估算风险区间」的 skill 名。

    **直接读扫描器给的名单，绝不在这里重算。**重算过一次，因为手上只有被
    截断到前 5 条的 longest_descriptions，算出来的条数与
    skills_possibly_dropped 对不上 —— 同一份报告里两个数互相打架，读者无从
    判断该信哪个。
    """
    b = out.get("description_budget", {}) or {}
    return set(b.get("at_risk_skills") or ())


def explain_record(out, s, budget_at_risk, overlap_min=DEFAULT_OVERLAP_MIN):
    """`explain` 的数据层，供 `--json` 与呈现共用。"""
    rows = funnel(s, out, budget_at_risk)
    states = dict((n, (st, r)) for n, st, r in rows)
    blocked = next((n for n, st, _ in rows if st == "false"), None)
    pairs = [p for p in overlap_pairs(out, overlap_min)
             if s["name"] in (p["a"], p["b"]) or
             (s.get("namespace") and "%s:%s" % (s["namespace"], s["name"]) in (p["a"], p["b"]))]
    sh = _shadow_map(out).get(s["path"])
    return {
        "name": s["name"],
        "namespace": s.get("namespace"),
        "path": s["path"],
        "host": s["host_family"],
        "status": ("NOT IN EFFECT" if blocked in ("Enabled", "Loaded")
                   else "NEVER TRIGGERED" if blocked == "Triggered"
                   else "IN EFFECT"),
        "blocked_at": blocked,
        "funnel": [{"stage": n, "state": st, "reason": r} for n, st, r in rows],
        "cost": {"tier1_tokens": s["tier1_tokens"],
                 "tier2_core_tokens": s["tier2_core_tokens"],
                 "tier2_refs_tokens": s["tier2_refs_tokens"],
                 "tier2_max_tokens": s["tier2_max_tokens"],
                 "tier2_refs_files": s["tier2_refs_files"],
                 "body_lines": s["body_lines"]},
        "conflict": sh[0] if sh else None,
        "is_shadowed": bool(sh and sh[1]),
        "overlap_candidates": pairs,
        "security": {k: s["security"][k] for k in
                     ("max_severity", "max_severity_uncited", "all_findings_cited",
                      "external_url_count", "findings")},
        "_states": states,
    }


def _explain_fix_lines(rec, out):
    """修复建议，**按省事程度排序**，且每条都要能直接执行。"""
    if rec["is_shadowed"]:
        c, eff = rec["conflict"], rec["conflict"]["effective"]
        me = next(x for x in c["shadowed"] if x["path"] == rec["path"])
        # 三种关系要说三种话。**相等不能归进「较旧」** —— 两份同时写下的
        # 副本说「你的较旧」是编的，而这一整段的价值就在于「为什么」可信。
        if me["mtime"] > eff["mtime"]:
            rel = "The copy you edited is newer but is not effective"
        elif me["mtime"] < eff["mtime"]:
            rel = "The effective copy is newer than this copy"
        else:
            rel = "Both copies have the same modification time; precedence selects the other copy"
        return ([
            rel + ".",
            "",
            "1. Rename: prefix project-specific skills (%s → <prefix>-%s) to eliminate the conflict"
            % (rec["name"], rec["name"]),
            "2. Symlink: for one source of truth, Claude Code follows symlinks and loads the same target only once",
            "3. Layer: keep stable cross-project skills in home; keep project-specific skills in version control",
            "",
            "Note: some runtimes have shown both same-named skills in the selector instead of shadowing one. "
            "If you observe both, runtime behavior may differ from documentation; rename them to avoid ambiguity.",
        ])
    st = rec["_states"]
    if st["Enabled"][0] == "false":
        return ["1. Enable it in the host configuration (Claude Code: enabledPlugins)",
                "2. If unneeded, remove the on-disk copy to avoid future confusion"]
    if st["Enabled"][0] == "unknown":
        return ["1. Make the host configuration readable; otherwise this stage remains unknown",
                "   Claude Code requires a readable ~/.claude.json"]
    if st["Loaded"][0] == "false":
        return ["1. Move it to a location scanned by this host (see the reason above)"]
    lines = []
    if st["Discoverable"][0] == "at_risk":
        if "frontmatter" in st["Discoverable"][1]:
            lines.append("1. Add missing frontmatter fields; without description the skill cannot be selected")
        else:
            lines.append("1. Shorten the longest descriptions or disable unneeded skills to get under budget")
    if st["Triggered"][0] == "false":
        lines.append("%d. Check why it was not selected (does the description clearly say when to use it?), "
                     "then disable only if it is unnecessary. This tool never deletes anything automatically."
                     % (len(lines) + 1))
    if rec["overlap_candidates"]:
        lines.append("%d. It has %d lexically overlapping neighbors; run `skill-vitals overlap` to inspect shared terms"
                     % (len(lines) + 1, len(rec["overlap_candidates"])))
    return lines or ["All measurable funnel stages pass; there is no actionable fix."]


def render_explain(out, args):
    matches = find_skills(out, args.name)
    if not matches:
        names = sorted({s["name"] for s in out.get("skills", [])})
        near = [n for n in names if args.name.lower() in n.lower()][:8]
        print("No skill named %r." % args.name, file=sys.stderr)
        if near:
            print("Did you mean: %s" % ", ".join(near), file=sys.stderr)
        else:
            print("Run `skill-vitals list` to see what was discovered.", file=sys.stderr)
        return 1

    at_risk = _budget_at_risk_names(out)
    recs = [explain_record(out, s, at_risk, args.min) for s in matches]

    if args.json:
        Path(args.json).write_text(json.dumps(
            [{k: v for k, v in r.items() if k != "_states"} for r in recs],
            ensure_ascii=False, indent=2), encoding="utf-8")
        print("Wrote %s: %d copies" % (args.json, len(recs)))
        return 0

    for i, rec in enumerate(recs):
        if i:
            print()
            print("=" * 50)
        _print_explain(rec, out, len(recs), i)
    return 0


def _print_explain(rec, out, total, idx):
    full = "%s:%s" % (rec["namespace"], rec["name"]) if rec["namespace"] else rec["name"]
    print()
    print(full + ("   (copy %d/%d)" % (idx + 1, total) if total > 1 else ""))
    print("─" * 50)
    print("STATUS   %s" % rec["status"])
    print()
    print("Funnel")
    print()
    for row in rec["funnel"]:
        print("  %s %-16s %s" % (FUNNEL_GLYPH[row["state"]], row["stage"], row["reason"]))

    print()
    print("Reason")
    print()
    if rec["is_shadowed"] or (rec["conflict"] and not rec["is_shadowed"]):
        c = rec["conflict"]
        for line in _wrap(out.get("precedence_note", ""), "  "):
            print(line)
        print()
        # **标出「你问的是哪一份」。**同名两份的路径长得很像，不标的话读者
        # 得逐字符比对才知道自己在看的是生效的那份还是被盖的那份。
        def mark(path):
            return " ← requested copy" if path == rec["path"] else ""
        print("  active    %-10s %s%s" % (c["effective"]["level"], c["effective"]["path"],
                                      mark(c["effective"]["path"])))
        print("            hash %s  modified %s" % (
            c["effective"]["hash"], human_last_used(_days_since_epoch(c["effective"]["mtime"]))))
        for sh in c["shadowed"]:
            print("  shadowed  %-10s %s%s" % (sh["level"], sh["path"], mark(sh["path"])))
            print("            hash %s  modified %s" % (
                sh["hash"], human_last_used(_days_since_epoch(sh["mtime"]))))
    else:
        blocked = rec["blocked_at"]
        if blocked:
            st = rec["_states"][blocked]
            for line in _wrap("Blocked at %s: %s" % (blocked, st[1]), "  "):
                print(line)
        else:
            print("  No blocked stage; all six measurable stages pass.")

    print()
    print("Impact")
    print()
    impact = {
        "Enabled": "This skill is not in context; body changes cannot reach the model.",
        "Loaded": "This skill body cannot reach the user.",
        "Triggered": "It consumes description budget and startup context but has never been invoked.",
    }.get(rec["blocked_at"])
    if impact:
        for line in _wrap(impact, "  "):
            print(line)
    else:
        c = rec["cost"]
        # 四个桶不能合并：core 每次触发都载入，refs 按需，max 是全读时的上限。
        print("  In effect. Cost:")
        print("    tier1 (resident at startup)      %s tokens" % human_tokens(c["tier1_tokens"]))
        print("    tier2 core (loaded per trigger)  %s tokens  (%d lines)"
              % (human_tokens(c["tier2_core_tokens"]), c["body_lines"]))
        print("    tier2 refs (read on demand)      %s tokens  (%d files)"
              % (human_tokens(c["tier2_refs_tokens"]), c["tier2_refs_files"]))
        print("    tier2 max (all references read)  %s tokens" % human_tokens(c["tier2_max_tokens"]))

    if rec["overlap_candidates"]:
        print()
        print("Potentially competing neighbors       [Lexical, review required]")
        print()
        for p in rec["overlap_candidates"][:5]:
            other = p["b"] if p["a"] in (rec["name"], full) else p["a"]
            print("  %s   Jaccard %.2f   shared terms %s"
                  % (other, p["jaccard"], " · ".join(p["shared"][:4]) or "—"))

    sec = rec["security"]
    print()
    print("Security")
    print()
    if sec["max_severity"] == "none":
        # **绝不说「这个 skill 是安全的」。**没命中只说明这几条正则没匹配上。
        print("  No rules matched. This does not prove safety; heuristics have false negatives.")
    else:
        print("  Highest severity %s (outside citation-like context: %s)"
              % (sec["max_severity"], sec["max_severity_uncited"]))
        for f in sec["findings"][:6]:
            print("    %-24s %s:%s  %s%s" % (
                f["rule"], f["where"], f["line"], f["severity"],
                " (citation-like context)" if f["cited"] else ""))
        for line in _wrap("Citation-like context affects sorting only; it does not reduce severity or suppress reporting. "
                          "Open the reported line and review it.", "  ! "):
            print(line)
    if sec["external_url_count"]:
        print("  The body contains %d external URLs; third-party content can change at any time."
              % sec["external_url_count"])

    print()
    print("Fixes (easiest first)")
    print()
    for line in _explain_fix_lines(rec, out):
        if not line:
            print()
            continue
        # 编号条目的续行缩进到编号之后（"  1. " 宽 5），免得和下一条的编号顶齐
        numbered = len(line) > 2 and line[0].isdigit() and line[1] == "."
        for w in _wrap(line, "  ", cont="     " if numbered else "  "):
            print(w)


def _days_since_epoch(mtime):
    return (time.time() - mtime) / 86400.0
