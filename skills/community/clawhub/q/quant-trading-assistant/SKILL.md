---
name: quant-trading-assistant
description: >
  量化交易助手 - A股技术分析+量化选股。
  用于：分析A股实时行情、计算技术指标（均线/KDJ/MACD/布林带）、
  量化选股策略、生成交易信号、龙虎榜/情绪周期判断。
  触发场景：问股票、分析行情、选股推荐、风险提示、技术指标计算。
---

# 量化交易助手

> 整合热门Skill源码开发的A股量化交易工具，不只是数据展示，是真正的实战决策辅助。

## 核心能力

| 模块 | 能力 | 数据来源 |
|------|------|---------|
| 📊 **实时行情** | 腾讯/新浪API实时价格 | 腾讯财经/新浪财经 |
| 📈 **技术分析** | 均线/KDJ/MACD/布林带/量比 | 计算得出 |
| 💰 **量化选股** | PE/ROE/营收增速筛选 | 规则筛选 |
| 🔥 **情绪周期** | 冰点/启动/发酵/高潮/退潮 | 市场情绪判断 |
| 🐉 **龙头战法** | 连板/首阴/分歧转一致 | 实战逻辑 |
| ⚠️ **避坑指南** | ST/减持/商誉雷/PE异常 | 血泪教训 |
| 📋 **综合分析** | 多维度综合研判+建议 | 自动生成 |

## 股票代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 上交所 | sh + 6位 | sh600519 (贵州茅台) |
| 深交所 | sz + 6位 | sz000001 (平安银行) |
| 创业板 | sz + 6位 | sz300750 (宁德时代) |
| 科创板 | sh + 6位 | sh688981 (中芯国际) |

## 常用指数

| 指数 | 代码 |
|------|------|
| 上证指数 | sh000001 |
| 深证成指 | sz399001 |
| 创业板指 | sz399006 |
| 沪深300 | sh000300 |
| 科创50 | sh000688 |

## 核心功能

### 1. 实时行情查询

```python
from quant_trading_assistant import get_stock_quote

# 单股
quote = get_stock_quote('sh600519')
# 返回: {name, code, price, change, change_pct, open, high, low, volume, turnover, pe, PB}

# 批量查询
quotes = get_stock_quotes(['sh600519', 'sz000858', 'sz300750'])
```

### 2. 技术指标计算

```python
from quant_trading_assistant import get_technical_indicators

# 获取完整技术指标
indicators = get_technical_indicators('sh600519')
# 返回: {ma5, ma10, ma20, ma60, kdj{k/d/j}, macd{dif/dea/macd}, boll{upper/mid/lower}, ma_trend, volume_ratio}
```

### 3. 量化选股策略

```python
from quant_trading_assistant import quant_screen

# 量化筛选
result = quant_screen(
    pe_max=50,       # PE上限
    roe_min=15,      # ROE下限(%)
    growth_min=20,   # 营收增速下限(%)
    debt_max=70      # 资产负债率上限(%)
)
# 返回: 符合条件股票列表
```

### 4. 市场情绪判断

```python
from quant_trading_assistant import get_market_sentiment

# 获取市场情绪周期
sentiment = get_market_sentiment()
# 返回: {phase, score, change_pct, turnover, suggestion}
# phase: 冰点/启动前期/启动后期/发酵期/高潮期/分歧期/退潮期
```

### 5. 龙头战法信号

```python
from quant_trading_assistant import check_dragon_signals

# 检测龙头信号
signals = check_dragon_signals('sh600519')
# 返回: {signals: [{type, level, emoji, desc, action}], summary, action}
# 信号类型: 连板/首阴/分歧转一致/放量突破/回踩5日线/低位放量
```

### 6. 避坑风险检查

```python
from quant_trading_assistant import risk_check

# 风险检查
risk = risk_check('sh600519')
# 返回: {risks, risk_score, risk_level}
# risk_level: 安全/中等/高危
```

### 7. 综合分析报告

```python
from quant_trading_assistant import analyze_stock

# 综合分析一只股票
result = analyze_stock('sh600519')
# 返回完整分析报告，包含quote/technical/risk/dragon/sentiment/advice
```

## 命令行用法

