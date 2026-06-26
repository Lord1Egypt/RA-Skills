# 市场情绪指标系统 (Market Sentiment Indicator System)

## 概述

L3 专家级能力提升 - 多维度市场情绪评分系统

本系统通过整合四大情绪维度（机构、散户、新闻、期权），提供全面的市场情绪分析和交易信号。

## 功能特性

### 1. 情绪维度

| 维度 | 权重 | 指标 |
|------|------|------|
| **机构情绪** | 40% | 北向资金流向、主力资金流向、龙虎榜机构买卖 |
| **散户情绪** | 20% | 融资融券余额变化、散户持仓比例、论坛舆情分析 |
| **新闻情绪** | 20% | 新闻舆情评分、政策解读、行业消息 |
| **期权情绪** | 20% | 期权隐含波动率、Put/Call 比率、期权持仓量 |

### 2. 情绪评分计算

```python
情绪评分 = 机构×0.4 + 散户×0.2 + 新闻×0.2 + 期权×0.2
```

**评分等级:**
- 90-100: 极度乐观
- 70-90: 乐观
- 50-70: 中性
- 30-50: 悲观
- 0-30: 极度悲观

### 3. 输出格式

```json
{
    "score": 75,
    "level": "乐观",
    "factors": {
        "institutional": 80,
        "retail": 70,
        "news": 65,
        "options": 75
    },
    "trend": "上升",
    "signal": "看涨",
    "timestamp": "2026-03-14T22:00:00",
    "weights": {
        "institutional": 0.4,
        "retail": 0.2,
        "news": 0.2,
        "options": 0.2
    }
}
```

## 快速开始

### 基础用法

```python
from market_sentiment import MarketSentimentAnalyzer

# 创建分析器
analyzer = MarketSentimentAnalyzer()

# 执行情绪分析
result = analyzer.analyze(symbol='sh')

# 打印结果
print(f"综合评分：{result['score']}")
print(f"情绪等级：{result['level']}")
print(f"交易信号：{result['signal']}")
```

### 获取 JSON 输出

```python
# 获取 JSON 格式结果
json_output = analyzer.analyze_to_json()
print(json_output)
```

### 回测验证

```python
from market_sentiment import MarketSentimentAnalyzer
from test_market_sentiment import SentimentBacktester

# 创建分析器和回测器
analyzer = MarketSentimentAnalyzer()
backtester = SentimentBacktester(analyzer)

# 运行回测
backtest_result = backtester.run_backtest(days=30)

# 获取统计信息
stats = backtest_result['statistics']
print(f"看涨胜率：{stats['bullish_win_rate']}%")
print(f"看跌胜率：{stats['bearish_win_rate']}%")
```

## 文件结构

```
skills/technical-indicators/
├── market_sentiment.py       # 主模块
├── test_market_sentiment.py  # 测试与回测模块
├── backtest_result.json      # 回测结果
└── README_MARKET_SENTIMENT.md # 本文档
```

## API 参考

### MarketSentimentAnalyzer

#### 初始化
```python
analyzer = MarketSentimentAnalyzer()
```

#### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `analyze(symbol='sh')` | 执行综合分析 | Dict[str, Any] |
| `analyze_to_json()` | 获取 JSON 格式结果 | str |
| `get_sentiment_level(score)` | 根据评分获取情绪等级 | str |
| `get_signal(score, trend)` | 根据评分和趋势获取交易信号 | str |

#### 情绪维度计算

| 方法 | 说明 |
|------|------|
| `calculate_institutional_sentiment()` | 计算机构情绪 (40%) |
| `calculate_retail_sentiment()` | 计算散户情绪 (20%) |
| `calculate_news_sentiment()` | 计算新闻情绪 (20%) |
| `calculate_options_sentiment()` | 计算期权情绪 (20%) |

### SentimentBacktester

#### 初始化
```python
backtester = SentimentBacktester(analyzer)
```

#### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `run_backtest(days=30)` | 运行回测 | Dict[str, Any] |
| `generate_historical_signals(days)` | 生成历史信号 | List[Dict] |
| `analyze_signals(signals)` | 分析信号有效性 | Dict[str, Any] |
| `calculate_sharpe_ratio(signals)` | 计算夏普比率 | float |
| `calculate_max_drawdown(signals)` | 计算最大回撤 | float |

## 数据源

本系统使用 AkShare 库获取 A 股市场数据：

- **北向资金**: `stock_hsgt_fund_flow_summary_em()`
- **主力资金**: `stock_individual_fund_flow_rank()`
- **龙虎榜**: `stock_lhb_detail_daily_sina()`
- **融资融券**: `stock_margin_sse()`
- **行业板块**: `stock_board_industry_name_em()`
- **新闻舆情**: `stock_news_em()`

> **注意**: 部分数据源可能因网络问题或 API 变更而暂时不可用。系统已实现容错机制，会自动使用默认值。

## 回测结果示例

```json
{
  "statistics": {
    "total_signals": 30,
    "bullish_signals": 0,
    "bearish_signals": 7,
    "neutral_signals": 23,
    "bullish_win_rate": 0,
    "bearish_win_rate": 42.86,
    "overall_avg_return": -0.248
  },
  "sharpe_ratio": -4.329,
  "max_drawdown": -8.58
}
```

## 注意事项

1. **数据延迟**: 实时数据可能存在 15 分钟延迟
2. **网络依赖**: 需要稳定的网络连接获取实时数据
3. **容错机制**: 数据获取失败时使用默认值 (50 分中性)
4. **回测限制**: 当前回测使用模拟数据，实盘效果可能不同

## 版本历史

- **v1.0.0** (2026-03-14): 初始版本
  - 实现四大情绪维度
  - 完成数据源接入
  - 实现回测验证模块

## 依赖

```
akshare>=1.18.0
pandas>=2.0.0
numpy>=1.24.0
```

## 作者

AITechnicals 团队

## 许可证

MIT License
