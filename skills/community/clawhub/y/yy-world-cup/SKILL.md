---
name: world-cup-predictor-enhanced
description: Use when predicting World Cup match results and generating China Sports Lottery betting strategies (胜平负/让球/半全场/总进球/比分), including injury factor analysis, weather impact assessment, market price calibration with Polymarket, and **3 differentiated strategies** with hidden odds estimation. **All times must be 北京时间** - Polymarket endDate is UTC, requires +8h conversion.
---

# 增强版世界杯预测器 v3.6.0

## Overview
基于双模式评分模型和Elo评级系统的增强型世界杯赛事预测工具，**v3.6.0 重大升级**：
- **真实FIFA Elo** (Wikipedia官方)
- **Polymarket市场赔率** (P2P预测市场)
- **中国体彩盘口估算** (基于Polymarket + 8%庄家利润)
- **🆕 时区正确处理**: 严格区分北京时间 vs UTC
- **🆕 动态赛程**: 不再 hard-code，从 Polymarket 实时拉取
- **🆕 差异化策略**: 3 种玩法不同 (单关/让球/半全场+心理战)
- **🆕 隐藏赔率推算**: 让球/半全场等中国体彩盘口
- **🆕 AI 深度见解**: C罗心理战 + 历史交锋 + 实力悬殊判断

## v3.6.0 关键能力

### 1. 时区严格处理 (用户反馈后修复)
```python
from predictor.utils.timezone import bjt_day_range, is_in_bjt_day, utc_to_bjt_str

# 北京时间 6/18 当天 = UTC 6/17 16:00 ~ UTC 6/18 16:00
utc_start, utc_end = bjt_day_range('2026-06-18')
```

### 2. 动态赛程拉取
```python
from predictor.data.polymarket_client import PolymarketClient

poly = PolymarketClient()
matches = poly.get_matches_by_bjt('2026-06-18')  # 北京时间6/18的所有比赛
# Returns: 葡萄牙/英格兰/加纳/乌兹别克 vs 刚果/克罗地亚/巴拿马/哥伦比亚
```

### 3. 差异化3种策略
- **策略1 (稳)**: 单关 - 押最高胜率 (葡萄牙胜 1.45)
- **策略2 (中)**: 2串1 - 让球混合 (实力悬殊场让1球胜 + 实力接近场让1球平)
- **策略3 (高)**: 半场+让球 - 含 C 罗心理战

### 4. 让球玩法逻辑 (用户纠正后修复)
- **让1球胜** = 强队**赢2球以上** → 用于实力悬殊场 (Elo 差 > 150)
- **让1球平** = 强队**赢1球** → 用于实力接近场 (Elo 差 < 100)
- ❌ 错误: 实力悬殊场推"让1球平", 实力接近场推"让1球胜"

### 5. 隐藏赔率推算公式
```
体彩胜平负赔率 = 1 / (Polymarket概率 × 0.92)   # 8% 庄家利润
让1球胜赔率 ≈ 1 / (主胜概率 × 0.95)
让1球平赔率 ≈ 1 / (主胜概率 × 0.90)
半场胜赔率 ≈ 1 / (主胜概率 × 0.88)
```

## v3.0 核心能力（保留）

## When to Use
- 需要预测世界杯单场或多场比赛结果时
- 需要生成中国体育彩票足球竞猜购票策略时
- 需要对比模型预测与Polymarket市场赔率找套利机会时
- 需要结合多数据源（FIFA+Polymarket+体彩）综合分析时

**When NOT to use**
- 非世界杯赛事预测（可适配但针对性优化不足）
- 用于非法赌博用途（仅支持合法中国体育彩票分析）
- 构成任何投注建议（所有结果仅供参考，投注风险自担）

## v3.0 核心能力

### 🔴 6/16 实测结果（基准）
- **赛前预测准确率**: 0/4 (0%) — 4场全预测胜负，实际全平局
- **6/16后修复**: 引入"小组赛首轮谨慎因子"，平局概率从18%提升到25-40%
- **6/17 EV发现**: 利用体彩真实盘口找到多个正EV玩法（最高+43.4%）

### 🎯 三大数据源对比

| 数据源 | 优势 | 限制 |
|--------|------|------|
| 真实FIFA Elo | 客观、可复现、覆盖全部球队 | 不反映伤停/天气等即时因素 |
| Polymarket市场 | $24.5亿真金白银投票，反映集体智慧 | 部分比赛可能未上架 |
| 中国体彩盘口 | 中国市场真实赔率、含庄家利润 | 仅比赛前1-2天公布 |

### 📊 v3.0 修复历程

