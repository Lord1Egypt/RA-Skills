# 形态类型说明

本文档详细说明股票筛选器支持的所有形态类型。

---

## 一、价值指标类

### gxl - 高股息股票

- **说明**：股息率大于 3% 的股票
- **适用场景**：价值投资、红利策略、防守型配置
- **筛选标准**：股息率 > 3%
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern gxl
  ```

---

## 二、强度指标类

### rps - RPS 强势股

- **说明**：RPS（Relative Price Strength）大于 70 的股票
- **理论基础**：欧奈尔 CANSLIM 投资体系
- **适用场景**：动量选股、趋势跟踪
- **筛选标准**：RPS > 70
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern rps
  ```

### sctr - SCTR 强势股

- **说明**：SCTR（StockCharts Technical Rank）大于 70 的股票
- **理论基础**：StockCharts 技术排名系统
- **适用场景**：技术分析选股
- **筛选标准**：SCTR > 70
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern sctr
  ```

### rpsTop3 - RPS 行业前三

- **说明**：RPS 在所属行业排名前三的股票
- **适用场景**：行业内强势股挖掘
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern rpsTop3
  ```

### csTop3 - CS 行业前三

- **说明**：CS（Close-to-EMA Strength）在所属行业排名前三的股票
- **适用场景**：短期动量强势股
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern csTop3
  ```

### sctrTop3 - SCTR 行业前三

- **说明**：SCTR 在所属行业排名前三的股票
- **适用场景**：技术排名强势股
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern sctrTop3
  ```

---

## 三、趋势形态类

### trendUp - 趋势向上

- **说明**：K 线趋势向上的股票
- **适用场景**：趋势跟踪、右侧交易
- **判断标准**：价格站上关键均线，多头排列
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern trendUp
  ```

### newHigh - 新高附近

- **说明**：价格接近历史新高的股票
- **理论基础**：欧奈尔"新高买入"策略
- **适用场景**：突破买入、动量交易
- **判断标准**：价格距历史高点 5% 以内
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern newHigh
  ```

### high_60d - 创 60 日新高

- **说明**：大量创 60 日新高的股票
- **适用场景**：中期趋势跟踪
- **判断标准**：价格创 60 日新高
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern high_60d
  ```

### crossMa50 - 上穿 MA50

- **说明**：价格上穿 50 日均线的股票
- **适用场景**：中期趋势确认
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern crossMa50
  ```

### crossoverBox - 上穿箱体

- **说明**：价格行为交易法信号 K，上穿箱体的股票
- **理论基础**：威科夫价格行为分析
- **适用场景**：突破交易、箱体突破
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern crossoverBox
  ```

### cs_crossover_20 - CS 穿过 MA20

- **说明**：CS 指标穿过其 20 日均线
- **适用场景**：动量转强信号
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern cs_crossover_20
  ```

---

## 四、成交量形态类

### fangliang - 放量上涨

- **说明**：前一天是 VCP/3C 形态，当天放量突破收盘在高点
- **理论基础**：马克·米勒维尼 VCP 形态
- **适用场景**：突破确认、量价配合
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern fangliang
  ```

### fangliangtupo - 放量突破箱体

- **说明**：放量突破箱体的股票
- **适用场景**：突破交易、成交量确认
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern fangliangtupo
  ```

---

## 五、涨幅排名类

### zdf1dTop3 - 1 日涨幅行业前三

- **说明**：当日涨幅在所属行业排名前三的股票
- **适用场景**：短线热点追踪
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern zdf1dTop3
  ```

### zdf5dTop3 - 5 日涨幅行业前三

- **说明**：5 日涨幅在所属行业排名前三的股票
- **适用场景**：短期趋势跟踪
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern zdf5dTop3
  ```

### zdf10dTop3 - 10 日涨幅行业前三

- **说明**：10 日涨幅在所属行业排名前三的股票
- **适用场景**：中期趋势跟踪
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern zdf10dTop3
  ```

### zdf20dTop3 - 20 日涨幅行业前三

- **说明**：20 日涨幅在所属行业排名前三的股票
- **适用场景**：中期趋势确认
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern zdf20dTop3
  ```

### shizhiTop3 - 行业市值前三

