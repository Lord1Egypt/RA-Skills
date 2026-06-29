# 综合数据模型 v3.1 - 技术设计文档

> **版本**: v3.1 (深度Polymarket集成)  
> **日期**: 2026-06-16  
> **作者**: world-cup-predictor-enhanced

## 1. 概述

v3.1 是基于v3.0的深度升级版本，核心改进是**全面接入Polymarket订单簿数据**，从单一赔率查询升级到订单簿级别的市场微观结构分析。

## 2. 三大数据源架构

```
┌─────────────────────────────────────────────────────┐
│           综合数据模型 v3.1 架构                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ 真实FIFA Elo │  │  Polymarket  │  │ 中国体彩   ││
│  │   (40%)      │  │    (35%)     │  │   (25%)   ││
│  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘│
│         │                 │                 │      │
│         └─────────────────┼─────────────────┘      │
│                           ▼                         │
│                  ┌─────────────────┐                │
│                  │  综合概率计算   │                │
│                  └────────┬────────┘                │
│                           ▼                         │
│                  ┌─────────────────┐                │
│                  │  市场质量评分   │                │
│                  │  (0-100分)      │                │
│                  └────────┬────────┘                │
│                           ▼                         │
│                  ┌─────────────────┐                │
│                  │   最终EV计算    │                │
│                  └─────────────────┘                │
└─────────────────────────────────────────────────────┘
```

## 3. 权重设计

| 数据源 | 权重 | 理由 |
|--------|------|------|
| **真实FIFA Elo模型** | 40% | 客观可复现、覆盖所有球队、可计算 |
| **Polymarket** | 35% | $24.5亿真金白银投票、订单簿深度信息 |
| **中国体彩** | 25% | 中国市场真实赔率、含庄家利润校准 |

## 4. 核心模型：双模式评分

### 4.1 模型选择逻辑
```
Elo差 ≥ 15分 → 爆冷模式（upset_factor + 对数衰减）
Elo差 < 15分 → 平衡模式（泊松分布）
matchday=1  → 小组赛首轮谨慎因子 +6%
```

### 4.2 平衡模式公式
```python
# Elo差计算
elo_diff = (home_elo * home_factor) - (away_elo * away_factor) + home_advantage

# 主胜率（标准Elo公式）
win_prob = 1 / (1 + 10^(-elo_diff / 400))

# 平局概率（动态）
if actual_diff < 50:   base_draw = 0.36
elif actual_diff < 100: base_draw = 0.32
elif actual_diff < 200: base_draw = 0.28
else:                   base_draw = 0.22

# 小组赛首轮谨慎因子
if matchday == 1: cautious_boost = 0.06
draw_prob = min(0.50, base_draw + cautious_boost)
```

### 4.3 爆冷模式公式
```python
# 强队基础胜率
stronger_win = 1 / (1 + 10^(-actual_diff / 400))

# 爆冷因子（对数衰减）
upset_factor = min(0.30, 0.10 * log(1 + actual_diff/100))

# 强队胜率因爆冷降低
stronger_adjusted = stronger_win * (1 - upset_factor)

# 平局概率
if actual_diff < 100:  base_draw = 0.36
elif actual_diff < 200: base_draw = 0.32
elif actual_diff < 300: base_draw = 0.30
else:                   base_draw = 0.26
if matchday == 1: cautious_boost = 0.06
```

## 5. 10类预测因子体系

| 因子 | 权重 | 计算方式 |
|------|------|----------|
| 基础Elo | 35% | 1300-2000 Elo区间 |
| 伤病与上场概率 | 15% | 主力+位置差异化权重 |
| 近期比赛状态 | 12% | 近5场加权评分 |
| 比赛日天气 | 8% | 温度/降水/风力 |
| 小组排名 | 7% | 出线形势对战意 |
| 平均攻防数据 | 7% | 进球/失球差值 |
| 主场优势 | 5% | 中立25/真实70 Elo |
| 实时赛事平局率 | 5% | 同阶段校正 |
| 平局偏差 | 4% | 历史对战 |
| 战术克制关系 | 2% | 风格相克 |

## 6. Polymarket 订单簿深度集成

### 6.1 接入端点
- `GET /book` - 完整订单簿
- `GET /midpoint` - 中间价
- `GET /spread` - 买卖价差
- `GET /price` - 当前价格
- `GET /markets` - 市场列表
- `GET /events` - 事件列表

### 6.2 关键指标计算

**1. 简单中间价**
```python
mid = (best_bid + best_ask) / 2
```

**2. 深度加权中间价（更稳定）**
```python
def weighted_midpoint(book, depth=3):
    top_bids = book.bids[:depth]  # 前N档买单
    top_asks = book.asks[:depth]  # 前N档卖单
    bid_avg = Σ(price × size) / Σ(size)
    ask_avg = Σ(price × size) / Σ(size)
    return (bid_avg + ask_avg) / 2
```

**3. 流动性**
```python
total_liquidity = Σ(bid_sizes) + Σ(ask_sizes)
```

**4. 市场质量评分 (0-100)**
```python
score = 0
# 流动性贡献 (0-40)
if total_liquidity > 100000: score += 40
elif total_liquidity > 50000: score += 30
# 价差贡献 (0-30)
if spread < 0.005: score += 30
elif spread < 0.01: score += 25
# 深度贡献 (0-30)
if bid_depth + ask_depth >= 10: score += 30
```

## 7. 综合概率计算

```python
weighted_prob = (model_prob × 0.40 + 
                poly_prob × 0.35 + 
                cn_prob × 0.25)
quality_adj = (poly_quality / 100) × 0.1 + 0.9
final_prob = weighted_prob × quality_adj
```

## 8. EV计算

```python
ev = final_prob × odds - 1
```

## 9. 模型验证历史

| 阶段 | 准确率 | 备注 |
|------|--------|------|
| v1.0 | 0/4 = 0% | 6/16预测4场全错 |
| v2.0 | 3/3 = 100% | 2024欧洲杯3场 |
| v2.1 | 6/11 = 54.5% | 扩展回测11场 |
| v3.0 | 25/25 测试通过 | 单元测试 |
| v3.1 | 6/17 实战 | 待验证 |

## 10. 已知局限性

1. 模型在2022世界杯的极端爆冷（沙特胜阿根廷等）仍难预测
2. Polymarket部分比赛（特别是小组赛早期）的单场市场还未上架
3. 模型没有考虑：天气实时变化、球员个人状态、裁判倾向
4. 历史数据有限（6/16的0%准确率是前车之鉴）

## 11. 未来改进方向

1. 接入football-data.org获取实时伤停
2. 接入Open-Meteo获取场馆精准天气预报
3. 引入XGBoost机器学习（需要2022世界杯64场+2024欧洲杯36场作为训练集）
4. 增加"世界杯经验"因子（球队历史参赛经验）
5. 增加"小组赛紧张度"因子（出线形势对战意的影响）

## 12. 使用示例

```python
from predictor import WorldCupPredictor
from predictor.data import PolymarketClient
from predictor.calibration import MarketCalibrator

# 1. 基础预测
predictor = WorldCupPredictor()
prediction = predictor.predict(match_info)

# 2. 获取Polymarket数据
poly = PolymarketClient()
odds = poly.get_midpoint(token_id)

# 3. 综合校准
calibrator = MarketCalibrator(poly)
report = calibrator.generate_report(model_probs=..., match_calibrations=...)
```

## 13. 依赖

- Python 3.9+
- requests
- urllib3
- math, json, datetime（标准库）

无重型依赖，可直接在任何Python环境运行。

