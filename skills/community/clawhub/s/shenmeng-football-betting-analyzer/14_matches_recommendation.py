#!/usr/bin/env python3
"""
14场足彩胜平负推荐
基于足彩分析工具的预测模型
"""

import sys
sys.path.insert(0, '~/.openclaw/workspace/skills/football-betting-analyzer')

from analyzer import FootballBettingAnalyzer
from odds_analyzer import ComprehensiveOddsAnalyzer, KellyCalculator


def generate_14_matches():
    """生成14场模拟比赛数据（基于近期热门赛事）"""
    
    matches = [
        # 英超
        {
            "id": 1,
            "league": "英超",
            "home_team": "曼城",
            "away_team": "阿森纳",
            "home_form": "WWWDW",
            "away_form": "WDWWL",
            "h2h_home_wins": 6,
            "h2h_away_wins": 2,
            "h2h_draws": 2,
            "home_goals_scored": 14,
            "home_goals_conceded": 4,
            "away_goals_scored": 11,
            "away_goals_conceded": 6,
            "home_advantage": 1.1,
            "odds": {"home": 1.75, "draw": 3.60, "away": 4.50}
        },
        {
            "id": 2,
            "league": "英超",
            "home_team": "利物浦",
            "away_team": "布莱顿",
            "home_form": "WWWWW",
            "away_form": "WDLWD",
            "h2h_home_wins": 7,
            "h2h_away_wins": 1,
            "h2h_draws": 2,
            "home_goals_scored": 16,
            "home_goals_conceded": 3,
            "away_goals_scored": 9,
            "away_goals_conceded": 8,
            "home_advantage": 1.15,
            "odds": {"home": 1.55, "draw": 4.20, "away": 5.50}
        },
        {
            "id": 3,
            "league": "英超",
            "home_team": "切尔西",
            "away_team": "曼联",
            "home_form": "WDWDL",
            "away_form": "LDWDW",
            "h2h_home_wins": 3,
            "h2h_away_wins": 4,
            "h2h_draws": 3,
            "home_goals_scored": 10,
            "home_goals_conceded": 7,
            "away_goals_scored": 8,
            "away_goals_conceded": 9,
            "home_advantage": 1.05,
            "odds": {"home": 2.10, "draw": 3.40, "away": 3.40}
        },
        {
            "id": 4,
            "league": "英超",
            "home_team": "热刺",
            "away_team": "纽卡斯尔",
            "home_form": "WLWDL",
            "away_form": "WWLWD",
            "h2h_home_wins": 4,
            "h2h_away_wins": 3,
            "h2h_draws": 3,
            "home_goals_scored": 12,
            "home_goals_conceded": 9,
            "away_goals_scored": 13,
            "away_goals_conceded": 7,
            "home_advantage": 1.08,
            "odds": {"home": 2.40, "draw": 3.50, "away": 2.80}
        },
        # 西甲
        {
            "id": 5,
            "league": "西甲",
            "home_team": "皇马",
            "away_team": "巴萨",
            "home_form": "WWWDW",
            "away_form": "WWWDL",
            "h2h_home_wins": 4,
            "h2h_away_wins": 4,
            "h2h_draws": 2,
            "home_goals_scored": 15,
            "home_goals_conceded": 5,
            "away_goals_scored": 16,
            "away_goals_conceded": 6,
            "home_advantage": 1.05,
            "odds": {"home": 2.20, "draw": 3.40, "away": 3.10}
        },
        {
            "id": 6,
            "league": "西甲",
            "home_team": "马竞",
            "away_team": "毕尔巴鄂",
            "home_form": "WDWDW",
            "away_form": "DWWDL",
            "h2h_home_wins": 6,
            "h2h_away_wins": 2,
            "h2h_draws": 2,
            "home_goals_scored": 11,
            "home_goals_conceded": 4,
            "away_goals_scored": 10,
            "away_goals_conceded": 7,
            "home_advantage": 1.12,
            "odds": {"home": 1.85, "draw": 3.40, "away": 4.20}
        },
        # 意甲
        {
            "id": 7,
            "league": "意甲",
            "home_team": "国际米兰",
            "away_team": "AC米兰",
            "home_form": "WWWWW",
            "away_form": "WDWDL",
            "h2h_home_wins": 5,
            "h2h_away_wins": 2,
            "h2h_draws": 3,
            "home_goals_scored": 14,
            "home_goals_conceded": 3,
            "away_goals_scored": 12,
            "away_goals_conceded": 8,
            "home_advantage": 1.10,
            "odds": {"home": 1.90, "draw": 3.50, "away": 4.00}
        },
        {
            "id": 8,
            "league": "意甲",
            "home_team": "尤文图斯",
            "away_team": "那不勒斯",
            "home_form": "WDWDW",
            "away_form": "WLWDL",
            "h2h_home_wins": 4,
            "h2h_away_wins": 3,
            "h2h_draws": 3,
            "home_goals_scored": 10,
            "home_goals_conceded": 5,
            "away_goals_scored": 11,
            "away_goals_conceded": 9,
            "home_advantage": 1.08,
            "odds": {"home": 2.30, "draw": 3.20, "away": 3.20}
        },
        # 德甲
        {
            "id": 9,
            "league": "德甲",
            "home_team": "拜仁慕尼黑",
            "away_team": "多特蒙德",
            "home_form": "WWWDW",
            "away_form": "WWLWD",
            "h2h_home_wins": 6,
            "h2h_away_wins": 2,
            "h2h_draws": 2,
            "home_goals_scored": 18,
            "home_goals_conceded": 5,
            "away_goals_scored": 14,
            "away_goals_conceded": 10,
            "home_advantage": 1.15,
            "odds": {"home": 1.60, "draw": 4.20, "away": 5.00}
        },
        {
            "id": 10,
            "league": "德甲",
            "home_team": "勒沃库森",
            "away_team": "莱比锡",
            "home_form": "WWWWD",
            "away_form": "WDWDL",
            "h2h_home_wins": 4,
            "h2h_away_wins": 3,
            "h2h_draws": 3,
            "home_goals_scored": 16,
            "home_goals_conceded": 6,
            "away_goals_scored": 13,
            "away_goals_conceded": 8,
            "home_advantage": 1.10,
            "odds": {"home": 1.95, "draw": 3.60, "away": 3.60}
        },
        # 法甲
        {
            "id": 11,
            "league": "法甲",
            "home_team": "巴黎圣日耳曼",
            "away_team": "摩纳哥",
            "home_form": "WWWWW",
            "away_form": "WDWDL",
            "h2h_home_wins": 6,
            "h2h_away_wins": 2,
            "h2h_draws": 2,
            "home_goals_scored": 17,
            "home_goals_conceded": 6,
            "away_goals_scored": 12,
            "away_goals_conceded": 9,
            "home_advantage": 1.12,
            "odds": {"home": 1.50, "draw": 4.50, "away": 6.00}
        },
        {
            "id": 12,
            "league": "法甲",
            "home_team": "马赛",
            "away_team": "里尔",
            "home_form": "WDWDL",
            "away_form": "DWWWD",
            "h2h_home_wins": 3,
            "h2h_away_wins": 4,
            "h2h_draws": 3,
            "home_goals_scored": 11,
            "home_goals_conceded": 9,
            "away_goals_scored": 12,
            "away_goals_conceded": 7,
            "home_advantage": 1.05,
            "odds": {"home": 2.40, "draw": 3.30, "away": 2.90}
        },
        # 欧冠/其他
        {
            "id": 13,
            "league": "欧冠",
            "home_team": "曼城",
            "away_team": "皇马",
            "home_form": "WWWWW",
            "away_form": "WWWDW",
            "h2h_home_wins": 3,
            "h2h_away_wins": 3,
            "h2h_draws": 4,
            "home_goals_scored": 16,
            "home_goals_conceded": 4,
            "away_goals_scored": 15,
            "away_goals_conceded": 6,
            "home_advantage": 1.08,
            "odds": {"home": 1.85, "draw": 3.80, "away": 3.80}
        },
        {
            "id": 14,
            "league": "欧联",
            "home_team": "利物浦",
            "away_team": "勒沃库森",
            "home_form": "WWWWW",
            "away_form": "WWWWD",
            "h2h_home_wins": 2,
            "h2h_away_wins": 1,
            "h2h_draws": 1,
            "home_goals_scored": 15,
            "home_goals_conceded": 4,
            "away_goals_scored": 14,
            "away_goals_conceded": 5,
            "home_advantage": 1.10,
            "odds": {"home": 1.70, "draw": 3.80, "away": 4.80}
        }
    ]
    
    return matches


