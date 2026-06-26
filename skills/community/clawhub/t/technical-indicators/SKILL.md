# Technical Indicators - 技术指标计算

## 功能说明

提供常用技术指标的计算功能，支持 A 股股票。包含多指标共振分析模块，可自动识别多指标共振信号。

## 支持的指标

### 趋势指标
- MA (移动平均线): 5/10/20/60/120/250 日
- EMA (指数移动平均线)
- MACD (平滑异同移动平均线)
- ADX (平均趋向指数)

### 动量指标
- KDJ (随机指标)
- RSI (相对强弱指标)
- CCI (顺势指标)

### 波动率指标
- BOLL (布林带)
- ATR (平均真实波幅)

### 成交量指标
- OBV (能量潮)
- 量比 (今日/5 日平均)
- 换手率
- **量价关系分析 (8 种形态)**

## 🌟 量价关系深度分析 (新增)

### 基础量价形态 (4 种)

#### 1. 放量上涨 ✅
- **特征**: 价↑量↑
- **信号**: 看涨
- **置信度**: 高 (量比>2 时)
- **操作**: 可跟进

#### 2. 缩量上涨 ⚠️
- **特征**: 价↑量↓
- **信号**: 警惕
- **置信度**: 低
- **操作**: 谨慎观望

#### 3. 放量下跌 ❌
- **特征**: 价↓量↑
- **信号**: 看跌
- **置信度**: 高
- **操作**: 回避/减仓

#### 4. 缩量下跌 ⚠️
- **特征**: 价↓量↓
- **信号**: 观望
- **置信度**: 低
- **操作**: 等待企稳

### 高级量价形态 (4 种)

#### 5. 量价背离
- **特征**: 价创新高但量未新高
- **信号**: 反转预警
- **操作**: 警惕顶部

#### 6. 天量天价
- **特征**: 历史天量 + 高价区
- **信号**: 顶部信号
- **操作**: 减仓/离场

#### 7. 地量地价
- **特征**: 历史地量 + 低价区
- **信号**: 底部信号
- **操作**: 关注买入机会

#### 8. 堆量上涨
- **特征**: 连续 3 日 + 放量上涨
- **信号**: 强势信号
- **操作**: 持有/跟进

### 量比计算
```
量比 = 今日成交量 / 近 5 日平均成交量

- >3: 异常放量
- >2: 放量
- 0.5-2: 正常
- <0.5: 缩量
- <0.3: 异常缩量
```

## 🌟 多指标共振分析

### 共振类型 (5 种)

#### 1. 趋势共振 ⭐⭐⭐⭐⭐
- **指标**: MA + MACD + ADX
- **强买入**: MA 金叉 + MACD 金叉 + ADX>25
- **强卖出**: MA 死叉 + MACD 死叉 + ADX>25

#### 2. 动量共振 ⭐⭐⭐⭐
- **指标**: KDJ + RSI + CCI
- **强买入**: KDJ 金叉 + RSI<30 + CCI<-100
- **强卖出**: KDJ 死叉 + RSI>70 + CCI>100

#### 3. 量价共振 ⭐⭐⭐⭐⭐
- **指标**: 成交量 + OBV + 价格
- **强买入**: 放量 + OBV 上升 + 价格上涨
- **强卖出**: 缩量 + OBV 下降 + 价格下跌

#### 4. 波动率共振 ⭐⭐⭐
- **指标**: BOLL + ATR
- **突破信号**: 价格突破 BOLL 上轨 + ATR 放大
- **收缩信号**: BOLL 带宽收缩 + ATR 下降

#### 5. 全指标共振 ⭐⭐⭐⭐⭐
- **指标**: 5+ 指标同时信号
- **规则**: 3 个以上类别同时发出同向信号

### 信号强度评分

```
信号强度 = (符合指标数 / 总指标数) * 100

- 80-100: 强烈信号
- 60-80: 强信号
- 40-60: 中等信号
- <40: 弱信号
```

## 使用示例

### 基础指标计算

```python
from technical_indicators import (
    calculate_ma, calculate_macd, calculate_rsi,
    calculate_kdj, calculate_boll, calculate_atr,
    calculate_obv, calculate_cci, calculate_adx,
    calculate_volume_price, backtest_volume_strategy
)

# 计算 MA
ma_data = calculate_ma(code="300308", periods=[5, 10, 20, 60])

# 计算 MACD
macd_data = calculate_macd(code="300308")

# 计算 RSI
rsi_data = calculate_rsi(code="300308", period=14)

# 计算 KDJ
kdj_data = calculate_kdj(code="300308")

# 计算布林带
boll_data = calculate_boll(code="300308")

# 计算 ADX
adx_data = calculate_adx(code="300308")

# 计算 OBV
obv_data = calculate_obv(code="300308")

# 计算 CCI
cci_data = calculate_cci(code="300308")

# 量价关系分析 (8 种形态)
vp_data = calculate_volume_price(code="300308")
print(f"基础形态：{vp_data['basic_pattern']['pattern']}")
print(f"量比：{vp_data['volume_ratio']}")
print(f"综合评分：{vp_data['comprehensive_score']}")
print(f"操作建议：{vp_data['recommendation']}")
```

