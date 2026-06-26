---
name: signalbot
description: 量化行情分析工具，对 BTC、黄金（XAUUSD）等标的计算 10 类技术指标（RSI、MACD、布林带、EMA、ATR、成交量、顾比均线、斐波那契回撤、锚定 VWAP、固定范围成交量分布），输出结构化 JSON 行情报告，可据此生成行情分析推文或做出操作建议。同时支持 1h/4h/日/周/月 多周期综合分析。
homepage: https://github.com/shanhuhai5739/signalbot
metadata: {"openclaw": {"emoji": "📊", "homepage": "https://github.com/shanhuhai5739/signalbot", "install": [{"id": "go-install", "kind": "go", "package": "github.com/shanhuhai5739/signalbot@latest", "bins": ["signalbot"], "label": "Install signalbot via go install"}]}}
---

# Signalbot 量化行情分析技能

## 何时使用

当用户提出以下类型的请求时，主动调用此技能：

- 询问 BTC、比特币、黄金、XAUUSD 等标的的行情、走势、涨跌
- 需要技术指标分析（RSI、MACD、布林带、EMA、ATR、成交量、顾比均线、斐波那契、VWAP、成交量分布）
- 需要判断趋势方向、主力资金态度（顾比均线长期组位置）
- 需要识别斐波那契关键支撑/阻力位
- 需要判断价格相对 VWAP 的强弱（机构持仓成本参考）
- 需要了解主力成交密集区（POC/VAH/VAL）
- 需要生成行情分析推文、日报、周报
- 需要判断当前趋势方向、支撑阻力位、操作建议（BUY/SELL/HOLD）
- 需要同时查看多个时间周期（1h/4h/日/周/月）综合研判
- 用户要求"分析一下今天行情"、"BTC 现在多空如何"、"黄金值得买吗"等

## 调用前置检查（每次调用前必须执行）

**在运行 signalbot 前，先检查二进制是否存在：**

```bash
which signalbot
```

- 若有输出路径 → 直接继续调用
- 若无输出（command not found）→ 立即自动执行以下命令编译安装，**无需询问用户**：

```bash
go install github.com/shanhuhai5739/signalbot@latest
```

安装完成后继续执行原始分析请求。如果 `go` 也不存在，提示用户先安装 Go（https://go.dev/dl）。

## 调用方式

### 单周期分析

使用 `exec` 工具（或 `bash`）运行以下命令，将 stdout 捕获为 JSON：

```bash
signalbot analyze --asset <标的> --timeframe <周期>
```

**注意**：命令会在 stderr 输出进度提示（可忽略），JSON 报告输出到 stdout。

### 多周期综合分析（推荐用于趋势研判）

```bash
signalbot multi --asset <标的>
```

并发分析 1h / 4h / 1d / 1w / 1M 五个时间维度，返回含 `summary.alignment`（趋势共振方向）的综合报告。

### --asset 合法值

| 值 | 含义 |
|---|---|
| `BTC` | 比特币 (BTCUSDT) |
| `XAUUSD` | 黄金 (XAUUSDT) |
| `ETH` | 以太坊 (ETHUSDT) |
| `SOL` | Solana (SOLUSDT) |
| `BNB` | 币安币 (BNBUSDT) |

也可直接填写 Binance 符号，如 `BTCUSDT`。

### --timeframe 合法值

| 值 | 适用场景 |
|---|---|
| `1h` | 短线日内分析 |
| `4h` | 中线波段分析（**推荐默认**） |
| `1d` | 长线趋势分析 |
| `1w` | 周线趋势 |
| `1M` | 月线（年线方向参考） |
| `15m` | 超短线 |

### 可选参数

- `--limit <数量>`：拉取 K 线数量，默认 200，最多 1500
- `--output <文件路径>`：将 JSON 写入文件而非 stdout

---

## JSON 输出字段解读

拿到 JSON 后，按以下规则解读各字段，再生成自然语言分析：

### price（最新价格快照）
- `current`：当前收盘价
- `change_pct`：较上一根 K 线的涨跌幅（%）

