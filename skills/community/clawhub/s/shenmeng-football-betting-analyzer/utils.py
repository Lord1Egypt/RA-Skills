#!/usr/bin/env python3
"""
工具函数模块 - 足彩分析助手
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


def format_team_form(form_string: str) -> str:
    """格式化球队战绩字符串"""
    emoji_map = {
        "W": "✅",
        "D": "➖", 
        "L": "❌"
    }
    return "".join([emoji_map.get(c, c) for c in form_string])


def calculate_stake(
    bankroll: float,
    confidence: float,
    odds: float,
    kelly_fraction: float = 0.25,
    max_stake_pct: float = 0.05
) -> Dict[str, float]:
    """
    计算建议投注金额
    
    Args:
        bankroll: 总资金
        confidence: 置信度 (0-1)
        odds: 赔率
        kelly_fraction: 凯利分数
        max_stake_pct: 单次最大投注比例
    
    Returns:
        包含不同策略投注金额的字典
    """
    # 固定比例法
    fixed_pct = 0.02  # 2%
    fixed_stake = bankroll * fixed_pct
    
    # 凯利公式
    p = confidence
    q = 1 - p
    b = odds - 1
    kelly_pct = (p * b - q) / b if b > 0 else 0
    kelly_pct = max(0, kelly_pct * kelly_fraction)
    kelly_stake = bankroll * min(kelly_pct, max_stake_pct)
    
    # 置信度加权
    confidence_stake = bankroll * (confidence * 0.03)  # 最高3%
    
    return {
        "fixed": round(fixed_stake, 2),
        "kelly": round(kelly_stake, 2),
        "confidence_weighted": round(confidence_stake, 2),
        "recommended": round(min(kelly_stake, confidence_stake, bankroll * max_stake_pct), 2)
    }


def generate_parlay_combinations(
    matches: List[Dict],
    max_matches: int = 3,
    min_confidence: float = 0.55
) -> List[Dict]:
    """
    生成串关组合
    
    Args:
        matches: 比赛列表，每项包含 prediction 和 confidence
        max_matches: 最大串关场数
        min_confidence: 最低置信度
    
    Returns:
        推荐的串关组合
    """
    # 筛选高置信度比赛
    qualified = [m for m in matches if m.get("confidence", 0) >= min_confidence]
    qualified.sort(key=lambda x: x.get("confidence", 0), reverse=True)
    
    combinations = []
    
    for n in range(2, min(max_matches + 1, len(qualified) + 1)):
        # 取前n场最高置信度的比赛
        selected = qualified[:n]
        
        # 计算组合赔率
        total_odds = 1.0
        for match in selected:
            # 根据推荐结果获取对应赔率
            rec = match.get("recommendation", "")
            if "主" in rec:
                odds = match.get("odds", {}).get("home", 1.5)
            elif "客" in rec:
                odds = match.get("odds", {}).get("away", 3.0)
            else:
                odds = match.get("odds", {}).get("draw", 3.2)
            total_odds *= odds
        
        combinations.append({
            "matches": selected,
            "total_odds": round(total_odds, 2),
            "avg_confidence": round(sum(m["confidence"] for m in selected) / len(selected), 3),
            "risk_level": "高" if total_odds > 5 else ("中" if total_odds > 2.5 else "低")
        })
    
    return combinations


def analyze_league_standings(standings_data: List[Dict]) -> Dict:
    """分析联赛积分榜"""
    if not standings_data:
        return {}
    
    top_team = standings_data[0]
    bottom_team = standings_data[-1]
    
    # 计算争冠/保级形势
    title_race = len([t for t in standings_data if t.get("points", 0) >= top_team.get("points", 0) - 6])
    relegation_battle = len([t for t in standings_data[-5:] if t.get("points", 0) - bottom_team.get("points", 0) <= 6])
    
    return {
        "leader": top_team.get("team", {}).get("name"),
        "leader_points": top_team.get("points"),
        "title_race_teams": title_race,
        "relegation_battle_teams": relegation_battle,
        "competitiveness": "激烈" if title_race > 3 or relegation_battle > 3 else "平稳"
    }


def get_injury_impact_score(injuries: List[Dict]) -> Tuple[int, str]:
    """
    计算伤病影响评分
    
    Returns:
        (评分0-10, 描述)
    """
    if not injuries:
        return 0, "无重大伤病"
    
    impact_score = 0
    key_players_out = 0
    
    for injury in injuries:
        player_rating = injury.get("player", {}).get("rating", 6.5)
        if player_rating > 7.0:  # 关键球员
            key_players_out += 1
            impact_score += 2
        else:
            impact_score += 1
    
    if impact_score >= 6:
        description = f"严重影响 ({key_players_out}名核心缺阵)"
    elif impact_score >= 3:
        description = f"中度影响 ({key_players_out}名核心缺阵)"
    else:
        description = f"轻微影响 ({len(injuries)}人)"
    
    return min(impact_score, 10), description


def format_analysis_report(analysis: Dict) -> str:
    """格式化分析报告为文本"""
    lines = []
    
    # 标题
    info = analysis.get("match_info", {})
    lines.append("=" * 60)
    lines.append(f"⚽ {info.get('home_team', 'Unknown')} vs {info.get('away_team', 'Unknown')}")
    lines.append(f"🏆 {info.get('league', 'Unknown')} | 📅 {info.get('date', 'Unknown')[:10]}")
    lines.append("=" * 60)
    
    # 近期状态
    home = analysis.get("home_analysis", {})
    away = analysis.get("away_analysis", {})
    lines.append("\n📊 近期状态 (近5场):")
    lines.append(f"  主队: {format_team_form(home.get('form_string', '?????'))} "
                f"({home.get('points', 0)}/15分)")
    lines.append(f"        进{home.get('goals_scored', 0)} 失{home.get('goals_conceded', 0)} "
                f"净{home.get('goal_diff', 0):+d}")
    lines.append(f"  客队: {format_team_form(away.get('form_string', '?????'))} "
                f"({away.get('points', 0)}/15分)")
    lines.append(f"        进{away.get('goals_scored', 0)} 失{away.get('goals_conceded', 0)} "
                f"净{away.get('goal_diff', 0):+d}")
    
    # 历史对战
    h2h = analysis.get("head_to_head", {})
    lines.append("\n📈 历史对战 (近10场):")
    lines.append(f"  主队胜: {h2h.get('home_wins', 0)} | "
                f"客队胜: {h2h.get('away_wins', 0)} | "
                f"平: {h2h.get('draws', 0)}")
    
    # 预测
    pred = analysis.get("prediction", {})
    probs = pred.get("probabilities", {})
    lines.append("\n🎯 预测结果:")
    lines.append(f"  主胜: {probs.get('home_win', 0)*100:.1f}%")
    lines.append(f"  平局: {probs.get('draw', 0)*100:.1f}%")
    lines.append(f"  客胜: {probs.get('away_win', 0)*100:.1f}%")
    lines.append(f"\n  ⭐ 推荐: {pred.get('recommendation', 'Unknown')} "
                f"(置信度: {pred.get('confidence', 0)*100:.1f}%)")
    
    if "analysis_summary" in pred:
        lines.append(f"\n📝 {pred['analysis_summary']}")
    
    # 风险提示
    lines.append("\n⚠️ 风险提示:")
    lines.append("  • 足球比赛具有不确定性，分析仅供参考")
    lines.append("  • 请理性购彩，量力而行")
    lines.append("  • 伤病、天气等临场因素可能影响结果")
    
    lines.append("=" * 60)
    return "\n".join(lines)


def save_analysis_to_file(analysis: Dict, filename: Optional[str] = None) -> str:
    """保存分析结果到文件"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"
    
    filepath = os.path.join(os.path.dirname(__file__), "outputs", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    return filepath


class BankrollManager:
    """资金管理器"""
    
    def __init__(self, initial_bankroll: float = 1000.0):
        self.bankroll = initial_bankroll
        self.initial_bankroll = initial_bankroll
        self.bets: List[Dict] = []
    
    def place_bet(self, match: str, selection: str, stake: float, odds: float) -> Dict:
        """记录投注"""
        if stake > self.bankroll:
            return {"error": "资金不足"}
        
        bet = {
            "match": match,
            "selection": selection,
            "stake": stake,
            "odds": odds,
            "potential_return": stake * odds,
            "timestamp": datetime.now().isoformat(),
            "settled": False
        }
        
        self.bets.append(bet)
        self.bankroll -= stake
        
        return {
            "success": True,
            "bet": bet,
            "remaining_bankroll": self.bankroll
        }
    
    def settle_bet(self, bet_index: int, won: bool) -> Dict:
        """结算投注"""
        if bet_index >= len(self.bets):
            return {"error": "投注不存在"}
        
        bet = self.bets[bet_index]
        if bet["settled"]:
            return {"error": "已结算"}
        
        bet["settled"] = True
        bet["won"] = won
        
        if won:
            profit = bet["stake"] * (bet["odds"] - 1)
            self.bankroll += bet["potential_return"]
            bet["profit"] = profit
        else:
            bet["profit"] = -bet["stake"]
        
        return {
            "bet": bet,
            "current_bankroll": self.bankroll,
            "total_profit": self.bankroll - self.initial_bankroll
        }
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        settled_bets = [b for b in self.bets if b.get("settled")]
        
        if not settled_bets:
            return {
                "total_bets": len(self.bets),
                "settled_bets": 0,
                "win_rate": 0,
                "profit": 0,
                "roi": 0
            }
        
        wins = len([b for b in settled_bets if b.get("won")])
        total_profit = sum(b.get("profit", 0) for b in settled_bets)
        total_staked = sum(b["stake"] for b in settled_bets)
        
        return {
            "total_bets": len(self.bets),
            "settled_bets": len(settled_bets),
            "wins": wins,
            "losses": len(settled_bets) - wins,
            "win_rate": round(wins / len(settled_bets) * 100, 1),
            "profit": round(total_profit, 2),
            "roi": round(total_profit / total_staked * 100, 2) if total_staked > 0 else 0,
            "current_bankroll": round(self.bankroll, 2)
        }


def print_usage_guide():
    """打印使用指南"""
    guide = """
🏆 足彩分析助手使用指南
========================

1. 基础分析
   python analyzer.py --demo
   
2. 分析指定比赛
   python analyzer.py --match 12345
   
3. 查看今日比赛
   python analyzer.py --today

4. 赔率分析
   python odds_analyzer.py

环境变量:
   export FOOTBALL_API_KEY="your_api_key"

API 来源:
   • API-Football (推荐): https://www.api-football.com/
   • Football-Data.org: https://www.football-data.org/

========================
"""
    print(guide)


if __name__ == "__main__":
    print_usage_guide()
