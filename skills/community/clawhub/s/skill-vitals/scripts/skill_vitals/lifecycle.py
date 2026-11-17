"""Lifecycle classification and list rendering."""

import json
from pathlib import Path

ZOMBIE_MIN_AGE_DAYS = 14

# ── 生命周期与呈现（PRODUCT §5.2、§6）──────────────────────

DEFAULT_DORMANT_DAYS = 30


def lifecycle_status(skill, trigger_available, zombie_age=ZOMBIE_MIN_AGE_DAYS,
                     dormant_days=DEFAULT_DORMANT_DAYS):
    """返回 active / occasional / dormant / zombie / too-new / unknown。

    **宿主没有触发数据时一律 unknown**，不是 zombie —— 零触发与「问不到」
    是两件事，混起来会让用户删掉一个其实天天在用的 skill（不变量 12）。
    """
    if not trigger_available:
        return "unknown"
    uses = skill.get("usage_count") or 0
    if uses == 0:
        age = skill.get("installed_days_ago")
        if age is None:
            return "unknown"
        # 零触发必须先过年龄闸：今早刚装的说明不了任何事（不变量 9）
        return "zombie" if age >= zombie_age else "too-new"
    last = skill.get("last_used_days_ago")
    if last is None:
        # 有触发数但没有时间戳：能说的只有「用过」，不能推断新鲜度
        return "occasional"
    if last <= 7:
        return "active"
    if last <= dormant_days:
        return "occasional"
    return "dormant"


def load_state(skill, shadowed_paths):
    """LOAD 与 STATUS 必须分列（PRODUCT §5.2）。

    前者是**加载状态**，后者是**使用生命周期**，两者正交：一个 skill 完全
    可以既 shadowed 又 active —— 生效的那份在被用、你改的那份没生效。
    挤成一列会把它显示成 shadowed 并**隐藏使用数据**，而这恰恰是最该被
    看见的情况。
    """
    if skill.get("path") in shadowed_paths:
        return "shadowed"
    if skill.get("loaded"):
        return "loaded"
    reason = skill.get("loaded_reason") or ""
    if reason.startswith("other-host"):
        return "other-host"
    if "not-enabled" in reason or "disabled" in reason or "filtered" in reason:
        return "disabled"
    return "unknown"


def human_tokens(n):
    if n is None:
        return "—"
    return "%.1fk" % (n / 1000.0) if n >= 1000 else str(n)


def human_last_used(days):
    if days is None:
        return "never"
    if days < 1:
        return "%dh ago" % max(1, int(days * 24))
    return "%dd ago" % int(days)


def render_list(out, args):
    """`list` 的呈现。回答「你到底看到了什么」。"""
    trigger_available = out["trigger_data"]["available"]
    zombie_age = out["trigger_data"]["zombie_min_age_days"]
    shadowed = {x["path"] for c in out["conflicts"] for x in c["shadowed"]}

    rows = []
    for s in out["skills"]:
        load = load_state(s, shadowed)
        # **未加载的 skill 不谈使用生命周期。**它没进上下文，"zombie" 或
        # "too-new" 对它没有意义，写上去等于用一个生命周期词去解释一件
        # 加载状态的事。规格里 legacy-tool 那行就是 `disabled  —  —  —`。
        #
        # shadowed **要**显示使用数据：生效的那份在被用、你改的那份没生效，
        # 这恰恰是最该被看见的情况（§5.2）。
        active_form = load in ("loaded", "shadowed")
        rows.append({
            "name": s["name"],
            "load": load,
            "status": (lifecycle_status(s, trigger_available, zombie_age,
                                        args.stale or DEFAULT_DORMANT_DAYS)
                       if active_form else None),
            "uses": s.get("usage_count") if (active_form and trigger_available) else None,
            "last": s.get("last_used_days_ago") if (active_form and trigger_available) else None,
            "core": s.get("tier2_core_tokens"),
            "max": s.get("tier2_max_tokens"),
            "_shown": active_form,
        })

    if args.unused:
        rows = [r for r in rows if r["status"] in ("zombie", "dormant")]
    if args.shadowed:
        rows = [r for r in rows if r["load"] == "shadowed"]
    # **先按 LOAD 分组，再按排序键。**这张表回答「你到底看到了什么」，
    # 真正进了上下文的那批必须在最前面 —— 否则一堆未启用的大块头会把
    # 唯一生效的那个顶到屏幕外（实测：默认按 cost 排时正是如此）。
    load_rank = {"loaded": 0, "shadowed": 1, "disabled": 2,
                 "other-host": 3, "unknown": 4}
    key = {"usage": lambda r: -(r["uses"] or 0),
           "cost": lambda r: -(r["core"] or 0),
           "name": lambda r: r["name"]}[args.sort]
    rows.sort(key=lambda r: (load_rank.get(r["load"], 9), key(r)))
    if args.top:
        rows = rows[:args.top]

    if args.json:
        Path(args.json).write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Wrote %s: %d rows" % (args.json, len(rows)))
        return

    if not rows:
        print("No matching skills.")
        return
    w = max(len(r["name"]) for r in rows)
    w = max(w, 4)
    print("%-*s  %-10s %-11s %6s  %-10s %7s %7s" %
          (w, "NAME", "LOAD", "STATUS", "USES", "LAST USED", "CORE", "MAX"))
    print("─" * (w + 58))
    for r in rows:
        print("%-*s  %-10s %-11s %6s  %-10s %7s %7s" % (
            w, r["name"], r["load"], r["status"] or "—",
            "—" if r["uses"] is None else r["uses"],
            human_last_used(r["last"]) if (r["_shown"] and trigger_available) else "—",
            human_tokens(r["core"]), human_tokens(r["max"])))

    loaded = sum(1 for r in rows if r["load"] == "loaded")
    # **阈值必须显示在末行**：没有阈值的状态词无法解释也无法复现（§6.1）
    print()
    print("%d loaded · %d not loaded  ·  thresholds dormant=%dd zombie=%dd%s" % (
        loaded, len(rows) - loaded, args.stale or DEFAULT_DORMANT_DAYS, zombie_age,
        "" if trigger_available else "  ·  trigger data unavailable; STATUS is unknown"))
