# 特征工程详细说明

## 28维特征向量

| # | 特征名 | 描述 | 单位 | 来源模型权重 |
|---|--------|------|------|------------|
| 1 | pi_diff | Pi-Rating进攻-防守综合差值 | 数值 | 20% |
| 2 | pi_home_exp | Pi-Rating主队预期得分 | 数值 | 20% |
| 3 | pi_away_exp | Pi-Rating客队预期得分 | 数值 | 20% |
| 4 | win_odds | 主胜赔率 | 赔率 | 25% |
| 5 | draw_odds | 平局赔率 | 赔率 | 25% |
| 6 | lose_odds | 主负赔率 | 赔率 | 25% |
| 7 | odds_change | 赔率变化趋势 | ±值 | 25% |
| 8 | odds_implied_win | 赔率隐含主胜概率 | % | 25% |
| 9 | odds_implied_draw | 赔率隐含平局概率 | % | 25% |
| 10 | odds_implied_lose | 赔率隐含主负概率 | % | 25% |
| 11 | home_form | 主队近期5场得分率 | 0-1 | 15% |
| 12 | away_form | 客队近期5场得分率 | 0-1 | 15% |
| 13 | form_diff | 主客队状态差 | 差值 | 15% |
| 14 | home_win_rate | 主队联赛胜率 | % | 10% |
| 15 | away_win_rate | 客队联赛胜率 | % | 10% |
| 16 | home_goals_avg | 主队场均进球 | 数值 | 10% |
| 17 | away_goals_avg | 客队场均进球 | 数值 | 10% |
| 18 | home_goals_conceded | 主队场均失球 | 数值 | 10% |
| 19 | away_goals_conceded | 客队场均失球 | 数值 | 10% |
| 20 | home_boost | 联赛主场优势系数 | 系数 | 10% |
| 21 | home_absent | 主队缺阵人数 | 人数 | 10% |
| 22 | away_absent | 客队缺阵人数 | 人数 | 10% |
| 23 | absent_diff | 伤病差值 | 差值 | 10% |
| 24 | h2h_home_winrate | 历史交锋主队胜率 | % | 8% |
| 25 | h2h_count | 历史交锋样本数 | 场次 | 8% |
| 26 | home_rest_days | 主队休息天数 | 天 | 7% |
| 27 | away_rest_days | 客队休息天数 | 天 | 7% |
| 28 | rest_diff | 休息天数差 | 天 | 7% |
| 29 | temperature | 比赛气温 | ℃ | 5% |
| 30 | referee_bias | 裁判对主队偏好 | 0-1 | 5% |

## Pi-Rating 计算公式

```
主队预期得分 = 主队进攻评分 - 客队防守评分 + 主场优势
客队预期得分 = 客队进攻评分 - 主队防守评分

进攻评分更新 = 旧评分 + η × (实际进球 - 预期进球) × 0.5
防守评分更新 = 旧评分 - η × (实际失球 - 预期失球) × 0.3
```

## CatBoost + XGBoost 融合策略

```
最终概率 = 赔率概率 × 25% + Pi-Rating概率 × 20% + CatBoost × 20% + XGBoost × 15%

CatBoost特征重要性排序：
  1. pi_diff (Pi-Rating分差)
  2. odds_implied_win (赔率隐含概率)
  3. form_diff (近期状态差)
  4. home_goals_avg (主场场均进球)
  5. h2h_home_winrate (历史交锋)
```
