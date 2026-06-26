# 技术指标分析 L2 - 高级指标模块

## 概述

本模块包含三个高级技术指标的实现，用于增强技术分析能力:

1. **Ichimoku Cloud (一目均衡表)** - 综合趋势判断指标
2. **VWAP (成交量加权平均价)** - 机构成本参考指标
3. **SuperTrend (超级趋势)** - ATR 基础趋势跟踪指标

## 文件结构

```
skills/technical-indicators/
├── ichimoku_cloud.py           # 一目均衡表实现
├── vwap.py                     # VWAP 实现
├── supertrend.py               # SuperTrend 实现
├── test_technical_indicators_l2.py  # 单元测试 (29 个测试用例)
├── examples_usage.py           # 使用示例
└── README_L2_INDICATORS.md     # 本文档
```

## 快速开始

### 1. Ichimoku Cloud (一目均衡表)

```python
from ichimoku_cloud import (
    calculate_ichimoku,
    get_all_ichimoku_parameters,
    get_ichimoku_summary,
    identify_cloud_breakout,
    identify_tk_cross
)

# 准备数据 (需要包含 high, low, close 列)
df = prepare_your_data()

# 方法 1: 获取 9 个参数
params = get_all_ichimoku_parameters(df)
# 返回：转换线、基准线、先行跨度 A/B、滞后跨度、云团顶部/底部、云团颜色、价格位置

# 方法 2: 获取综合分析报告
summary = get_ichimoku_summary(df)
# 返回：当前价格、总体趋势、操作建议、信号强度等

# 方法 3: 识别云团突破
df_ichimoku = calculate_ichimoku(df)
cloud = identify_cloud_breakout(df_ichimoku)
# 返回：云团颜色、价格位置、突破信号

# 方法 4: 识别 TK 交叉
tk = identify_tk_cross(df_ichimoku)
# 返回：交叉信号 (金叉/死叉)、当前位置
```

**9 个参数说明:**
- 转换线 (Tenkan-sen): 9 周期最高价和最低价的平均值
- 基准线 (Kijun-sen): 26 周期最高价和最低价的平均值
- 先行跨度 A (Senkou Span A): (转换线 + 基准线) / 2, 向前平移 26 周期
- 先行跨度 B (Senkou Span B): 52 周期最高价和最低价的平均值，向前平移 26 周期
- 滞后跨度 (Chikou Span): 当前收盘价，向后平移 26 周期
- 云团顶部：先行跨度 A 和 B 的最大值
- 云团底部：先行跨度 A 和 B 的最小值
- 云团颜色：bullish (看涨) 或 bearish (看跌)
- 价格相对云团位置：above_cloud / below_cloud / inside_cloud

### 2. VWAP (成交量加权平均价)

```python
from vwap import (
    calculate_vwap,
    calculate_vwap_intraday,
    identify_vwap_position,
    get_vwap_summary
)

# 日线数据
df_daily = prepare_daily_data()  # 需要 high, low, close, volume 列
df_vwap = calculate_vwap(df_daily)

# 日内分钟数据
df_intraday = prepare_intraday_data()  # 需要 datetime, high, low, close, volume 列
df_vwap = calculate_vwap_intraday(df_intraday)

# 识别价格相对 VWAP 位置
position = identify_vwap_position(df_vwap)
# 返回：位置、偏离度、穿越信号

# 获取综合报告
summary = get_vwap_summary(df_daily)
# 返回：当前价格、VWAP 值、趋势、建议等
```

**VWAP 特点:**
- 日内指标，每个交易日重新开始计算
- 反映机构平均建仓成本
- 价格 > VWAP: 看涨，买方主导
- 价格 < VWAP: 看跌，卖方主导

### 3. SuperTrend (超级趋势)

```python
from supertrend import (
    calculate_supertrend,
    get_supertrend_summary,
    identify_trend_reversal
)

# 准备数据 (需要 high, low, close 列)
df = prepare_your_data()

# 计算 SuperTrend (可自定义参数)
df_st = calculate_supertrend(df, period=10, multiplier=3.0)

# 识别趋势反转
reversal = identify_trend_reversal(df_st)
# 返回：当前趋势、反转信号、最近反转历史

# 获取综合报告
summary = get_supertrend_summary(df, period=10, multiplier=3.0)
# 返回：当前价格、SuperTrend 值、趋势、强度、建议、置信度
```

**参数说明:**
- period: ATR 周期 (默认 10)
- multiplier: 乘数 (默认 3.0)

## 综合使用示例

