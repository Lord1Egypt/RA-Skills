"""
融合引擎：三种模型加权集成
权重分配（可配置）:
  - CatBoost+XGBoost+Pi-Rating: 45%
  - Pi-Rating+梯度提升树: 35%
  - Dixon-Coles: 20%
"""
import json
from .catboost_xgb_pirating import CatBoostXGBPiRating
from .dc_gbt_pirating import GradientBoostPiRating, DixonColesModel
from .pi_rating import PiRating


class ThreeModelEnsemble:
    """
    三模型融合引擎
    目标：提高预测准确率，降低单一模型偏差
    """

    # 默认融合权重
    DEFAULT_WEIGHTS = {
        'cb_xgb_pi': 0.45,   # CatBoost+XGBoost+Pi-Rating
        'gbt_pi': 0.35,       # 梯度提升+Pi-Rating
        'dc': 0.20,           # Dixon-Coles
    }

    def __init__(self, weights: dict = None):
        self.weights = weights or self.DEFAULT_WEIGHTS
        self.model1 = CatBoostXGBPiRating()
        self.model2 = GradientBoostPiRating()
        self.model3 = DixonColesModel()
        self.pi = PiRating()
        self.pi_ratings = {}
        self._trained = False

    def fit(self, historical_matches: list):
        """
        训练/拟合所有子模型
        historical_matches: [{home_team, away_team, home_goals, away_goals, league, odds, ...}, ...]
        """
        # 拟合 Pi-Rating（共享）
        formatted = [(m['home_team'], m['away_team'], m['home_goals'], m['away_goals'])
                     for m in historical_matches]
        self.pi_ratings = self.pi.fit_team_ratings(formatted)

        # 为各模型注入评分
        self.model1.pi_ratings = self.pi_ratings
        self.model2.pi_ratings = self.pi_ratings

        # 训练 GBT 模型（如果有标注数据）
        if historical_matches and 'result' in historical_matches[0]:
            labels = [m['result'] for m in historical_matches]
            feat_matches = []
            import math
            for m in historical_matches:
                home = m['home_team']
                away = m['away_team']
                h_att, h_def = self.pi_ratings.get(home, (1.0, 1.0))
                a_att, a_def = self.pi_ratings.get(away, (1.0, 1.0))
                feat = {
                    'pi_diff': (h_att - a_att) - (h_def - a_def),
                    'pi_home_exp': (h_att - a_def) * 1.1,
                    'pi_away_exp': a_att - h_def,
                    'form_diff': m.get('form_diff', 0),
                    'home_win_rate': m.get('home_win_rate', 0.5),
                    'away_win_rate': m.get('away_win_rate', 0.5),
                    'home_goals_avg': m.get('home_goals_avg', 1.5),
                    'away_goals_avg': m.get('away_goals_avg', 1.2),
                    'absent_diff': m.get('absent_diff', 0),
                    'h2h_home_winrate': m.get('h2h_home_winrate', 0.5),
                    'rest_diff': m.get('rest_diff', 0),
                    'home_boost': 1.1,
                    'temperature': 20,
                }
                feat_matches.append(feat)
            self.model2.fit_gbt(feat_matches, labels)

        self._trained = True
        return self

    def predict_single(self, match_info: dict) -> dict:
        """单场比赛融合预测"""
        if not self._trained:
            # 无历史数据时用 Pi-Rating 兜底
            home = match_info['home_team']
            away = match_info['away_team']
            pi_probs = self.pi.predict(home, away, self.pi_ratings)
            return {
                'win': round(pi_probs[0], 4),
                'draw': round(pi_probs[1], 4),
                'lose': round(pi_probs[2], 4),
                'confidence': '中',
                'is_upset': False,
                'model_preds': {'pi_rating': pi_probs, 'cb_xgb_pi': pi_probs, 'gbt_pi': pi_probs, 'dc': pi_probs},
                'weights': self.weights,
            }

        # 子模型预测
        try:
            pred1 = self.model1.predict_single(match_info)
        except Exception:
            home = match_info['home_team']
            away = match_info['away_team']
            pi_p = self.pi.predict(home, away, self.pi_ratings)
            pred1 = {'win': pi_p[0], 'draw': pi_p[1], 'lose': pi_p[2], 'model_preds': {}}

        try:
            pred2 = self.model2.predict_single(match_info)
        except Exception:
            pred2 = {'win': 0.33, 'draw': 0.33, 'lose': 0.34, 'model_preds': {}}

        try:
            dc = DixonColesModel()
            dc.pi_ratings = self.pi_ratings
            dc_probs = list(dc.predict(match_info['home_team'], match_info['away_team']))
            pred3 = {'win': dc_probs[0], 'draw': dc_probs[1], 'lose': dc_probs[2], 'model_preds': {'dixon_coles': dc_probs}}
        except Exception:
            pred3 = {'win': 0.33, 'draw': 0.33, 'lose': 0.34, 'model_preds': {}}

        # 加权融合
        w1, w2, w3 = self.weights['cb_xgb_pi'], self.weights['gbt_pi'], self.weights['dc']
        final = [0.0, 0.0, 0.0]
        for i, pred in enumerate([pred1, pred2, pred3]):
            final[0] += pred['win'] * [w1, w2, w3][i]
            final[1] += pred['draw'] * [w1, w2, w3][i]
            final[2] += pred['lose'] * [w1, w2, w3][i]

        total = sum(final)
        final = [f / total for f in final]

        # 冷门检测
        odds = match_info.get('odds', {})
        market_win = 1 / odds.get('win', 2.0) if odds.get('win', 0) > 0 else 0.33
        is_upset = final[0] < market_win - 0.10

        confidence = '高' if max(final) > 0.55 else ('中' if max(final) > 0.40 else '低')

        return {
            'win': round(final[0], 4),
            'draw': round(final[1], 4),
            'lose': round(final[2], 4),
            'confidence': confidence,
            'is_upset': is_upset,
            'model_preds': {
                'cb_xgb_pi': [pred1['win'], pred1['draw'], pred1['lose']],
                'gbt_pi': [pred2['win'], pred2['draw'], pred2['lose']],
                'dixon_coles': [pred3['win'], pred3['draw'], pred3['lose']],
            },
            'weights': self.weights,
        }

    def predict_batch(self, matches: list) -> list:
        """批量预测"""
        results = []
        for m in matches:
            try:
                r = self.predict_single(m)
                r['match_id'] = m.get('match_id', '')
                r['home_team'] = m['home_team']
                r['away_team'] = m['away_team']
                r['league'] = m.get('league', '')
                r['match_time'] = m.get('match_time', '')
                results.append(r)
            except Exception as e:
                results.append({
                    'match_id': m.get('match_id', ''),
                    'home_team': m['home_team'],
                    'away_team': m['away_team'],
                    'error': str(e)
                })
        return results

    def export_predictions(self, results: list, format='json') -> str:
        """导出预测结果"""
        if format == 'json':
            return json.dumps(results, ensure_ascii=False, indent=2)
        elif format == 'md':
            lines = ['# 胜负彩预测报告\n']
            for r in results:
                if 'error' in r:
                    continue
                flag = '🔥 冷门' if r.get('is_upset') else ''
                lines.append(f"## {r['home_team']} vs {r['away_team']} {flag}")
                lines.append(f"- 联赛: {r.get('league', '')}")
                lines.append(f"- 时间: {r.get('match_time', '')}")
                lines.append(f"- 预测: 胜 {r['win']*100:.1f}% | 平 {r['draw']*100:.1f}% | 负 {r['lose']*100:.1f}%")
                lines.append(f"- 置信度: {r.get('confidence', '中')}")
                lines.append(f"- 胜平负建议: {self._get_recommendation(r)}")
                lines.append('')
            return '\n'.join(lines)
        return str(results)

    def _get_recommendation(self, r: dict) -> str:
        probs = [r['win'], r['draw'], r['lose']]
        idx = probs.index(max(probs))
        labels = ['胜', '平', '负']
        return labels[idx]