```bash
# 分析单只股票
python quant_trading_assistant.py analyze sh600519

# 查询行情
python quant_trading_assistant.py quote sh600519

# 技术指标
python quant_trading_assistant.py tech sh600519

# 量化选股
python quant_trading_assistant.py screen

# 市场情绪
python quant_trading_assistant.py sentiment

# 龙虎信号
python quant_trading_assistant.py dragon sh600519
```

## 分析报告模板

```
## 📊 {股票名称}({代码}) 量化分析

### 📈 实时行情
| 指标 | 数值 | 信号 |
|------|------|------|
| 现价 | XX元 | 🟢涨/🔴跌 |
| 涨幅 | X% | - |
| 换手率 | X% | 高/低 |
| 市盈率 | X | 高/中/低 |
| 量比 | X | 放量/缩量 |

### 📉 技术面
- 均线: MA5=XX, MA10=XX, MA20=XX, MA60=XX
- KDJ: K=XX, D=XX, J=XX
- MACD: DIF=XX, DEA=XX, MACD=XX
- 布林带: 上轨=XX, 中轨=XX, 下轨=XX
- 趋势: {多头排列/空头排列/震荡整理}

### 🐉 龙头信号
- 最优信号: {信号类型}
- 动作建议: {操作建议}

### ⚠️ 风险检查
- 风险等级: {安全/中等/高危}
- 风险点: {无明显风险/具体风险}

### 🔥 市场情绪
- 当前阶段: {冰点/启动/发酵/高潮/分歧/退潮}
- 情绪评分: XX/100

### 💡 结论
**建议: {买入/持有/卖出/观望}**
- 买入逻辑: {X}
- 止损位: {X元(-8%)}
- 风险提示: {X}
```

## 技术指标说明

### 均线系统 (MA)
- MA5: 5日均线，短期趋势
- MA10: 10日均线，短中期趋势
- MA20: 20日均线，中期趋势
- MA60: 60日均线，长期趋势
- 多头排列: MA5 > MA10 > MA20 > MA60 → 强势
- 空头排列: MA5 < MA10 < MA20 < MA60 → 弱势

### KDJ指标
- K值: 快速随机指标
- D值: 慢速随机指标
- J值: 超买超卖预警
- KDJ金叉(K上穿D): 买入信号
- KDJ死叉(K下穿D): 卖出信号
- J>80: 超买区域，谨慎追高
- J<20: 超卖区域，关注反弹

### MACD指标
- DIF: 快线，EMA12-EMA26
- DEA: 慢线，DIF的9日EMA
- MACD柱: (DIF-DEA)×2
- DIF上穿DEA(金叉): 买入信号
- DIF下穿DEA(死叉): 卖出信号
- MACD柱由负转正: 动能转强
- MACD柱由正转负: 动能转弱

### 布林带 (BOLL)
- 上轨: MA20 + 2×标准差
- 中轨: MA20
- 下轨: MA20 - 2×标准差
- 价格触及上轨: 可能有压力
- 价格触及下轨: 可能有支撑
- 布林带收口: 变盘信号

## 量化选股策略

### 成长股策略
- 连续3年营收增速 ≥ 30%
- 净利润增速 ≥ 25%
- ROE ≥ 15%
- PE < 50

### 价值股策略
- 市盈率（PE）< 行业均值
- 股息率 ≥ 3%
- 资产负债率 ≤ 50%

### 短线策略
- 沿5日线上涨
- 放量突破（量比>1.5）
- 换手率3%-20%
- 无ST/减持/商誉雷

## 龙头战法信号

| 信号类型 | 说明 | 操作 |
|------|------|------|
| 🔥🔥🔥 连板 | 连续涨停，换手率3-20% | 打板介入 |
| 🔥🔥 首阴 | 涨停后次日回调 | 低吸博弈 |
| 🔥🔥🔥 分歧转一致 | 高开高走 | 追涨介入 |
| 🔥🔥 放量突破 | 量比>1.8，涨幅>3% | 跟进 |
| 🔥 回踩5日线 | 价格回踩MA5企稳 | 低吸 |
| 🔥🔥 低位放量 | 量比>2，低位启动 | 关注 |

## 风险提示

⚠️ **重要声明**
- 本分析仅供参考，不构成投资建议
- 市场有风险，投资需谨慎
- 亏损8%请无条件止损
- 请根据自身风险承受能力决策

## 更新日志

### v1.0.1 (2026-03-22)
- 修复：Windows控制台UTF-8编码输出问题
- 修复：_meta.json作者信息修正为dxie48892-jpg