```python
# 多指标综合分析
ichimoku = get_ichimoku_summary(df)
vwap = get_vwap_summary(df)
supertrend = get_supertrend_summary(df)

# 统计看涨/看跌信号
bullish_count = 0
bearish_count = 0

if ichimoku['overall_trend'] in ['bullish', 'strong_bullish']:
    bullish_count += 1
elif ichimoku['overall_trend'] in ['bearish', 'strong_bearish']:
    bearish_count += 1

if vwap['trend'] == 'bullish':
    bullish_count += 1
elif vwap['trend'] == 'bearish':
    bearish_count += 1

if supertrend['trend'] == 'bullish':
    bullish_count += 1
elif supertrend['trend'] == 'bearish':
    bearish_count += 1

# 综合判断
if bullish_count >= 2:
    recommendation = "买入/持有"
elif bearish_count >= 2:
    recommendation = "卖出/观望"
else:
    recommendation = "观望"
```

## 运行测试

```bash
cd skills/technical-indicators
python test_technical_indicators_l2.py
```

**测试结果:** 29 个测试用例全部通过

## 运行示例

```bash
cd skills/technical-indicators
python examples_usage.py
```

## API 参考

### Ichimoku Cloud

| 函数 | 说明 | 输入 | 输出 |
|------|------|------|------|
| `calculate_ichimoku(df)` | 计算所有组件 | DataFrame (high, low, close) | DataFrame (含 5 条线) |
| `get_all_ichimoku_parameters(df)` | 获取 9 个参数 | DataFrame | Dict (9 个参数) |
| `get_ichimoku_summary(df)` | 综合分析报告 | DataFrame | Dict (完整报告) |
| `identify_cloud_breakout(df)` | 云团突破检测 | DataFrame (含 Ichimoku) | Dict (突破信号) |
| `identify_tk_cross(df)` | TK 交叉检测 | DataFrame (含 Ichimoku) | Dict (交叉信号) |
| `identify_chikou_signal(df)` | 滞后跨度信号 | DataFrame (含 Ichimoku) | Dict (信号强度) |

### VWAP

| 函数 | 说明 | 输入 | 输出 |
|------|------|------|------|
| `calculate_vwap(df, reset_daily)` | 计算 VWAP | DataFrame (high, low, close, volume) | DataFrame (含 vwap) |
| `calculate_vwap_intraday(df)` | 日内 VWAP | DataFrame (datetime, OHLCV) | DataFrame (含 vwap) |
| `identify_vwap_position(df)` | 位置检测 | DataFrame (含 vwap) | Dict (位置、偏离度) |
| `get_vwap_support_resistance(df)` | 支撑阻力位 | DataFrame (含 vwap) | Dict (支撑/阻力) |
| `get_vwap_summary(df)` | 综合报告 | DataFrame | Dict (完整报告) |

### SuperTrend

| 函数 | 说明 | 输入 | 输出 |
|------|------|------|------|
| `calculate_atr(df, period)` | 计算 ATR | DataFrame (high, low, close) | Series (ATR) |
| `calculate_supertrend(df, period, multiplier)` | 计算 SuperTrend | DataFrame (high, low, close) | DataFrame (含 supertrend, trend) |
| `identify_trend_reversal(df)` | 趋势反转检测 | DataFrame (含 SuperTrend) | Dict (反转信号) |
| `get_supertrend_levels(df)` | 关键价位 | DataFrame (含 SuperTrend) | Dict (支撑/阻力) |
| `get_supertrend_summary(df)` | 综合报告 | DataFrame | Dict (完整报告) |
| `scan_supertrend_signals(df)` | 信号扫描 | DataFrame (含 SuperTrend) | List (信号列表) |

## 注意事项

1. **数据要求**: 所有指标需要足够的历史数据
   - Ichimoku: 至少 52 个周期
   - VWAP: 至少 2 个周期
   - SuperTrend: 至少 20 个周期

2. **数据格式**: 
   - 必须包含列：high, low, close
   - VWAP 还需要：volume
   - 日内 VWAP 还需要：datetime

3. **参数调整**:
   - Ichimoku: 默认 (9, 26, 52, 26) 适用于日线
   - SuperTrend: 默认 (10, 3.0) 适用于大多数情况
   - 可根据交易品种和时间周期调整参数

4. **信号解读**:
   - 单一指标可能产生假信号
   - 建议多指标结合使用
   - 结合其他分析方法 (基本面、消息面等)

## 版本信息

- 版本：1.0.0
- 创建日期：2024-03-14
- 测试状态：29/29 测试通过