def calculate_probabilities(match):
    """计算胜平负概率"""
    
    # 基础权重
    form_weight = 0.25
    h2h_weight = 0.20
    home_advantage_weight = 0.20
    goals_weight = 0.15
    odds_weight = 0.20
    
    # 1. 近期状态分析 (近5场积分占比)
    def form_to_points(form):
        return sum(3 if c == 'W' else (1 if c == 'D' else 0) for c in form)
    
    home_form_points = form_to_points(match['home_form'])
    away_form_points = form_to_points(match['away_form'])
    form_diff = (home_form_points - away_form_points) / 15  # 标准化到 -1 ~ 1
    
    # 2. 历史对战
    total_h2h = match['h2h_home_wins'] + match['h2h_away_wins'] + match['h2h_draws']
    if total_h2h > 0:
        h2h_home_prob = match['h2h_home_wins'] / total_h2h
        h2h_away_prob = match['h2h_away_wins'] / total_h2h
        h2h_draw_prob = match['h2h_draws'] / total_h2h
    else:
        h2h_home_prob, h2h_away_prob, h2h_draw_prob = 0.4, 0.3, 0.3
    
    # 3. 主客场优势
    home_boost = (match['home_advantage'] - 1) * 0.5  # 转换为主队优势系数
    
    # 4. 进球数据
    home_attack = match['home_goals_scored'] / 5  # 场均进球
    home_defense = 1 - (match['home_goals_conceded'] / 10)  # 防守评分
    away_attack = match['away_goals_scored'] / 5
    away_defense = 1 - (match['away_goals_conceded'] / 10)
    
    home_strength = home_attack * 0.5 + home_defense * 0.5
    away_strength = away_attack * 0.5 + away_defense * 0.5
    strength_diff = (home_strength - away_strength) * 0.3
    
    # 5. 赔率隐含概率
    home_odds = match['odds']['home']
    draw_odds = match['odds']['draw']
    away_odds = match['odds']['away']
    
    margin = 1/home_odds + 1/draw_odds + 1/away_odds
    implied_home = (1/home_odds) / margin
    implied_draw = (1/draw_odds) / margin
    implied_away = (1/away_odds) / margin
    
    # 综合计算
    home_prob = (
        (0.5 + form_diff * 0.3) * form_weight +
        h2h_home_prob * h2h_weight +
        (0.5 + home_boost) * home_advantage_weight +
        (0.5 + strength_diff) * goals_weight +
        implied_home * odds_weight
    )
    
    away_prob = (
        (0.5 - form_diff * 0.3) * form_weight +
        h2h_away_prob * h2h_weight +
        (0.5 - home_boost * 0.3) * home_advantage_weight +
        (0.5 - strength_diff) * goals_weight +
        implied_away * odds_weight
    )
    
    draw_prob = (
        h2h_draw_prob * (h2h_weight + form_weight) +
        implied_draw * (odds_weight + goals_weight + home_advantage_weight)
    )
    
    # 归一化
    total = home_prob + draw_prob + away_prob
    home_prob /= total
    draw_prob /= total
    away_prob /= total
    
    return {
        'home': home_prob,
        'draw': draw_prob,
        'away': away_prob
    }


