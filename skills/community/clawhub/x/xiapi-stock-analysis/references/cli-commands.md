# CLI 命令参考

本文档汇总个股分析所需的 CLI 命令，便于快速查阅。

## 前期准备

### Token 配置

```bash
# 检查当前配置
npx daxiapi-cli@latest config get token

# 配置 Token（方式一：CLI 配置）
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 配置 Token（方式二：环境变量）
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI
```

### 标的搜索与验证

```bash
# 搜索股票
npx daxiapi-cli@latest search <公司名> --type stock

# 验证单股数据可用性
npx daxiapi-cli@latest stock info <code>

# 验证多股数据可用性（最多20只）
npx daxiapi-cli@latest stock info <code1>,<code2>,<code3>
```

---

## Step 2: 数据收集命令

### 2.1 stock info — 个股快照（核心命令）

```bash
# 单股
npx daxiapi-cli@latest stock info <code>

# 多股（最多20只，适合横向对比）
npx daxiapi-cli@latest stock info <code1>,<code2>,<code3>
```

**返回字段完整说明**：

#### 基础行情

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `name` | 股票名称 | 三一重工 |
| `code` / `stockId` | 股票代码 | 600031 |
| `date` / `fullDate` | 数据日期 | 2026-04-09 |
| `close` / `price` | 收盘价 | 20.66 |
| `open` | 开盘价 | 20.70 |
| `high` | 最高价 | 20.85 |
| `low` | 最低价 | 20.57 |
| `vol` | 当日成交量（手） | 540802 |
| `vol1` | 昨日成交量（手） | 1190927 |
| `vma5` | 5日均量（手） | 698997 |
| `shizhi` | 总市值（亿元） | 1899.69 |
| `shizhi_lt` | 流通市值（亿元） | 1750.81 |

#### 涨跌幅动量

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `zdf` | 当日涨跌幅（%） | -0.96 |
| `zdf_5d` | 5日涨跌幅（%） | 1.77 |
| `zdf_10d` | 10日涨跌幅（%） | 4.71 |
| `zdf_20d` | 20日涨跌幅（%） | -7.15 |
| `zdf_30d` | 30日涨跌幅（%） | -13.84 |

> 判断方法：`zdf_5d / zdf_10d / zdf_20d` 同向为趋势连续，反向则动量分化。

#### 技术指标

| 字段 | 说明 | 关键阈值 |
|------|------|----------|
| `cs` | Close-to-EMA Strength，收盘价相对EMA20乖离率 | 0~15 健康偏强；>15 短期过热；< -5 跌破趋势 |
| `ncs` | 标准化CS | 辅助参考 |
| `sm` | EMA20与EMA60乖离率（中期动量） | >0 多头排列；<0 空头排列 |
| `ml` | EMA60与EMA120乖离率（长期动量） | >0 长期趋势向上 |
| `ibs` | Internal Bar Strength，收盘在当日高低区间的位置 | 接近100强收；接近0弱收；>70 偏强 |
| `mfi` | 资金流量指标（短期） | >50 资金净流入 |
| `mfi_long` | 资金流量指标（长期） | >50 长期资金净流入 |
| `sctr` | StockCharts Technical Rank，个股技术综合排名 | >80 强势；<20 弱势 |
| `rps` / `rps_score` | 相对价格强度（欧奈尔RPS） | >80 强势股 |
| `qd` | QD强度指标（综合强度评分） | 正值偏强，负值偏弱 |
| `pr` / `pr2` | 价格相对强度辅助指标 | 辅助参考 |

#### 成交量强度

| 字段 | 说明 | 说明 |
|------|------|------|
| `vcs` | 成交量相对短期均量强度 | 正值放量，负值缩量 |
| `vsm` | 成交量相对中期均量强度 | 同上 |
| `vsl` | 成交量相对长期均量强度 | 同上 |
| `vml` | 成交量中长期均量强度 | 同上 |

#### 均线

| 字段 | 说明 |
|------|------|
| `ema20` | 20日指数移动平均线 |
| `ma20` | 20日简单移动平均线 |
| `ma50` | 50日均线 |
| `ma150` | 150日均线 |
| `ma200` | 200日均线 |
| `ma20_slope` | MA20斜率，正值向上，负值向下 |

#### 高低点位置

| 字段 | 说明 |
|------|------|
| `low_52w` / `high_52w` | 52周最低/最高价 |
| `low_52w_days` / `high_52w_days` | 距52周低点/高点的天数 |
| `low_120d_days` / `high_120d_days` | 距120日低点/高点的天数 |
| `low_60d_days` / `high_60d_days` | 距60日低点/高点的天数 |
| `low_20d_days` / `high_20d_days` | 距20日低点/高点的天数 |

> 判断方法：`high_52w_days` 越小说明近期创新高；`low_52w_days` 越小说明近期创新低。

#### 估值

| 字段 | 说明 |
|------|------|
| `pe_ttm` | 市盈率（TTM） |
| `pe_temp` | PE估值温度（历史百分位，-1表示无数据） |
| `pb_temp` | PB估值温度（历史百分位，-1表示无数据） |
| `roe` | 净资产收益率（年化） |
| `roe_ttm` | ROE（TTM） |
| `roe_ttm_avg` | ROE（TTM均值） |
| `gxl_ttm` | 股息率（TTM，%） |
| `gxl_5y` | 5年平均股息率（%） |

