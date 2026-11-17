# TA-Lib 技术指标函数总览

> 来源：https://ta-lib.org/functions/
> 整理目的：作为因子表达式初始收集的「技术指标」补充来源。TA-Lib 是量价技术指标的事实标准库，
> 其函数均可作为因子构造的基础算子或独立因子。
> 约定：函数名使用 TA-Lib 官方原名（大写），公式中使用 `close/high/low/volume/open` 表示对应序列，
> `n` 表示时间窗口参数。`MA(x, n)` 默认简单移动平均，`EMA(x, n)` 指数移动平均（α=2/(n+1)）。

---

## 0. 分类速览

| 类别 | 函数数 | 用途 |
|------|-------|------|
| Overlap Studies（重叠研究 / 均线类） | 20 | 各类移动平均、布林带、SAR |
| Momentum Indicators（动量指标） | 33 | RSI/MACD/CCI/ROC/ADX/随机等 |
| Volume Indicators（成交量指标） | 7 | OBV/CMF/AD/PVO 等 |
| Volatility Indicators（波动率指标） | 3 | ATR/NATR/TRANGE |
| Price Transform（价格变换） | 5 | 典型价/加权价等中间量 |
| Cycle Indicators（周期指标） | 5 | Hilbert 变换类 |
| Statistic Functions（统计函数） | 9 | 线性回归/相关/标准差 |
| Math Transform（数学变换） | 15 | 三角/对数/指数等逐点变换 |
| Math Operators（数学算子） | 11 | 向量加減乘除/最值 |
| Pattern Recognition（形态识别） | 61 | K 线形态布尔检测 |

---

## 1. Overlap Studies（重叠研究 / 均线类）

| 函数 | 全称 | 说明 / 公式 |
|------|------|------------|
| `SMA` | Simple Moving Average | 简单移动平均：`SMA(close,n) = mean(close, n)` |
| `EMA` | Exponential Moving Average | 指数移动平均：`EMA_t = α·close_t + (1-α)·EMA_{t-1}`，`α=2/(n+1)` |
| `WMA` | Weighted Moving Average | 线性加权移动平均，权重 `1,2,…,n` |
| `DEMA` | Double Exponential MA | `2·EMA(close,n) − EMA(EMA(close,n))` |
| `TEMA` | Triple Exponential MA | `3·EMA1 − 3·EMA2 + EMA3`（EMA1=EMA(close), EMA2=EMA(EMA1), EMA3=EMA(EMA2)） |
| `T3` | Triple Exponential MA (T3) | Tim Tillson 六重 EMA，带音量因子 `v`，平滑系数 `a=0.7` |
| `TRIMA` | Triangular MA | 双重平滑 SMA：`SMA(SMA(close, ceil(n/2)), floor(n/2))` |
| `KAMA` | Kaufman Adaptive MA | 根据效率比（ER）自适应的 EMA，趋势强时贴近价格 |
| `MAMA` | MESA Adaptive MA | 基于希尔伯特变换的相位自适应均线（含 FAMA 输出） |
| `HMA` | Hull Moving Average | `WMA(2·WMA(close,n/2) − WMA(close,n), √n)`，降延迟 |
| `MA` | Moving Average | 通用移动平均，可指定 MA 类型（SMA/EMA/WMA/DEMA/TEMA/TRIMA 等） |
| `MAVP` | Moving Average with Variable Period | 周期随另一个序列变化的移动平均 |
| `VWMA` | Volume Weighted MA | 成交量加权移动平均：`sum(close·vol, n)/sum(vol, n)` |
| `BBANDS` | Bollinger Bands | 布林带：`mid = MA(close,n)`，`upper = mid + k·STDDEV(close,n)`，`lower = mid − k·STDDEV(close,n)`（默认 n=20,k=2） |
| `ACCBANDS` | Acceleration Bands | 加速带：`mid = SMA(high+low+close)/3`，上下带为 mid 再乘 `(1±k·(high−low)/(high+low))` |
| `MIDPOINT` | MidPoint over period | `MIDPOINT = (max + min)/2` over n |
| `MIDPRICE` | Midpoint Price over period | `(HHV(high,n) + LLV(low,n))/2` |
| `SAR` | Parabolic SAR | 抛物线止损转向指标（加速因子 step/max） |
| `SAREXT` | Parabolic SAR Extended | 扩展版 SAR，起止加速参数可独立配置 |
| `HT_TRENDLINE` | Hilbert Transform - Instantaneous Trendline | 希尔伯特变换瞬时趋势线 |