def get_recommendation(probs, odds):
    """获取推荐"""
    max_prob = max(probs.values())
    
    # 计算期望值
    home_ev = probs['home'] * odds['home'] - 1
    draw_ev = probs['draw'] * odds['draw'] - 1
    away_ev = probs['away'] * odds['away'] - 1
    
    evs = {'3': home_ev, '1': draw_ev, '0': away_ev}
    best_ev = max(evs.values())
    
    if probs['home'] > probs['draw'] and probs['home'] > probs['away']:
        pick = '3'
        pick_name = '主胜'
        confidence = probs['home']
    elif probs['away'] > probs['home'] and probs['away'] > probs['draw']:
        pick = '0'
        pick_name = '客胜'
        confidence = probs['away']
    else:
        pick = '1'
        pick_name = '平局'
        confidence = probs['draw']
    
    # 双选建议
    double_chance = None
    if probs['home'] + probs['draw'] > 0.65:
        double_chance = '31 (不败)'
    elif probs['away'] + probs['draw'] > 0.65:
        double_chance = '01 (不败)'
    
    return {
        'pick': pick,
        'pick_name': pick_name,
        'confidence': confidence,
        'ev': evs[pick],
        'double_chance': double_chance
    }


def print_14_matches_recommendation():
    """打印14场推荐"""
    matches = generate_14_matches()
    
    print("=" * 80)
    print("🏆 14场足彩胜平负推荐")
    print("=" * 80)
    print(f"{'场次':<4} {'联赛':<6} {'对阵':<30} {'胜':<8} {'平':<8} {'负':<8} {'推荐':<6} {'信心':<6}")
    print("-" * 80)
    
    picks = []
    double_picks = []
    
    for match in matches:
        probs = calculate_probabilities(match)
        rec = get_recommendation(probs, match['odds'])
        picks.append(rec['pick'])
        
        home_name = match['home_team'][:12]
        away_name = match['away_team'][:12]
        vs_str = f"{home_name} vs {away_name}"
        
        # 信心度颜色
        conf_str = f"{rec['confidence']*100:.0f}%"
        
        print(f"{match['id']:<4} {match['league']:<6} {vs_str:<30} "
              f"{probs['home']*100:>6.1f}%  {probs['draw']*100:>6.1f}%  {probs['away']*100:>6.1f}%  "
              f"{rec['pick']:<6} {conf_str:<6}")
        
        if rec['double_chance']:
            double_picks.append((match['id'], rec['double_chance']))
    
    print("=" * 80)
    
    # 单式推荐
    print("\n🎯 单式推荐 (14场):")
    print(" ".join(picks))
    
    # 复式建议
    print("\n🔀 复式建议:")
    if double_picks:
        print("以下场次可考虑双选:")
        for idx, dc in double_picks:
            print(f"  第{idx:2d}场: {dc}")
    
    # 信心场次
    high_conf = []
    for match in matches:
        probs = calculate_probabilities(match)
        rec = get_recommendation(probs, match['odds'])
        if rec['confidence'] >= 0.55:
            high_conf.append((match['id'], match['home_team'], match['away_team'], rec['pick_name'], rec['confidence']))
    
    print(f"\n⭐ 高信心场次 (≥55%): {len(high_conf)} 场")
    for idx, home, away, pick, conf in high_conf[:5]:
        print(f"  第{idx}场: {home} vs {away} → {pick} ({conf*100:.0f}%)")
    
    # 风险提示
    print("\n" + "=" * 80)
    print("⚠️ 重要提示:")
    print("  • 以上分析基于模拟数据和算法模型")
    print("  • 实际投注请结合最新伤停、天气等临场信息")
    print("  • 足球比赛具有不确定性，请理性购彩")
    print("  • 建议小额娱乐，量力而行")
    print("=" * 80)


if __name__ == "__main__":
    print_14_matches_recommendation()
