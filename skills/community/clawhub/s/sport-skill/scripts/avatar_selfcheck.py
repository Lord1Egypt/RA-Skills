#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头像自检脚本（质量闸门）
======================
合规模型：默认每名重点球员使用【内置 SVG 插画头像】（纯矢量、无二进制文件、无真人肖像权风险，
由 analytics.py 的 player_spotlight_html 动态生成）。仅当数据显式提供真实头像（avatar_b64 /
avatar 字段，须为已获合法授权的素材）时才做以下校验：

  (1) 不重复      —— 同一场所有「真实头像」base64 两两互异（杜绝"对手撞脸"）
  (2) 有效        —— 真实头像必须是合法 PNG 且体积合理（杜绝破损/空图）
  (3) 性别符合预期 —— 优先用数据里声明的 match.gender / key_player.avatar_gender，
                     否则用「项目 + 联赛」启发式推断；声明与预期不符即报错。

未提供真实头像、走 SVG 插画默认路径的球员，记为通过（info 提示，不计风险）。

用法：
  python scripts/avatar_selfcheck.py <match.json>            # 检查（单场或含 matches[]）
  python scripts/avatar_selfcheck.py <match.json> --write-gender   # 顺便把推断性别回写进数据
  python scripts/avatar_selfcheck.py <match.json> --strict         # 未声明性别也视为失败

退出码：0 = 通过；1 = 存在风险（可作为打包/生成流水线闸门）
"""
import json
import sys
import os
import base64
import argparse

# 项目默认性别期望（仅启发式；生产以显式 gender 字段为准）
SPORT_GENDER = {
    "volleyball": "女",
    "beach_volleyball": "女",
}
# 联赛名里赛果这些词 → 视为女子赛事
FEMALE_LEAGUE_KW = ["女排", "女单", "女子", "女足", "女篮", "沙排女", "WNBA", "女组", "women"]

PNG_HEADER = b"\x89PNG\r\n\x1a\n"
MIN_LEN = 3000  # base64 长度下限，约 2KB 出头，过滤空图/占位


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
        raw = base64.b64decode(b64[:64])
        return raw.startswith(PNG_HEADER)
    except Exception:
        return False


def load_matches(path):
    d = json.load(open(path, encoding="utf-8"))
    if "matches" in d:
        return d, d["matches"]
    return d, [d]


def check_match(m, strict):
    expected = expected_gender(m)
    sport = m.get("sport", "")
    league = m.get("league", "")
    label = "%s · %s" % (league or sport or "?", m.get("match", ""))
    kps = m.get("key_players", [])
    issues = []
    notes = []

    # (1) 两两互异（仅对「真实头像」校验；SVG 插画默认路径不参与）
    by_hash = {}
    for kp in kps:
        h = kp.get("avatar_b64", "")
        if h:
            by_hash.setdefault(h, []).append(kp.get("name", "?"))
    dupes = {h: names for h, names in by_hash.items() if len(names) > 1}
    if dupes:
        for h, names in dupes.items():
            issues.append(("重复", "真实头像完全相同：%s" % " / ".join(names)))

    # (2) 有效 + (3) 性别；未提供真实头像 → SVG 插画默认路径，记为 info
    for kp in kps:
        nm = kp.get("name", "?")
        b64 = kp.get("avatar_b64", "")
        if not b64:
            notes.append("%s 走内置 SVG 插画头像（合规默认）" % nm)
            continue
        if not is_valid_png(b64) or len(b64) < MIN_LEN:
            issues.append(("破损", "%s 真实头像非合法 PNG 或体积过小" % nm))
        tag = kp.get("avatar_gender") or kp.get("gender")
        if tag:
            if tag != expected:
                issues.append(("性别", "%s 头像标记=%s，但本场预期=%s" % (nm, tag, expected)))
        else:
            notes.append("%s 真实头像缺 gender 标记（预期=%s）" % (nm, expected))

    return label, expected, kps, issues, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--write-gender", action="store_true", help="把推断性别回写进数据")
    ap.add_argument("--strict", action="store_true", help="未声明性别也视为失败")
    args = ap.parse_args()

    root, matches = load_matches(args.path)
    critical = 0
    total_kp = 0
    print("头像自检 · %s\n" % os.path.basename(args.path))
    changed = False
    for m in matches:
        label, expected, kps, issues, notes = check_match(m, args.strict)
        total_kp += len(kps)
        if args.write_gender:
            m["gender"] = expected
            for kp in kps:
                if "avatar_gender" not in kp or kp.get("avatar_gender") != expected:
                    kp["avatar_gender"] = expected
                    changed = True
        status = "✅" if not issues else "⚠️"
        print("[%s] %s  (预期性别=%s, 重点球员=%d)" % (status, label, expected, len(kps)))
        for kind, msg in issues:
            mark = "❌" if kind in ("重复", "破损", "性别") else "🔸"
            print("      %s %s：%s" % (mark, kind, msg))
            if kind in ("重复", "破损", "性别") or (args.strict and kind == "未声明"):
                critical += 1
        for msg in notes:
            print("      🔹 %s" % msg)
        if not issues:
            print("      全部通过")

    if args.write_gender and changed:
        json.dump(root, open(args.path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("\n已回写性别标记 → %s" % args.path)

    print("\n=== 汇总 ===  比赛=%d  重点球员=%d  风险项=%d" % (len(matches), total_kp, critical))
    if critical:
        print("结论：存在需处理的风险项，建议人工/重生成核对。")
        sys.exit(1)
    print("结论：通过 ✅")
    sys.exit(0)


if __name__ == "__main__":
    main()
