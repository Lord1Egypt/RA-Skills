"""
足球量化预测引擎 v2.1

模块:
  - Elo 评级期望 + Elo→xG 耦合
  - 泊松比分矩阵 + Dixon-Coles 低比分相关性修正
  - 主场优势 xG 乘数
  - 修正因子叠加
  - 市场赔率融合 (搜索到的赔率手动喂入, 无需 API)
  - 淘汰赛晋级概率 (常规时间 + 加时/点球折算, 不预测点球比分)
  - 单队晋级路径蒙特卡洛 / 小组赛完整循环蒙特卡洛
  - 赔率→去vig隐含概率 / 价值检测 / 半 Kelly
  - 三层爆冷分析 (风格克制/状态变量/赛制红利)
  - Brier 分数校准

依赖: 纯标准库

v2.1 变更 (目标: 预测更准):
  1. Dixon-Coles τ 修正: 独立泊松系统性低估 0-0/1-1, 加 rho 修正低比分相关性
  2. Elo→xG 耦合: Elo 差距直接调整期望进球 (进 xG 空间), 概率空间 Elo 权重
     从 0.30 降至 0.15 避免双重计算
  3. 主场优势改为 xG 乘数 (×1.10), 比扁平概率修正更有物理意义;
     predict 新增 home 参数 ('a'/'b'/None)
  4. blend_with_market: 模型×(1-w) + 市场隐含×w 融合, 默认 w=0.30,
     市场概率可由 agent 网页搜索赔率后经 odds_to_probability 得到
v2.0 变更:
  - 删除 v1 死代码; 平局统一由泊松导出; 新增小组/淘汰赛模拟与 Brier 校准
"""

import math
import json
import os
import random
from typing import Dict, List, Tuple, Optional

# ============================================
# 核心参数
# ============================================
LEAGUE_AVG_GOALS = 1.35          # 赛事场均进球基准
ELO_WEIGHT = 0.15                # 概率空间 Elo 权重 (v2.1 降低, Elo 已进 xG)
POISSON_WEIGHT = 0.85            # 概率空间泊松权重
ELO_XG_COUPLING = 0.25           # Elo 差距 → xG 调整强度
HOME_XG_MULT = 1.10              # 主场 xG 乘数
DIXON_COLES_RHO = -0.10          # DC 低比分相关性参数 (负值→抬升 0-0/1-1)
MARKET_BLEND_WEIGHT = 0.30       # 市场融合默认权重
DEFENSE_REGRESSION = 0.30        # 淘汰赛极端防守均值回归比例
DEFENSE_EXTREME_THRESHOLD = 0.5  # 触发回归的防守系数阈值
DEFAULT_ELO = 1500
MAX_GOALS = 8


