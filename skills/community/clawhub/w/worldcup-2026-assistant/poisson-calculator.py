#!/usr/bin/env python3
"""
足球泊松分布概率计算器 v2.0 / Football Poisson Distribution Calculator v2.0

改进：λ 估算不再拍脑袋，加入对手实力权重、近期状态修正、赛事阶段修正

用法 / Usage:
  # 模式1：直接输入λ（快速模式）
  python3 poisson-calculator.py --lambda-home 2.5 --lambda-away 0.4 --handicap -2

  # 模式2：智能估算λ（推荐模式）
  python3 poisson-calculator.py --smart \
    --home-goals-scored 2.1 --home-goals-conceded 0.8 \
    --away-goals-scored 0.9 --away-goals-conceded 1.6 \
    --home-fifa 6 --away-fifa 57 \
    --home-form 0.7 --away-form 0.5 \
    --must-win home \
    --handicap -2

  # 模式3：带赔率自动期望值计算
  python3 poisson-calculator.py --lambda-home 2.5 --lambda-away 0.4 \
    --handicap -2 --odds 1.94 4.05 2.73

参数说明：
  --lambda-home / --lambda-away   直接指定预期进球
  --smart                         启用智能λ估算
  --home-goals-scored             主队近期场均进球
  --home-goals-conceded           主队近期场均失球
  --away-goals-scored             客队近期场均进球
  --away-goals-conceded           客队近期场均失球
  --home-fifa / --away-fifa       FIFA排名
  --home-form / --away-form       近期状态系数(0.5-1.5，1.0=正常)
  --must-win                      哪队必须赢(home/away/none)
  --handicap                      让球数(正=主队受让，负=主队让)
  --odds                          三个赔率(让胜 让平 让负 或 胜 平 负)
  --tournament-avg-goals          赛事平均进球(默认2.5)
"""

import sys
import math
import argparse
from typing import Dict, Tuple, List, Optional


def poisson(k: int, lam: float) -> float:
    """泊松分布概率 P(X=k) = (λ^k × e^(-λ)) / k!"""
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def calc_score_matrix(lam_home: float, lam_away: float, max_goals: int = 10) -> Dict[Tuple[int, int], float]:
    """计算所有比分概率矩阵"""
    matrix = {}
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            matrix[(i, j)] = poisson(i, lam_home) * poisson(j, lam_away)
    return matrix


def calc_outcomes(matrix: Dict[Tuple[int, int], float]) -> Tuple[float, float, float]:
    """计算胜/平/负概率"""
    win = draw = loss = 0.0
    for (i, j), prob in matrix.items():
        if i > j:
            win += prob
        elif i == j:
            draw += prob
        else:
            loss += prob
    return win, draw, loss


def calc_handicap_outcomes(matrix: Dict[Tuple[int, int], float], handicap: int) -> Tuple[float, float, float]:
    """计算让球胜/平/负概率"""
    win = draw = loss = 0.0
    for (i, j), prob in matrix.items():
        adjusted_diff = (i - j) + handicap
        if adjusted_diff > 0:
            win += prob
        elif adjusted_diff == 0:
            draw += prob
        else:
            loss += prob
    return win, draw, loss


def calc_total_goals(matrix: Dict[Tuple[int, int], float]) -> Dict[int, float]:
    """计算总进球概率"""
    goals = {}
    for (i, j), prob in matrix.items():
        total = i + j
        if total not in goals:
            goals[total] = 0.0
        goals[total] += prob
    return goals


def top_scores(matrix: Dict[Tuple[int, int], float], n: int = 10) -> List[Tuple[Tuple[int, int], float]]:
    """返回概率最高的 n 个比分"""
    return sorted(matrix.items(), key=lambda x: -x[1])[:n]


def expected_value(prob: float, odds: float) -> float:
    """期望值 = (概率 × 赔率) - 1"""
    return prob * odds - 1


def ev_label(ev: float) -> str:
    """期望值标签"""
    if ev < 0:
        return "❌"
    elif ev < 0.05:
        return "⚠️观望"
    elif ev < 0.15:
        return "🟡轻仓"
    else:
        return "🟢正常投入"


