#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自查自纠（self-check & self-correct）质量闸门
============================================
这是 Skill 的「质量中枢」，把"人肉逐个校对"升级为"机器自动拦 + 自动纠"。
本工具只做**信息质量**检查，不涉及任何赛果判断或结论性建议：

  A. 头像质量（仅当数据携带 avatar_b64 照片时生效；本 Skill 默认用 SVG 插画，故通常跳过）
       - 同场重点球员头像两两互异（杜绝对手撞脸）
       - 头像合法 PNG 且体积合理（杜绝破损/空图）
       - 性别标记符合联赛预期（杜绝女排放男照之类）

  B. 信息质量（自纠核心）
       - 信息完整性：match / sport / teams 等必备字段是否齐全
       - 数据新鲜度：updated_at 距今过久触发"数据偏旧"警告
       - 专家可信度：每位专家必须有有效 tier；缺 tier 标记警告
       - 专家冲突：两位「权威专家」方向明显相反 → 提示人工复核
       - 重复观点：专家 view 文本高度重复 → 去重（自纠）
       - 置信度有效：confidence 文本异常过长提示

退出码：0 = 通过（无抑制断项）；1 = 存在风险项（建议人工/重生成核对）；
        2 = 致命错误（如无法解析数据）。--fix 会自动修正可纠项并回写。
