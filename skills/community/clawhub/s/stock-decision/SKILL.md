---
name: stock-decision
description: "Comprehensive stock decision analysis combining technical indicators (MA, MACD, KDJ, RSI, DMI), macro environment assessment (industry cycle, governance, macro economy), and historical backtesting. Provides buy/sell recommendations with stop-loss/take-profit levels."
description_zh: "综合股票决策分析：技术指标（MA/MACD/KDJ/RSI/DMI）+ 宏观环境（行业周期/公司治理/宏观经济）+ 历史回测，提供买卖建议和止盈止损价位"
version: 2.4.0
allowed-tools: Bash,Read,Search
---

# Stock Decision — 综合股票决策分析

基于改进策略一的完整股票决策分析系统，整合技术面、宏观面和历史回测。

## 触发条件

当用户询问以下内容时使用此技能：
- "腾讯控股可以买入吗？"
- "00700今天适合买吗？"
- "帮我分析一下XX股票的买入点"
- "这只股票现在能买吗？"
- "XX股票止盈止损设置在哪里？"
- "XX股票风险大吗？"

## 核心功能

### 1. 技术面分析 (Improved Strategy 1)

**7个买入条件**：
- ✅ 均线多头排列 (MA5 > MA10 > MA20 > MA60)
- ✅ MACD金叉 (DIF > DEA,且在零轴上方)
- ✅ KDJ金叉 (K > D,且K值在20-80之间)
- ✅ RSI适中 (RSI12在50-70之间)
- ✅ 价格站上MA20 (收盘价 > MA20)
- ✅ 成交量放大 (较5日均值放大30%以上)
- ✅ DMI多头 (PDI > MDI,且ADX > 20)

**6个高位预警**：
- ⚠️ KDJ超买 (K > 70)
- ⚠️ RSI超买 (RSI12 > 65)
- ⚠️ 偏离MA20 (偏离度 > 15%)
- ⚠️ 突破布林带上轨
- ⚠️ 近期涨幅过大 (近5日涨幅 > 25%)
- ⚠️ OBV背离

**技术评分**：
```
技术评分 = (满足条件数 × 10) - (预警数量 × 5) + 50
范围: 0-100分

85-100分: ✅✅✅ 强烈推荐买入
70-84分: ✅✅ 推荐买入
60-69分: ✅ 谨慎买入
50-59分: ⏸️ 观望
0-49分: ❌ 不建议买入
```

### 2. 宏观环境分析 (自动查询)

**行业周期判断**：
- 上行期: 调整系数 1.0
- 平稳期: 调整系数 0.9
- 下行期: 调整系数 0.6
- 衰退期: 调整系数 0.4

**公司治理评估**：
- 无明显问题: 调整系数 1.0
- 轻微问题: 调整系数 0.85
- 中等问题: 调整系数 0.6
- 严重问题: 调整系数 0.2

**宏观经济环境**：
- 利好环境: 调整系数 1.1
- 中性环境: 调整系数 1.0
- 利空环境: 调整系数 0.85
- 严重利空: 调整系数 0.5

### 3. 历史回测

**回测策略**：
- 买入条件: 满足5/7以上技术指标，且高位预警≤2个
- 仓位管理: 每次买入30%仓位
- 卖出条件:
  - 止损: 跌破MA20且亏损超过5%
  - 止盈1: 收益超过20%
  - 止盈2: 偏离MA20超过25%
  - 止盈3: RSI严重超买且收益超过15%
  - 止盈4: 连续3天下跌且收益为正

**关键指标**：
- 胜率: 盈利交易占比
- 平均收益率: 每笔交易平均收益
- 最大回撤: 从峰值到谷底的最大跌幅
- 风险收益比: 平均收益 / 最大回撤

## 使用方法

### 基本工作流

```bash
# 1. 获取股票数据（使用westock-data技能）
node ~/.workbuddy/skills/westock-data/scripts/index.js search <股票名称或代码>
node ~/.workbuddy/skills/westock-data/scripts/index.js kline <代码> daily 120 hfq
node ~/.workbuddy/skills/westock-data/scripts/index.js technical <代码> ma,macd,kdj,rsi,dmi

# 2. 技术分析
python ~/.workbuddy/skills/stock-decision/scripts/analyze.py <股票名称或代码>

# 3. 宏观环境分析
python ~/.workbuddy/skills/stock-decision/scripts/macro_analyzer.py <股票名称> <股票代码> <行业>

# 4. 历史回测
python ~/.workbuddy/skills/stock-decision/scripts/backtest.py <股票代码> [回测天数]
```

### 示例