---

## 2. Momentum Indicators（动量指标）

| 函数 | 全称 | 说明 / 公式 |
|------|------|------------|
| `RSI` | Relative Strength Index | `RS = SMA(max(Δclose,0),n)/SMA(max(−Δclose,0),n)`，`RSI = 100 − 100/(1+RS)`（默认 n=14） |
| `MACD` | Moving Average Convergence/Divergence | `MACD = EMA(close,12) − EMA(close,26)`，信号线 `SIGNAL = EMA(MACD,9)`，柱 `HIST = MACD − SIGNAL` |
| `MACDEXT` | MACD with controllable MA type | MACD 的快/慢/信号线均可自选 MA 类型 |
| `MACDFIX` | MACD Fix 12/26 | 固定 12/26 的 MACD 版 |
| `STOCH` | Stochastic | `%K = 100·(close − LLV(low,n))/(HHV(high,n) − LLV(low,n))`，`%D = SMA(%K, m)`（默认 n=14, m=3） |
| `STOCHF` | Stochastic Fast | 快随机：%K 不做平滑，%D = SMA(%K, m) |
| `STOCHRSI` | Stochastic RSI | 对 RSI 自身再做随机处理：`100·(RSI − LLV(RSI,n))/(HHV(RSI,n) − LLV(RSI,n))` |
| `CCI` | Commodity Channel Index | `(TP − SMA(TP,n)) / (0.015·MeanDev(TP))`，`TP=(high+low+close)/3`（默认 n=20） |
| `ROC` | Rate of change | `((close/prevClose) − 1)·100`，prevClose 为 n 期前 |
| `ROCP` | Rate of change Percentage | `(close − prevClose)/prevClose` |
| `ROCR` | Rate of change ratio | `close / prevClose` |
| `ROCR100` | Rate of change ratio 100 | `(close / prevClose)·100` |
| `MOM` | Momentum | `close − close[n]`（n 期动量） |
| `APO` | Absolute Price Oscillator | `EMA(close,fast) − EMA(close,slow)`（绝对差） |
| `PPO` | Percentage Price Oscillator | `(EMA(fast) − EMA(slow))/EMA(slow)·100`（百分比差） |
| `TRIX` | Triple EMA ROC | 对 EMA 三重平滑后再取 1 日变化率，过滤噪声 |
| `WILLR` | Williams' %R | `−100·(HHV(high,n) − close)/(HHV(high,n) − LLV(low,n))`（默认 n=14） |
| `ADX` | Average Directional Movement Index | 平均方向指数，衡量趋势强度（0~100，>25 强趋势） |
| `ADXR` | ADX Rating | `ADXR = (ADX_t + ADX_{t−n})/2`，平滑 ADX |
| `DX` | Directional Movement Index | +DI/−DI 的相对强度，±DM 经平滑后归一 |
| `PLUS_DI` / `MINUS_DI` | Plus/Minus Directional Indicator | 正向/负向方向指标 |
| `PLUS_DM` / `MINUS_DM` | Plus/Minus Directional Movement | 正向/负向方向运动 |
| `AROON` | Aroon | `AroonUp = 100·(n − 距 n 期最高价周期数)/n`，`AroonDown = 100·(n − 距 n 期最低价周期数)/n` |
| `AROONOSC` | Aroon Oscillator | `AroonUp − AroonDown` |
| `CCI` | Commodity Channel Index | 见上 |
| `CMO` | Chande Momentum Oscillator | `(SumUp − SumDown)/(SumUp + SumDown)·100`，Up/Down 为 n 期内涨跌和 |
| `CMOU` | Chande Momentum Oscillator (Unsmoothed) | 未平滑的 CMO |
| `BOP` | Balance Of Power | `(close − open)/(high − low)`，衡量多空力量平衡 |
| `MFI` | Money Flow Index | 类 RSI 但用典型价×成交量加权：`100 − 100/(1 + 正资金流/负资金流)`（默认 n=14） |
| `ULTOSC` | Ultimate Oscillator | 多周期（7/14/28）加权 ROC 合成，降低假信号 |
| `IMI` | Intraday Momentum Index | 日内动量：`(close − open)` 与 `(close − prevclose)` 关系的归一 |

---

## 3. Volume Indicators（成交量指标）

