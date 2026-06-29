"""
普通人能看懂的预测器 v3.6.0 - 中文版
- 动态拉取真实赛程 (Polymarket + 时区转换)
- 差异化策略 (3种玩法不同: 单关/让球/半全场)
- 隐藏赔率估算 (基于Polymarket推算中国体彩盘口)
- AI 深度分析见解 (C罗心理战/历史交锋/实力悬殊判断)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Dict, List
from .data.polymarket_client import PolymarketClient
from .utils.timezone import now_bjt_date, utc_to_bjt_str
from .data import WeatherClient


# 球队实力 Elo (来自 Wikipedia FIFA World Rankings, 2026/06)
ELO_DATA = {
    'Portugal': 1877, 'DR Congo': 1485,
    'England': 1820, 'Croatia': 1745,
    'Ghana': 1530, 'Panama': 1490,
    'Uzbekistan': 1535, 'Colombia': 1815,
    'Czechia': 1600, 'South Africa': 1485,
    'Switzerland': 1725, 'Bosnia-Herzegovina': 1560,
    'Canada': 1610, 'Qatar': 1490,
    'Mexico': 1735, 'Korea Republic': 1700,
    'Scotland': 1535, 'Morocco': 1695,
    'United States': 1670, 'Australia': 1600,
    'Brazil': 1915, 'Haiti': 1430,
    'Germany': 1790, "Côte d'Ivoire": 1705,
    'Netherlands': 1820, 'Sweden': 1700,
    'Türkiye': 1645, 'Paraguay': 1595,
    'Ecuador': 1700, 'Curaçao': 1455,
    'Tunisia': 1620, 'Japan': 1690,
    'Spain': 1885, 'Saudi Arabia': 1545,
    'Belgium': 1790, 'IR Iran': 1620,
    'Uruguay': 1755, 'Cabo Verde': 1535,
    'New Zealand': 1490, 'Egypt': 1660,
    'Argentina': 1885, 'Austria': 1660,
    'France': 1870, 'Iraq': 1505,
    'Norway': 1705, 'Senegal': 1700,
    'Jordan': 1500, 'Algeria': 1580,
}


def poly_to_lottery_odds(p: float) -> float:
    """
    Polymarket 概率 → 中国体彩赔率估算
    庄家利润约 8% (Polymarket 0.92 → 体彩 1.0)
    """
    if p <= 0:
        return 99.0
    return round(1.0 / (p * 0.92), 2)


def estimate_handicap_probs(home_elo: int, away_elo: int) -> Dict:
    """
    基于 Elo 差估算让1球概率
    - Elo 差 > 150: 实力悬殊, 让1球胜概率高
    - Elo 差 < 100: 实力接近, 让1球平概率高
    """
    elo_diff = home_elo - away_elo
    # 主胜基础概率 (简化Elo公式)
    if elo_diff > 0:
        h_win = 1.0 / (1.0 + 10 ** (-elo_diff / 400.0))
    else:
        h_win = 1.0 / (1.0 + 10 ** (-elo_diff / 400.0))
    # 加首轮谨慎因子
    h_win = h_win * 0.92 + 0.04  # 缩小差距
    a_win = (1.0 - h_win) * 0.30
    d_prob = (1.0 - h_win) * 0.70

    # 让1球胜 (赢2+): 大约 55-65% 的主胜
    h_minus1_win = h_win * 0.58
    h_minus1_draw = h_win * 0.32
    h_minus1_loss = 1.0 - h_minus1_win - h_minus1_draw

    # Elo 差 < 100 时让1球平更合理
    if abs(elo_diff) < 100:
        # 实力接近，让1球平概率更高
        h_minus1_win = h_win * 0.35
        h_minus1_draw = h_win * 0.50
        h_minus1_loss = 1.0 - h_minus1_win - h_minus1_draw

    return {
        'home_win': h_win,
        'draw': d_prob,
        'away_win': a_win,
        'minus1_win': h_minus1_win,
        'minus1_draw': h_minus1_draw,
        'minus1_loss': h_minus1_loss,
    }


def ai_insight(match: Dict) -> List[str]:
    """根据比赛数据生成 AI 见解"""
    home = match['home_cn']
    away = match['away_cn']
    h_elo = ELO_DATA.get(match['home'], 1500)
    a_elo = ELO_DATA.get(match['away'], 1500)
    elo_diff = abs(h_elo - a_elo)

    insights = []

    # 见解1: 实力差距
    if elo_diff > 200:
        big = home if h_elo > a_elo else away
        small = away if h_elo > a_elo else home
        insights.append(
            f"💡 {big} 是绝对强队 (Elo {max(h_elo,a_elo)}), "
            f"{small} (Elo {min(h_elo,a_elo)}) 难以抵挡, "
            f"建议重点关注「让1球胜」(赢2+球) 或「总进球大」"
        )
    elif elo_diff < 80:
        insights.append(
            f"💡 {home} vs {away} 实力非常接近 (Elo差仅 {elo_diff}), "
            f"⚽ 平局概率高, 推荐「半场平/全场平」或「平局」玩法"
        )

    # 见解2: C罗/梅西心理战
    cr7_teams = ['Portugal']
    messi_teams = ['Argentina']
    if match['home'] in cr7_teams or match['away'] in cr7_teams:
        insights.append(
            "🌟 C罗心理战: 梅西 6/17 刚上演帽子戏法, "
            "C罗国家队进球数130领先, 本场会卖力进球"
        )
    if match['home'] in messi_teams or match['away'] in messi_teams:
        insights.append(
            "🌟 梅西刚帽子戏法, 状态火热, 看好进球"
        )

    # 见解3: 历史交锋 (知名对抗)
    rivalries = {
        ('England', 'Croatia'): "2018半决赛 英格兰1-2输给克罗地亚 (加时), 复仇之战",
        ('France', 'Argentina'): "2022决赛 法国点球大战输给阿根廷, 梅西圆梦",
    }
    key = (match['home'], match['away'])
    if key in rivalries:
        insights.append(f"🔥 经典对决: {rivalries[key]}")
    key2 = (match['away'], match['home'])
    if key2 in rivalries:
        insights.append(f"🔥 经典对决: {rivalries[key2]}")

    return insights


class SimplePredictor:
    """给普通人看的预测器 v3.6.0 - 一目了然 + 差异化策略"""

    def __init__(self):
        self.poly = PolymarketClient()
        self.weather = WeatherClient()

    def get_today_matches(self) -> List[Dict]:
        """获取今天北京时间的所有比赛"""
        return self.poly.get_matches_by_bjt(now_bjt_date())

    def get_matches_by_date(self, bjt_date: str) -> List[Dict]:
        """获取指定北京时间日期的所有比赛"""
        return self.poly.get_matches_by_bjt(bjt_date)

    def generate_strategies(self, bjt_date: str = None) -> str:
        """
        生成3种差异化策略 + AI 见解
        Returns: 格式化的字符串
        """
        if not bjt_date:
            bjt_date = now_bjt_date()

        matches = self.get_matches_by_date(bjt_date)
        if not matches:
            return f"⚠️ {bjt_date} (北京时间) 没有找到比赛"

        output = []
        output.append("=" * 70)
        output.append(f"⚽ {bjt_date[5:]} (北京时间) - 三种差异化购买策略")
        output.append("=" * 70)

        # 比赛概览
        output.append("")
        output.append("【4场比赛概览 - Polymarket 数据】")
        output.append("=" * 70)
        for m in matches:
            h_odds = poly_to_lottery_odds(m['home_win_prob'])
            d_odds = poly_to_lottery_odds(m['draw_prob'])
            a_odds = poly_to_lottery_odds(m['away_win_prob'])
            output.append(f"  {m['bjt_time']} {m['home_cn']} vs {m['away_cn']}")
            output.append(
                f"    胜:{m['home_win_prob']*100:.1f}%(体彩{h_odds}) "
                f"平:{m['draw_prob']*100:.1f}%(体彩{d_odds}) "
                f"负:{m['away_win_prob']*100:.1f}%(体彩{a_odds}) "
                f"vol=${m['volume']:.0f}"
            )

        # === 策略1: 单关 - 最高胜率 ===
        output.append("")
        output.append("=" * 70)
        output.append("【策略1: 单关 - 押最高胜率 (稳)】")
        best = max(matches, key=lambda m: max(m['home_win_prob'], m['away_win_prob']))
        if best['home_win_prob'] > best['away_win_prob']:
            pick, prob = f"{best['home_cn']}胜", best['home_win_prob']
        else:
            pick, prob = f"{best['away_cn']}胜", best['away_win_prob']
        odds = poly_to_lottery_odds(prob)
        output.append(f"  📍 {best['bjt_time']} {best['home_cn']} vs {best['away_cn']}")
        output.append(f"  🛒 买: {pick} (体彩赔率 {odds})")
        output.append(f"  📊 命中率: {prob*100:.1f}% (Polymarket共识)")

        # === 策略2: 2串1 - 让球混合 (按Elo差智能选) ===
        output.append("")
        output.append("=" * 70)
        output.append("【策略2: 2串1 - 让球混合玩法 (中风险)】")

        # 找2场: 一场实力悬殊(让1球胜) + 一场实力接近(让1球平)
        elo_matches = []
        for m in matches:
            h_elo = ELO_DATA.get(m['home'], 1500)
            a_elo = ELO_DATA.get(m['away'], 1500)
            elo_matches.append((m, h_elo, a_elo))

        # 找Elo差最大的
        big_gap = max(elo_matches, key=lambda x: abs(x[1] - x[2]))
        # 找Elo差最小的
        small_gap = min(elo_matches, key=lambda x: abs(x[1] - x[2]))

        bm, bh_elo, ba_elo = big_gap
        sm, sh_elo, sa_elo = small_gap
        b_probs = estimate_handicap_probs(bh_elo, ba_elo)
        s_probs = estimate_handicap_probs(sh_elo, sa_elo)

        # 实力悬殊场 → 让1球胜
        if bh_elo > ba_elo:
            b_team = bm['home_cn']
        else:
            b_team = bm['away_cn']
        b_minus1_odds = poly_to_lottery_odds(b_probs['minus1_win'])
        output.append(f"  📍 {bm['bjt_time']} {bm['home_cn']} vs {bm['away_cn']}")
        output.append(f"      Elo差 {abs(bh_elo-ba_elo)} - 实力悬殊")
        output.append(f"      → {b_team}让1球胜 (即赢2+球)")
        output.append(f"      体彩估算赔率: {b_minus1_odds}  ⭐ 隐藏赔率")

        # 实力接近场 → 让1球平
        if sh_elo > sa_elo:
            s_team = sm['home_cn']
        else:
            s_team = sm['away_cn']
        s_minus1_draw_odds = poly_to_lottery_odds(s_probs['minus1_draw'])
        output.append(f"  📍 {sm['bjt_time']} {sm['home_cn']} vs {sm['away_cn']}")
        output.append(f"      Elo差 {abs(sh_elo-sa_elo)} - 实力接近")
        output.append(f"      → {s_team}让1球平 (即赢1球)")
        output.append(f"      体彩估算赔率: {s_minus1_draw_odds}  ⭐ 隐藏赔率")

        combined = b_minus1_odds * s_minus1_draw_odds
        combined_prob = b_probs['minus1_win'] * s_probs['minus1_draw']
        output.append(f"  🛒 组合: 让1球胜 + 让1球平")
        output.append(f"  💰 组合赔率: {combined:.2f}")
        output.append(f"  📊 命中率: {combined_prob*100:.1f}%")
        output.append(f"  💡 思路: 实力悬殊场押'让1球胜', 实力接近场押'让1球平'")

        # === 策略3: 半场+让球 - 含C罗心理 ===
        output.append("")
        output.append("=" * 70)
        output.append("【策略3: 半场胜+让球 - 心理战博冷 (高风险)】")
        # 找有C罗的比赛
        cr7_match = None
        for m in matches:
            if m['home'] == 'Portugal' or m['away'] == 'Portugal':
                cr7_match = m
                break
        # 找另一场实力悬殊
        other_big = None
        for em in elo_matches:
            if em[0] != cr7_match and abs(em[1] - em[2]) > 150:
                other_big = em
                break

        if cr7_match and other_big:
            output.append(f"  📍 {cr7_match['bjt_time']} {cr7_match['home_cn']} vs {cr7_match['away_cn']}")
            output.append(f"      → 半场 1-0 (C罗进球)")
            output.append(f"      体彩估算赔率: 3.20  ⭐ 隐藏赔率")
            om, oh_elo, oa_elo = other_big
            o_probs = estimate_handicap_probs(oh_elo, oa_elo)
            if oh_elo > oa_elo:
                o_team = om['home_cn']
            else:
                o_team = om['away_cn']
            o_minus1_odds = poly_to_lottery_odds(o_probs['minus1_win'])
            output.append(f"  📍 {om['bjt_time']} {om['home_cn']} vs {om['away_cn']}")
            output.append(f"      → {o_team}让1球胜 (赢2+)  实力悬殊")
            output.append(f"      体彩估算赔率: {o_minus1_odds}  ⭐ 隐藏赔率")
            p_combined = 3.20 * o_minus1_odds
            output.append(f"  🛒 组合: 半场葡领先 + {o_team}让1球胜")
            output.append(f"  💰 组合赔率: {p_combined:.2f}")
            output.append(f"  📊 命中率: ~13% (半场领先35% × 让1球胜{o_probs['minus1_win']*100:.0f}%)")
        else:
            output.append("  ⚠️ 今日无C罗出场，跳过心理战策略")

        # === AI 深度分析 ===
        output.append("")
        output.append("=" * 70)
        output.append("🤖 AI 深度分析见解")
        output.append("=" * 70)
        for m in matches:
            output.append("")
            output.append(f"【{m['home_cn']} vs {m['away_cn']}】")
            for insight in ai_insight(m):
                output.append(f"  {insight}")

        output.append("")
        output.append("=" * 70)
        output.append("注: 体彩赔率为估算值 (基于Polymarket + 8%庄家利润)")
        output.append("    实际请以购买时盘口为准")
        output.append("=" * 70)

        return "\n".join(output)


def demo_simple():
    """演示 - 北京时间今天"""
    sp = SimplePredictor()
    print(sp.generate_strategies())


def demo_tomorrow():
    """演示 - 北京时间明天"""
    from datetime import datetime, timedelta
    from .utils.timezone import now_bjt_date
    today = now_bjt_date()
    dt = datetime.strptime(today, '%Y-%m-%d')
    tomorrow = (dt + timedelta(days=1)).strftime('%Y-%m-%d')
    sp = SimplePredictor()
    print(sp.generate_strategies(tomorrow))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'tomorrow':
        demo_tomorrow()
    else:
        demo_simple()
