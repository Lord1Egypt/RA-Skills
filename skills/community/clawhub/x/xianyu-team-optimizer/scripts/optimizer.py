#!/usr/bin/env python3
"""
咸鱼之王 · 十殿星级挑战组队优化器

多方案输出 + 升档建议。
- 输出最优方案及若干差异化替代方案供用户选择
- 对每个方案，分析"再引入多少星可升档"

用法:
    python3 optimizer.py players.json
    echo '{"players": [...]}' | python3 optimizer.py

输入 JSON:
{
  "players": [{"name": "老四", "stars": 16}, ...],
  "tiers": [120, 105, 90, 75, 60, 50, 40, 30],
  "max_stars_per_player": 24
}
tiers 可选，默认 [120, 105, 90, 75, 60, 50, 40, 30]。

输出 JSON:
{
  "plans": [
    {
      "label": "方案一（推荐）",
      "teams": [...],
      "unassigned": [...],
      "summary": {...},
      "upgrade_hints": [...]
    },
    ...
  ]
}
"""

import json
import sys
from itertools import combinations

DEFAULT_TIERS = [120, 105, 90, 75, 60, 50, 40, 30]
TEAM_SIZE = 5
MAX_STARS = 24  # 单人最高星级


def find_min_sum_team(stars, available_indices, threshold):
    """
    在 available_indices 中找 5 个下标，使对应 stars 之和 >= threshold 且和最小。
    返回选中的下标元组，或 None。
    """
    avail = sorted(available_indices, key=lambda i: stars[i])
    n = len(avail)
    if n < TEAM_SIZE:
        return None

    top5_sum = sum(stars[avail[n - 1 - j]] for j in range(TEAM_SIZE))
    if top5_sum < threshold:
        return None

    bot5_sum = sum(stars[avail[j]] for j in range(TEAM_SIZE))
    if bot5_sum >= threshold:
        return tuple(avail[:TEAM_SIZE])

    best = None
    best_sum = float("inf")

    for combo in combinations(avail, TEAM_SIZE):
        total = sum(stars[i] for i in combo)
        if threshold <= total < best_sum:
            best_sum = total
            best = combo
            if best_sum == threshold:
                break

    return best


# ---------------------------------------------------------------------------
# 全局最优搜索（递归 + 记忆化）
# ---------------------------------------------------------------------------

def _solve_optimal(stars, tiers_desc, n):
    """返回 (best_value, plan)。value = 各队达到的 tier 之和。"""
    memo = {}

    def solve(avail_fs):
        if avail_fs in memo:
            return memo[avail_fs]

        avail = set(avail_fs)
        if len(avail) < TEAM_SIZE:
            memo[avail_fs] = (0, [])
            return (0, [])

        best_val = 0
        best_plan = []

        for tier in tiers_desc:
            team = find_min_sum_team(stars, avail, tier)
            if team is None:
                continue
            remaining = frozenset(avail - set(team))
            rest_val, rest_plan = solve(remaining)
            total = tier + rest_val
            if total > best_val:
                best_val = total
                best_plan = [(tier, list(team))] + rest_plan

        memo[avail_fs] = (best_val, best_plan)
        return (best_val, best_plan)

    return solve(frozenset(range(n)))


def _solve_greedy(stars, tiers_desc, n):
    """贪心回退。"""
    available = set(range(n))
    plan = []
    total_val = 0

    for tier in tiers_desc:
        while len(available) >= TEAM_SIZE:
            team = find_min_sum_team(stars, available, tier)
            if team is None:
                break
            available -= set(team)
            plan.append((tier, list(team)))
            total_val += tier

    return total_val, plan


# ---------------------------------------------------------------------------
# 多方案生成
# ---------------------------------------------------------------------------