| 函数 | 全称 | 说明 / 公式 |
|------|------|------------|
| `OBV` | On Balance Volume | 累积能量潮：涨加、跌减成交量，反映资金流向 |
| `AD` | Chaikin A/D Line | 累积派发线：`Σ vol·((close−low)−(high−close))/(high−low)` |
| `ADOSC` | Chaikin A/D Oscillator | 快 A/D（3）− 慢 A/D（10）的差 |
| `CMF` | Chaikin Money Flow | `Σ vol·((close−low)−(high−close))/(high−low) / Σvol`，n 期资金流强度 |
| `NVI` | Negative Volume Index | 成交量下降时按价格变动累积，捕捉「聪明钱」 |
| `PVI` | Positive Volume Index | 成交量上升时按价格变动累积，捕捉「散户」 |
| `PVO` | Percentage Volume Oscillator | `(EMA(vol,fast) − EMA(vol,slow))/EMA(vol,slow)·100`，成交量版 MACD |

---

## 4. Volatility Indicators（波动率指标）

| 函数 | 全称 | 说明 / 公式 |
|------|------|------------|
| `ATR` | Average True Range | 真实波幅均值。`TR = max(high−low, |high−prevClose|, |low−prevClose|)`，`ATR = SMA(TR, n)`（默认 n=14） |
| `NATR` | Normalized ATR | `ATR / close · 100`，消除价格量级影响，跨标的可比 |
| `TRANGE` | True Range | 单期真实波幅 `TR`（不带平滑） |

> 波动率类指标本身就是极常用的风险/波动因子，亦是许多策略的止损与仓位参数来源。

---

## 5. Price Transform（价格变换）

| 函数 | 全称 | 说明 / 公式 |
|------|------|------------|
| `TYPPRICE` | Typical Price | `(high + low + close)/3` |
| `WCLPRICE` | Weighted Close Price | `(high + low + close·2)/4` |
| `AVGPRICE` | Average Price | `(high + low + open + close)/4` |
| `MEDPRICE` | Median Price | `(high + low)/2` |
| `AVGDEV` | Average Deviation | 平均绝对偏差：`mean(|x − mean(x)|)` over n |

---

## 6. Cycle Indicators（周期指标，Hilbert 变换类）

| 函数 | 全称 | 说明 |
|------|------|------|
| `HT_DCPERIOD` | Hilbert Transform - Dominant Cycle Period | 估计主导周期长度（以 K 线根数计） |
| `HT_DCPHASE` | Hilbert Transform - Dominant Cycle Phase | 主导周期相位 |
| `HT_PHASOR` | Hilbert Transform - Phasor Components | 输出 In-Phase / Quadrature 分量，用于相位分析 |
| `HT_SINE` | Hilbert Transform - SineWave | 输出正弦波及其滞后版本，用于趋势/拐点判定 |
| `HT_TRENDMODE` | Hilbert Transform - Trend vs Cycle Mode | 标识当前处于趋势态（1）还是震荡态（0） |

---

## 7. Statistic Functions（统计函数）

| 函数 | 全称 | 说明 / 公式 |
|------|------|------------|
| `STDDEV` | Standard Deviation | `sqrt(VAR(close, n, nbdev))`，默认 n=5，nbdev=1（总体标准差） |
| `VAR` | Variance | 方差，可指定总体/样本（nbdev） |
| `CORREL` | Pearson's Correlation | 两序列皮尔逊相关系数 `r` over n |
| `BETA` | Beta | 资产相对基准的线性回归斜率（系统风险） |
| `LINEARREG` | Linear Regression | 对 n 期窗口做最小二乘拟合，取当前点预测值 |
| `LINEARREG_SLOPE` | Linear Regression Slope | 拟合直线斜率（趋势速度） |
| `LINEARREG_INTERCEPT` | Linear Regression Intercept | 拟合直线截距 |
| `LINEARREG_ANGLE` | Linear Regression Angle | 拟合直线角度（度） |
| `TSF` | Time Series Forecast | 线性回归外推下一期预测值（= LINEARREG + slope） |

---

## 8. Math Transform（数学变换，逐点运算）

