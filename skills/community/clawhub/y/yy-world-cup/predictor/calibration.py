"""
市场赔率校准模块
对比模型预测概率 vs Polymarket市场隐含概率，生成套利机会报告

核心功能:
1. 套利机会检测（edge > 5%）
2. 跨市场对比（Polymarket vs 中国体彩）
3. 实时赔率校准
4. 风险等级评估
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EdgeLevel(Enum):
    """套利机会等级"""
    NONE = "无机会"
    LOW = "低 (5-10%)"
    MEDIUM = "中 (10-20%)"
    HIGH = "高 (20-30%)"
    EXTREME = "极高 (>30%)"


@dataclass
class ArbitrageOpportunity:
    """套利机会"""
    match: str
    market_type: str           # 'moneyline' / 'spread' / 'total' / 'world_cup_winner'
    outcome: str               # 'home' / 'draw' / 'away' / 具体比分
    model_prob: float          # 模型预测概率 (0-1)
    market_prob: float         # 市场隐含概率 (0-1)
    edge: float                # 差值 (model - market)
    edge_pct: float            # 差值百分比
    edge_level: EdgeLevel
    suggested_action: str      # 'BUY' / 'SELL' / 'HOLD'
    confidence: str            # '高' / '中' / '低'
    volume: Optional[float] = None  # 交易量


@dataclass
class CalibrationReport:
    """校准报告"""
    timestamp: str
    opportunities: List[ArbitrageOpportunity]
    polymarket_winner_odds: Dict[str, float]  # 球队→概率
    summary: Dict


class MarketCalibrator:
    """市场赔率校准器"""

    # 套利机会阈值
    EDGE_THRESHOLDS = {
        EdgeLevel.LOW: 0.05,
        EdgeLevel.MEDIUM: 0.10,
        EdgeLevel.HIGH: 0.20,
        EdgeLevel.EXTREME: 0.30,
    }

    def __init__(self, polymarket_client=None):
        """
        Args:
            polymarket_client: PolymarketClient实例，None则自动创建
        """
        if polymarket_client is None:
            from .data.polymarket_client import PolymarketClient
            self.polymarket = PolymarketClient()
        else:
            self.polymarket = polymarket_client

    def classify_edge(self, edge_abs: float) -> EdgeLevel:
        """根据edge大小分类"""
        if edge_abs >= self.EDGE_THRESHOLDS[EdgeLevel.EXTREME]:
            return EdgeLevel.EXTREME
        elif edge_abs >= self.EDGE_THRESHOLDS[EdgeLevel.HIGH]:
            return EdgeLevel.HIGH
        elif edge_abs >= self.EDGE_THRESHOLDS[EdgeLevel.MEDIUM]:
            return EdgeLevel.MEDIUM
        elif edge_abs >= self.EDGE_THRESHOLDS[EdgeLevel.LOW]:
            return EdgeLevel.LOW
        return EdgeLevel.NONE

    def find_world_cup_winner_arb(
        self, model_probs: Dict[str, float]
    ) -> List[ArbitrageOpportunity]:
        """
        对比模型冠军预测 vs Polymarket市场
        Args:
            model_probs: 球队→模型概率，如 {'France': 0.20, 'Spain': 0.18, ...}
        Returns:
            套利机会列表
        """
        try:
            market = self.polymarket.get_world_cup_winner()
            market_probs = market.get('teams', {})
        except Exception as e:
            print(f"获取Polymarket冠军赔率失败: {e}")
            return []

        opportunities = []
        from datetime import datetime
        timestamp = datetime.now().isoformat()

        # 对比每个球队
        all_teams = set(model_probs.keys()) | set(market_probs.keys())
        for team in all_teams:
            model_p = model_probs.get(team, 0)
            market_p = market_probs.get(team, 0)
            edge = model_p - market_p
            edge_abs = abs(edge)
            edge_level = self.classify_edge(edge_abs)

            if edge_level == EdgeLevel.NONE:
                continue

            # 建议操作
            if edge > 0:
                # 模型认为被低估→买入YES
                action = "BUY YES (模型高于市场)"
                confidence = "高" if edge_abs > 0.10 else "中"
            else:
                # 模型认为被高估→卖出YES/买入NO
                action = "BUY NO (模型低于市场)"
                confidence = "高" if edge_abs > 0.10 else "中"

            opportunities.append(ArbitrageOpportunity(
                match="2026 FIFA World Cup Winner",
                market_type="world_cup_winner",
                outcome=team,
                model_prob=model_p,
                market_prob=market_p,
                edge=edge,
                edge_pct=edge_abs * 100,
                edge_level=edge_level,
                suggested_action=action,
                confidence=confidence,
                volume=market.get('volume'),
            ))

        return opportunities

    def find_match_arb(
        self, match_name: str, model_probs: Dict[str, float],
        team_a: str, team_b: str,
        market_volume: Optional[float] = None
    ) -> List[ArbitrageOpportunity]:
        """
        对比单场比赛模型 vs Polymarket
        Args:
            match_name: 比赛名
            model_probs: 模型预测 {'home': 0.6, 'draw': 0.25, 'away': 0.15}
            team_a: 主队名
            team_b: 客队名
            market_volume: 市场交易量（可选）
        Returns:
            套利机会列表
        """
        try:
            market_data = self.polymarket.get_match_implied_prob(team_a, team_b)
            if not market_data or not market_data.get('moneyline'):
                return []

            ml = market_data['moneyline']
            # Polymarket的moneyline是2-way (没有平局) 或 3-way
            market_probs = {
                'home': ml.get(team_a, 0.5),
                'away': ml.get(team_b, 0.5),
            }
            # 如果是3-way，提取draw
            draw_key = 'Draw'
            if draw_key in ml:
                market_probs['draw'] = ml[draw_key]
        except Exception as e:
            print(f"获取Polymarket比赛赔率失败: {e}")
            return []

        opportunities = []
        for outcome in ['home', 'draw', 'away']:
            if outcome not in model_probs or outcome not in market_probs:
                continue
            model_p = model_probs[outcome]
            market_p = market_probs[outcome]
            edge = model_p - market_p
            edge_abs = abs(edge)
            edge_level = self.classify_edge(edge_abs)

            if edge_level == EdgeLevel.NONE:
                continue

            if edge > 0:
                action = f"BUY YES (模型{outcome}概率{edge*100:+.1f}%)"
                confidence = "高" if edge_abs > 0.10 else "中"
            else:
                action = f"BUY NO (市场{outcome}概率{-edge*100:+.1f}%)"
                confidence = "高" if edge_abs > 0.10 else "中"

            outcome_name = {'home': team_a, 'draw': '平局', 'away': team_b}[outcome]
            opportunities.append(ArbitrageOpportunity(
                match=match_name,
                market_type="moneyline",
                outcome=outcome_name,
                model_prob=model_p,
                market_prob=market_p,
                edge=edge,
                edge_pct=edge_abs * 100,
                edge_level=edge_level,
                suggested_action=action,
                confidence=confidence,
                volume=market_volume,
            ))

        return opportunities

    def compare_with_chinese_lottery(
        self,
        match_name: str,
        model_probs: Dict[str, float],
        cn_odds: Dict[str, float],
    ) -> List[ArbitrageOpportunity]:
        """
        与中国体彩赔率对比找套利
        Args:
            match_name: 比赛名
            model_probs: 模型 {'home': 0.6, 'draw': 0.25, 'away': 0.15}
            cn_odds: 体彩赔率 {'胜': 1.33, '平': 4.15, '负': 7.30}
        Returns:
            跨市场套利机会
        """
        # 体彩隐含概率 = 1/赔率（去除庄家利润前）
        # 实际庄家利润率约15-20%，所以真实概率 ≈ 0.85/赔率
        opportunities = []

        outcome_map = {'home': '胜', 'draw': '平', 'away': '负'}
        outcome_name_map = {'home': '主胜', 'draw': '平局', 'away': '客胜'}

        for outcome_key, odds_key in outcome_map.items():
            if outcome_key not in model_probs or odds_key not in cn_odds:
                continue
            model_p = model_probs[outcome_key]
            cn_odd = cn_odds[odds_key]
            cn_implied = 1.0 / cn_odd
            # 调整庄家利润（庄家抽水约15%）
            cn_implied_adj = cn_implied * 0.85

            # 体彩EV
            cn_ev = model_p * cn_odd - 1

            # 体彩隐含概率 vs 模型
            edge = model_p - cn_implied_adj
            edge_abs = abs(edge)
            edge_level = self.classify_edge(edge_abs)

            if edge_level == EdgeLevel.NONE and cn_ev < 0.05:
                continue

            if cn_ev > 0.05:
                action = f"体彩买入{outcome_name_map[outcome_key]} EV={cn_ev*100:+.1f}%"
                confidence = "高" if cn_ev > 0.20 else "中"
                opportunities.append(ArbitrageOpportunity(
                    match=f"{match_name} (中国体彩)",
                    market_type="cn_sporttery",
                    outcome=outcome_name_map[outcome_key],
                    model_prob=model_p,
                    market_prob=cn_implied_adj,
                    edge=edge,
                    edge_pct=edge_abs * 100,
                    edge_level=EdgeLevel.HIGH if cn_ev > 0.20 else EdgeLevel.MEDIUM,
                    suggested_action=action,
                    confidence=confidence,
                ))

        return opportunities

    def generate_report(
        self,
        model_winner_probs: Dict[str, float] = None,
        match_calibrations: List[Dict] = None,
    ) -> CalibrationReport:
        """
        生成综合校准报告
        Args:
            model_winner_probs: 模型冠军预测
            match_calibrations: 比赛校准数据
                [{'match': 'France vs Senegal', 'model_probs': {...},
                  'team_a': 'France', 'team_b': 'Senegal'}, ...]
        Returns:
            完整校准报告
        """
        from datetime import datetime
        opportunities = []

        # 1. 冠军市场校准
        polymarket_winner_odds = {}
        if model_winner_probs:
            winner_arb = self.find_world_cup_winner_arb(model_winner_probs)
            opportunities.extend(winner_arb)
            try:
                market = self.polymarket.get_world_cup_winner()
                polymarket_winner_odds = market.get('teams', {})
            except:
                pass

        # 2. 单场比赛校准
        if match_calibrations:
            for mc in match_calibrations:
                match_arb = self.find_match_arb(
                    mc['match'],
                    mc['model_probs'],
                    mc.get('team_a', ''),
                    mc.get('team_b', ''),
                    mc.get('volume'),
                )
                opportunities.extend(match_arb)

        # 按edge排序
        opportunities.sort(key=lambda x: abs(x.edge), reverse=True)

        # 统计
        high_edge = sum(1 for o in opportunities if o.edge_level in [EdgeLevel.HIGH, EdgeLevel.EXTREME])
        medium_edge = sum(1 for o in opportunities if o.edge_level == EdgeLevel.MEDIUM)

        report = CalibrationReport(
            timestamp=datetime.now().isoformat(),
            opportunities=opportunities,
            polymarket_winner_odds=polymarket_winner_odds,
            summary={
                'total_opportunities': len(opportunities),
                'high_edge_count': high_edge,
                'medium_edge_count': medium_edge,
                'best_opportunity': opportunities[0] if opportunities else None,
            },
        )
        return report

    @staticmethod
    def format_report(report: CalibrationReport) -> str:
        """格式化报告输出"""
        lines = ["=" * 90]
        lines.append("📊 市场赔率校准报告（Polymarket vs 中国体彩）")
        lines.append("=" * 90)
        lines.append(f"⏰ 报告时间: {report.timestamp}")
        lines.append(f"\n📈 套利机会总数: {report.summary['total_opportunities']}")
        lines.append(f"   高EV机会 (>20%): {report.summary['high_edge_count']}")
        lines.append(f"   中EV机会 (10-20%): {report.summary['medium_edge_count']}")

        if report.polymarket_winner_odds:
            lines.append(f"\n🏆 Polymarket 2026世界杯冠军 Top 5:")
            for i, (team, prob) in enumerate(
                sorted(report.polymarket_winner_odds.items(), key=lambda x: x[1], reverse=True)[:5], 1
            ):
                lines.append(f"   {i}. {team:<20} {prob*100:>5.2f}%")

        if report.opportunities:
            lines.append(f"\n💰 套利机会排行（按Edge降序）:")
            lines.append(f"{'#':<3} {'比赛':<25} {'玩法':<8} {'选项':<12} {'模型%':<7} {'市场%':<7} {'Edge%':<7} {'等级':<8} {'建议'}")
            lines.append("-" * 130)
            for i, op in enumerate(report.opportunities[:20], 1):
                lines.append(
                    f"{i:<3} {op.match[:25]:<25} {op.market_type:<8} {op.outcome[:12]:<12} "
                    f"{op.model_prob*100:<7.1f} {op.market_prob*100:<7.1f} "
                    f"{op.edge_pct:<+7.1f} {op.edge_level.value:<8} {op.suggested_action}"
                )

        lines.append("=" * 90)
        return "\n".join(lines)


def test_calibrator():
    """测试校准器"""
    print("🧪 市场赔率校准测试")
    cal = MarketCalibrator()

    # 模拟模型冠军预测（基于FIFA排名+Elo估算）
    model_winner = {
        'France': 0.20,    # 模型比市场(17.65%)高
        'Spain': 0.13,     # 模型比市场(14.05%)低
        'Argentina': 0.10, # 模型比市场(9.25%)高
        'Brazil': 0.08,    # 模型比市场(6.65%)高
        'England': 0.09,
        'Portugal': 0.10,
        'Germany': 0.05,
    }

    report = cal.generate_report(model_winner_probs=model_winner)
    print(MarketCalibrator.format_report(report))


if __name__ == '__main__':
    test_calibrator()