### indicators.rsi
- `value`：RSI 值（0–100）
- `signal`：
  - `overbought`（≥70）→ 超买，注意回调
  - `bullish`（55–69）→ 强势区间
  - `neutral`（46–54）→ 中性观望
  - `bearish`（31–45）→ 弱势区间
  - `oversold`（≤30）→ 超卖，关注反弹

### indicators.macd
- `histogram > 0` → 多头动能增强
- `histogram < 0` → 空头动能增强
- `cross: "golden_cross"` → 金叉（强看涨信号）
- `cross: "death_cross"` → 死叉（强看跌信号）

### indicators.bollinger
- `percent_b`：价格在布林带中的位置（0=下轨，0.5=中轨，1=上轨）
- `position: "upper_zone"` → 强势突破区，`"lower_zone"` → 弱势区
- `width`：带宽越窄代表价格越压缩，往往是行情突破前兆

### indicators.ema
- `alignment: "strongly_bullish"` → EMA9>21>50>200，四线多头完全排列
- `alignment: "bullish"` → EMA9>21>50，短中期多头
- `alignment: "bearish"` / `"strongly_bearish"` → 空头排列

### indicators.atr
- `pct`：ATR 占当前价格的百分比
- `regime: "low_volatility"` → 市场压缩，突破在即；`"high_volatility"` → 波动剧烈，注意止损

### indicators.volume
- `ratio`：当前成交量 / 20日均量
- `signal: "high_volume"` 或 `"above_average"` → 成交量放大确认行情
- `signal: "low_volume"` → 量能不足，信号可信度下降

### indicators.guppy（顾比均线 GMMA）
- **短期组**（`ema3`~`ema21`）代表投机/交易者资金；**长期组**（`ema34`~`ema377`）代表机构/长线资金
- `alignment`:
  - `"above_long"` → 短期组整体高于长期组，趋势强劲（多头）
  - `"below_long"` → 短期组整体低于长期组，趋势向下（空头）
  - `"crossing"` → 两组交叉重叠，处于压缩期（趋势转换中，谨慎）
- `gap_pct` > 0 → 短期组高于长期组的幅度；< 0 → 短期组低于长期组
- `signal`: `bullish` / `compression` / `bearish`
- **注意**：`ema233` 和 `ema377` 需 233+/377+ 根 K 线，不足时为 `0`（信号仍基于已有数据）

### indicators.fibonacci（斐波那契回撤）
- 基于**最近 100 根** K 线的摆动高低点，自动标定 0%→100% 七个水平
- `levels[]`：每个水平含 `label`（如 `"61.8%"`）、`price`、`is_above`（当前价是否高于该水平）
- `nearest_level`：当前价最近的斐波那契水平
- `distance_pct`：距最近水平的百分比距离；< 1.5% 时触发 `signal`
- `signal`:
  - `"at_support"` → 价格贴近斐波那契支撑位，关注多头反弹
  - `"at_resistance"` → 价格贴近斐波那契阻力位，关注回调压力
  - `"between_levels"` → 价格在两水平之间，方向中性
- `direction: "upper_half"` → 处于摆动区间上半段（多头占优）；`"lower_half"` → 下半段（空头占优）

### indicators.vwap（锚定 VWAP）
- 锚定最近 **50 根** K 线起点，计算量价加权均价及 ±1σ / ±2σ 标准差通道
- `value`：VWAP 值（机构持仓均价参考）
- `deviation_pct`：当前价格偏离 VWAP 的百分比
- `position`:
  - `"above_band2"` → 严重超买（偏离 > 2σ）
  - `"above_band1"` → 偏强势（偏离 > 1σ）
  - `"above_vwap"` → 价格高于 VWAP，多头主导
  - `"below_vwap"` → 价格低于 VWAP，空头主导
  - `"below_band1"` → 偏弱势
  - `"below_band2"` → 严重超卖（偏离 > 2σ），均值回归机会
- `signal`: `overbought` / `bullish` / `bearish` / `oversold`