| 函数 | 全称 | 说明 |
|------|------|------|
| `SQRT` | Square Root | 逐点平方根 |
| `LN` | Log Natural | 逐点自然对数 |
| `LOG10` | Log10 | 逐点常用对数 |
| `EXP` | Exp | 逐点指数 |
| `SIN` / `COS` / `TAN` | Trigonometric | 逐点正弦/余弦/正切 |
| `ASIN` / `ACOS` / `ATAN` | Inverse Trigonometric | 逐点反三角 |
| `SINH` / `COSH` / `TANH` | Hyperbolic | 逐点双曲函数 |
| `CEIL` | Ceil | 逐点上取整 |
| `FLOOR` | Floor | 逐点下取整 |

---

## 9. Math Operators（数学算子，向量运算）

| 函数 | 全称 | 说明 |
|------|------|------|
| `ADD` | Vector Add | 两序列逐点相加 |
| `SUB` | Vector Sub | 逐点相减 |
| `MULT` | Vector Mult | 逐点相乘 |
| `DIV` | Vector Div | 逐点相除 |
| `SUM` | Summation | 窗口内求和 `Σ x over n` |
| `MAX` | Highest value | 窗口内最大值 |
| `MIN` | Lowest value | 窗口内最小值 |
| `MINMAX` | Lowest & Highest | 同时返回窗口内最小与最大 |
| `MAXINDEX` | Index of Highest | 窗口内最大值所在下标 |
| `MININDEX` | Index of Lowest | 窗口内最小值所在下标 |
| `MINMAXINDEX` | Indexes of Low/High | 同时返回最小/最大下标 |

---

## 10. Pattern Recognition（形态识别，K 线）

> 全部返回整数：`100`=看涨形态，`−100`=看跌形态，`0`=无形态。函数名均为 `CDL*` 前缀。
> 完整形态列表（共 61 个）：

