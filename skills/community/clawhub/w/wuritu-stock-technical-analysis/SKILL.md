---
name: stock_technical_analysis
description: 对A股/美股/港股进行全面技术分析，包括K线形态识别、技术指标计算、趋势判断、量价分析，生成可操作的技术分析报告
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "version": "1.0.0",
      "requires": {
        "bins": ["python3"],
        "env": ["STOCK_DATA_API_KEY"]
      },
      "primaryEnv": "STOCK_DATA_API_KEY",
      "os": ["darwin", "linux"]
    }
  }
---

# 股票技术分析技能

## 触发条件
当用户提出以下类型请求时激活：
- "XX股票技术面分析"
- "帮我看看K线/均线/MACD"
- "这只股票趋势怎么样"
- "有没有买入/卖出信号"
- "分析一下XX的量价关系"

## 工具调用流程

### Step 1: 数据获取
使用 `exec` 工具运行 `{baseDir}/tools/kline_fetcher.py`：
```bash
python3 {baseDir}/tools/kline_fetcher.py --symbol <股票代码> --period <周期> --count <数量>
```
参数:
- `--symbol`: 股票代码 (如 600519, AAPL)
- `--period`: K线周期 (1min|5min|15min|30min|60min|daily|weekly|monthly)
- `--count`: K线数量 (默认120根)
- `--market`: 市场 (A|US|HK)

### Step 2: 技术指标计算
使用 `exec` 运行 `{baseDir}/tools/indicator_engine.py`：
```bash
python3 {baseDir}/tools/indicator_engine.py --symbol <代码> --indicators <指标列表>
```
支持指标: MA,EMA,MACD,KDJ,RSI,BOLL,CCI,WR,OBV,VWAP,ATR,DMI

### Step 3: K线形态识别
```bash
python3 {baseDir}/tools/pattern_recognizer.py --symbol <代码> --period daily
```

### Step 4: 趋势分析
```bash
python3 {baseDir}/tools/trend_analyzer.py --symbol <代码>
```

### Step 5: 量价分析
```bash
python3 {baseDir}/tools/volume_analyzer.py --symbol <代码>
```

### Step 6: 图表生成
```bash
python3 {baseDir}/tools/chart_generator.py --symbol <代码> --type comprehensive --output /tmp/chart.png
```

## 分析框架（模型遵循此框架组织输出）

### 1) 趋势判断
- 当前处于什么趋势（上升/下降/震荡）
- 趋势强度如何（强/中/弱）
- 趋势持续时间

### 2) 关键价位
- 支撑位（近期低点、均线支撑、前期密集成交区）
- 阻力位（近期高点、均线压力、前期套牢区）

### 3) 技术指标信号
- 均线系统：多头/空头排列、金叉/死叉
- MACD：快慢线位置、柱状图变化、背离
- KDJ：超买/超卖、金叉/死叉
- RSI：强弱区间、背离信号
- BOLL：收口/扩张、轨道位置

### 4) K线形态
- 识别的经典形态（锤子线、十字星、吞没形态等）
- 形态的多空含义

### 5) 量价配合
- 放量/缩量状态
- 量价是否背离
- 换手率水平

### 6) 综合技术评分
给出 1-100 分的综合技术评分，标注多空倾向

## 输出格式
以结构化 Markdown 报告输出，包含数据表格和文字解读
必须包含⚠️风险提示：技术分析仅供参考，不构成投资建议