def _plan_to_output(players, stars, plan, label):
    """把 (tier, indices) list 转换为输出 dict。"""
    assigned = set()
    teams = []
    for tier, indices in plan:
        assigned.update(indices)
        team_players = [
            {"name": players[i]["name"], "stars": stars[i]}
            for i in sorted(indices, key=lambda i: -stars[i])
        ]
        teams.append({
            "tier": tier,
            "players": team_players,
            "total_stars": sum(p["stars"] for p in team_players),
        })

    n = len(players)
    unassigned = [
        {"name": players[i]["name"], "stars": stars[i]}
        for i in sorted(set(range(n)) - assigned, key=lambda i: -stars[i])
    ]

    tier_dist = {}
    for t in teams:
        tier_dist[t["tier"]] = tier_dist.get(t["tier"], 0) + 1

    total_val = sum(t["tier"] for t in teams)

    return {
        "label": label,
        "teams": teams,
        "unassigned": unassigned,
        "summary": {
            "total_players": n,
            "assigned": n - len(unassigned),
            "unassigned_count": len(unassigned),
            "teams_formed": len(teams),
            "tier_distribution": tier_dist,
            "total_tier_value": total_val,
        },
    }


def _generate_alternative(stars, tiers_desc, n, exclude_tier_from_first):
    """
    生成替代方案：强制第一支队伍不使用 exclude_tier_from_first 的档位，
    而是从下一个档位开始。用 greedy 或 optimal 求解剩余。
    """
    alt_tiers = [t for t in tiers_desc if t != exclude_tier_from_first]
    if not alt_tiers:
        return None

    if n <= 35:
        val, plan = _solve_optimal(stars, alt_tiers, n)
    else:
        val, plan = _solve_greedy(stars, alt_tiers, n)

    if not plan:
        return None
    return val, plan


def _generate_variants(stars, tiers_desc, n, base_plan):
    """
    基于最优方案，尝试生成不同的替代方案：
    1. 去掉最高档位限制，看能否换成更多中档队
    2. 去掉最低队的档位，看能否让其他队升档
    """
    variants = []
    seen_signatures = set()

    # 基础方案签名
    base_sig = tuple(sorted(t for t, _ in base_plan))
    seen_signatures.add(base_sig)

    # 策略1：禁用最优方案里最高的那个档位
    if base_plan:
        highest_tier = max(t for t, _ in base_plan)
        result = _generate_alternative(stars, tiers_desc, n, highest_tier)
        if result:
            val, plan = result
            sig = tuple(sorted(t for t, _ in plan))
            if sig not in seen_signatures:
                seen_signatures.add(sig)
                variants.append((val, plan))

    # 策略2：禁用最优方案里最低的那个档位
    if base_plan:
        lowest_tier = min(t for t, _ in base_plan)
        if lowest_tier != highest_tier:
            result = _generate_alternative(stars, tiers_desc, n, lowest_tier)
            if result:
                val, plan = result
                sig = tuple(sorted(t for t, _ in plan))
                if sig not in seen_signatures:
                    seen_signatures.add(sig)
                    variants.append((val, plan))

    # 策略3：只用中间档位
    if len(tiers_desc) >= 3:
        mid_tiers = tiers_desc[1:-1]
        if n <= 35:
            val, plan = _solve_optimal(stars, mid_tiers, n)
        else:
            val, plan = _solve_greedy(stars, mid_tiers, n)
        if plan:
            sig = tuple(sorted(t for t, _ in plan))
            if sig not in seen_signatures:
                seen_signatures.add(sig)
                variants.append((val, plan))

    # 按总价值降序排列
    variants.sort(key=lambda x: -x[0])
    return variants


# ---------------------------------------------------------------------------
# 升档建议
# ---------------------------------------------------------------------------