| 函数 | 形态 | 方向 |
|------|------|------|
| `CDL2CROWS` | Two Crows 两只乌鸦 | 看跌 |
| `CDL3BLACKCROWS` | Three Black Crows 三黑鸦 | 看跌 |
| `CDL3WHITESOLDIERS` | Three Advancing White Soldiers 三白兵 | 看涨 |
| `CDL3INSIDE` | Three Inside Up/Down 内困三一 | 反转 |
| `CDL3LINESTRIKE` | Three-Line Strike 三连线 | 反转 |
| `CDL3OUTSIDE` | Three Outside Up/Down 外困三一 | 反转 |
| `CDL3STARSINSOUTH` | Three Stars In The South 南方三星 | 看涨 |
| `CDLABANDONEDBABY` | Abandoned Baby 弃婴 | 反转 |
| `CDLADVANCEBLOCK` | Advance Block 推进块 | 看跌 |
| `CDLBELTHOLD` | Belt-hold 腰带线 | 反转 |
| `CDLBREAKAWAY` | Breakaway 脱离 | 反转 |
| `CDLCLOSINGMARUBOZU` | Closing Marubozu 收官光头光脚 | 中性偏强 |
| `CDLCONCEALBABYSWALL` | Concealing Baby Swallow 藏婴吞没 | 看涨 |
| `CDLCOUNTERATTACK` | Counterattack 反击线 | 反转 |
| `CDLDARKCLOUDCOVER` | Dark Cloud Cover 乌云盖顶 | 看跌 |
| `CDLDOJI` | Doji 十字星 | 中性 |
| `CDLDOJISTAR` | Doji Star 十字星星 | 反转 |
| `CDLDRAGONFLYDOJI` | Dragonfly Doji 蜻蜓十字 | 看涨 |
| `CDLENGULFING` | Engulfing Pattern 吞没 | 反转 |
| `CDLEVENINGDOJISTAR` | Evening Doji Star 暮星十字 | 看跌 |
| `CDLEVENINGSTAR` | Evening Star 暮星 | 看跌 |
| `CDLGAPSIDESIDEWHITE` | Up/Down-gap side-by-side white lines 并列阳线缺口 | 持续 |
| `CDLGRAVESTONEDOJI` | Gravestone Doji 墓碑十字 | 看跌 |
| `CDLHAMMER` | Hammer 锤头 | 看涨 |
| `CDLHANGINGMAN` | Hanging Man 上吊线 | 看跌 |
| `CDLHARAMI` | Harami Pattern 孕线 | 反转 |
| `CDLHARAMICROSS` | Harami Cross Pattern 十字孕线 | 反转 |
| `CDLHIGHWAVE` | High-Wave Candle 高浪线 | 中性 |
| `CDLHIKKAKE` | Hikkake Pattern 陷阱 | 反转 |
| `CDLHIKKAKEMOD` | Modified Hikkake Pattern 修正陷阱 | 反转 |
| `CDLHOMINGPIGEON` | Homing Pigeon 家鸽 | 看涨 |
| `CDLIDENTICAL3CROWS` | Identical Three Crows 三胞胎乌鸦 | 看跌 |
| `CDLINNECK` | In-Neck Pattern 颈内线 | 看跌 |
| `CDLINVERTEDHAMMER` | Inverted Hammer 倒锤头 | 看涨 |
| `CDLKICKING` | Kicking 反冲 | 反转 |
| `CDLKICKINGBYLENGTH` | Kicking (by length) 反冲（按长度） | 反转 |
| `CDLLADDERBOTTOM` | Ladder Bottom 梯底 | 看涨 |
| `CDLLONGLEGGEDDOJI` | Long Legged Doji 长脚十字 | 中性 |
| `CDLLONGLINE` | Long Line Candle 长实体 | 持续 |
| `CDLMARUBOZU` | Marubozu 光头光脚 | 强势 |
| `CDLMATCHINGLOW` | Matching Low 呼应低价 | 看涨 |
| `CDLMATHOLD` | Mat Hold 铺垫 | 看涨 |
| `CDLMORNINGDOJISTAR` | Morning Doji Star 晨星十字 | 看涨 |
| `CDLMORNINGSTAR` | Morning Star 晨星 | 看涨 |
| `CDLONNECK` | On-Neck Pattern 颈上线 | 看跌 |
| `CDLPIERCING` | Piercing Pattern 刺透 | 看涨 |
| `CDLRICKSHAWMAN` | Rickshaw Man 轿夫 | 中性 |
| `CDLRISEFALL3METHODS` | Rising/Falling Three Methods 上升/下降三法 | 持续 |
| `CDLSEPARATINGLINES` | Separating Lines 分离线 | 持续 |
| `CDLSHOOTINGSTAR` | Shooting Star 流星 | 看跌 |
| `CDLSHORTLINE` | Short Line Candle 短实体 | 中性 |
| `CDLSPINNINGTOP` | Spinning Top 纺锤 | 中性 |
| `CDLSTALLEDPATTERN` | Stalled Pattern 停顿 | 看跌 |
| `CDLSTICKSANDWICH` | Stick Sandwich 条形三明治 | 看涨 |
| `CDLTAKURI` | Takuri 啄底（长下影蜻蜓十字） | 看涨 |
| `CDLTASUKIGAP` | Tasuki Gap 跳空并列 | 持续 |
| `CDLTHRUSTING` | Thrusting Pattern 插入 | 看跌 |
| `CDLTRISTAR` | Tristar Pattern 三星 | 反转 |
| `CDLUNIQUE3RIVER` | Unique 3 River 奇特三河 | 看涨 |
| `CDLUPSIDEGAP2CROWS` | Upside Gap Two Crows 上跳缺口两乌鸦 | 看跌 |
| `CDLXSIDEGAP3METHODS` | Upside/Downside Gap Three Methods 跳空三法 | 持续 |

---

## 11. 转写 QuantAll 的注意点

1. **字段映射**：TA-Lib 用 `open/high/low/close/volume`，QuantAll 中对应 `d['open']/d['high']/d['low']/d['close']/d['vol']`。
2. **复权**：TA-Lib 公式默认用原始价；QuantAll 需先算复权价 `adj_close = d['close']*d['adj_factor']`。
3. **移动平均**：TA-Lib 的 `MA` 可指定类型，QuantAll 中可用内置算子的组合表达（受 `禁止循环/apply` 约束，需用向量化）。
4. **滚动窗口算子**：QuantAll 提供 `MA/STD/REF/HHV/LLV/WMA/CORR` 等向量化算子，可对应 TA-Lib 的 SMA/STDDEV/REF/max/min/相关等。
5. **形态识别**：`CDL*` 返回 ±100/0，在 QuantAll 中可作为布尔/类别因子（注意需 OHLC 四价齐备）。
6. **逐点数学变换**（第 8 类）在 QuantAll 中直接用 `np.log`/`np.sqrt` 等即可。

> 本文件是「初始基线」收集，公式为通用定义（非 QuantAll 代码）。后续按 `因子表达式初始收集.md` 第 5 节的映射规则转写为 QuantAll 表达式。
