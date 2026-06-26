"""
CatBoost + XGBoost + Pi-Rating 特征融合模型
权重配置:
  - 赔率变化趋势: 25%
  - Pi-Rating分差: 20%
  - 近期状态: 15%
  - 主客场优势: 10%
  - 伤病/停赛: 10%
  - 历史交锋: 8%
  - 赛程密度: 7%
  - 天气/裁判: 5%
"""
import json
import math
from .pi_rating import PiRating

try:
    from catboost import CatBoostClassifier
    HAS_CATBOOST = True
except ImportError:
    HAS_CATBOOST = False

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


class MatchFeatureEngine:
    """特征工程引擎"""

    # 联赛风格系数（影响主场优势）
    LEAGUE_STYLE = {
        '英超': {'home_boost': 1.2, 'scoring': 'high'},
        '西甲': {'home_boost': 1.1, 'scoring': 'medium'},
        '意甲': {'home_boost': 1.15, 'scoring': 'medium'},
        '德甲': {'home_boost': 1.2, 'scoring': 'high'},
        '法甲': {'home_boost': 1.1, 'scoring': 'medium'},
        '欧冠': {'home_boost': 1.0, 'scoring': 'medium'},
        '欧联': {'home_boost': 1.0, 'scoring': 'medium'},
        '中超': {'home_boost': 1.25, 'scoring': 'medium'},
        '亚冠': {'home_boost': 1.05, 'scoring': 'medium'},
        '世预赛': {'home_boost': 1.3, 'scoring': 'medium'},
        '欧洲杯': {'home_boost': 1.2, 'scoring': 'medium'},
        '默认': {'home_boost': 1.1, 'scoring': 'medium'},
    }

    def __init__(self):
        self.pi = PiRating()

    def build_features(self, match_info: dict, ratings: dict) -> dict:
        """构建模型输入特征"""
        home = match_info['home_team']
        away = match_info['away_team']
        league = match_info.get('league', '默认')

        league_cfg = self.LEAGUE_STYLE.get(league, self.LEAGUE_STYLE['默认'])
        home_boost = league_cfg['home_boost']

        # 1. Pi-Rating特征 (权重20%)
        h_att, h_def = ratings.get(home, (1.0, 1.0))
        a_att, a_def = ratings.get(away, (1.0, 1.0))
        pi_diff = (h_att - a_att) - (h_def - a_def)
        pi_home_exp = (h_att - a_def) * home_boost
        pi_away_exp = a_att - h_def

        # 2. 赔率特征 (权重25%)
        odds = match_info.get('odds', {})
        win_odds = odds.get('win', 2.0)
        draw_odds = odds.get('draw', 3.2)
        lose_odds = odds.get('lose', 3.5)
        odds_change = odds.get('change_trend', 0)  # 赔率变化方向

        # 3. 近期状态特征 (权重15%)
        recent = match_info.get('recent_form', {})
        home_recent = recent.get('home', [0, 0, 0, 0, 0])   # 最近5场得分率
        away_recent = recent.get('away', [0, 0, 0, 0, 0])
        home_form = sum(home_recent) / max(len(home_recent), 1)
        away_form = sum(away_recent) / max(len(away_recent), 1)
        form_diff = home_form - away_form

        # 4. 主客场特征 (权重10%)
        home_stats = match_info.get('home_stats', {})
        away_stats = match_info.get('away_stats', {})
        home_win_rate = home_stats.get('win_rate', 0.5)
        away_win_rate = away_stats.get('win_rate', 0.5)
        home_goals_avg = home_stats.get('goals_avg', 1.5)
        away_goals_avg = away_stats.get('goals_avg', 1.2)
        home_goals_conceded = home_stats.get('goals_conceded', 1.2)
        away_goals_conceded = away_stats.get('goals_conceded', 1.5)

        # 5. 伤病/停赛 (权重10%)
        absentees = match_info.get('absentees', {})
        home_absent = absentees.get('home', 0)
        away_absent = absentees.get('away', 0)
        absent_diff = home_absent - away_absent

        # 6. 历史交锋 (权重8%)
        h2h = match_info.get('head_to_head', [])
        home_h2h_win = sum(1 for r in h2h if r['winner'] == 'home')
        away_h2h_win = sum(1 for r in h2h if r['winner'] == 'away')
        h2h_home_winrate = home_h2h_win / max(len(h2h), 1)

        # 7. 赛程密度 (权重7%)
        schedule = match_info.get('schedule', {})
        home_days_rest = schedule.get('home_rest_days', 7)
        away_days_rest = schedule.get('away_rest_days', 7)
        rest_diff = home_days_rest - away_days_rest

        # 8. 天气/裁判 (权重5%)
        weather = match_info.get('weather', {})
        temperature = weather.get('temperature', 20)
        is_home_ref = weather.get('home_referee', 0.5)  # 裁判对主队偏好

        features = {
            # Pi-Rating
            'pi_diff': pi_diff,
            'pi_home_exp': pi_home_exp,
            'pi_away_exp': pi_away_exp,
            # 赔率
            'win_odds': win_odds,
            'draw_odds': draw_odds,
            'lose_odds': lose_odds,
            'odds_change': odds_change,
            'odds_implied_home_win': 1 / win_odds if win_odds > 0 else 0.33,
            'odds_implied_draw': 1 / draw_odds if draw_odds > 0 else 0.31,
            'odds_implied_away_win': 1 / lose_odds if lose_odds > 0 else 0.29,
            # 近期状态
            'home_form': home_form,
            'away_form': away_form,
            'form_diff': form_diff,
            # 主客场
            'home_win_rate': home_win_rate,
            'away_win_rate': away_win_rate,
            'home_goals_avg': home_goals_avg,
            'away_goals_avg': away_goals_avg,
            'home_goals_conceded': home_goals_conceded,
            'away_goals_conceded': away_goals_conceded,
            'home_boost': home_boost,
            # 伤病/停赛
            'home_absent': home_absent,
            'away_absent': away_absent,
            'absent_diff': absent_diff,
            # 历史交锋
            'h2h_home_winrate': h2h_home_winrate,
            'h2h_count': len(h2h),
            # 赛程
            'home_rest_days': home_days_rest,
            'away_rest_days': away_days_rest,
            'rest_diff': rest_diff,
            # 天气/裁判
            'temperature': temperature,
            'home_referee_bias': is_home_ref,
            # 综合
            'league_type': league,
        }
        return features

    def features_to_array(self, features: dict) -> list:
        """特征转数值数组"""
        numeric_keys = [
            'pi_diff', 'pi_home_exp', 'pi_away_exp',
            'win_odds', 'draw_odds', 'lose_odds', 'odds_change',
            'odds_implied_home_win', 'odds_implied_draw', 'odds_implied_away_win',
            'home_form', 'away_form', 'form_diff',
            'home_win_rate', 'away_win_rate',
            'home_goals_avg', 'away_goals_avg',
            'home_goals_conceded', 'away_goals_conceded', 'home_boost',
            'home_absent', 'away_absent', 'absent_diff',
            'h2h_home_winrate', 'h2h_count',
            'home_rest_days', 'away_rest_days', 'rest_diff',
            'temperature', 'home_referee_bias'
        ]
        return [features.get(k, 0) for k in numeric_keys]