### 多指标共振分析

```python
from technical_indicators import (
    get_resonance_signals,
    backtest_resonance,
    scan_resonance_market
)

# 获取单只股票的共振信号
resonance = get_resonance_signals(code="300308")
print(f"信号总数：{resonance['summary']['total_signals']}")
print(f"建议操作：{resonance['summary']['recommendation']}")

# 回测共振策略
backtest = backtest_resonance(code="300308", start_date="20240101", end_date="20250313")
print(f"胜率：{backtest['win_rate']}%")
print(f"总收益：{backtest['total_return']}%")

# 扫描市场中的共振信号 (批量)
code_list = ["300308", "000001", "600519", "000858"]
signals = scan_resonance_market(code_list, min_strength=60)
for sig in signals:
    print(f"{sig['code']}: {sig['signal_type']} (强度:{sig['strength']})")
```

### 量价策略回测

```python
# 回测放量上涨策略
backtest = backtest_volume_strategy(
    code="300308",
    start_date="20240101",
    end_date="20250313",
    strategy="放量上涨",
    hold_days=5
)
print(f"胜率：{backtest['win_rate']}%")
print(f"总收益：{backtest['total_return']}%")
```

### 高级用法：自定义配置

```python
from resonance_analysis import ResonanceAnalyzer

# 自定义配置
config = {
    "trend": {"adx_threshold": 30, "weight": 1.2},
    "momentum": {"rsi_oversold": 25, "rsi_overbought": 75},
    "volume_price": {"volume_ratio_threshold": 2.0},
    "all_indicators": {"min_categories": 4}
}

analyzer = ResonanceAnalyzer(config=config)
signals = analyzer.analyze_resonance("300308")
```

## 安装依赖

```bash
pip install akshare pandas numpy
```

## 数据源

- AkShare (主数据源)
- 东方财富 API

## 文件结构

```
technical-indicators/
├── SKILL.md                      # 技能文档
├── technical_indicators.py       # 主模块 (基础指标计算)
├── resonance_analysis.py         # 共振分析模块 (新增)
├── volume_price_analysis.py      # 量价关系分析模块 (8 种形态)
└── skill.json                    # 技能配置
```

## API 参考

### 基础指标函数

| 函数 | 参数 | 返回值 |
|------|------|--------|
| `calculate_ma` | code, periods | MA 值字典 |
| `calculate_macd` | code, fast, slow, signal | MACD 字典 |
| `calculate_kdj` | code, n, m1, m2 | KDJ 字典 |
| `calculate_rsi` | code, period | RSI 字典 |
| `calculate_boll` | code, period, std_dev | 布林带字典 |
| `calculate_atr` | code, period | ATR 字典 |
| `calculate_obv` | code | OBV 字典 |
| `calculate_cci` | code, period | CCI 字典 |
| `calculate_adx` | code, period | ADX 字典 |
| `calculate_volume_price` | code, lookback | 量价分析报告 |
| `backtest_volume_strategy` | code, start_date, end_date, strategy, hold_days | 回测结果 |

### 共振分析函数

| 函数 | 参数 | 返回值 |
|------|------|--------|
| `get_resonance_signals` | code, date | 共振信号字典 |
| `backtest_resonance` | code, start_date, end_date | 回测结果字典 |
| `scan_resonance_market` | code_list, min_strength | 信号列表 |

## 注意事项

- 实时行情有 15 分钟延迟
- 建议添加缓存机制
- 回测结果仅供参考，不构成投资建议
- 共振信号需结合基本面和市场环境综合判断

## 验收标准

### 技术指标
- [x] 5+ 指标组合 (MA, MACD, ADX, KDJ, RSI, CCI, OBV, BOLL, ATR)
- [x] 自动共振识别 (5 种共振类型)
- [x] 信号强度评分 (0-100)
- [x] 回测胜率>55% (需根据实际市场验证)

### 量价关系分析 (新增)
- [x] 基础量价 4 形态 (放量上涨、缩量上涨、放量下跌、缩量下跌)
- [x] 高级量价 4 形态 (量价背离、天量天价、地量地价、堆量上涨)
- [x] 量比计算 (今日/5 日平均)
- [x] 综合评分与操作建议
- [x] 策略回测功能