"""
import json
import os
import sys
import base64
import argparse
from datetime import datetime, timedelta

SPORT_GENDER = {"volleyball": "女", "beach_volleyball": "女"}
FEMALE_LEAGUE_KW = ["女排", "女单", "女子", "女足", "女篮", "沙排女", "WNBA", "女组", "women"]
PNG_HEADER = b"\x89PNG\r\n\x1a\n"
MIN_LEN = 3000
CONF_LEVELS = {"高", "较高", "中", "低", "很低", "极低", "未评估"}

EXPERT_TIERS = {"权威专家", "数据方分析师", "知名解说", "非权威专家", "民间高手", "社媒博主"}

# 仅用于"专家观点方向是否相反"的粗略判定（描述性，不涉及敏感方向）
OPP_DIR = {"主胜": "客胜", "客胜": "主胜"}


# ---------------------------------------------------------------------------
# 头像部分（仅在数据携带照片头像时生效）
# ---------------------------------------------------------------------------

def expected_gender(match):
    if match.get("gender") in ("男", "女"):
        return match["gender"]
    league = match.get("league", "") or ""
    for kw in FEMALE_LEAGUE_KW:
        if kw in league:
            return "女"
    return SPORT_GENDER.get(match.get("sport", ""), "男")


def is_valid_png(b64):
    if not b64:
        return False
    try:
        return base64.b64decode(b64[:64]).startswith(PNG_HEADER)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# 信息质量检查
# ---------------------------------------------------------------------------

def _parse_dt(s):
    if not s:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except Exception:
            continue
    return None


def check_match(m, now=None, strict=False):
    """
    对单场比赛做全量自查自纠，返回：
      {label, gender, avatar_issues[], analysis_issues[], corrections[], freshness}
    corrections 为"已自动修正"项（供 --fix 回写数据）。
    """
    if now is None:
        now = datetime.now()
    label = "%s · %s" % (m.get("league", m.get("sport", "?")), m.get("match", ""))
    expected = expected_gender(m)
    avatar_issues, analysis_issues, corrections = [], [], []

    # —— A. 头像（仅当数据携带 avatar_b64 时检查）——
    kps = m.get("key_players", []) or []
    if any(kp.get("avatar_b64") for kp in kps):
        by_hash = {}
        for kp in kps:
            h = kp.get("avatar_b64", "")
            by_hash.setdefault(h, []).append(kp.get("name", "?"))
        for h, names in by_hash.items():
            if len(names) > 1 and h:
                avatar_issues.append(("重复", "头像完全相同：%s" % " / ".join(names)))
        for kp in kps:
            nm = kp.get("name", "?")
            b64 = kp.get("avatar_b64", "")
            if not b64:
                avatar_issues.append(("缺失", "%s 无 avatar_b64" % nm))
                continue
            if not is_valid_png(b64) or len(b64) < MIN_LEN:
                avatar_issues.append(("破损", "%s 头像非合法 PNG 或体积过小" % nm))
            tag = kp.get("avatar_gender") or kp.get("gender")
            if tag and tag != expected:
                avatar_issues.append(("性别", "%s 头像标记=%s，预期=%s" % (nm, tag, expected)))
            elif not tag:
                avatar_issues.append(("未声明", "%s 缺 gender 标记(预期=%s)" % (nm, expected)))

    # —— B. 信息质量 ——
    # 1) 信息完整性（必备字段）
    missing = []
    if not m.get("match"):
        missing.append("match")
    if not m.get("sport"):
        missing.append("sport")
    if not (m.get("teams") or []):
        missing.append("teams")
    has_detail = any([m.get("players"), m.get("intel"), m.get("experts"),
                     m.get("info_points"), m.get("analysis"), m.get("key_players")])
    if not has_detail:
        missing.append("至少一项明细(players/intel/experts/info_points/analysis)")
    if missing:
        analysis_issues.append(("信息不完整", "缺失字段：%s" % "、".join(missing)))

    # 2) 数据新鲜度
    ud = m.get("updated_at") or (m.get("meta", {}) or {}).get("updated_at")
    dt = _parse_dt(ud)
    fresh = "未知"
    if dt:
        age_h = (now - dt).total_seconds() / 3600.0
        if age_h > 36:
            analysis_issues.append(("数据偏旧", "updated_at=%s（距今 %.0f 小时），建议刷新" % (ud, age_h)))
            fresh = "偏旧"
        else:
            fresh = "新鲜"

    # 3) 专家可信度 / 冲突 / 重复
    experts = m.get("experts", []) or []
    seen_views = {}
    authority = []
    for i, e in enumerate(list(experts)):
        tier = e.get("tier")
        if tier not in EXPERT_TIERS:
            analysis_issues.append(("专家tier", "专家「%s」缺有效 tier=%s" % (e.get("name", "?"), tier)))
        view = (e.get("view", "") or "").strip()
        key = view[-40:] if view else ""
        if key and key in seen_views:
            analysis_issues.append(("重复观点", "专家「%s」观点与「%s」高度重复，已去重" % (e.get("name", "?"), seen_views[key])))
            corrections.append("去重专家观点：%s" % e.get("name", "?"))
            experts.remove(e)
            continue
        if key:
            seen_views[key] = e.get("name", "?")
        if tier in ("权威专家", "数据方分析师"):
            authority.append(e)
    # 权威冲突（方向明显相反）
    for a in authority:
        for b in authority:
            if a is b:
                continue
            va, vb = (a.get("view", "") or ""), (b.get("view", "") or "")
            if _opposite(va, vb):
                analysis_issues.append(("权威冲突", "两位权威专家方向明显相反：%s vs %s（建议人工复核）" %
                                         (a.get("name", "?"), b.get("name", "?"))))

    # 4) 置信度有效（仅作文本合理性提示）
    conf = m.get("confidence")
    if isinstance(conf, str) and conf not in CONF_LEVELS and conf not in ("未评估",):
        if len(conf) > 20:
            analysis_issues.append(("置信度", "confidence 文本过长，疑似异常：%s" % conf[:20]))

    # 5) 专家新鲜度闸门（仅对实时场 / 非静态兜底场）——
    #    这是"专家每期必须自动更新"的强制保障：缺本期 experts_refreshed_at 即视为陈旧阻断。
    if m.get("live") and not m.get("experts_static"):
        ref = m.get("experts_refreshed_at")
        if not ref:
            analysis_issues.append(("专家未更新",
                                    "实时场缺少 experts_refreshed_at（本期未联网核实专家观点），视为陈旧，须先 WebSearch 刷新再出报"))
        else:
            dt_ref = _parse_dt(ref)
            if dt_ref is None:
                analysis_issues.append(("专家偏旧", "experts_refreshed_at=%s 无法解析" % ref))
            elif (now - dt_ref).days > 0:
                analysis_issues.append(("专家偏旧", "experts_refreshed_at=%s 非本期，疑似未更新" % ref))

    # 6) 非实时示例兜底线索（仅作提示，不阻断；但确保审计与报告都显式揭示，避免冒用实时）
    if (not m.get("live")) and (m.get("experts_static") or m.get("_demo")):
        analysis_issues.append(("非实时示例",
                                "本场为内置示例兜底（非今日真实赛程），仅作信息结构/版式演示；专家为精选静态库，非本期新采集"))

    return {"label": label, "gender": expected, "avatar_issues": avatar_issues,
            "analysis_issues": analysis_issues, "corrections": corrections, "freshness": fresh}


def _opposite(va, vb):
    """粗略判断两条观点是否方向明显相反（用于权威冲突检测）。"""
    def side(t):
        for k in OPP_DIR:
            if k in t:
                return k
        return None
    sa, sb = side(va), side(vb)
    if sa and sb and OPP_DIR.get(sa) == sb:
        return True
    return False


def audit(data, now=None, strict=False):
    """对整份数据（单场或含 matches[]）做自查自纠，返回汇总字典。"""
    if now is None:
        now = datetime.now()
    if "matches" in data:
        matches = data["matches"]
    else:
        matches = [data]
    results = [check_match(m, now=now, strict=strict) for m in matches]
    avatar_crit = sum(1 for r in results for (k, _) in r["avatar_issues"] if k in ("重复", "破损", "性别"))
    analysis_rit = sum(len(r["analysis_issues"]) for r in results)
    corrections = sum(len(r["corrections"]) for r in results)
    # 致命抑制断项：头像重复/破损/性别 + 信息不完整 + 专家未更新/偏旧（数据层面硬伤；专家须每期刷新）
    blocking = avatar_crit + sum(1 for r in results for (k, _) in r["analysis_issues"]
                                 if k in ("信息不完整", "专家未更新", "专家偏旧"))
    return {
        "results": results,
        "match_count": len(matches),
        "avatar_critical": avatar_crit,
        "analysis_issues": analysis_rit,
        "corrections": corrections,
        "blocking": blocking,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_report(a, show_corrections=True):
    print("自查自纠审计 · %s\n" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    for r in a["results"]:
        print("[%s] %s  (性别预期=%s, 新鲜度=%s)" % ("✅" if not r["avatar_issues"] and not r["analysis_issues"] else "⚠️",
                                                    r["label"], r["gender"], r["freshness"]))
        for kind, msg in r["avatar_issues"]:
            mark = "❌" if kind in ("重复", "破损", "性别") else "🔸"
            print("    %s 头像/%s：%s" % (mark, kind, msg))
        for kind, msg in r["analysis_issues"]:
            mark = "❌" if kind in ("信息不完整",) else "🔸"
            print("    %s 分析/%s：%s" % (mark, kind, msg))
        if show_corrections and r["corrections"]:
            for c in r["corrections"]:
                print("    🛠️ 自纠：%s" % c)
        if not r["avatar_issues"] and not r["analysis_issues"]:
            print("    全部通过")
    print("\n=== 汇总 ===  比赛=%d  头像风险=%d  分析风险=%d  已自纠=%d  抑制断项=%d" % (
        a["match_count"], a["avatar_critical"], a["analysis_issues"], a["corrections"], a["blocking"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--fix", action="store_true", help="把自纠修正（去重/剔除）回写数据")
    ap.add_argument("--strict", action="store_true", help="未声明性别等也视为失败")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出（供流水线消费）")
    args = ap.parse_args()

    try:
        root = json.load(open(args.path, encoding="utf-8"))
    except Exception as e:
        print("❌ 无法解析数据：%s" % e)
        sys.exit(2)

    a = audit(root, strict=args.strict)
    if args.json:
        print(json.dumps(a, ensure_ascii=False))
    else:
        _print_report(a)

    if args.fix:
        json.dump(root, open(args.path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\n已自纠回写 → %s" % args.path)

    if a["blocking"] > 0:
        sys.exit(1)
    print("\n结论：通过 ✅")
    sys.exit(0)


if __name__ == "__main__":
    main()
