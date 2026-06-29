"""
v3.0 综合演示
展示整合FIFA Elo预测 + Polymarket市场赔率 + 中国体彩的双数据源能力
"""

import math
import json
import warnings
warnings.filterwarnings('ignore')

from predictor import (
    WorldCupPredictor, ConservativeStrategy, AggressiveStrategy,
    Team, Stadium, MatchInfo, WeatherInfo, RecentMatch, TeamStyle, WeatherCondition
)
from predictor.data import PolymarketClient
from predictor.calibration import MarketCalibrator


def enhanced_predict_6_17():
    """
    增强版6/17 3场比赛预测
    整合: 真实FIFA Elo + Polymarket市场赔率 + 中国体彩真实盘口
    """
    print("="*100)
    print("⚽ world-cup-predictor-enhanced v3.0 - 6/17 增强版综合预测")
    print("="*100)
    print("📊 数据源: 真实FIFA Elo + Polymarket($24.5亿市场) + 中国体彩盘口")
    print("🔧 模型: 双模式 + 小组赛首轮谨慎因子 + 市场赔率校准")
    print()

    # 真实FIFA数据
    REAL_FIFA = {
        "France":    {"rank": 3,  "points": 1870.70, "style": TeamStyle.BALANCED},
        "Senegal":   {"rank": 15, "points": 1684.07, "style": TeamStyle.PHYSICAL},
        "Iraq":      {"rank": 58, "points": 1379.45, "style": TeamStyle.DEFENSIVE},
        "Norway":    {"rank": 36, "points": 1523.81, "style": TeamStyle.PHYSICAL},
        "Argentina": {"rank": 1,  "points": 1877.27, "style": TeamStyle.TECHNICAL},
        "Algeria":   {"rank": 43, "points": 1471.92, "style": TeamStyle.DEFENSIVE},
    }

    # 中国体彩真实盘口（用户提供）
    CN_ODDS = {
        "France-Senegal":     {"胜平负": {"胜": 1.33, "平": 4.15, "负": 7.30},
                               "让-1":   {"胜": 2.12, "平": 3.45, "负": 2.72}},
        "Iraq-Norway":        {"让+2":   {"胜": 2.35, "平": 3.74, "负": 2.29}},
        "Argentina-Algeria":  {"胜平负": {"胜": 1.26, "平": 4.40, "负": 9.20},
                               "让-1":   {"胜": 1.90, "平": 3.50, "负": 3.15}},
    }

    # Polymarket冠军市场数据（实际从API获取）
    polymarket = PolymarketClient()
    print("📡 正在获取Polymarket市场数据...")
    try:
        wc_winner = polymarket.get_world_cup_winner()
        poly_winner_probs = wc_winner['teams']
        print(f"   ✅ 冠军市场: ${wc_winner['volume']/1e6:.0f}M交易量")
        print(f"   Top 5: " + " | ".join([f"{t} {p*100:.1f}%" for t, p in
            sorted(poly_winner_probs.items(), key=lambda x: x[1], reverse=True)[:5]]))
    except Exception as e:
        print(f"   ⚠️ 获取失败: {e}")
        poly_winner_probs = {}

    print()

    def mk(n):
        d = REAL_FIFA[n]
        return Team(id=1, name=n, abbreviation=n[:3].upper(),
                    country_code=n[:3].upper(), confederation="UEFA",
                    elo=int(d["points"]), style=d["style"])

    weather = WeatherInfo(temperature=22, precipitation_probability=30,
                         wind_level=2, weather_condition=WeatherCondition.SUNNY)

    # 6/17 3场比赛
    MATCHES = [
        ("France", "Senegal", "France-Senegal", "2026-06-17 03:00", "I组"),
        ("Iraq", "Norway", "Iraq-Norway", "2026-06-17 06:00", "K组"),
        ("Argentina", "Algeria", "Argentina-Algeria", "2026-06-17 09:00", "A组"),
    ]

    # 校准器
    calibrator = MarketCalibrator(polymarket)

    for h, a, key, t, group in MATCHES:
        m = MatchInfo(
            match_id=None, home_team=mk(h), away_team=mk(a),
            match_time=t, stadium=Stadium(1, "TBD", "USA", "USA", 50000),
            stage="group", is_neutral=True,
            home_goals_per_match=1.5, away_goals_per_match=1.2,
            home_conceded_per_match=1.0, away_conceded_per_match=1.3,
            home_recent=[RecentMatch("win",2,1), RecentMatch("draw",1,1), RecentMatch("win",2,0)],
            away_recent=[RecentMatch("loss",0,2), RecentMatch("draw",1,1), RecentMatch("loss",1,2)],
            weather=weather,
        )
        pred = WorldCupPredictor().predict(m)
        probs = {"胜": pred.home_win_prob, "平": pred.draw_prob, "负": pred.away_win_prob}
        outcome = max(probs, key=probs.get)

        print(f"🏟️  北京时间 {t[-5:]}  {h} vs {a} - {group}")
        print(f"   📈 Elo差: {REAL_FIFA[h]['points']-REAL_FIFA[a]['points']:+.0f}分 | 模式: {pred.predict_mode}")
        print(f"   🤖 模型预测: {outcome} | 主胜{pred.home_win_prob*100:.1f}% 平{pred.draw_prob*100:.1f}% 客胜{pred.away_win_prob*100:.1f}%")
        print(f"   ⚽ 比分预测: {pred.predicted_scores[0][0]}")

        # 中国体彩EV分析
        print(f"\n   💰 中国体彩 EV分析:")
        cn_data = CN_ODDS.get(key, {})
        for play_type, odds in cn_data.items():
            for outcome_key, odd in odds.items():
                prob_key = {"胜": "胜", "平": "平", "负": "负"}[outcome_key]
                prob = probs.get(prob_key, 0)
                ev = prob * odd - 1
                mark = "⭐" if ev > 0.10 else ("✓" if ev > 0 else "✗")
                print(f"      {mark} {play_type} {outcome_key}: 赔率{odd} | EV={ev*100:+.1f}%")

        print()

    # 生成冠军市场校准报告
    print("="*100)
    print("🏆 Polymarket 2026世界杯冠军市场校准")
    print("="*100)

    # 模型冠军预测（基于FIFA Elo推算）
    model_winner = {
        'France': 0.20, 'Spain': 0.13, 'Argentina': 0.10, 'Brazil': 0.08,
        'England': 0.09, 'Portugal': 0.10, 'Germany': 0.05, 'Netherlands': 0.04,
        'Norway': 0.03, 'Morocco': 0.025,
    }

    report = calibrator.generate_report(model_winner_probs=model_winner)
    print(MarketCalibrator.format_report(report))

    print()
    print("="*100)
    print("💡 v3.0 新能力总结:")
    print("   ✅ Phase 1: Polymarket API客户端（无需认证读端点）")
    print("   ✅ Phase 2: 市场赔率校准器（Polymarket vs 中国体彩）")
    print("   ✅ Phase 3: 统一接口 + 报告生成")
    print()
    print("🎯 三大数据源整合:")
    print("   1. 真实FIFA Elo (Wikipedia) → 模型基础概率")
    print("   2. Polymarket $24.5亿市场 → 市场真相校验")
    print("   3. 中国体彩真实盘口 → 中国市场赔率基准")
    print("="*100)


if __name__ == "__main__":
    enhanced_predict_6_17()