### indicators.vpvr（固定范围成交量分布）
- 取最近 **100 根** K 线，划分为 **24 档**，按比例分配成交量
- `poc`（Point of Control）：成交量最密集的价格档，最强支撑/阻力参考
- `vah`（Value Area High）：70% 价值区间上边界
- `val`（Value Area Low）：70% 价值区间下边界
- `bins[]`：每档含 `price_low/high/mid`、`volume`、`is_poc`、`is_value_area`
- `signal`:
  - `"above_vah"` → 价格突破价值区高点，强势看涨（若有量配合）
  - `"above_poc"` → 在 POC 上方，多头占优
  - `"at_poc"` → 价格在 POC 附近（±0.5%），强支撑/阻力博弈
  - `"below_poc"` → 在 POC 下方，空头占优
  - `"below_val"` → 价格跌破价值区低点，弱势信号

### analysis（综合研判）
- `trend`：`bullish` / `neutral` / `bearish`
- `strength`：`strong` / `moderate` / `weak`
- `signal`：`BUY` / `SELL` / `HOLD`
- `confidence`：0–100 置信度，基于多指标共振程度
- `score`：原始评分（-8 到 +8），负数越大越空头
- `key_levels.support`：近期支撑价位列表（从近到远）
- `key_levels.resistance`：近期阻力价位列表（从近到远）

### multi 命令专属字段（summary）
- `alignment`：`all_bullish` / `mostly_bullish` / `mixed` / `mostly_bearish` / `all_bearish`
- `dominant_signal`：多周期共振后的综合信号（BUY/SELL/HOLD）
- `signals`：各周期单独信号（如 `{"1h":"BUY","4h":"HOLD","1d":"SELL",...}`）
- `confidence`：多周期共振置信度

---

## 推文生成指南

拿到 JSON 数据后，按以下结构生成中文行情分析推文（约 220–300 字）：

```
📊 $<标的> | <时间周期>行情分析

📈/📉 趋势：<多头/空头/震荡>（<strength>）

关键指标：
• RSI(<value>)：<信号描述>
• MACD：<histogram方向 + 是否金叉/死叉>
• EMA排列：<描述>
• 布林带：<价格位置描述>
• 顾比均线：<短长期组关系 + alignment 信号>
• VWAP：<价格偏离描述，position 信号>

🎯 关键价位：
支撑：$<support[0]> / $<support[1]>（含 Fib <nearest_level> 水平）
阻力：$<resistance[0]> / $<resistance[1]>
成交密集区(POC)：$<vpvr.poc>（价值区 $<val>–$<vah>）

⚡️ ATR波动：<regime>（<pct>%）
📊 成交量：<signal描述>

🔖 操作建议：<BUY/SELL/HOLD>（置信度 <confidence>%）
<简要理由，1–2句>

#BTC #Bitcoin #行情分析 #量化交易
```

---

## 多标的分析示例

如需同时分析 BTC 和黄金，依次运行两条命令，再合并分析：

```bash
signalbot analyze --asset BTC --timeframe 4h
signalbot analyze --asset XAUUSD --timeframe 1d
```

## 多周期分析示例

```bash
# BTC 五周期综合研判（推荐用于趋势确认）
signalbot multi --asset BTC

# 黄金多周期分析
signalbot multi --asset XAUUSD
```

解读 multi 报告时重点关注：
1. `summary.alignment` — 多周期趋势是否共振（all_bullish/all_bearish 信号最强）
2. 各周期 `indicators.guppy.alignment` — 不同时间维度下的资金分布
3. 各周期 `indicators.vpvr.poc` — 不同周期的主力成交密集区

## 更新二进制

当用户要求更新 signalbot 或检测到有新版本时，自动运行：

```bash
go install github.com/shanhuhai5739/signalbot@latest
```

更新完成后告知用户已更新至最新版本。

## 常见问题处理

- **go 命令不存在**：提示用户安装 Go https://go.dev/dl，安装后重新触发 `go install`
- **EMA233/EMA377 为 0**：数据不足，属正常现象；顾比信号仍基于可用的 EMA 值计算
- **数据不足**：XAUUSD 建议使用 `1d` 周期；BTC 各周期均可
- **网络超时**：建议设置 `BINANCE_BASE_URL` 环境变量切换为代理地址