```bash
# 分析腾讯控股
node ~/.workbuddy/skills/westock-data/scripts/index.js search 腾讯
python ~/.workbuddy/skills/stock-decision/scripts/analyze.py 腾讯
python ~/.workbuddy/skills/stock-decision/scripts/macro_analyzer.py 腾讯 hk00700 互联网
python ~/.workbuddy/skills/stock-decision/scripts/backtest.py hk00700 120

# 分析康方生物
python ~/.workbuddy/skills/stock-decision/scripts/analyze.py 康方生物
python ~/.workbuddy/skills/stock-decision/scripts/macro_analyzer.py 康方生物 hk09926 生物医药
python ~/.workbuddy/skills/stock-decision/scripts/backtest.py hk09926 120
```

## 输出格式

### 技术分析输出

```
📊 股票基本信息
━━━━━━━━━━━━━━━━━━━━━━━━━━
股票名称: 康方生物
股票代码: hk09926
当前价格: 139.3港元
MA5/MA10/MA20/MA60: [详细数据]

📈 技术面分析 (改进策略一)
━━━━━━━━━━━━━━━━━━━━━━━━━━

7个买入条件满足情况:
[详细列表]

6个高位预警信号:
[详细列表]

技术评分: 77/100

⭐ 技术评级
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅✅ 推荐买入
综合评分: 77/100
风险等级: 🟢 中低风险

🎯 止盈止损建议
━━━━━━━━━━━━━━━━━━━━━━━━━━
[具体价位]
```

### 宏观环境输出

```json
{
    "industry": {
        "status": "stable",
        "risk_coefficient": 1.0,
        "adjustment_coefficient": 0.9,
        "reasoning": ["行业处于平稳期,需求稳定,政策中性"]
    },
    "governance": {
        "status": "none",
        "risk_coefficient": 1.0,
        "adjustment_coefficient": 1.0,
        "reasoning": ["公司治理良好,无明显问题"]
    },
    "macro": {
        "status": "neutral",
        "risk_coefficient": 1.0,
        "adjustment_coefficient": 1.0,
        "reasoning": ["宏观经济环境中性,政策稳健"]
    },
    "total_coefficient": 0.9
}
```

### 历史回测输出

```
📊 改进策略一 回测报告
━━━━━━━━━━━━━━━━━━━━━━━━━━

股票代码: hk00700
回测天数: 120天

📈 交易统计
━━━━━━━━━━━━━━━━━━━━━━━━━━
总交易次数: 12次
盈利交易: 8次
亏损交易: 4次
胜率: 66.67%

💰 收益统计
━━━━━━━━━━━━━━━━━━━━━━━━━━
总收益: 25,600港元
平均收益率: 12.5%
最大回撤: 8.5%

📋 交易明细
━━━━━━━━━━━━━━━━━━━━━━━━━━
[详细交易记录]
```

## 综合评分计算

```
综合评分 = 技术评分 × 行业系数 × 治理系数 × 宏观系数

示例：
技术评分: 77分
行业系数: 0.9 (平稳期)
治理系数: 1.0 (无问题)
宏观系数: 1.0 (中性)

综合评分 = 77 × 0.9 × 1.0 × 1.0 = 69.3分
评级: ✅ 谨慎买入
```

## 止盈止损建议

### 多层止盈

```
第一止盈点 = MA20 × 1.15 (偏离度达15%)
第二止盈点 = MA20 × 1.20 (偏离度达20%)
第三止盈点 = 成本价 × 1.05 (回本+5%)
理想止盈点 = MA60 × 1.30
```

### 止损设置

```
基础止损 = MA20
严格止损 = MA60
最大风险 = (MA20 / 当前价格 - 1) × 100%
```

## 注意事项

- 本技能提供的技术分析和决策建议仅供参考，不构成任何投资建议
- 投资有风险，入市需谨慎
- 用户应根据自身风险承受能力和投资目标独立做出决策
- 宏观环境分析需要联网查询最新信息
- 历史回测结果不代表未来表现
- 建议结合技术面、宏观面和回测结果综合判断

## 脚本说明

- **analyze.py**: 技术面分析核心脚本，基于改进策略一
- **macro_analyzer.py**: 宏观环境自动化分析器
- **backtest.py**: 历史回测引擎

## 依赖技能

- westock-data: 获取股票数据和技术指标
- web_search: 查询宏观环境信息（可选）

## 版本历史

### v2.0.0 (2026-04-01)
- 新增宏观环境自动化分析
- 新增历史回测功能
- 优化SKILL.md符合WorkBuddy标准规范

### v1.0.0 (2026-04-01)
- 初始版本
- 实现技术面分析（改进策略一）
- 实现止盈止损建议