#### 形态信号（布尔值）

| 字段 | 说明 |
|------|------|
| `isTrendUp` | 是否趋势向上 |
| `isVCP` / `vcp` | 是否VCP形态 |
| `isLPS` | 是否LPS（Last Point of Support，吸筹阶段最后支撑点） |
| `isSOS` | 是否SOS（Sign of Strength，强势走势） |
| `isSpring` | 是否Spring（弹簧形态） |
| `isW` | 是否W底形态 |
| `is3C` | 是否3C形态 |
| `isNR7` / `isNR4` | 是否NR7/NR4（窄幅整理） |
| `isIB` | 是否内包线（Inside Bar） |
| `isCrossoverBox` | 是否突破箱体 |
| `isAnt` | 是否蚂蚁形态 |
| `isHigh1` | 是否创近期新高 |

#### 行业与概念

| 字段 | 说明 |
|------|------|
| `bkId` / `bkName` | 所属板块ID与名称 |
| `thsBkId` | 同花顺板块ID |
| `gainian` | 所属概念（逗号分隔） |
| `tags` | 标签 |
| `cg` | 概念个数 |
| `qs` | 强势评分 |

---

### 2.2 kline — K线数据

```bash
# 默认返回最近60条日线
npx daxiapi-cli@latest kline <code>

# 指定条数
npx daxiapi-cli@latest kline <code> -l 120

# 周线
npx daxiapi-cli@latest kline <code> -t week
```

**返回字段**：`date, open, close, high, low, vol`

**用途**：用于自行计算 MA60/MA120/MA250 等均线、MACD/RSI/KDJ 等指标，以及识别经典形态（W底、M头、旗形等）。`stock info` 已提供大量技术快照，`kline` 主要用于需要历史序列的深度复算场景。

---

### 2.3 report finance — 财务报告

```bash
# 单股财务报告（返回最近25期季报/年报）
npx daxiapi-cli@latest report finance <code>

# 多股财务对比（逐只执行，保持同一报告期口径）
npx daxiapi-cli@latest report finance <code1>
npx daxiapi-cli@latest report finance <code2>
```

**返回字段**：净利润、净利润同比、扣非净利润、营业总收入、营收同比、基本每股收益、每股净资产、每股经营现金流、销售净利率、销售毛利率、净资产收益率、存货周转率、应收账款周转天数、流动比率、速动比率、资产负债率等。

**联动 Skill**：`xiapi-financial-roe-analysis`

**注意**：`stock info` 已直接返回 `roe / roe_ttm / pe_ttm` 等核心估值字段，做快速判断时可直接使用，无需额外跑 `report finance`。`report finance` 适合需要多期趋势对比或完整财务结构分析的场景。

---

### 2.4 stock capital-flow — 个股主力资金流向

```bash
# 获取个股主力资金流向（返回最近约13天）
npx daxiapi-cli@latest stock capital-flow <code>
```

**返回字段**：

| 字段 | 说明 |
|------|------|
| `date` | 日期 |
| `当日资金流入` | 当日主力净流入金额（元，正流入负流出） |
| `当日资金流入占比` | 当日主力净流入占成交额比例 |
| `5日资金流入金额` | 近5日主力净流入累计（元） |
| `5日资金流入占比` | 近5日主力净流入占比 |
| `板块资金流入` | 所属板块当日资金净流入（元） |
| `5日板块资金流入金额` | 所属板块近5日资金净流入（元） |
| `板块代码` / `板块名称` | 所属板块信息 |

**用途**：判断主力资金是否持续流入/流出，结合板块资金流向判断个股是否顺势。

---

### 2.5 sector stocks — 板块内个股排名

```bash
# 按CS强度排序查看板块内个股
npx daxiapi-cli@latest sector stocks --code <BK_CODE> --order cs
```

**用途**：判断目标股票在所属板块内的相对强弱位置。`bkId` 字段可从 `stock info` 返回结果中直接获取。

---

### 2.6 sector heatmap + market compass — 市场环境校准

```bash
# 板块热力图（判断行业景气）
npx daxiapi-cli@latest sector heatmap --order cs --limit 20

# 市场温度（判断整体风险偏好）
npx daxiapi-cli@latest market compass
```

**用途**：校准个股分析结论是否顺势，不作为个股分析的核心数据。

---

## 命令执行顺序建议

### 单股模式

| 分析阶段 | 优先命令 | 可选命令 |
|---------|---------|---------|
| 标的确认 | `search`, `stock info` | — |
| 技术快照 | `stock info` | `kline`（需历史序列时） |
| 基本面 | `stock info`（快速）/ `report finance`（深度） | — |
| 资金流向 | `stock capital-flow` | — |
| 行业定位 | `sector stocks --code <bkId>` | `sector heatmap` |
| 市场环境 | `market compass` | — |

### 多股对比模式

| 阶段 | 优先命令 | 目标 |
|------|---------|------|
| 标的确认 | `stock info <code1,code2,...>` | 一次性获取多股快照 |
| 技术细化 | `kline <code>`（逐只） | 复算趋势与形态一致性 |
| 财务对比 | `report finance <code>`（逐只） | 财报质量横向比较 |
| 资金对比 | `stock capital-flow <code>`（逐只） | 主力资金流向对比 |
| 市场校准 | `market compass`, `sector heatmap` | 判断比较结果是否顺势 |