| 版本 | 修复点 | 验证 |
|------|--------|------|
| v1.0 | 基础Elo模型（用编造数据） | 失败 |
| v2.0 | 修复upset_mode bug，补全因子 | 2024欧洲杯3/3 |
| v2.1 | 引入首轮谨慎因子 | 15场66.7%准确率 |
| v3.0 | 整合Polymarket + 体彩 | 25个测试通过 |

## 目录结构
```
world-cup-predictor-enhanced/
├── SKILL.md                       # 本文件
├── predictor/
│   ├── __init__.py
│   ├── core.py                    # 双模式预测引擎（v2.1）
│   ├── factors.py                 # 10类预测因子
│   ├── calibration.py             # 🆕 市场赔率校准器（v3.0）
│   ├── enhanced_demo.py           # 🆕 综合演示脚本（v3.0）
│   ├── data/                      # 数据接入层
│   │   ├── models.py
│   │   ├── api_client.py          # balldontlie FIFA API
│   │   ├── polymarket_client.py   # 🆕 Polymarket API（v3.0）
│   │   └── cache.py
│   ├── strategy/                  # 策略引擎
│   │   ├── lottery.py
│   │   ├── conservative.py
│   │   └── aggressive.py
│   └── validator/                 # 验证模块
│       └── backtest.py
├── tests/                         # 🆕 25个测试全部通过
│   ├── test_factors.py
│   └── test_polymarket.py         # 🆕 v3.0 测试
└── data/                          # 运行时数据
```

## 核心模式

### 双模式预测模型
```
Elo差 ≥ 15分 → 爆冷模式（爆冷因子+客胜加权）
Elo差 < 15分 → 平衡模式（泊松分布+动态平局）
小组赛首轮  → 谨慎因子 +6%（v2.1新增）
```

### 10类预测因子
| 因子 | 权重 | 说明 |
|------|------|------|
| 基础Elo | 35% | 1600-1950区间 |
| 伤病上场概率 | 15% | 主力+位置差异化 |
| 近期状态 | 12% | 近5场加权 |
| 天气影响 | 8% | 温度/降水/风力 |
| 小组排名 | 7% | 出线形势对战意 |
| 攻防数据 | 7% | 进球/失球差值 |
| 主场优势 | 5% | 中立25/真实70 Elo |
| 平局率 | 5% | 同阶段校正 |
| 平局偏差 | 4% | 历史对战 |
| 战术克制 | 2% | 风格相克 |

### 三种数据源整合
```
真实FIFA Elo → 基础预测概率
        ↓
Polymarket市场 → 校验/调整（24.5亿市场智慧）
        ↓
中国体彩盘口 → 中国市场赔率 + 庄家利润评估
        ↓
最终预测 + 套利机会报告
```

## 快速使用

### 综合预测（含市场校准）
```python
from predictor.enhanced_demo import enhanced_predict_6_17
enhanced_predict_6_17()  # 6/17 3场完整预测+EV分析
```

### 单场比赛预测
```python
from predictor import WorldCupPredictor
from predictor.data import Team, MatchInfo, TeamStyle

home = Team(id=1, name="France", elo=1870, style=TeamStyle.BALANCED, ...)
away = Team(id=2, name="Senegal", elo=1684, style=TeamStyle.PHYSICAL, ...)
match = MatchInfo(home_team=home, away_team=away, ..., is_neutral=True)

pred = WorldCupPredictor().predict(match)
print(f"主胜 {pred.home_win_prob*100:.1f}%")
```

### Polymarket市场数据
```python
from predictor.data import PolymarketClient

poly = PolymarketClient()
wc = poly.get_world_cup_winner()
print(f"法国: {wc['teams']['France']*100:.2f}%")  # 17.65%
```

### 市场校准报告
```python
from predictor.calibration import MarketCalibrator

cal = MarketCalibrator()
report = cal.generate_report(
    model_winner_probs={'France': 0.20, 'Spain': 0.13, ...}
)
print(MarketCalibrator.format_report(report))
```

## 单元测试
```bash
# 全部25个测试
python3 -m unittest tests.test_factors tests.test_polymarket -v

# 仅Polymarket相关
python3 -m unittest tests.test_polymarket -v
```

## Important Disclaimer
1. 本工具所有预测仅供参考，不构成任何投注建议
2. 中国体育彩票购买请遵守国家相关法律法规，理性购彩
3. 彩票有风险，投注需谨慎，未成年人禁止购彩
4. 模型存在历史失败案例（6/16预测0%准确率），使用前请充分测试
5. 套利机会仅基于模型估算，实际赔率会随时间变化

## 上传状态
- **ClawHub URL**: https://clawhub.ai/deloyong/yy-world-cup
- **当前版本**: v3.0 (待发布)
- **已发布版本**: v2.0 (v3.0 待手动上传)