class FootballPredictionEngine:
    """足球比赛预测引擎"""

    VERSION = "2.1"

    def __init__(self, data_dir: str = None):
        self.elo_ratings: Dict[str, float] = {}
        self.team_stats: Dict[str, Dict] = {}
        self.corrections_lib: Dict[str, Dict] = {}
        self.prediction_log: List[Dict] = []
        self.data_dir = data_dir
        if data_dir:
            self.load_data(data_dir)

    # ------------------------------------------------
    # 数据加载
    # ------------------------------------------------
    def load_data(self, data_dir: str):
        """从目录加载 elo / stats / corrections"""
        def _load(name):
            path = os.path.join(data_dir, name)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        self.elo_ratings = _load('elo_ratings.json') or self.elo_ratings
        self.team_stats = _load('team_stats.json') or self.team_stats
        self.corrections_lib = _load('corrections.json') or self.corrections_lib

    def inject_live(self, elo: Dict = None, stats: Dict = None):
        """注入校准后的实时 Elo / 攻防数据 (calibrate.py 或 agent 搜索后)"""
        if elo:
            self.elo_ratings.update(elo)
        if stats:
            self.team_stats.update(stats)

    # ------------------------------------------------
    # 基础数学
    # ------------------------------------------------
    def elo_expected(self, elo_a: float, elo_b: float) -> float:
        """Elo 期望得分 (含平局折半, 0~1)"""
        return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    @staticmethod
    def poisson_prob(lam: float, k: int) -> float:
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    def _stats(self, team: str) -> Dict:
        return self.team_stats.get(
            team, {'avg_goals': LEAGUE_AVG_GOALS, 'avg_conceded': LEAGUE_AVG_GOALS})

    def expected_goals(self, team_a: str, team_b: str,
                       is_knockout: bool = False) -> Tuple[float, float]:
        """基础期望进球 (xG): 攻击力 × 对手防守 × 基准 (不含 Elo/主场调整)"""
        sa, sb = self._stats(team_a), self._stats(team_b)
        attack_a = sa['avg_goals'] / LEAGUE_AVG_GOALS
        defense_a = sa['avg_conceded'] / LEAGUE_AVG_GOALS
        attack_b = sb['avg_goals'] / LEAGUE_AVG_GOALS
        defense_b = sb['avg_conceded'] / LEAGUE_AVG_GOALS

        # 淘汰赛: 极端防守均值回归 (避免铁桶队被高估)
        if is_knockout:
            if defense_b < DEFENSE_EXTREME_THRESHOLD:
                defense_b = defense_b * (1 - DEFENSE_REGRESSION) + 1.0 * DEFENSE_REGRESSION
            if defense_a < DEFENSE_EXTREME_THRESHOLD:
                defense_a = defense_a * (1 - DEFENSE_REGRESSION) + 1.0 * DEFENSE_REGRESSION

        xg_a = LEAGUE_AVG_GOALS * attack_a * defense_b
        xg_b = LEAGUE_AVG_GOALS * attack_b * defense_a
        return xg_a, xg_b

    def poisson_matrix(self, xg_a: float, xg_b: float,
                       max_goals: int = MAX_GOALS,
                       rho: float = DIXON_COLES_RHO) -> Dict:
        """
        泊松比分矩阵 → W/D/L 概率 + 各比分概率。

        v2.1: Dixon-Coles τ 修正 —— 低比分格 (0-0/1-0/0-1/1-1) 存在相关性,
        独立泊松会低估 0-0 和 1-1。rho<0 时抬升 0-0/1-1、压低 1-0/0-1。
        """
        win_a = draw = win_b = 0.0
        score_probs: Dict[str, float] = {}
        pa = [self.poisson_prob(xg_a, k) for k in range(max_goals)]
        pb = [self.poisson_prob(xg_b, k) for k in range(max_goals)]
        for ga in range(max_goals):
            for gb in range(max_goals):
                p = pa[ga] * pb[gb]
                # Dixon-Coles τ
                if rho:
                    if ga == 0 and gb == 0:
                        p *= 1 - xg_a * xg_b * rho
                    elif ga == 0 and gb == 1:
                        p *= 1 + xg_a * rho
                    elif ga == 1 and gb == 0:
                        p *= 1 + xg_b * rho
                    elif ga == 1 and gb == 1:
                        p *= 1 - rho
                    p = max(0.0, p)
                score_probs[f"{ga}-{gb}"] = p
                if ga > gb:
                    win_a += p
                elif ga == gb:
                    draw += p
                else:
                    win_b += p
        # 归一化 (DC 修正 + 矩阵截断)
        tot = win_a + draw + win_b
        if tot > 0:
            win_a, draw, win_b = win_a / tot, draw / tot, win_b / tot
            score_probs = {k: round(v / tot * 100, 3) for k, v in score_probs.items()}
        return {'win_a': win_a, 'draw': draw, 'win_b': win_b,
                'score_probs': score_probs}

    # ------------------------------------------------
    # 单场预测
    # ------------------------------------------------
    def predict(self, team_a: str, team_b: str,
                corrections: Dict = None, is_knockout: bool = False,
                home: Optional[str] = None) -> Dict:
        """
        单场 W/D/L 预测。

        v2.1 建模链路:
          stats → 基础 xG → Elo 耦合调整 → 主场 xG 乘数 → DC 泊松矩阵
          → 概率空间小幅 Elo 融合 → 修正因子 → 终值

        home: 'a'/'b' 表示真主场 (东道主), None 为中立场。
        """
        corrections = corrections or {}
        elo_a = self.elo_ratings.get(team_a, DEFAULT_ELO)
        elo_b = self.elo_ratings.get(team_b, DEFAULT_ELO)
        elo_exp_a = self.elo_expected(elo_a, elo_b)

        xg_a, xg_b = self.expected_goals(team_a, team_b, is_knockout)

        # v2.1: Elo→xG 耦合 (Elo 差距直接改变进球期望)
        elo_shift = (elo_a - elo_b) / 400 * ELO_XG_COUPLING
        xg_a *= max(0.3, 1 + elo_shift)
        xg_b *= max(0.3, 1 - elo_shift)

        # v2.1: 主场优势 xG 乘数 (替代扁平概率修正)
        if home == 'a':
            xg_a *= HOME_XG_MULT
        elif home == 'b':
            xg_b *= HOME_XG_MULT

        pois = self.poisson_matrix(xg_a, xg_b)
        p_draw = pois['draw']

        # 概率空间小幅 Elo 融合 (权重已降, 仅作平滑)
        elo_w_a = max(0.0, elo_exp_a - p_draw / 2)
        elo_w_b = max(0.0, (1 - elo_exp_a) - p_draw / 2)
        s = elo_w_a + elo_w_b
        if s > 0:
            elo_w_a = elo_w_a / s * (1 - p_draw)
            elo_w_b = elo_w_b / s * (1 - p_draw)
        comb_a = ELO_WEIGHT * elo_w_a + POISSON_WEIGHT * pois['win_a']
        comb_b = ELO_WEIGHT * elo_w_b + POISSON_WEIGHT * pois['win_b']
        comb_d = p_draw
        tot = comb_a + comb_d + comb_b
        comb_a, comb_d, comb_b = comb_a / tot, comb_d / tot, comb_b / tot

        # 修正因子叠加 (伤病/内讧/裁判等, 由 agent 搜索情报后构建)
        adj_a = max(0.0, comb_a + corrections.get('a', 0))
        adj_d = max(0.0, comb_d + corrections.get('draw', 0))
        adj_b = max(0.0, comb_b + corrections.get('b', 0))
        tot2 = adj_a + adj_d + adj_b
        adj_a, adj_d, adj_b = adj_a / tot2, adj_d / tot2, adj_b / tot2

        top_scores = sorted(pois['score_probs'].items(),
                            key=lambda x: x[1], reverse=True)[:5]

        return {
            'team_a': team_a, 'team_b': team_b,
            'elo_a': elo_a, 'elo_b': elo_b,
            'elo_gap': round(abs(elo_a - elo_b)),
            'elo_expected_a': round(elo_exp_a, 3),
            'xg_a': round(xg_a, 2), 'xg_b': round(xg_b, 2),
            'home': home,
            'poisson': {'win_a': round(pois['win_a'] * 100, 1),
                        'draw': round(pois['draw'] * 100, 1),
                        'win_b': round(pois['win_b'] * 100, 1)},
            'combined': {'win_a': round(comb_a * 100, 1),
                         'draw': round(comb_d * 100, 1),
                         'win_b': round(comb_b * 100, 1)},
            'final': {'win_a': round(adj_a * 100, 1),
                      'draw': round(adj_d * 100, 1),
                      'win_b': round(adj_b * 100, 1)},
            'top_scores': top_scores,
            'corrections': corrections,
            'is_knockout': is_knockout,
            'model_version': self.VERSION,
        }

    # ------------------------------------------------
    # 市场融合 (v2.1, 搜索到的赔率手动喂入)
    # ------------------------------------------------
    @staticmethod
    def blend_with_market(model_final: Dict, market: Dict,
                          market_weight: float = MARKET_BLEND_WEIGHT) -> Dict:
        """
        模型概率与市场隐含概率加权融合 (均为百分比 0~100)。
        市场概率含全市场信息, 融合通常显著降低 Brier。
        market 可由 agent 网页搜索赔率 → odds_to_probability 得到。
        """
        out = {}
        for k in ['win_a', 'draw', 'win_b']:
            out[k] = model_final.get(k, 0) * (1 - market_weight) + \
                     market.get(k, 0) * market_weight
        tot = sum(out.values())
        return {k: round(v / tot * 100, 1) for k, v in out.items()}

    # ------------------------------------------------
    # 淘汰赛晋级 (常规时间 + 加时/点球折算)
    # ------------------------------------------------
    def knockout_advance_prob(self, team_a: str, team_b: str,
                              corrections: Dict = None,
                              home: Optional[str] = None) -> Dict:
        """
        淘汰赛单场晋级概率。
        常规时间平局 → 加时/点球按 Elo 期望切分晋级 (向 0.5 收缩 40%, 不预测点球比分)。
        """
        pred = self.predict(team_a, team_b, corrections,
                            is_knockout=True, home=home)
        f = pred['final']
        w_a, draw, w_b = f['win_a'] / 100, f['draw'] / 100, f['win_b'] / 100
        et_a = 0.5 + (pred['elo_expected_a'] - 0.5) * 0.6
        adv_a = w_a + draw * et_a
        adv_b = w_b + draw * (1 - et_a)
        return {
            'team_a': team_a, 'team_b': team_b,
            'reg_win_a': round(w_a * 100, 1),
            'reg_draw': round(draw * 100, 1),
            'reg_win_b': round(w_b * 100, 1),
            'advance_a': round(adv_a * 100, 1),
            'advance_b': round(adv_b * 100, 1),
            'et_split_a': round(et_a * 100, 1),
            'prediction': pred,
        }

    # ------------------------------------------------
    # 蒙特卡洛: 单队晋级路径
    # ------------------------------------------------
    def monte_carlo_path(self, team: str, stages: List[Dict],
                         simulations: int = 100000) -> Dict:
        """stages: [{'name': '16强', 'win_prob': 0.62}, ...] 逐阶段连乘"""
        results = {i: 0 for i in range(len(stages) + 1)}
        results[0] = simulations
        for _ in range(simulations):
            for idx, st in enumerate(stages):
                if random.random() < st['win_prob']:
                    results[idx + 1] += 1
                else:
                    break
        names = ['起点'] + [s.get('name', f'阶段{i+1}') for i, s in enumerate(stages)]
        return {
            'team': team, 'simulations': simulations,
            'probabilities': {
                names[i]: round(results[i] / simulations * 100, 1)
                for i in range(len(stages) + 1)
            },
        }

    # ------------------------------------------------
    # 蒙特卡洛: 小组赛完整循环
    # ------------------------------------------------
    def simulate_group(self, teams: List[str], simulations: int = 50000,
                       advance: int = 2,
                       home_teams: List[str] = None) -> Dict:
        """
        4 队单循环蒙特卡洛。泊松采样比分 (含 Elo-xG 耦合与东道主主场),
        积分→净胜球→进球→随机 排序, 统计出线/头名/名次分布。
        home_teams: 东道主列表 (该队比赛享受主场 xG 乘数)。
        """
        n = len(teams)
        home_teams = home_teams or []
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        xg_cache = {}
        for i, j in pairs:
            xa, xb = self.expected_goals(teams[i], teams[j])
            # Elo 耦合
            ea = self.elo_ratings.get(teams[i], DEFAULT_ELO)
            eb = self.elo_ratings.get(teams[j], DEFAULT_ELO)
            shift = (ea - eb) / 400 * ELO_XG_COUPLING
            xa *= max(0.3, 1 + shift)
            xb *= max(0.3, 1 - shift)
            # 东道主主场
            if teams[i] in home_teams:
                xa *= HOME_XG_MULT
            if teams[j] in home_teams:
                xb *= HOME_XG_MULT
            xg_cache[(i, j)] = (xa, xb)

        finish = {t: [0] * n for t in teams}
        advance_cnt = {t: 0 for t in teams}
        first_cnt = {t: 0 for t in teams}

        for _ in range(simulations):
            pts = {i: 0 for i in range(n)}
            gf = {i: 0 for i in range(n)}
            ga = {i: 0 for i in range(n)}
            for i, j in pairs:
                xa, xb = xg_cache[(i, j)]
                sa = self._sample_poisson(xa)
                sb = self._sample_poisson(xb)
                gf[i] += sa; ga[i] += sb
                gf[j] += sb; ga[j] += sa
                if sa > sb:
                    pts[i] += 3
                elif sa < sb:
                    pts[j] += 3
                else:
                    pts[i] += 1; pts[j] += 1
            order = sorted(range(n),
                           key=lambda k: (pts[k], gf[k] - ga[k], gf[k], random.random()),
                           reverse=True)
            for rank, k in enumerate(order):
                finish[teams[k]][rank] += 1
                if rank < advance:
                    advance_cnt[teams[k]] += 1
                if rank == 0:
                    first_cnt[teams[k]] += 1

        return {
            'teams': teams, 'simulations': simulations, 'advance_slots': advance,
            'advance_prob': {t: round(advance_cnt[t] / simulations * 100, 1) for t in teams},
            'first_prob': {t: round(first_cnt[t] / simulations * 100, 1) for t in teams},
            'finish_dist': {
                t: {f'第{r+1}': round(finish[t][r] / simulations * 100, 1) for r in range(n)}
                for t in teams
            },
        }

    @staticmethod
    def _sample_poisson(lam: float) -> int:
        """Knuth 泊松采样"""
        L = math.exp(-lam)
        k, p = 0, 1.0
        while True:
            k += 1
            p *= random.random()
            if p <= L:
                return k - 1

    # ------------------------------------------------
    # 赔率 / 价值 / Kelly
    # ------------------------------------------------
    @staticmethod
    def odds_to_probability(odds_a: float, odds_draw: float, odds_b: float) -> Dict:
        """小数赔率 → 去 vig 隐含概率 (赔率可由 agent 网页搜索获得)"""
        ra, rd, rb = 1 / odds_a, 1 / odds_draw, 1 / odds_b
        tot = ra + rd + rb
        return {'win_a': round(ra / tot * 100, 1),
                'draw': round(rd / tot * 100, 1),
                'win_b': round(rb / tot * 100, 1),
                'vig': round((tot - 1) * 100, 1)}

    def value_detection(self, model_prob: Dict, market_prob: Dict,
                        threshold: float = 3.0) -> Dict:
        edges = {}
        for key in ['win_a', 'draw', 'win_b']:
            model = model_prob.get(key, 0)
            market = market_prob.get(key, 0)
            edge = model - market
            edges[key] = {'model': model, 'market': market,
                          'edge': round(edge, 1),
                          'is_value': abs(edge) >= threshold}
        return edges

    @staticmethod
    def kelly(prob: float, odds: float, fraction: float = 0.5) -> float:
        """半 Kelly 仓位 (prob 为 0~1 概率, odds 为小数赔率)"""
        full = (prob * odds - 1) / (odds - 1)
        return round(max(0, full * fraction), 4)

    # ------------------------------------------------
    # 爆冷分析 (三层判据)
    # ------------------------------------------------
    def upset_analysis(self, team_a: str, team_b: str,
                       match_context: Dict = None) -> Dict:
        match_context = match_context or {}
        elo_a = self.elo_ratings.get(team_a, DEFAULT_ELO)
        elo_b = self.elo_ratings.get(team_b, DEFAULT_ELO)
        favorite = team_a if elo_a >= elo_b else team_b
        underdog = team_b if favorite == team_a else team_a
        elo_gap = abs(elo_a - elo_b)

        base = self.predict(team_a, team_b)
        und_key = 'win_b' if favorite == team_a else 'win_a'
        base_upset = base['final'][und_key] / 100.0
        base_draw = base['final']['draw'] / 100.0

        corr = {'style': 0.0, 'status': 0.0, 'format': 0.0}
        sf = self._stats(favorite)
        su = self._stats(underdog)
        # 1. 风格克制
        if sf['avg_goals'] > 1.8 and sf['avg_conceded'] > 0.9 and su['avg_conceded'] < 0.9:
            corr['style'] += 0.04   # 铁桶克攻强守弱
        if su['avg_goals'] > 1.3 and su['avg_conceded'] < 1.0 and sf['avg_goals'] > 2.0:
            corr['style'] += 0.03   # 反击克控球
        # 2. 状态变量
        if match_context.get('internal_strife'):
            corr['status'] -= 0.04
        if match_context.get('key_injury'):
            corr['status'] -= 0.03
        if match_context.get('slow_starter'):
            corr['status'] += 0.02
        # 3. 赛制红利
        if match_context.get('is_first_match'):
            corr['format'] += 0.03
        if match_context.get('rotation_risk'):
            corr['format'] += 0.06
        if match_context.get('is_last_group_match'):
            corr['format'] += 0.02
        if match_context.get('expansion_format'):
            corr['format'] += 0.03

        total = corr['style'] + corr['status'] + corr['format']
        adj_upset = min(0.95, base_upset + total)
        adj_draw = min(0.50, base_draw + abs(corr['status']) * 0.3)
        combined = adj_upset + adj_draw * 0.5

        if combined >= 0.40:
            tier = "Tier 1 - 高概率爆冷"
        elif combined >= 0.30:
            tier = "Tier 2 - 中概率爆冷"
        elif combined >= 0.20:
            tier = "Tier 3 - 值得盯的暗冷"
        else:
            tier = "常规 - 爆冷概率低"

        return {
            'favorite': favorite, 'underdog': underdog, 'elo_gap': elo_gap,
            'base_upset_prob': round(base_upset * 100, 1),
            'base_draw_prob': round(base_draw * 100, 1),
            'corrections': {k: round(v * 100, 1) for k, v in corr.items()},
            'total_correction': round(total * 100, 1),
            'adjusted_upset_prob': round(adj_upset * 100, 1),
            'adjusted_draw_prob': round(adj_draw * 100, 1),
            'upset_combined': round(combined * 100, 1),
            'tier': tier,
            'key_factors': [f for f, v in corr.items() if abs(v) >= 0.01],
        }

    # ------------------------------------------------
    # 校准: Brier 分数
    # ------------------------------------------------
    @staticmethod
    def brier_score(predicted: Dict, outcome: str) -> float:
        """
        predicted: {'win_a': %, 'draw': %, 'win_b': %}
        outcome: 'win_a' | 'draw' | 'win_b'
        多分类 Brier (越低越准, 0~2)
        """
        s = 0.0
        for key in ['win_a', 'draw', 'win_b']:
            p = predicted.get(key, 0) / 100.0
            y = 1.0 if key == outcome else 0.0
            s += (p - y) ** 2
        return round(s, 4)