- **说明**：行业市值排名前三的股票
- **适用场景**：行业龙头筛选、大盘股配置
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern shizhiTop3
  ```

---

## 六、经典技术形态类

### vcp - VCP 波动收缩形态

- **说明**：股魔 VCP 形态（Volatility Contraction Pattern）
- **理论基础**：马克·米勒维尼《股票魔法师》
- **形态特征**：
  - 波动幅度逐渐收缩
  - 成交量逐渐萎缩
  - 突破时放量
- **适用场景**：趋势跟踪、突破买入
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern vcp
  ```

### joc - 跨越小溪 Joc

- **说明**：跨越小溪（Jump Over Creek）形态
- **理论基础**：威科夫量价分析
- **形态特征**：价格突破阻力带（小溪）
- **适用场景**：突破交易
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern joc
  ```

### sos - 强势上涨 SOS

- **说明**：强势上涨（Sign of Strength）形态
- **理论基础**：威科夫量价分析
- **形态特征**：放量上涨，显示需求主导
- **适用场景**：趋势确认、主力资金入场
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern sos
  ```

### sos_h1 - SOS 后高 1 入场点

- **说明**：SOS 之后出现高 1 入场点的股票
- **理论基础**：威科夫量价分析
- **形态特征**：SOS 后的第一次回调高点
- **适用场景**：回调买入
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern sos_h1
  ```

### spring - Spring 弹簧形态

- **说明**：上涨波段回调后出现 spring 向上的股票
- **理论基础**：威科夫量价分析
- **形态特征**：价格下探支撑后快速反弹
- **适用场景**：抄底买入、支撑位确认
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern spring
  ```

### w - W 底吸收

- **说明**：SOS 之后出现 W 底吸收形态
- **理论基础**：威科夫量价分析
- **形态特征**：双底形态，第二次低点成交量萎缩
- **适用场景**：底部反转
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern w
  ```

### lps - LPS 最后支撑点

- **说明**：LPS（Last Point of Support）最后支撑点，出现在吸筹阶段（Accumulation），是上涨前最后一次回调测试支撑
- **理论基础**：威科夫量价分析
- **形态特征**：SOS 之后价格回调至支撑位，成交量萎缩，随后向上反转；LPS 创更高低点（区别于 Spring 的假破位）
- **适用场景**：吸筹阶段末期买入，趋势启动前的低风险入场点
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern lps
  ```

### ibs - IBS 强势K线

- **说明**：IBS（Internal Bar Strength）内部K线强度，当日放量上涨收盘超昨日高点，K 线实体长度超当日振幅 69%，衡量收盘价在当日高低点区间内的相对位置
- **理论基础**：价格行为学，收盘价越靠近当日最高点，买方力量越强
- **适用场景**：强势K线确认，量价配合的短期买入信号
- **使用示例**：
  ```bash
  npx daxiapi-cli@latest stock pattern ibs
  ```

---

## 形态组合建议

### 动量选股组合

```bash
# RPS 强势 + 新高 + 放量
npx daxiapi-cli@latest stock pattern rps
npx daxiapi-cli@latest stock pattern newHigh
npx daxiapi-cli@latest stock pattern fangliang
```

### 威科夫形态组合

```bash
# SOS + Spring + LPS
npx daxiapi-cli@latest stock pattern sos
npx daxiapi-cli@latest stock pattern spring
npx daxiapi-cli@latest stock pattern lps
```

### 趋势跟踪组合

```bash
# VCP + 上穿箱体 + 放量突破
npx daxiapi-cli@latest stock pattern vcp
npx daxiapi-cli@latest stock pattern crossoverBox
npx daxiapi-cli@latest stock pattern fangliangtupo
```

### 价值投资组合

```bash
# 高股息 + 行业龙头
npx daxiapi-cli@latest stock pattern gxl
npx daxiapi-cli@latest stock pattern shizhiTop3
```

---

## 注意事项

1. **形态有效性**：技术形态在趋势市中更有效，震荡市可能频繁失效
2. **止损设置**：所有形态买入都应设置止损位
3. **市场环境**：结合大盘环境判断形态有效性
4. **成交量确认**：突破形态需要成交量配合
5. **时间周期**：形态在不同时间周期下表现不同