class CatBoostXGBPiRating:
    """
    CatBoost + XGBoost + Pi-Rating 融合模型
    三模型加权平均输出预测
    """

    def __init__(self):
        self.feature_engine = MatchFeatureEngine()
        self.pi = PiRating()
        self.pi_ratings = {}
        self.catboost_model = None
        self.xgb_model = None
        self._models_loaded = False

    def load_models(self):
        """加载预训练模型（如果存在）"""
        import os
        model_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
        if HAS_CATBOOST:
            cb_path = os.path.join(model_dir, 'catboost_model.cbm')
            if os.path.exists(cb_path):
                self.catboost_model = CatBoostClassifier()
                self.catboost_model.load_model(cb_path)
        if HAS_XGB:
            xgb_path = os.path.join(model_dir, 'xgb_model.json')
            if os.path.exists(xgb_path):
                self.xgb_model = xgb.XGBClassifier()
                self.xgb_model.load_model(xgb_path)
        self._models_loaded = True

    def fit_pi(self, historical_matches: list):
        """拟合Pi-Rating球队评分"""
        formatted = [(m['home'], m['away'], m['home_goals'], m['away_goals'])
                     for m in historical_matches]
        self.pi_ratings = self.pi.fit_team_ratings(formatted)
        return self.pi_ratings

    def predict_single(self, match_info: dict) -> dict:
        """
        预测单场比赛
        返回: {win: float, draw: float, lose: float, confidence: str, model_preds: dict}
        """
        # 获取特征
        features = self.feature_engine.build_features(match_info, self.pi_ratings)
        feat_array = self.feature_engine.features_to_array(features)

        # Pi-Rating 模型预测
        home = match_info['home_team']
        away = match_info['away_team']
        pi_probs = self.pi.predict(home, away, self.pi_ratings)
        league = match_info.get('league', '默认')
        league_cfg = MatchFeatureEngine.LEAGUE_STYLE.get(league, MatchFeatureEngine.LEAGUE_STYLE['默认'])
        pi_probs_adv = self.pi.predict(home, away, self.pi_ratings, home_adv=league_cfg.get('home_boost', 1.1) * 0.05)

        # CatBoost/XGBoost 模型预测
        cb_prob = [0.33, 0.33, 0.34]  # 默认
        xgb_prob = [0.33, 0.33, 0.34]

        if self._models_loaded and self.catboost_model:
            try:
                cb_prob = self.catboost_model.predict_proba([feat_array])[0]
            except Exception:
                pass

        if self._models_loaded and self.xgb_model:
            try:
                xgb_prob = self.xgb_model.predict_proba([feat_array])[0]
            except Exception:
                pass

        # 赔率权重融合
        odds = match_info.get('odds', {})
        win_odds = odds.get('win', 2.0)
        draw_odds = odds.get('draw', 3.2)
        lose_odds = odds.get('lose', 3.5)
        try:
            odds_prob = [1 / win_odds, 1 / draw_odds, 1 / lose_odds]
            odds_sum = sum(odds_prob)
            odds_prob = [p / odds_sum for p in odds_prob]
        except (ZeroDivisionError, KeyError):
            odds_prob = [0.33, 0.33, 0.34]

        # 加权融合 (赔率25%, Pi-Rating20%, CatBoost+XGB 55%)
        # 其中 CatBoost 和 XGB 各占 55%的一半
        cb_weight, xgb_weight, pi_weight, odds_weight = 0.20, 0.15, 0.40, 0.25

        final_probs = [0.0, 0.0, 0.0]
        for i in range(3):
            final_probs[i] = (
                odds_prob[i] * odds_weight +
                pi_probs[i] * pi_weight +
                cb_prob[i] * cb_weight +
                xgb_prob[i] * xgb_weight
            )

        # 归一化
        total = sum(final_probs)
        final_probs = [p / total for p in final_probs]

        # 判断冷门
        market_win = odds_prob[0]
        is_upsets = final_probs[0] < market_win - 0.08  # 市场热捧但模型看低
        confidence = '高' if max(final_probs) > 0.55 else ('中' if max(final_probs) > 0.40 else '低')

        return {
            'win': round(final_probs[0], 4),
            'draw': round(final_probs[1], 4),
            'lose': round(final_probs[2], 4),
            'confidence': confidence,
            'is_upset': is_upsets,
            'model_preds': {
                'odds': odds_prob,
                'pi_rating': pi_probs,
                'catboost': cb_prob,
                'xgboost': xgb_prob,
            },
            'features': features,
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