# ====================================================
# CLI 自测
# ====================================================
if __name__ == "__main__":
    here = os.path.dirname(__file__)
    engine = FootballPredictionEngine(data_dir=os.path.join(here, '..', 'data'))
    print(f"引擎 v{engine.VERSION} | 已加载 {len(engine.elo_ratings)} 队 Elo / "
          f"{len(engine.team_stats)} 队攻防 / {len(engine.corrections_lib)} 项修正因子\n")

    print("=== 单场预测: 美国(主) vs 巴拉圭 ===")
    p = engine.predict("美国", "巴拉圭", home='a')
    print(f"  xG {p['xg_a']}-{p['xg_b']} | 终值 "
          f"胜{p['final']['win_a']}% 平{p['final']['draw']}% 负{p['final']['win_b']}% "
          f"| 最可能 {p['top_scores'][0][0]}")

    print("\n=== Dixon-Coles 效果对比 (rho=0 vs -0.10) ===")
    xa, xb = engine.expected_goals("加拿大", "波黑")
    m0 = engine.poisson_matrix(xa, xb, rho=0)
    m1 = engine.poisson_matrix(xa, xb)
    print(f"  独立泊松: 平 {round(m0['draw']*100,1)}% (0-0: {m0['score_probs']['0-0']}%)")
    print(f"  DC修正后: 平 {round(m1['draw']*100,1)}% (0-0: {m1['score_probs']['0-0']}%)")

    print("\n=== 市场融合演示 (搜索到赔率 2.10/3.30/3.80) ===")
    mk = engine.odds_to_probability(2.10, 3.30, 3.80)
    blended = engine.blend_with_market(p['final'], mk)
    print(f"  市场: {mk['win_a']}/{mk['draw']}/{mk['win_b']} (vig {mk['vig']}%)")
    print(f"  融合: {blended['win_a']}/{blended['draw']}/{blended['win_b']}")

    print("\n=== 淘汰赛晋级: 西班牙 vs 克罗地亚 ===")
    k = engine.knockout_advance_prob("西班牙", "克罗地亚")
    print(f"  常规 {k['reg_win_a']}/{k['reg_draw']}/{k['reg_win_b']} "
          f"| 晋级 西班牙{k['advance_a']}% 克罗地亚{k['advance_b']}%")

    print("\n=== 小组赛模拟 (东道主主场): 墨西哥/南非/韩国/捷克 ===")
    g = engine.simulate_group(["墨西哥", "南非", "韩国", "捷克"],
                              simulations=20000, home_teams=["墨西哥"])
    for t in g['teams']:
        print(f"  {t}: 出线{g['advance_prob'][t]}% / 头名{g['first_prob'][t]}%")

    print("\n=== 爆冷分析: 法国 vs 塞内加尔 ===")
    r = engine.upset_analysis("法国", "塞内加尔",
                              {"is_first_match": True, "expansion_format": True})
    print(f"  基础{r['base_upset_prob']}%→调整{r['adjusted_upset_prob']}% | {r['tier']}")
