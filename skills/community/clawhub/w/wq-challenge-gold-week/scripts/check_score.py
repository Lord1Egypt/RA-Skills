#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_score.py —— 查竞赛分:GET /competitions/challenge(SKILL.md §1.3 / §4.5)

打印当前 score / level / rank,以及距下一等级的差距:
    BRONZE > 1,000    SILVER > 5,000    GOLD > 10,000

注意:实测返回结构是嵌套的 {"leaderboard": {"score": …, "level": …, "rank": …}},
本脚本按嵌套结构解析(并兼容顶层平铺的旧结构以防万一)。

每天封顶约 2000 分、3AM EDT 刷新——提交后要到次日刷新才完全反映,
没涨就回查:是被自相关挡了,还是当天平均被弱因子拖低(§4.5 收尾核对)。

用法:
    python scripts/check_score.py
"""

import sys

from wq_common import BASE, BrainSession

# 等级门槛(SKILL.md §1.3)
LEVELS = [("BRONZE", 1000), ("SILVER", 5000), ("GOLD", 10000)]
DAILY_CAP = 2000   # 每日封顶约 2000 分


def main():
    bs = BrainSession()
    print("查询 GET /competitions/challenge …\n")
    r = bs.get(f"{BASE}/competitions/challenge")
    if r.status_code == 404:
        print("[提示] 返回 404:账号可能还没报名 Challenge。"
              "请先在网页端竞赛页(platform.worldquantbrain.com)加入 Challenge。")
        sys.exit(1)
    r.raise_for_status()
    data = r.json()

    # 实测结构是嵌套的 {'leaderboard': {'score','level','rank'}};兼容顶层平铺
    lb = data.get("leaderboard")
    if not isinstance(lb, dict):
        lb = data
    score = lb.get("score")
    level = lb.get("level")
    rank = lb.get("rank")

    if score is None and level is None:
        print("[异常] 没解析出 score/level,原始返回如下,请人工核对结构:")
        print(str(data)[:800])
        sys.exit(1)

    print("=" * 46)
    print("WorldQuant Challenge 当前战绩")
    print("=" * 46)
    print(f"  score : {score}")
    print(f"  level : {level}")
    print(f"  rank  : {rank}")

    if isinstance(score, (int, float)):
        print("\n  等级进度(每天封顶约 2000 分,3AM EDT 刷新):")
        next_shown = False
        for name, threshold in LEVELS:
            if score > threshold:
                print(f"    {name:<7}(>{threshold:>6,}) ✓ 已达成")
            else:
                gap = threshold - score
                mark = ""
                if not next_shown:
                    days = max(1, -(-int(gap) // DAILY_CAP))  # 向上取整
                    mark = f"  ← 下一目标,还差 {gap:,.0f} 分(约 {days} 个满分日)"
                    next_shown = True
                print(f"    {name:<7}(>{threshold:>6,}) 还差 {gap:>8,.0f}{mark}")
        if not next_shown:
            print("\n  🏆 已到 GOLD!保持每天精提 1-2 个的节奏即可(§Day5 维持)。")

    print("\n  提醒:当天提交的分要到次日 3AM EDT 刷新后才完全反映;"
          "没涨就回查提交是否 ACTIVE、当天平均是否被弱因子拖低(§4.5)。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[中断] 已手动停止。")
        sys.exit(130)