def _compute_upgrade_hints(teams, unassigned, tiers_desc, max_stars):
    """
    升档建议，聚焦"从外部引入新玩家"的策略：
    - 每支队伍：引入1名外部玩家替换最弱队员，需要多少星可升到各个更高档位
    - 未分组玩家：引入几名外部玩家、每人需多少星，可以组成什么档位的新队伍
    - 全局总结：引入N人可提升总收益多少
    """
    hints = []

    # ---------------------------------------------------------------
    # 1. 已组队 -> 外部引援升档
    # ---------------------------------------------------------------
    for i, team in enumerate(teams):
        current_tier = team["tier"]
        total = team["total_stars"]
        team_sorted_asc = sorted(team["players"], key=lambda p: p["stars"])
        weakest = team_sorted_asc[0]

        # 对每个更高档位，算引入1名外援替换最弱需要多少星
        recruit_options = []
        for target in sorted(tiers_desc):
            if target <= current_tier:
                continue
            # 替换最弱后需要达到 target: new_player_stars >= target - (total - weakest)
            other_total = total - weakest["stars"]
            min_stars = target - other_total
            if min_stars <= 0:
                min_stars = 1  # 随便来个人就行
            if min_stars > max_stars:
                continue  # 不可能达到
            recruit_options.append({
                "target_tier": target,
                "replace_player": weakest["name"],
                "replace_stars": weakest["stars"],
                "min_recruit_stars": min_stars,
                "new_total_if_max": other_total + max_stars,
            })

        # 不替换任何人，只靠引入额外外援不行（队伍已满5人），
        # 所以升档只能靠"替换最弱"或"多替换几个"
        # 如果替换最弱不够升到某些档位，试试替换最弱的2人
        if len(team_sorted_asc) >= 2:
            w1, w2 = team_sorted_asc[0], team_sorted_asc[1]
            other_total_2 = total - w1["stars"] - w2["stars"]
            multi_recruit = []
            for target in sorted(tiers_desc):
                if target <= current_tier:
                    continue
                # 已经能通过换1人达到的就不重复
                if any(r["target_tier"] == target for r in recruit_options):
                    continue
                total_needed = target - other_total_2
                if total_needed <= 0:
                    avg = 1
                else:
                    avg = total_needed / 2
                if avg > max_stars:
                    continue
                multi_recruit.append({
                    "target_tier": target,
                    "replace_players": [
                        {"name": w1["name"], "stars": w1["stars"]},
                        {"name": w2["name"], "stars": w2["stars"]},
                    ],
                    "recruit_count": 2,
                    "total_stars_needed": max(0, total_needed),
                    "avg_stars_per_recruit": round(max(1, avg), 1),
                })
        else:
            multi_recruit = []

        hint = {
            "type": "team_upgrade",
            "team_index": i + 1,
            "current_tier": current_tier,
            "total_stars": total,
            "weakest_player": {"name": weakest["name"], "stars": weakest["stars"]},
            "recruit_1_options": recruit_options,
            "recruit_2_options": multi_recruit,
        }
        hints.append(hint)

    # ---------------------------------------------------------------
    # 2. 未分组玩家 -> 外部引援组新队
    # ---------------------------------------------------------------
    if unassigned:
        un_total = sum(p["stars"] for p in unassigned)
        un_count = len(unassigned)
        need_more_players = max(0, TEAM_SIZE - un_count)

        tier_options = []
        for t in sorted(tiers_desc):
            deficit = t - un_total

            if un_count >= TEAM_SIZE:
                if deficit <= 0:
                    # 人够星也够——但这不该出现（应该已被分组）
                    tier_options.append({
                        "tier": t,
                        "recruit_count": 0,
                        "total_recruit_stars": 0,
                        "avg_stars_per_recruit": 0,
                        "achievable": True,
                    })
                else:
                    # 人够但星不够——不能引外援（已满5人），跳过
                    continue
            else:
                # 需要引入外部玩家补齐5人
                extra_stars = max(0, deficit)
                avg = extra_stars / need_more_players if need_more_players > 0 else 0
                if avg > max_stars:
                    continue  # 不可能
                tier_options.append({
                    "tier": t,
                    "recruit_count": need_more_players,
                    "total_recruit_stars": extra_stars,
                    "avg_stars_per_recruit": round(max(0, avg), 1),
                    "achievable": True,
                })

        # 也考虑：如果引入更多人（超过补齐5人所需），能否组多队
        # 比如未分组3人 + 引入7人 = 10人 = 2队
        extra_team_options = []
        if un_count > 0 and un_count < TEAM_SIZE:
            for extra_count in [TEAM_SIZE, TEAM_SIZE + need_more_players]:
                total_people = un_count + extra_count
                num_teams = total_people // TEAM_SIZE
                if num_teams < 2:
                    continue
                # 每队都达到最低档需要多少
                for t in sorted(tiers_desc):
                    total_needed = t * num_teams - un_total
                    if total_needed <= 0:
                        total_needed = extra_count  # 至少每人1星
                    avg = total_needed / extra_count
                    if avg > max_stars:
                        continue
                    extra_team_options.append({
                        "recruit_count": extra_count,
                        "total_teams": num_teams,
                        "target_tier_per_team": t,
                        "total_recruit_stars": max(0, total_needed),
                        "avg_stars_per_recruit": round(max(1, avg), 1),
                    })
                    break  # 只取该人数下的最低可达档

        hint = {
            "type": "unassigned_potential",
            "unassigned_count": un_count,
            "unassigned_total_stars": un_total,
            "unassigned_players": [{"name": p["name"], "stars": p["stars"]} for p in unassigned],
            "players_needed_for_one_team": need_more_players,
            "tier_options": tier_options,
            "extra_team_options": extra_team_options,
        }
        hints.append(hint)

    # ---------------------------------------------------------------
    # 3. 全局引援汇总
    # ---------------------------------------------------------------
    # 找出性价比最高的引援方案：引入最少的人获得最大的档位提升
    global_recruits = []
    for h in hints:
        if h["type"] == "team_upgrade" and h["recruit_1_options"]:
            best = h["recruit_1_options"][-1]  # 最高可达档位
            improvement = best["target_tier"] - h["current_tier"]
            global_recruits.append({
                "action": f"第{h['team_index']}队引入1人(≥{best['min_recruit_stars']}星)替{best['replace_player']}",
                "recruit_count": 1,
                "tier_change": f"{h['current_tier']}→{best['target_tier']}",
                "value_gain": improvement,
            })
        if h["type"] == "unassigned_potential" and h["tier_options"]:
            best_tier = h["tier_options"][-1]  # 最高可达档位
            global_recruits.append({
                "action": f"引入{best_tier['recruit_count']}人(人均≥{best_tier['avg_stars_per_recruit']}星)与未分组玩家组新队",
                "recruit_count": best_tier["recruit_count"],
                "tier_change": f"无→{best_tier['tier']}",
                "value_gain": best_tier["tier"],
            })

    # 按性价比排序（value_gain / recruit_count）
    global_recruits.sort(key=lambda x: -x["value_gain"] / max(1, x["recruit_count"]))

    if global_recruits:
        hints.append({
            "type": "global_recruit_summary",
            "ranked_options": global_recruits,
        })

    return hints


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def optimize(players, tiers=None, max_stars=MAX_STARS):
    if tiers is None:
        tiers = DEFAULT_TIERS[:]
    tiers_desc = sorted(set(tiers), reverse=True)

    stars = [p["stars"] for p in players]
    n = len(players)

    # 最优方案
    if n <= 35:
        best_val, best_plan = _solve_optimal(stars, tiers_desc, n)
    else:
        best_val, best_plan = _solve_greedy(stars, tiers_desc, n)

    plans = []
    primary = _plan_to_output(players, stars, best_plan, "方案一（推荐）")
    primary["upgrade_hints"] = _compute_upgrade_hints(
        primary["teams"], primary["unassigned"], tiers_desc, max_stars
    )
    plans.append(primary)

    # 替代方案
    variants = _generate_variants(stars, tiers_desc, n, best_plan)
    for idx, (val, plan) in enumerate(variants[:3]):  # 最多3个替代
        alt = _plan_to_output(players, stars, plan, f"方案{'二三四'[idx]}")
        alt["upgrade_hints"] = _compute_upgrade_hints(
            alt["teams"], alt["unassigned"], tiers_desc, max_stars
        )
        plans.append(alt)

    return {"plans": plans}


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    players = data.get("players", data if isinstance(data, list) else [])
    tiers = data.get("tiers", DEFAULT_TIERS)
    max_stars = data.get("max_stars_per_player", MAX_STARS)

    result = optimize(players, tiers, max_stars)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