def format_pct(p: float) -> str:
    return f"{p * 100:.1f}%"


def odds_implied_prob(odds: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """赔率反推去抽水概率"""
    raw = [1 / o for o in odds]
    total = sum(raw)
    return tuple(r / total for r in raw)


def fifa_strength_factor(fifa_home: int, fifa_away: int) -> Tuple[float, float]:
    """FIFA排名转换实力系数

    排名差越大，强队λ越高，弱队λ越低
    系数范围 0.6 ~ 1.4
    """
    diff = fifa_away - fifa_home  # 正数=主队排名靠前

    # 用对数函数压缩，避免极端值
    if diff > 0:
        home_factor = 1.0 + min(0.4, math.log10(abs(diff) + 1) * 0.15)
        away_factor = 1.0 - min(0.4, math.log10(abs(diff) + 1) * 0.15)
    elif diff < 0:
        home_factor = 1.0 - min(0.4, math.log10(abs(diff) + 1) * 0.15)
        away_factor = 1.0 + min(0.4, math.log10(abs(diff) + 1) * 0.15)
    else:
        home_factor = away_factor = 1.0

    return home_factor, away_factor


def smart_lambda(
    home_goals_scored: float,
    home_goals_conceded: float,
    away_goals_scored: float,
    away_goals_conceded: float,
    home_fifa: int,
    away_fifa: int,
    home_form: float = 1.0,
    away_form: float = 1.0,
    must_win: str = "none",
    tournament_avg: float = 2.5,
) -> Tuple[float, float, str]:
    """智能估算预期进球 λ

    公式（Dixon-Coles 经典模型）：
    赛事每队平均进球 = tournament_avg / 2
    λ_主队 = 主队进攻力 × 客队防守力 × FIFA实力系数 × 状态系数 × 战意系数 × 主场优势
    λ_客队 = 客队进攻力 × 主队防守力 × FIFA实力系数 × 状态系数 × 战意系数

    进攻力 = 球队场均进球 / 赛事每队平均进球
    防守力 = 球队场均失球 / 赛事每队平均进球
    主场优势 ≈ 1.15
    """
    notes = []

    per_team_avg = tournament_avg / 2  # 每队每场平均进球

    # Step 1: 基础攻防力
    home_attack = home_goals_scored / per_team_avg
    home_defense = home_goals_conceded / per_team_avg
    away_attack = away_goals_scored / per_team_avg
    away_defense = away_goals_conceded / per_team_avg

    notes.append(f"每队场均进球基准: {per_team_avg:.2f}")
    notes.append(f"进攻力: 主队{home_attack:.2f} 客队{away_attack:.2f}")
    notes.append(f"防守力: 主队{home_defense:.2f} 客队{away_defense:.2f}")

    # Step 2: FIFA排名实力系数
    home_fifa_factor, away_fifa_factor = fifa_strength_factor(home_fifa, away_fifa)
    notes.append(f"FIFA系数: 主队{home_fifa_factor:.2f} 客队{away_fifa_factor:.2f}")

    # Step 3: 近期状态修正
    home_form = max(0.5, min(1.5, home_form))
    away_form = max(0.5, min(1.5, away_form))
    notes.append(f"状态系数: 主队{home_form:.2f} 客队{away_form:.2f}")

    # Step 4: 战意系数
    home_motivation = 1.0
    away_motivation = 1.0
    if must_win == "home":
        home_motivation = 1.15
        away_motivation = 0.95
        notes.append("战意: 主队必须赢(+15%) 客队可接受平(-5%)")
    elif must_win == "away":
        away_motivation = 1.15
        home_motivation = 0.95
        notes.append("战意: 客队必须赢(+15%) 主队可接受平(-5%)")

    # Step 5: 主场优势
    home_advantage = 1.15

    # Step 6: 综合 λ
    lam_home = home_attack * away_defense * home_fifa_factor * home_form * home_motivation * home_advantage
    lam_away = away_attack * home_defense * away_fifa_factor * away_form * away_motivation

    # 限制范围
    lam_home = max(0.2, min(5.0, lam_home))
    lam_away = max(0.1, min(4.0, lam_away))

    notes.append(f"最终 λ: 主队{lam_home:.2f} 客队{lam_away:.2f}")

    return lam_home, lam_away, "\n".join(notes)


def print_result(
    lam_home: float,
    lam_away: float,
    handicap: int,
    odds: Optional[Tuple[float, float, float]],
    lambda_notes: Optional[str] = None,
):
    """打印完整结果"""
    print(f"\n{'='*60}")
    print(f"⚽ 泊松分布概率计算 v2.0 / Poisson Calculator v2.0")
    print(f"{'='*60}")
    print(f"📊 主队预期进球 λ₁ = {lam_home}")
    print(f"📊 客队预期进球 λ₂ = {lam_away}")
    if handicap != 0:
        direction = "主队让" + str(abs(handicap)) + "球" if handicap < 0 else "主队受让" + str(handicap) + "球"
        print(f"📊 让球数 = {handicap}（{direction}）")
    if lambda_notes:
        print(f"\n📝 λ 估算过程:")
        print(f"{'-'*40}")
        for line in lambda_notes.split("\n"):
            print(f"  {line}")
    print(f"{'='*60}\n")

    # 计算比分矩阵
    matrix = calc_score_matrix(lam_home, lam_away)

    # Top 10 比分
    print(f"🎯 比分概率 Top 10 / Top 10 Score Probabilities:")
    print(f"{'-'*50}")
    for (i, j), prob in top_scores(matrix, 10):
        bar = "█" * int(prob * 100)
        print(f"  {i}-{j:>2}  {format_pct(prob):>7}  {bar}")
    print()

    # 胜平负
    win, draw, loss = calc_outcomes(matrix)
    print(f"📈 胜平负概率 / Win-Draw-Loss:")
    print(f"{'-'*50}")
    print(f"  主队胜: {format_pct(win):>7}")
    print(f"  平局:   {format_pct(draw):>7}")
    print(f"  客队胜: {format_pct(loss):>7}")
    print()

    # 让球胜平负
    if handicap != 0:
        h_win, h_draw, h_loss = calc_handicap_outcomes(matrix, handicap)
        print(f"📈 让球胜平负 ({handicap}) / Handicap Outcomes:")
        print(f"{'-'*50}")
        print(f"  让胜: {format_pct(h_win):>7}")
        print(f"  让平: {format_pct(h_draw):>7}")
        print(f"  让负: {format_pct(h_loss):>7}")
        print()

    # 期望值
    if odds:
        print(f"💡 期望值分析 / Expected Value:")
        print(f"{'-'*50}")
        print(f"  公式: E = (概率 × 赔率) - 1")
        if handicap != 0:
            ev_win = expected_value(h_win, odds[0])
            ev_draw = expected_value(h_draw, odds[1])
            ev_loss = expected_value(h_loss, odds[2])
            print(f"  让胜: {format_pct(h_win):>7} × {odds[0]:>5} - 1 = {format_pct(ev_win):>8} {ev_label(ev_win)}")
            print(f"  让平: {format_pct(h_draw):>7} × {odds[1]:>5} - 1 = {format_pct(ev_draw):>8} {ev_label(ev_draw)}")
            print(f"  让负: {format_pct(h_loss):>7} × {odds[2]:>5} - 1 = {format_pct(ev_loss):>8} {ev_label(ev_loss)}")
        else:
            ev_win = expected_value(win, odds[0])
            ev_draw = expected_value(draw, odds[1])
            ev_loss = expected_value(loss, odds[2])
            print(f"  胜: {format_pct(win):>7} × {odds[0]:>5} - 1 = {format_pct(ev_win):>8} {ev_label(ev_win)}")
            print(f"  平: {format_pct(draw):>7} × {odds[1]:>5} - 1 = {format_pct(ev_draw):>8} {ev_label(ev_draw)}")
            print(f"  负: {format_pct(loss):>7} × {odds[2]:>5} - 1 = {format_pct(ev_loss):>8} {ev_label(ev_loss)}")

        # 赔率反推交叉验证
        implied = odds_implied_prob(odds)
        print(f"\n  📊 赔率反推 vs 泊松模型对比:")
        labels = ["胜/让胜", "平/让平", "负/让负"]
        for i, label in enumerate(labels):
            poisson_prob = [win, draw, loss] if handicap == 0 else [h_win, h_draw, h_loss]
            diff = poisson_prob[i] - implied[i]
            flag = "⚠️分歧>10%" if abs(diff) > 0.10 else "✅接近"
            print(f"    {label}: 泊松{format_pct(poisson_prob[i]):>7} | 赔率反推{format_pct(implied[i]):>7} | 差{format_pct(abs(diff)):>6} {flag}")
        print()

    # 总进球
    goals = calc_total_goals(matrix)
    print(f"📈 总进球概率 / Total Goals:")
    print(f"{'-'*50}")
    for g in range(min(8, max(goals.keys()) + 1)):
        prob = goals.get(g, 0)
        label = f"{g}球" if g < 7 else "7+球"
        print(f"  {label:>4}: {format_pct(prob):>7}")
    if any(k > 7 for k in goals):
        over7 = sum(v for k, v in goals.items() if k > 7)
        print(f"  7+球: {format_pct(over7):>7}")
    print()

    print(f"{'='*60}")
    print(f"⚠️ 泊松分布是数学模型，基于预期进球估算概率。")
    print(f"   实际比赛受红牌、伤病、战术、天气等因素影响。")
    print(f"   概率仅供参考，不构成投注建议。")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="足球泊松分布概率计算器 v2.0")
    parser.add_argument("--lambda-home", type=float, help="主队预期进球（直接模式）")
    parser.add_argument("--lambda-away", type=float, help="客队预期进球（直接模式）")
    parser.add_argument("--smart", action="store_true", help="启用智能λ估算")
    parser.add_argument("--home-goals-scored", type=float, help="主队近期场均进球")
    parser.add_argument("--home-goals-conceded", type=float, help="主队近期场均失球")
    parser.add_argument("--away-goals-scored", type=float, help="客队近期场均进球")
    parser.add_argument("--away-goals-conceded", type=float, help="客队近期场均失球")
    parser.add_argument("--home-fifa", type=int, help="主队FIFA排名")
    parser.add_argument("--away-fifa", type=int, help="客队FIFA排名")
    parser.add_argument("--home-form", type=float, default=1.0, help="主队状态系数(0.5-1.5)")
    parser.add_argument("--away-form", type=float, default=1.0, help="客队状态系数(0.5-1.5)")
    parser.add_argument("--must-win", choices=["home", "away", "none"], default="none", help="必须赢的队伍")
    parser.add_argument("--handicap", type=int, default=0, help="让球数(负=主队让)")
    parser.add_argument("--odds", nargs=3, type=float, help="三个赔率")
    parser.add_argument("--tournament-avg-goals", type=float, default=2.5, help="赛事平均进球(默认2.5)")
    args = parser.parse_args()

    if args.smart:
        if not all([args.home_goals_scored, args.home_goals_conceded,
                    args.away_goals_scored, args.away_goals_conceded,
                    args.home_fifa, args.away_fifa]):
            print("❌ 智能模式需要: --home-goals-scored, --home-goals-conceded, "
                  "--away-goals-scored, --away-goals-conceded, --home-fifa, --away-fifa")
            sys.exit(1)

        lam_home, lam_away, notes = smart_lambda(
            args.home_goals_scored, args.home_goals_conceded,
            args.away_goals_scored, args.away_goals_conceded,
            args.home_fifa, args.away_fifa,
            args.home_form, args.away_form,
            args.must_win, args.tournament_avg_goals,
        )
    elif args.lambda_home is not None and args.lambda_away is not None:
        lam_home = args.lambda_home
        lam_away = args.lambda_away
        notes = None
    else:
        parser.print_help()
        sys.exit(1)

    odds = tuple(args.odds) if args.odds else None
    print_result(lam_home, lam_away, args.handicap, odds, notes)


if __name__ == "__main__":
    main()
