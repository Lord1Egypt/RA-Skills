"""6 维爻位计算 — 把多源数据融合成 6 个 0~1 的爻位评分"""
from typing import Dict, List, Tuple


def calc_attack(home_goals_per_match: float, away_goals_per_match: float) -> float:
    """攻防 — 主队进球能力 vs 客队进球能力"""
    return max(0.0, min(1.0, 0.5 + (home_goals_per_match - away_goals_per_match) * 0.3))


def calc_morale(home_form: List[str], away_form: List[str]) -> float:
    """士气 — 近 N 场积分对比

    Args:
        home_form / away_form: ['W','D','L','W','W']
    """
    pts = lambda f: sum(3 if x == 'W' else (1 if x == 'D' else 0) for x in f)
    h_pts = pts(home_form) / max(1, len(home_form) * 3)
    a_pts = pts(away_form) / max(1, len(away_form) * 3)
    return max(0.0, min(1.0, 0.5 + (h_pts - a_pts) * 0.5))


def calc_injury(home_key_outs: int = 0, away_key_outs: int = 0) -> float:
    """伤停 — 主队伤停影响 vs 客队伤停影响（值越高对主越有利）"""
    if home_key_outs == 0 and away_key_outs == 0:
        return 0.5
    delta = (away_key_outs - home_key_outs) / 5
    return max(0.0, min(1.0, 0.5 + delta * 0.3))


def calc_home_advantage(league: str = "") -> float:
    """主客场 — 主队主场加成（不同联赛权重不同）"""
    weights = {
        "premier-league": 0.62,
        "serie-a": 0.65,
        "la-liga": 0.66,
        "bundesliga": 0.63,
        "ligue-1": 0.64,
    }
    return weights.get(league.lower(), 0.65)


def calc_h2h(h2h_home_wins: int, draws: int, away_wins: int) -> float:
    """交锋 — H2H 历史"""
    total = h2h_home_wins + draws + away_wins
    if total == 0:
        return 0.5
    pts = (h2h_home_wins * 3 + draws) / (total * 3)
    return min(1.0, pts + 0.2)


def calc_odds(home_odd: float, draw_odd: float, away_odd: float) -> float:
    """赔率 — 去抽水后的真实主胜概率"""
    if home_odd <= 1 or draw_odd <= 1 or away_odd <= 1:
        return 0.5
    p_h = 1 / home_odd
    p_d = 1 / draw_odd
    p_a = 1 / away_odd
    total = p_h + p_d + p_a
    return p_h / total


def calc_xg_attack(home_xg: float, away_xga: float,
                   away_xg: float, home_xga: float) -> float:
    """xG 增强 — 用 xG/xGA 替代实际进球（更稳定）

    可选用，作为攻防爻位的更精确版本。
    """
    home_threat = home_xg / max(0.1, home_xga + away_xga) * 2
    away_threat = away_xg / max(0.1, away_xga + home_xga) * 2
    return max(0.0, min(1.0, 0.5 + (home_threat - away_threat) * 0.2))


def build_yao_summary(
    home_goals: List[int],
    away_goals: List[int],
    home_conceded: List[int],
    away_conceded: List[int],
    home_form: List[str],
    away_form: List[str],
    h2h: Tuple[int, int, int],
    odds: Tuple[float, float, float],
    league: str = "",
    home_key_outs: int = 0,
    away_key_outs: int = 0,
    home_xg: float = None,
    away_xg: float = None,
    home_xga: float = None,
    away_xga: float = None,
) -> Dict[str, float]:
    """主入口 — 综合所有数据源生成 6 维爻位"""
    n = max(1, len(home_goals))
    h_gpm = sum(home_goals) / n
    a_gpm = sum(away_goals) / max(1, len(away_goals))

    # 攻防：xG 优先，否则用进球
    if all(x is not None for x in [home_xg, away_xg, home_xga, away_xga]):
        attack = calc_xg_attack(home_xg, away_xga, away_xg, home_xga)
    else:
        attack = calc_attack(h_gpm, a_gpm)

    return {
        "攻防": round(attack, 3),
        "士气": round(calc_morale(home_form, away_form), 3),
        "伤停": round(calc_injury(home_key_outs, away_key_outs), 3),
        "主客场": round(calc_home_advantage(league), 3),
        "交锋": round(calc_h2h(*h2h), 3),
        "赔率": round(calc_odds(*odds), 3),
    }
