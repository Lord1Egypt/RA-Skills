# OpenAPI v1 端点速查（yyqdata）

所有端点在 `${YYQDATA_API_BASE_URL}` 之下；**`/openapi/v1/**` 数据端点 GET、POST 都支持**（M2M 发放接口 `/openapi/admin/**` 仍仅 POST）。下面示例统一写 POST，等价的 GET 见「### 请求」。

## 共享约定

### 请求
- **两种调法等价，任选其一**（同一端点 GET / POST 都行）：
  - **POST + JSON**（推荐，字段多时清晰）：Header `Authorization: Bearer ${TOKEN}` + `Content-Type: application/json`，body 传 JSON。
  - **GET + 查询参数**（字段少 / 浏览器 / 受限环境）：参数拼在 URL，如
    `GET ${YYQDATA_API_BASE_URL}/openapi/v1/stock/kline/daily?tsCode=000001.SZ&type=11&startDate=20240101&endDate=20240131`
    token 优先走 `Authorization: Bearer ${TOKEN}` 头；**无法设 header 的环境**（web_fetch / 浏览器 / 无 curl）把 token 也拼进 URL：`...&token=${TOKEN}`（或 `?access_token=`）。⚠️ URL 里的 token 会进访问日志，能设 header 时优先 header。
- 两种方式**字段名都严格 camelCase**（`tsCode` 不是 `ts_code`，`tradeDate` 不是 `trade_date`，`startDate` 不是 `start_date`，`endDate` 不是 `end_date`）。snake_case 字段会被忽略 → 端点用默认值，常常返回空数据/默认行为。
- **凡 form 继承 `OpenApiPageForm` 的端点**额外接受 `page`(int, 默认 `1`) + `size`(int, 默认 `50`，**硬上限 `100`**)；超出 100 静默截断到 100，<1 截断到 1。
- **凡 form 继承 `OpenApiBaseForm`（不分页）的端点没有 `page`/`size`**，传了也无效。每张表后会标注 form 是否支持分页。
- 不传任何字段（body `{}`）端点用全部默认值，必填字段缺失通常返回空列表或异常。

### 通用字段语义（出现多次时不再重复说明）
| 字段 | 类型 | 含义 |
|------|------|------|
| `tsCode` | string | 股票/合约/基金代码带交易所后缀，如 `600519.SH` / `000001.SZ` / `204001.SH` / `510300.SH`。**永远 camelCase**，不是 ts_code |
| `tsCodes` | string[] | 多代码批量，**一次 ≤ 50** |
| `tradeDate` / `startDate` / `endDate` | string | 时间字段（详见下方"时间字段规范"） |
| `adjType` | string | 复权：`bfq`(默认不复权) / `hfq`(后复权) / `qfq`(前复权)。**注意是 `adjType`，不是 `adj_type`** |
| `page` / `size` | int | 分页（仅 OpenApiPageForm 子类支持） |
| `nameKeyword` | string | 名称模糊匹配关键字。**注意是 `nameKeyword`，不是 `name_keyword`** |

### ⏰ 时间字段规范（**核心**——agent 必读）

**所有 OpenAPI v1 请求时只用 3 个时间字段**：`tradeDate`（单日）/ `startDate`（起始）/ `endDate`（截止）。响应里出现的 `annDate` / `publishDate` / `navDate` / `quarter` 等只是返回字段，**不要回填到请求 body**。

**字符串格式**（按端点数据粒度选择）：

| 格式 | 适用端点 | 示例值 | 说明 |
|------|--------|------|------|
| `YYYYMMDD` | **绝大多数日级端点**：K 线 / 估值 / 财务 / 龙虎榜 / 板块 / 资金流 / 大宗 / 集合竞价 / 公司事件 / 转债 / 期货 / ETF / 基金净值 等 | `"20260430"` | **默认格式**——拿不准就用这个 |
| `YYYYMM` | 宏观月度：CPI / PPI / PMI / M2 / 社融 / 月度宏观聚合 | `"202604"` | 月报数据，对应 `/market/macro/{cpi,ppi,pmi,money-supply,social-finance,monthly}` |
| `YYYYQX` | 季度数据：GDP | `"2024Q4"` | 仅 `/market/macro/gdp`，X = 1/2/3/4 |
| `YYYYMMDDHHmm` | 分钟 K（罕见）：用 `startDate` / `endDate` 分钟边界过滤 | `"202604301430"` | 仅 `*/kline/minutes` 端点；通常用 `YYYYMMDD` 默认到当日开收盘也可 |

**禁止**：
- ❌ `"2026-04-30"`（带 `-` 分隔符）→ 后端按 string 严格匹配，会被当作未传，端点用默认值/空结果
- ❌ `"2026/04/30"` → 同上
- ❌ ISO 8601 `"2026-04-30T00:00:00Z"` → 同上
- ❌ Unix 时间戳（数字）→ 同上
- ❌ 直接传 `tradeDate` 字段到只支持 `startDate/endDate` 的端点（反之亦然）—— 看每个端点的字段表

**字段使用模式**：

| 模式 | 怎么用 |
|------|--------|
| **指定一天** | `{"tradeDate":"20260430"}` 用于龙虎榜/板块/集合竞价等单日快照端点 |
| **指定区间** | `{"startDate":"20260101","endDate":"20260430"}` 用于 K 线 / 财务 / 净值 / 资金流等时序端点 |
| **只给 `endDate`** | 后端取"最早可得 ~ endDate"窗口（通常太大，配合 `size` 控制） |
| **只给 `startDate`** | 后端取"startDate ~ 最新交易日"窗口 |
| **都不给** | 端点取最近 N 个交易日（具体看 `size`，默认 50；财务类按 8 期） |

**常见映射**（用户口语 → body 字段）：

| 用户说 | 字段 |
|--------|------|
| "今天" | 不传时间字段（端点自动取最新交易日）；非要传就传当日 `tradeDate` |
| "昨天" / "上周五" | `tradeDate=<具体日 YYYYMMDD>`（agent 自己算日期，不要让用户算） |
| "最近 N 天 / 这周 / 近 1 个月" | 不传 `tradeDate`；可选 `startDate=今天-N天 endDate=今天`，或仅靠 `size` 控制 |
| "今年以来 / YTD" | `startDate="<当前年>0101", endDate=<今天>` |
| "2024 年" | `startDate="20240101", endDate="20241231"` |
| "近 8 个季度财报" | 不传时间，给 `size=8`（端点按 endDate 倒序，自然取最近 8 期） |
| "Q1 / 第一季度" | 财务用 `endDate="<年>0331"`；GDP 用 `quarter="<年>Q1"` |

### 响应
统一信封 `ApiResultModel<T>` = `{code, msg, data, traceId}`。`code != 0/200` 视为失败。

---

## 一、标的解析（stock.basic — 免费）

### `POST /openapi/v1/stock/basic/search` — 模糊搜索股票
form: `StockSearchForm` (无分页) · `{"nameOrCode": "茅台"}`
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `nameOrCode` | string | ✓ | 代码 / 简称 / 中文全名 / 拼音首字母。例 `"600519"` / `"600519.SH"` / `"茅台"` / `"贵州茅台"` / `"GZMT"` |

### `POST /openapi/v1/stock/basic/detail` — 股票详情
form: `StockDetailForm` (无分页) · `{"tsCode": "600519.SH"}`（必填，**精确**带交易所后缀）。完整响应字段（19个）：`tsCode`/`symbol`/`name`/`area`/`industry`/`cnSpell`(拼音首字母)/`market`/`exchange`/`currType`/`listStatus`/`isHs`(H=沪港通/S=深港通/N=否)/`actName`(实控人)/`actEntType`(企业类型如"地方国有企业")/`enName`/`fullName`(全称) + `listDate`(⚠️ **毫秒时间戳字符串**，如 `"998841600000"`)/`listDateStr`(YYYYMMDD)/`delistDate`(⚠️ **退市时为ms字符串，未退市为字符串 `"None"` 非 null！**)/`delistDateStr`(同样为 `"None"` 或 YYYYMMDD)

### `POST /openapi/v1/stock/basic/list` — 全市场股票精简列表
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可。完整字段（3个）：tsCode/symbol(纯数字代码)/name（不含 `listDate`/`industry` 等，需详情用 `/basic/detail`）

### `POST /openapi/v1/stock/basic/classify` — 行业 / 主题分类目录
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可。响应是简单 `id`（int）+`name` 的分类目录（不是行业名，是分类桶名），`id` 用于 `/classify/list` 的入参

### `POST /openapi/v1/stock/basic/classify/list` — 按分类拿成分股
form: `StockClassifyForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `id` | int | ✓ | 父级分类 ID（由 `/classify` 端点返回的 id 字段提供） |
| `level` | int | ✓ | 申万级别：`1` 一级（约31个）/ `2` 二级（约134个）/ `3` 三级（约346个） |

⚠️ **响应是分类汇总，不是个股列表**：每行一个行业/主题，完整字段（3个）：classifyName(行业/主题名)/stockCount(成分股数量，int)/swCode(申万行业代码，可null)。要拿行业内个股的估值/K线，需取 `classifyName` 再调 `/stock/indicator/last` 等端点。

---

## 二、K 线行情（stock.kline — 免费 / stock.minute — Plus）

> ⚠️ **K 线系响应日期格式不统一，极易踩坑**：
> - `stock/kline/daily`（A股日K）：`tradeDate` = **"YYYY-MM-DD" 带横杠字符串**（如 "2026-06-05"），另有 `time` 字段 = 毫秒时间戳
> - `stock/index/kline/daily`（指数日K）：`tradeDate` = **毫秒时间戳**
> - `stock/kline/percentage-change`（多周期涨跌幅）：`tradeDate` = **毫秒时间戳**
> - `stock/kline/limits`（涨跌停价）：`tradeDate` = **"YYYYMMDD" 紧凑字符串**
> - **输入参数** `startDate`/`endDate`：所有端点统一 YYYYMMDD 字符串

### `POST /openapi/v1/stock/kline/daily` — 日 / 周 / 月 K 线
form: `StockCandlesDailyForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 股票代码带交易所后缀 |
| `type` | int | – | K 线类型：`11` 日（默认） / `12` 周 / `13` 月。**只认这 3 个值**；若返回空 list 且你没传 `type`，补传 `type:11` 重试一次 |
| `startDate` | string | – | `YYYYMMDD`，可空 |
| `endDate` | string | – | `YYYYMMDD`，可空（不传取最新交易日） |

⚠️ **`startDate`/`endDate` 同时传会 `code:1 系统异常`（已知 PG 迁移 bug）**——用 `size` 控制返回条数代替日期范围过滤。响应字段（12个）：`tsCode`/`tradeDate`(**"YYYY-MM-DD" 横杠字符串**)/`time`(毫秒时间戳)/`open`/`high`/`low`/`close`/`preClose`/`chg`/`pctChg`/`vol`(手)/`amount`(元)

### `POST /openapi/v1/stock/kline/minute` — 分钟 K 线（Pro）
form: `StockCandlesMinutesForm` (分页) · 单次窗口 ≤ 1 个月。路由：`freq≠1min` 全走 Tushare 实时转发（5 分钟缓存）；`freq=1min` 近 30 交易日读库、更早走 Tushare。**上游失败返 `code=16`+msg（≠"无数据"，16=上游数据源故障可重试），等 1 分钟重试一次**；指数分钟历史另有 `/stock/index/kline/minutes`（读库，窗口更长）
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 股票代码 |
| `freq` | string | ✓ | `"1min"` / `"5min"` / `"15min"` / `"30min"` / `"60min"` |
| `startDate` | string | – | `YYYYMMDD` 或 `YYYYMMDDHHmm`，可空 |
| `endDate` | string | – | 同上 |

### `POST /openapi/v1/stock/kline/adj-factor` — 复权因子
form: `StockIndexKlineForm` (分页) · `{"tsCode": "600519.SH", "startDate": "20260101", "endDate": "20260430"}`（仅 tsCode 必填）。完整字段（3个）：tsCode/tradeDate(**⚠️ YYYYMMDD字符串，非毫秒！**)/adjFactor。用法：`HFQ_price = BFQ_price × adjFactor / 当日最新 adjFactor`

### `POST /openapi/v1/stock/kline/limits` — 每日涨跌停价
form: `StockIndexKlineForm` (分页) · `tsCode` 必填，缺日期默认最近 60 天。响应字段（5个）：`tradeDate`(YYYYMMDD字符串)/`tsCode`/`preClose`(⚠️ **可为 None/null**)/`upLimit`(涨停价)/`downLimit`(跌停价)

### `POST /openapi/v1/stock/kline/percentage-change` — 多周期涨跌幅
form: `StockPercentageChangeForm` (分页) · 1d/3d/1w/2w/1m/1q/2q/1y
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | – | 单只股票（与 orderBy 二选一） |
| `orderBy` | string | – | 排序字段，可选 `pctChg` / `pctChg3d` / `pctChg1w` / `pctChg2w` / `pctChg1m` / `pctChg1q` / `pctChg2q` / `pctChg1y` |
| `direction` | string | – | `"asc"` / `"desc"`（默认 `desc`） |
| `exchange` | string | – | `"SH"` / `"SZ"` / `"BJ"`，空=全市场 |

⚠ **注意**：旧文档写的是 `tsCodes`(数组)，**实际 form 字段是 `tsCode`（单数）+ `orderBy`**。该端点用 `StockPercentageChangeForm`，不是 `StockTsCodeForm`。响应字段（19个）：`tsCode`/`name`/`tradeDate`(⚠️ **毫秒时间戳**)/`pctChg`/`close` + 各周期 `pctChgXx`/`closeXx`（`3d`/`1w`/`2w`/`1m`/`1q`/`2q`/`1y`，共 7 个周期各 2 字段）

### `POST /openapi/v1/stock/kline/limit-up` — 涨停连板筛选
form: `StockCandlesDailyLimitUpForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tadeDays` | int | ✓ | 回看 N 个交易日。**字段名拼写为 `tadeDays`**（历史遗留，不要写成 `tradeDays`） |
| `limitUpNum` | int | ✓ | 至少 M 个涨停板。例 `2` = 近 N 日内 ≥ 2 板的票 |

> 🔎 **`data:null` ≠ `data:[]`**：本端点参数缺失或 ≤0 时服务端返回 `data:null`（code 仍是 0）——看到 **null 先查自己的参数**（两个字段都必须 >0）；`[]` 才是"查了但没有符合的票"。

### `POST /openapi/v1/stock/kline/graph-type` — K 线形态识别
form: `StockCandlesDailyLimitUpForm` (无分页) · 同上 form
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tadeDays` | int | ✓ | 回看 N 个交易日 |
| `type` | int | ✓ | 形态枚举。**当前服务端只实现了 `4`（W 双底）**；枚举里的 `1` 震荡上行 / `2` 震荡下行 / `3` W突破**未实现**，传了会静默返回 `[]`（不报错）。**永远传 `4`**，用户问其他形态时直接说明"该形态识别暂未上线" |
| `lineType` | int | ✓ | 周期：`11` 日 / `12` 周 / `13` 月。**只认这 3 个值**，传错/不传返回 `data:null` |
| `limitUpNum` | int | – | 该端点不用，可省略 |

---

## 三、估值 / 技术指标（stock.indicator — 免费）

> ⚠️ **本 scope 所有端点响应 `tradeDate`（或 `endDate`/`roeDate`）均为毫秒时间戳**——输入 `startDate`/`endDate` 仍是 YYYYMMDD 字符串（仅输入参数）。`roeDate` 可为 null。

### `POST /openapi/v1/stock/indicator/last/by-codes` — 批量最新估值快照
form: `StockTsCodeForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCodes` | string[] | ✓ | 多只代码，**单次 ≤ 50**。例 `["600519.SH","000858.SZ"]` |
| `tradeDate` | string | – | 可空，默认取最新交易日 |

响应字段（25个，与 `valuation/history` 相同但仅最新一期）：`tsCode`/`symbol`/`name`/`tradeDate`（毫秒）/`close`/`turnoverRate`/`turnoverRateF`/`volumeRatio`/`pe`/`peTtm`/`pb`/`ps`/`psTtm`/`dvRatio`/`dvTtm`（股息率）/`totalShare`/`floatShare`/`freeShare`/`totalMv`/`circMv`/`limitStatus`/`roe`/`chg`/`pctChg`/`roeDate`（可为 null）

### `POST /openapi/v1/stock/indicator/latest` — 同上（OpenApiV1StockController.indicatorLatest 入口）
form: `StockTsCodeForm` (无分页) · 字段同 `last/by-codes`

### `POST /openapi/v1/stock/indicator/last` — 按申万行业批量取估值快照
form: `StockIndicatorForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `id` | int | ✓ | 申万行业 ID（由 `/basic/classify` 提供） |
| `level` | int | ✓ | 行业级别：`1` / `2` / `3` |
| `name` | string | – | 子分类名（一般留空） |

### `POST /openapi/v1/stock/indicator/valuation/history` — 估值时间序列
form: `StockTechIndicatorForm` (分页) · `adjType` 字段被忽略。⚠️ `tradeDate` 是毫秒时间戳。完整字段（25个）：`tsCode`/`symbol`/`name`/`tradeDate`(ms) · 估值：`close`/`pe`/`peTtm`/`pb`/`ps`/`psTtm` · 股息：`dvRatio`/`dvTtm`(股息率%) · 活跃度：`turnoverRate`/`turnoverRateF`/`volumeRatio`/`limitStatus`(Byte：0普通/1涨停/2跌停/3一字涨停/4一字跌停) · 股本（万股）：`totalShare`/`floatShare`/`freeShare` · 市值（万元）：`totalMv`/`circMv` · 收益：`roe`/`chg`/`pctChg`/`roeDate`(ms，可为null)

### `POST /openapi/v1/stock/indicator/ma-channel` — MA/EMA/BOLL/KTN/TAQ/BBI/EXPMA
form: `StockTechIndicatorForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 股票代码 |
| `startDate` | string | – | `YYYYMMDD`，不传取最近 60 交易日 |
| `endDate` | string | – | `YYYYMMDD` |
| `adjType` | string | – | `"bfq"` / `"hfq"` / `"qfq"`（默认 `bfq`） |

完整字段（28个）：tsCode/tradeDate(ms) · MA：ma5/ma10/ma20/ma30/ma60/ma90/ma250 · EMA：ema5/ema10/ema20/ema30/ema60/ema90/ema250 · 布林：bollUpper/bollMid/bollLower · bbi · 肯特纳：ktnUpper/ktnMid/ktnDown · 唐安奇：taqUp/taqMid/taqDown · EXPMA：expma12/expma50

### `POST /openapi/v1/stock/indicator/oscillator` — MACD/KDJ/RSI/BIAS/DMI/CCI/WR/BRAR/CR
form: `StockTechIndicatorForm` (分页) · 同上字段。完整字段（28个）：tsCode/tradeDate(ms) · MACD：macd/macdDif/macdDea · KDJ：kdjK/kdjD/kdjJ · RSI：rsi6/rsi12/rsi24 · BIAS：bias1/bias2/bias3 · DMI：dmiPdi/dmiMdi/dmiAdx/dmiAdxr · cci · WR：wr/wr1 · BRAR：brarAr/brarBr · cr · 计数(Integer)：upDays/downDays/lowDays/topDays

### `POST /openapi/v1/stock/indicator/trend-volume` — ATR/OBV/ASI/TRIX/VR/PSY/MTM/ROC/EMV/DPO/MASS/MFI/XSII
form: `StockTechIndicatorForm` (分页) · 同上字段。完整字段（28个）：tsCode/tradeDate(ms) · atr/obv · asi/asit · trix/trma · vr · psy/psyMa · mtm/mtmMa · roc/maRoc · emv/maemv · dfmaDif/dfmaDifma · dpo/madpo · mass/maMass · mfi · XSII薛斯通道：xsiiTd1/xsiiTd2/xsiiTd3/xsiiTd4

### `POST /openapi/v1/stock/indicator/short-term` — 19 个量化短线因子
form: `StockTechIndicatorForm` (分页) · 同上但 `adjType` 被忽略
> ⚠️ **数据暂未生成**（2026-06-07 实测底表全空，任何票都返 `[]`）：拿到空属预期，直接告诉用户"短线因子模块暂未上线"，**不要**换票/换日期反复重试

### `POST /openapi/v1/stock/indicator/nine-turn` — DeMark 九转序列
form: `StockTechIndicatorForm` (分页) · 同上但 `adjType` 被忽略。⚠️ `tradeDate` 是毫秒；响应含 K 线基础字段（OHLCV+amount）+ `freq`（`"daily"`）+ `upCount`（当日上行计数）+ `downCount`（当日下行计数）+ `nineUpTurn`（九转买入信号，可为 null）+ `nineDownTurn`（九转卖出信号，可为 null）

### `POST /openapi/v1/stock/indicator/roe` — 单股 ROE 历史时间序列
form: `StockCandlesDailyForm` (分页) · 仅 `tsCode` + `startDate` + `endDate` 生效，其他字段忽略。⚠️ **响应没有 `tradeDate` 字段**，日期在 `endDate`（**毫秒时间戳**）；另有 `period`（季度标签如 `"Q1"`/`"Q2"`/`"Q3"`/`"Q4"`）和 `roe`（%）

---

## 四、财务（stock.financial — Plus）

> ⚠️ **财务报表日期三套机制，必须区分**：
> - `income-statement` / `balance-sheet` / `cash-flow` / `indicator` / **`repurchase`**（股票回购）：响应 **`annDate`/`endDate` 均为毫秒时间戳**（如 `1774886400000`）
> - `core` / `dividend` / `business-segment` / `pledge`：响应 `endDate`/`annDate` 均为 **YYYYMMDD 字符串**
> - **输入参数** `startDate`/`endDate`：全部端点一律 `YYYYMMDD` 字符串（无论响应是什么格式）

### `POST /openapi/v1/stock/financial/income-statement` — 利润表（25 列）
⚠️ **响应 `annDate`/`endDate` 均为毫秒时间戳**（与 `/financial/core` 的 YYYYMMDD 字符串不同！输入 `startDate`/`endDate` 仍用 YYYYMMDD）。完整字段（25个）：`tsCode`/`annDate`(⚠️ **毫秒时间戳**)/`endDate`(⚠️ **毫秒时间戳**)/`reportType`("1"合并/"2"母公司)·`basicEps`/`dilutedEps` EPS·`totalRevenue`(营业总收入)/`revenue`(营业收入)·`totalCogs`(营业总成本)/`operCost`(营业成本)/`bizTaxSurchg`(营业税金及附加)/`sellExp`/`adminExp`/`finExp`/`rdExp` 各项费用·`operateProfit`(营业利润)/`investIncome`(投资收益)/`fvValueChgGain`(公允价值变动)/`nonOperIncome`(营业外收入)/`nonOperExp`(营业外支出)·`totalProfit`(利润总额)/`nIncome`(⚠️ **净利润**，camelCase 注意大写 I，不是 `nincome`)/`nIncomeAttrP`(⚠️ **归母净利润**，注意大写 I 和 P，不是 `nincomeAttrP`)/`ebit`/`ebitda`
form: `StockFinancialForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 股票代码 |
| `startDate` | string | – | 起始报告期 `YYYYMMDD`（季末日如 `"20240331"`） |
| `endDate` | string | – | 结束报告期 |
| `reportType` | string | – | `"1"` 合并报表（推荐默认）/ `"2"` 母公司 / `"3"` 调整合并 / `"4"` 调整母公司。**字段名是 `reportType` 不是 `report_type`** |

### `POST /openapi/v1/stock/financial/balance-sheet` — 资产负债表（31 列）
form: `StockFinancialForm` (分页) · 同上。⚠️ **响应 `annDate`/`endDate` 均为毫秒时间戳**。完整字段（31个）：`tsCode`/`annDate`(ms)/`endDate`(ms)/`reportType`·[资产]`moneyCap`(货币资金)/`tradAsset`(交易性金融资产)/`notesReceiv`(应收票据)/`accountsReceiv`(应收账款)/`inventories`(存货)/`totalCurAssets`(流动资产合计)/`fixAssets`(固定资产)/`intanAssets`(无形资产)/`goodwill`(商誉)/`totalNca`(非流动资产合计)/`totalAssets`(资产总计)·[负债]`stBorr`(短期借款)/`notesPayable`(应付票据)/`acctPayable`(应付账款)/`payrollPayable`(应付职工薪酬)/`taxesPayable`(应交税费)/`totalCurLiab`(流动负债合计)/`ltBorr`(长期借款)/`bondPayable`(应付债券)/`totalLiab`(负债合计)·[权益]`totalShare`(股本)/`capRese`(资本公积)/`surplusRese`(盈余公积)/`undistrPorfit`(未分配利润)/`totalHldrEqyExcMinInt`(归母股东权益)/`totalHldrEqyIncMinInt`(股东权益含少数股东)/`totalLiabHldrEqy`(负债+权益合计，验证表平衡)

### `POST /openapi/v1/stock/financial/cash-flow` — 现金流量表（21 列）
form: `StockFinancialForm` (分页) · 同上。⚠️ **响应 `annDate`/`endDate` 均为毫秒时间戳**。完整字段（21个）：`tsCode`/`annDate`(ms)/`endDate`(ms)/`reportType`·[经营]`cFrSaleSg`(收到销售款)/`cPaidGoodsS`(付采购款)/`cPaidToForEmpl`(付职工薪酬)/`cPaidForTaxes`(付税)/`nCashflowAct`(经营净额)·[投资]`cPayAcqConstFiolta`(购建资产CapEx)/`cRecpReturnInvest`(收回投资)/`cPaidInvest`(投资支出)/`nCashflowInvAct`(投资净额)·[筹资]`cRecpBorrow`(借款收入)/`cRecpCapContrib`(增发收入)/`cPayDistDpcpIntExp`(付股利/利息)/`nCashFlowsFncAct`(筹资净额)·[余额]`cCashEquBegPeriod`(期初现金)/`cCashEquEndPeriod`(期末现金)·`freeCashflow`(FCF)/`provDeprAssets`(折旧摊销)

### `POST /openapi/v1/stock/financial/indicator` — 综合财务指标（27 列）
form: `StockFinancialForm` (分页) · 同上。⚠️ **响应 `annDate`/`endDate` 均为毫秒时间戳**。完整字段（27个）：`tsCode`/`annDate`(ms)/`endDate`(ms)·[每股]`eps`/`bps`/`ocfps`·[盈利]`roe`/`roa`/`roic`/`grossprofitMargin`/`netprofitMargin`·[现金流质量]`ocfToOr`(经营/营收)/`ocfToProfit`(经营/净利)/`ocfToDebt`(经营/总负债)/`ocfToShortdebt`(经营/流动负债)·[自由现金流]`fcff`(企业FCF)/`fcfe`(股权FCF)·[同比增速]`basicEpsYoy`/`netprofitYoy`/`dtNetprofitYoy`(扣非净利润同比)/`trYoy`(营业总收入同比)/`orYoy`(营业收入同比)·[单季度]`qEps`/`qRoe`/`qNetprofitMargin`/`qNetprofitYoy`/`qOcfToOr`（⚠️ 单季 q-字段首字母大写，如`qEps`不是`qeps`）

### `POST /openapi/v1/stock/financial/business-segment` — 分业务营收
form: `StockFinancialForm` (分页) · 同上。⚠️ **响应 `endDate` 是 YYYYMMDD 字符串（非毫秒时间戳）**；一个报告期多行（每个业务分部一行）；完整字段（8个）：`tsCode`/`endDate`(YYYYMMDD)/`bzItem`(业务名称)/`bzCode`(业务代码)/`bzSales`(业务收入)/`bzProfit`(业务利润)/`bzCost`(业务成本)/`currType`(货币类型)

### `POST /openapi/v1/stock/financial/repurchase` — 股票回购
form: `StockFinancialForm` (分页) · 同上。⚠️ **响应 `annDate`/`endDate`/`expDate` 均为毫秒时间戳**；完整字段（9个）：`tsCode`/`annDate`(ms)/`endDate`(ms)/`proc`(进度："实施"/"完成"/"预案")/`expDate`(ms, 回购期过期日)/`vol`(回购数量, 股)/`amount`(回购金额, 元)/`highLimit`(价格上限)/`lowLimit`(价格下限)

### `POST /openapi/v1/stock/financial/pledge` — 大股东质押
form: `StockFinancialForm` (分页) · 同上。⚠️ **响应 `endDate` 是 YYYYMMDD 字符串（非毫秒时间戳）**；完整字段（7个）：`tsCode`/`endDate`(YYYYMMDD)/`pledgeCount`(质押次数)/`unrestPledge`(无限售股质押, 万股)/`restPledge`(限售股质押, 万股)/`totalShare`(总股本, 万股)/`pledgeRatio`(⚠️ **质押比例%**，高于30%需关注平仓风险)

### `POST /openapi/v1/stock/financial/core` — 核心财务摘要（20 列）
form: `StockCoreFinancialsForm` (分页) · `{"tsCode": "600519.SH", "size": 8}`（仅 `tsCode` 必填，`size=8` 取近 2 年季报）。⚠️ **响应 `endDate` 是 YYYYMMDD 字符串（非毫秒！）**。完整字段（20个）：`tsCode`/`endDate`(YYYYMMDD)·[每股]`eps`(基本EPS)/`dtEps`(稀释EPS)/`bps`(每股净资产)/`ocfps`(每股经营现金流)·[盈利]`roe`(%)/`roeDt`(扣非ROE%)/`roa`(%)/`grossprofitMargin`(毛利率%)/`netprofitMargin`(净利率%)·[成长]`revenueYoy`(营收同比%)/`netprofitYoy`(净利同比%)/`dtNetprofitYoy`(扣非净利同比%)·[偿债]`currentRatio`(流动比率)/`quickRatio`(速动比率)/`debtToAssets`(资产负债率%)·[运营]`assetsTurn`(总资产周转率)/`arTurn`(应收账款周转率)/`ocfToOr`(经营现金流/营收比)

### `POST /openapi/v1/stock/financial/dividend` — 分红派息历史
form: `StockDividendForm` (分页) · `{"tsCode": "600519.SH"}`（仅 `tsCode` 必填）。⚠️ **响应所有日期字段均为 YYYYMMDD 字符串（非毫秒！）**。完整字段（12个）：`tsCode`/`endDate`(分红年度,YYYYMMDD)/`annDate`(公告日,YYYYMMDD)/`divProc`(⚠️ 实施进度："实施"/"完成"/"预案"/...)/`stkDiv`(每股送股,股)/`stkBoRate`(⚠️ **每股转增，不是"送股比"**,股)/`stkCoRate`(⚠️ **每股配股，不是"转增比"**,股)/`cashDiv`(每股分红税前,元)/`cashDivTax`(每股分红税后,元)/`recordDate`(股权登记日,YYYYMMDD)/`exDate`(除权除息日,YYYYMMDD)/`payDate`(派息日,YYYYMMDD)
> 📌 **覆盖语义**：库内 = 日增量公告 + 按需回填过的股票。某票返回空 ≠ 该公司从不分红，可能只是历史未回填——报告时说"库内暂无该股分红记录（可回填）"，不要说"该公司从不分红"

### `POST /openapi/v1/stock/financial/express` — 业绩快报（14 列）
form: `StockFinancialForm` (分页) · 同上。业绩快报 = 正式财报**前**的预披露，是判断超预期/不及预期的早期信号（通常早于年报/季报1-2个月）。⚠️ **响应 `annDate`/`endDate` 均为毫秒时间戳**；完整字段（14个）：`tsCode`/`annDate`(ms)/`endDate`(ms)/`revenue`(营业收入)/`operateProfit`(营业利润)/`totalProfit`(利润总额)/`nIncome`(⚠️ **归母净利润，大写I**)/`totalAssets`(总资产)/`totalHldrEqyExcMinInt`(归母股东权益)/`dilutedEps`(稀释EPS)/`dilutedRoe`(稀释ROE%)/`yoyNetProfit`(净利润同比%)/`bps`(每股净资产)/`yoySales`(营收同比%)

### `POST /openapi/v1/stock/financial/forecast` — 业绩预告（12 列）
form: `StockFinancialForm` (分页) · 同上。业绩预告 = 季度末后约30天内发布的未来业绩区间预测，是**事件驱动量化策略的高频信号源**。⚠️ **响应 `annDate`/`endDate`/`firstAnnDate` 均为毫秒时间戳**；完整字段（12个）：`tsCode`/`annDate`(ms)/`endDate`(ms)/`type`(⚠️ **预告类型**："预增"/"略增"/"续盈"/"扭亏"/"预减"/"略减"/"续亏"/"首亏"/"不确定")/`pChangeMin`(净利润变动下限%)/`pChangeMax`(净利润变动上限%)/`netProfitMin`(⚠️ **单位万元**，净利润预测下限)/`netProfitMax`(净利润预测上限, 万元)/`lastParentNet`(上年同期归母净利润, 万元)/`firstAnnDate`(ms, 首次公告日，修正公告时有值)/`summary`(变动原因摘要)/`changeReason`(变动原因详情)

### `POST /openapi/v1/stock/financial/disclosure-date` — 业绩披露日历（6 列）
form: `StockFinancialForm` (分页) · 同上。业绩披露日历 = 上市公司预约财报披露时间表，用于事件驱动策略的**时间维度预判**——"本周/本月有哪些公司即将披露财报"，可配合 `financial/express`（业绩快报）提前布局。⚠️ **响应所有日期字段均为毫秒时间戳**；完整字段（6个）：`tsCode`/`annDate`(ms, 最近公告日)/`endDate`(ms, 报告期，如2026-03-31=一季报)/`preDate`(ms, ⚠️ **预计披露日——策略核心字段**，按此排期监控)/`actualDate`(ms, 实际披露日，披露后才有值，null表示尚未披露)/`modifyDate`(ms, 预约日期修改时间，非null说明公司改过预约)

---

## 五、市场深度 / 龙虎榜 / 板块（Pro，scope 已拆分为 `stock.plate`/`stock.lhb`/`stock.moneyflow`/`stock.sentiment`；URL 前缀仍 `/stock/market/...`）

### `POST /openapi/v1/stock/market/moneyflow` — 个股资金流向
form: `StockMoneyFlowForm` (分页) · `{"tsCode": "600519.SH", "size": 60}`（仅 `tsCode` 必填）。⚠️ **响应 `tradeDate` 是 YYYYMMDD 字符串（非毫秒！）**。完整字段（14个）：`tsCode`/`tradeDate`(YYYYMMDD)·[万元] `buySmAmount`/`sellSmAmount`（散户小单）/`buyMdAmount`/`sellMdAmount`（中单）/`buyLgAmount`/`sellLgAmount`（大单）/`buyElgAmount`/`sellElgAmount`（超大单）/`netMfAmount`（全市场净流入）/`mainForceNetInflow`（主力净流入 = (buyLg+buyElg)-(sellLg+sellElg)，**已预计算**）/`retailNetInflow`（散户净流入 = -(mainForceNetInflow)）/`tradeCount`（成交笔数，Long类型非万元）。
⚠️ 与 `moneyflow-dc`（东财口径）的区别：**`moneyflow` 是原始买/卖分开**（可看各档净流向）；`moneyflow-dc` 是东财**净额**（buy*Amount 正=净买/负=净卖，无 sell 字段）。两套数据来源不同，主力判断逻辑可能不同。

### `POST /openapi/v1/stock/market/plate` — 全部板块涨跌幅快照
无 body（HttpServletRequest 直入）· 调用时 body 可省略或 `{}`
完整字段（25个）：tradeDate(ms)/tsCode/name/contentType/pctChange(%)/close/totalMv/turnoverRate(%)/upNum(Integer)/downNum(Integer)/netAmount/netAmountRate/buyElgAmount/buyElgAmountRate/buyLgAmount/buyLgAmountRate/buyMdAmount/buyMdAmountRate/buySmAmount/buySmAmountRate/buySmAmountStock(**⚠️ String，无数据时为 `"-"`，不是数字，禁止数值运算**)/rankNum(Integer)/leadingName/leadingCode/leadingPct(%，领涨股涨幅)。⚠️ 传 `type`/`tradeDate` 等字段**会被静默忽略**——要按类型/日期筛板块改用 `plate/list`

### `POST /openapi/v1/stock/market/plate/list` — 板块详情时间序列
form: `StockDcPlateListForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `type` | string | ✓ | 板块类型：`"概念"` / `"行业"` / `"地域"`。**这里是 `type` 不是 `contentType`** |
| `tradeDate` | string | – | 可空，默认最新交易日 |

完整字段（13个）：tradeDate(ms)/tsCode/name/contentType/pctChange(%)/close/totalMv/turnoverRate(%)/upNum(Integer)/downNum(Integer)/netAmount(万元)/netAmountRate(%)/rankNum(Integer)。**⚠️ 注意**：此端点用 `StockDcPlateModel`（仅13字段），**不含** `plate` 快照端点的 25 个字段（无 leadingName/buyElgAmount 等资金拆分字段）

### `POST /openapi/v1/stock/market/plate/cash-flow` — 板块资金榜
form: `StockDcPlateMarketCashFlowForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `contentType` | string | – | `"概念"` / `"行业"` / `"地域"`，不传默认 `"概念"` |
| `tsCode` | string | – | 板块代码（如 `"BK0475"`）。传了就只看这一个板块 |
| `tradeDate` | string | – | `YYYYMMDD`，可空 |
| `netInflowAndPctChangeGtZero` | bool | – | `true` 仅返回净流入且涨幅>0 的强势板块 |

完整字段（19个）：id(Long，内部主键)/tradeDate(ms)/contentType/tsCode/name/pctChange(%)/close/netAmount(万元)/netAmountRate(%)/buyElgAmount(特大单万元)/buyElgAmountRate(%)/buyLgAmount(大单万元)/buyLgAmountRate(%)/buyMdAmount(中单万元)/buyMdAmountRate(%)/buySmAmount(小单万元)/buySmAmountRate(%)/buySmAmountStock(**⚠️ String，无数据时为 `"-"`，不是数字**)/rankNum(Integer)；无 `leadingName` 字段

### `POST /openapi/v1/stock/market/plate/continue-net` — 板块连续净流入

> ℹ️ 本端点数据由 task 层每日采集生成，历史数据稀疏，当天 15:00 后刷新。

form: `StockDcPlateContinueNetAmountForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `continueNum` | int | ✓ | 连续天数。例 `5` = 找近 5 个交易日**每日都净流入**的板块。常用 `3` / `5` / `10` |
| `type` | string | ✓ | 板块类型：`"概念"` / `"行业"` / `"地域"` |

⚠ **此端点**最容易踩坑：旧文档写的是 `contentType, page, size`（**全部错误**）。实际字段只有 `continueNum` + `type`，且 form 不分页。**不要传 `trade_date` / `tradeDate` / `days`**——会被 Jackson 忽略，端点照默认值跑。⚠️ 响应 `lastDate` 是**毫秒时间戳**（非字符串）；`amount` = 连续净流入合计（元），`avgAmount` = 日均净流入（元）。

### `POST /openapi/v1/stock/market/plate/stocks-indicator` — 板块成分股估值快照
form: `StockDcPlateForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `code` | string | ✓ | 板块代码（东财口径），如 `"BK0475"`。**字段名是 `code` 不是 `tsCode`**；取自 `plate/list` 返回的 **`tsCode`** 字段（plate/list 没有名为 `code` 的字段） |
| `tradeDate` | string | ✓ | **`YYYY-MM-DD` 格式**（带横杠！），不是 YYYYMMDD——传紧凑格式会 code=1 系统异常。必填，不传返空。⚠️ 板块成分股数据按月更新，实测最新日期约滞后 1~2 个月（用 `plate/list` 返回的 `tradeDate` 字段取真实可用日期，转为 `YYYY-MM-DD` 格式传入） |

⚠️ **响应字段 25 个，与 `indicator/last/by-codes` 完全相同**（含 pe/peTtm/pb/ps/turnoverRate/circMv/roe/roeDate 等），且响应 `tradeDate` 是**毫秒时间戳**（输入用 YYYY-MM-DD，输出是毫秒，两个方向格式不同）

### `POST /openapi/v1/stock/market/plates-by-stock` — 个股所属板块反查
form: `StockPlatesByStockForm` (无分页) · `{"conCode": "600519.SH"}`
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `conCode` | string | ✓ | 成分股代码（constituent code）。**字段名是 `conCode` 不是 `tsCode`** |

完整字段（9个）：plateCode(**字段名是 `plateCode` 不是 `tsCode`**)/plateName(**字段名是 `plateName` 不是 `name`**)/contentType("行业"/"概念"/"地域")/pctChange(%)/close/totalMv(万元)/turnoverRate(%)/upNum(Integer)/downNum(Integer)。⚠️ 该端点**无 `tradeDate` 字段**；实测部分股票 `plateName` 为空字符串（数据覆盖不全），空结果不代表该股不属于任何板块

### `POST /openapi/v1/stock/market/lhb/latest-dates` — 最近 3 个龙虎榜日期
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可

### `POST /openapi/v1/stock/market/lhb/list` — 当日上榜清单
form: `StockLhbStockListForm` (无分页) · `{"tradeDate": "20260430"}`（必填）。`tradeDate` 兼容 `YYYYMMDD` / `YYYY-MM-DD` 两种写法——`latest-dates` 返回的横杠格式可直接回传。⚠️ 响应字段仅 3 个：`tsCode`/`name`/`pctChange`（无 buy/sell 等，席位明细需调 `lhb/details`）

### `POST /openapi/v1/stock/market/lhb/details` — 单股席位明细
form: `StockLhbDateForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tradeDate` | string | ✓ | 龙虎榜日 `YYYYMMDD` |
| `tsCode` | string | ✓ | 股票代码 |

完整字段（11个）：tsCode/tradeDate(ms)/exalter(席位名称：如"机构专用"/"中信证券...营业部"/"深股通专用")/buy(元)/buyRate(%)/sell(元)/sellRate(%)/netBuy(元，>0净买入 <0净卖出)/side(**⚠️ 字符串 `"B"`=买方/"S"=卖方，不是"0"/"1"！**)/reason(上榜原因：如"日涨幅偏离值达7%")/id(内部主键)

### 其他市场深度端点（scope 按类别：plate/lhb/moneyflow/sentiment；全部共用 `StockMarketQueryForm`，分页）

下列端点**全部**用同一个 form `StockMarketQueryForm`，业务字段都是 camelCase。各端点用其中一个子集，传无关字段会被忽略：

| 字段 | 类型 | 说明 |
|------|------|------|
| `tsCode` | string | 单只股票（cyq-perf / block-trade / auction-open / auction-close / ths-concept / moneyflow-dc 等） |
| `tradeDate` | string | 按日切片（hot-rank / limit-analysis / hsgt-top10 / kpl-list / mainboard / guba-rank） |
| `startDate`, `endDate` | string | 时间范围（block-trade / hsgt-moneyflow / moneyflow-dc / news-sentiment） |
| `nameKeyword` | string | 名称模糊匹配（hm-list 游资名 / kpl-list 概念名 / broker-trade 营业部） |
| `dataType` | string | 子分类标识，含义因端点而异：hot-rank `"1"` 股票热榜/`"2"` 板块；hsgt-top10 `"1"` 沪股通/`"2"` 深股通/`"3"` 港股通；cyq-perf `"D"`/`"W"`/`"M"`；**ths-hot 用中文标签**（`"热股"`/`"港股"`/`"行业板块"`/`"概念板块"`/`"期货"`/`"美股"`，不传 = 全类型返回） |
| `limitStat` | string | 涨跌停状态过滤（仅 limit-analysis）：`"U"` 涨停 / `"D"` 跌停 |

端点列表：

- `/openapi/v1/stock/market/hot-rank` — 东财热榜（dc_hot）⚠️ **底表暂无数据（返回 `data:[]`）**；热度类需求改用 `/ths-hot`（同花顺，数据更新）
- `/openapi/v1/stock/market/limit-analysis` — 涨跌停 / 连板分析（`tradeDate` YYYYMMDD 必填；`limitStat` "U"过滤涨停/"D"跌停。完整响应字段：`tsCode`/`name`/`industry`/`tradeDate`(YYYYMMDD字符串)/`close`/`pctChg`/`swing`(振幅，可null)/`amount`(成交额元)/`limitAmount`(封板额)/`floatMv`/`totalMv`/`turnoverRatio`/`fdAmount`(封单金额)/`firstTime`(⚠️ **"HHMMSS"无分隔符字符串**，如 `"93643"` = 9:36:43)/`lastTime`(同格式)/`openTimes`(开板次数)/`limitTimes`(涨跌停次数)/`upStat`("n/m" 连板格式，如 `"5/5"`)/`limitStat`("U"涨停/"D"跌停)；共19字段）
- `/openapi/v1/stock/market/block-trade` — 大宗交易（`tsCode` 必填；响应 `tradeDate` 是 YYYYMMDD 字符串；完整字段（7个）：`tsCode`/`tradeDate`(YYYYMMDD字符串)/`price`(成交价)/`vol`(⚠️ 成交量，单位：**万股**)/`amount`(⚠️ 成交金额，单位：**万元**)/`buyer`(买方营业部)/`seller`(卖方营业部)）
- `/openapi/v1/stock/market/auction-open` — 开盘集合竞价（`tsCode` 或 `tradeDate` 任意传）
- `/openapi/v1/stock/market/auction-close` — 收盘集合竞价（15:00 前无当日数据）
- `/openapi/v1/stock/market/cyq-perf` — 筹码胜率（`tsCode` 必填；`dataType` "D"日/"W"周/"M"月；响应 `tradeDate` YYYYMMDD 字符串。完整字段：`tsCode`/`tradeDate`/`hisLow`/`hisHigh`(历史极值)/`cost5pct`/`cost15pct`/`cost50pct`/`cost85pct`/`cost95pct`(5个分位成本价，共5个字段)/`weightAvg`(加权平均成本)/`winnerRate`(获利盘%，当前价高于该%的筹码即获利)；共11字段）
- `/openapi/v1/stock/market/hsgt-top10` — 沪深港通 top10（`tradeDate` YYYYMMDD 必填；响应 `tradeDate` 是 YYYYMMDD 字符串；`dataType` 请求过滤："1"沪股通/"2"深股通/"3"港股通。完整响应字段（11个）：`tsCode`/`name`/`tradeDate`(YYYYMMDD)/`rankNum`(1~10,int)/`marketType`(⚠️ **"1"=沪股通/"3"=深股通/"2"=港股通(沪)/"4"=港股通(深)**；与请求 dataType 枚举值不同！)/`close`/`chg`/`amount`/`netAmount`(买净额)/`buy`/`sell`；⚠️ **金额单位是元（不是万元！）**——`amount=3351828340` ≈ 33.5 亿元）
- `/openapi/v1/stock/market/hsgt-moneyflow` — 北向 / 南向资金净流入（无需 tradeDate，按最新返回）。字段（7个）：`tradeDate`(YYYYMMDD字符串)/`hgt`(沪股通,万元)/`sgt`(深股通,万元)/`ggtSs`(港股通沪,万元)/`ggtSz`(港股通深,万元)/`northMoney`(北向合计=hgt+sgt,万元)/`southMoney`(南向合计=ggtSs+ggtSz,万元)；⚠️ 金额单位均为万元）
- `/openapi/v1/stock/market/hm-list` — 游资名录（用 `nameKeyword` 模糊搜游资昵称，**不是 `name_keyword`**；不传返全部；完整字段（3个）：name/description/orgs(**⚠️ JSON字符串数组**——需 JSON.parse 解析，不是普通字符串，格式如 `"[\"中信证券...营业部\"]"`)）
- `/openapi/v1/stock/market/kpl-list` — 开盘啦榜单（`tradeDate` 传 YYYYMMDD；响应 `tradeDate` 是字符串。完整字段：`tsCode`/`name`/`tradeDate` + `luTime` 涨停时间 / `ldTime` 炸板时间 / `openTime` 开板时间 / `lastTime` 最后涨停时间 / `status` "首板"/"N连板" / `theme` 主题概念 / `luDesc` 涨停原因 / `netChange` 封板资金净额 / `bidAmount` 竞价封板金额 / `upDays` 连板天数 / `tag` 涨停或跌停）
- `/openapi/v1/stock/market/ths-concept` — 同花顺概念。tsCode = 概念代码（如 `885589.TI`），dataType 承载成分股代码
- `/openapi/v1/stock/market/moneyflow-dc` — 个股东财口径资金流（`tsCode` 必填）。字段（15个）：`tsCode`/`tradeDate`(YYYYMMDD)/`name`/`pctChange`/`close`/`netAmount`(全日净流入万元，正=净买)/`netAmountRate`(%)/`buyElgAmount`(超大单≥100万净流入)/`buyElgAmountRate`(%)/`buyLgAmount`(大单20~100万)/`buyLgAmountRate`(%)/`buyMdAmount`(中单4~20万)/`buyMdAmountRate`(%)/`buySmAmount`(小单<4万)/`buySmAmountRate`(%)；⚠️ 与 `moneyflow`（标准口径）区别：**`moneyflow-dc` 只有净额**（无分开的 sell 字段），`moneyflow` 有原始 buy/sell 双份）
- `/openapi/v1/stock/market/mainboard` — 大盘整体行情（`tradeDate` 或 `startDate`/`endDate` 至少传一个；⚠️ 响应 `tradeDate` 是 **YYYYMMDD 字符串**（非毫秒！）；完整字段（15个）：`tradeDate`(YYYYMMDD)/`closeSh`(上证收盘)/`pctChangeSh`(上证涨跌%)/`closeSz`(深证收盘)/`pctChangeSz`(深证涨跌%)/`netAmount`(⚠️ **单位：亿元**，不是元)/`netAmountRate`(%)/`buyElgAmount`(超大单净买亿元)/`buyElgAmountRate`(%)/`buyLgAmount`(大单净买亿元)/`buyLgAmountRate`(%)/`buyMdAmount`(中单净买亿元)/`buyMdAmountRate`(%)/`buySmAmount`(小单净买亿元)/`buySmAmountRate`(%)；适合"今天大盘整体资金流向怎样"类问题）
- `/openapi/v1/stock/market/ths-hot` — **同花顺 App 热榜（推荐，数据最新）**。`dataType` 用中文标签过滤：`"热股"` A股热股 / `"港股"` / `"行业板块"` / `"概念板块"` / `"期货"` / `"美股"`；不传返全类型。无需传 tradeDate，默认最新。完整响应字段：`tradeDate`(⚠️ **毫秒时间戳**，展示需 ÷1000 转秒) / `dataType` 热榜类型 / `tsCode` / `tsName` / `rank` 排名 / `pctChange` 涨跌幅 / `currentPrice` 现价 / `concept`(JSON 字符串数组，含概念标签) / `hot` 热度值 / `rankTime`(**"YYYY-MM-DD HH:mm:ss" 字符串**，直接用于时间标注) / `rankReason`(可为 null)
- `/openapi/v1/stock/market/guba-rank` — 东财股吧排名 ⚠️ 数据暂未生成（底表空，返回 `data:null`）；热度类需求优先用 `/ths-hot`（同花顺，更全）
- `/openapi/v1/stock/market/news-sentiment` — 新闻日度情绪聚合（完整字段（8个）：`tradeDate`(YYYYMMDD 字符串，⚠️ 非毫秒)/`totalNewsCount`/`positiveCount`/`negativeCount`/`avgSentimentScore`（-1~1，0 为中性）/`newsVolumeMa5`（5日均量）/`newsSurgeRatio`（量比）/`srcDiversity`（来源多样性，Integer）；可用于"今天市场情绪如何"判断）
- `/openapi/v1/stock/market/institution-trading` — 机构买卖明细（`tradeDate` YYYYMMDD；完整字段（9个）：`tradeDate`(YYYYMMDD)/`tsCode`/`buy`/`buyRate`/`sell`/`sellRate`/`netBuy`/`side`（**1=买方机构/2=卖方机构**）/`reason` 龙虎榜入选原因）
- `/openapi/v1/stock/market/broker-trade` — 龙虎榜券商营业部明细（`tradeDate` YYYYMMDD 或 `nameKeyword` 模糊搜营业部名；完整字段（10个）：`tradeDate`(YYYYMMDD)/`tsCode`/`exalter` 营业部名称/`buy`/`buyRate`/`sell`/`sellRate`/`netBuy`/`side`（**1=买方营业部/2=卖方营业部**）/`reason` 入选原因）

### `GET /openapi/v1/stock/market/volume-breakout` — 实时放量上涨突破信号
⚠ 唯一 GET 端点，无 body。直接 `GET ${BASE_URL}/openapi/v1/stock/market/volume-breakout`，仍需 `Authorization: Bearer ${TOKEN}` Header。

---

## 六、股东（stock.shareholder — Plus）

### `POST /openapi/v1/stock/shareholder/holder/find-stocks` — 反查持仓股票列表
form: `FindStocksByHoldersForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `holders` | string[] | ✓ | 股东名列表（中文）。**多名是交集**——返回"每个股东都持有"的票（不是并集）；**LIKE 模糊匹配**，可写简称（如 `"中央汇金"` 可命中全称）。例 `["社保基金", "中央汇金"]` = 两者共同持仓 |
| `endDate` | string | ✅ | **事实必填**：报告期**下界**（`end_date >= endDate`，不是"截止日"）。查最新持仓传最近季末日（如 `"20260331"`）；想看更久历史传更早日期。不传 = 参数错误（code=2） |

⚠️ **响应字段是股票基础信息（不只是 tsCode！）**：返回与 `basic/detail` 相同的 19 个字段，包括 `tsCode`/`name`/`area`/`industry`/`market`/`listDate`（毫秒）/`listDateStr`（YYYYMMDD）/`isHs`/`actName`/`actEntType`/`enName`/`fullName` 等——可直接获取股票基本属性，无需再调 `basic/detail`。注意：**不含 pe/pb/换手率** 等估值字段，需估值仍需再调 `indicator/last/by-codes`

### `POST /openapi/v1/stock/shareholder/holder/holdings` — 单股东持仓明细
form: `SelectShareholderByHolderForm` (无分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `holder` | string | ✓ | 股东名（中文，**精确匹配全称**，与 find-stocks 的模糊匹配不同）。支持英文逗号分隔多个（并集）。**字段名是 `holder` 不是 `holderName`** |
| `endDate` | string | ✅ | **事实必填**：报告期**下界**（`end_date >= endDate`）。不传 = 参数错误（code=2） |
| `calAvgPrice` | int | – | `0` 不算均价（默认）/ `1` 计算均价 |

⚠️ 响应 `annDate`/`endDate` 是 **"YYYY-MM-DD" 带横杠字符串**（如 `"2026-03-31"`），不是毫秒也不是 YYYYMMDD——跨端点对比日期时需转换格式。完整字段（12个）：`tsCode`/`tsCodeName`(股票中文简称)/`holderName`(股东全称)/`annDate`("YYYY-MM-DD"字符串)/`endDate`("YYYY-MM-DD"字符串) · 持仓：`holdAmount`(持股数量，万股，⚠️字符串非数字)/`holdRatio`(占总股本%)/`holdFloatRatio`(占流通股%)/`holdChange`(变动万股，正=增持/负=减持/空串=首次进入或退出，⚠️字符串) · 标签：`holderType`(⚠️代码：`"G"`=国资/`"P"`=个人/`"C"`=公司/`"F"`=境外)/`holderCategory`(中文细分，如"社保"/"公募基金"/"QFII")/`averagePrice`(均价元，仅当`calAvgPrice=1`时有值)

> 💡 组合用法：先 `find-stocks`（简称模糊）反查票池 → 再 `holdings`（**全称**精确）拿持仓明细；全称可从 find-stocks 结果或 `classify/list` 字典获得。2026-06-07 前老服务端这两个端点曾因 PG 迁移全挂（code=1 系统异常），已修复。

### `POST /openapi/v1/stock/shareholder/classify/list` — 股东类别字典
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可

> ⚠️ 底表 `stock_shareholder_classify` 暂无数据（PG 迁移后未回填），返回 `data:[]`。股东类型信息可从 `/holder/find-stocks` 或 `/holder/holdings` 返回的 `holderCategory`/`holderType` 字段取。

---

## 七、选股模型（stock.selection — Ultra）

### `POST /openapi/v1/stock/selection/ml/results` — ML 集成选股结果
form: `MlSelectionForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tradeDate` | string | ✅ | 选股交易日 `YYYYMMDD`。**事实必填**：后端 SQL 精确等值匹配，不传 = 必空（无"默认最新"）。先 `lhb/latest-dates` 拿最近交易日；空结果回退前一交易日 |
| `signalType` | string | – | `"BUY"` / `"HOLD"` / `"WATCH"`，可空。**字段名是 `signalType` 不是 `signal_type`** |
| `minScore` | number | – | 最低 ML 得分 `0.0`–`1.0`。**字段名是 `minScore` 不是 `min_score`** |

### `POST /openapi/v1/stock/selection/ml/execute` — 触发 ML 选股（异步）
form: `MlSelectionForm` (分页) · 仅读 `tradeDate` 字段；⚠ 重负载

### `POST /openapi/v1/stock/selection/momentum/results` — 动量选股结果
form: `MomentumSelectionForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tradeDate` | string | ✅ | `YYYYMMDD`。**事实必填**（同 ml/results：不传 = 必空），拿最新日期方法同上 |
| `minScore` | number | – | 最低综合得分 |
| `minConceptCount` | int | – | 最少概念叠加数（如 `3` 表示叠加 ≥ 3 个热门概念）。**字段名是 `minConceptCount` 不是 `min_concept_count`** |

### `POST /openapi/v1/stock/selection/momentum/execute` — 触发动量选股
form: `MomentumSelectionForm` (分页) · 仅读 `tradeDate`

### `POST /openapi/v1/stock/selection/value/results` — 价值选股结果
form: `ValueSelectionForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tradeDate` | string | ✅ | `YYYYMMDD`。**事实必填**（同 ml/results：不传 = 必空），拿最新日期方法同上 |
| `l1Code` | string | – | 申万一级行业代码（如 `"801080"` 电子）。**字段名是 `l1Code` 不是 `l1_code`** |
| `minScore` | number | – | 最低综合得分 |

### `POST /openapi/v1/stock/selection/value/execute` — 触发价值选股
form: `ValueSelectionForm` (分页) · 仅读 `tradeDate`

---

## 八、指数（stock.index — Plus）

> ⚠️ **stock/index 系所有时序端点响应日期均为毫秒时间戳**（kline/daily、kline/weekly、kline/monthly、dailybasic、weight、sw-industry-quo、main/snapshot 等的 `tradeDate` 字段）——输入 `startDate`/`endDate` 仍是 YYYYMMDD。
> ⚠️ **例外**：`stock/kline/index-minute`（分钟K）的响应日期字段名是 **`tradeTime`**（不是 `tradeDate`），值同样是毫秒时间戳。

### `POST /openapi/v1/stock/index/list` — 指数列表筛选
form: `StockIndexInfoForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | – | 精确指数代码（如 `"000300.SH"`） |
| `nameKeyword` | string | – | 名称模糊匹配（如 `"300"` / `"新能源"`）。**注意 `nameKeyword`** |
| `market` | string | – | `"SSE"` / `"SZSE"` / `"CSI"` / `"SW"` / `"MSCI"` |
| `indexType` | string | – | `"综合"` / `"规模"` / `"行业"` / `"风格"` / `"主题"` / `"策略"` |
| `category` | string | – | 风格细分（"价值" / "成长" / "高股息"） |
| `publisher` | string | – | 发布机构（"中证" / "申万" / "国证" / "上证" / "深证"） |

响应字段（13个）：`tsCode`/`name`/`fullname`/`market`/`publisher`/`indexType`(可为 null)/`category`/`baseDate`(⚠️ **YYYYMMDD 字符串，非毫秒戳**)/`basePoint`(基点数值，如 1000.0)/`listDate`(⚠️ **YYYYMMDD 字符串**)/`weightRule`/`dsc`(简介)/`expDate`(到期日，可为 null)

### `POST /openapi/v1/stock/index/kline/daily` — 指数日 K
form: `StockIndexKlineForm` (分页) · 字段：`tsCode`(必填) + `startDate` + `endDate`
响应字段（11个）：`tsCode`/`tradeDate`(⚠️ **毫秒时间戳，同章节说明**)/`open`/`high`/`low`/`close`/`preClose`/`chg`/`pctChg`/`vol`/`amount`
⚠️ **部分指数（如 `000300.SH`）可能因 PG 数据迁移返回空列表，改用 `000001.SH` 或 `399001.SZ` 验证**

### `POST /openapi/v1/stock/index/kline/minutes` — 指数分钟 K
form: `StockIndexKlineForm` (分页) · `tsCode` 必填
⚠️ **字段与日 K 不同**：响应字段（8个）：`tsCode`/`tradeTime`(⚠️ **字段名是 `tradeTime` 不是 `tradeDate`**，值为毫秒时间戳)/`open`/`high`/`low`/`close`/`vol`(⚠️ **可为 null**)/`amount`。**无** `preClose`/`chg`/`pctChg`

### `POST /openapi/v1/stock/index/sw-industry-quo` — 申万行业日 K + 估值
form: `StockIndexKlineForm` (分页) · `tsCode` 是申万行业代码（如 `"801010.SI"` 农林牧渔）。⚠️ **tsCode 必填，不传返空**（见反模式）。
响应字段（15个）：`tsCode`/`tradeDate`(ms)/`name`/`open`/`high`/`low`/`close`/`chg`/`pctChg`/`vol`/`amount`/`pe`/`pb`/`floatMv`(流通市值)/`totalMv`(总市值)/`weight`(权重，可为 null)

### `POST /openapi/v1/stock/index/main/snapshot` — 主要指数最新快照
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可
响应字段（12个）：`tsCode`/`name`/`tradeDate`(ms)/`close`/`open`/`high`/`low`/`preClose`/`chg`/`pctChg`/`vol`/`amount`

### `POST /openapi/v1/stock/index/main/history` — 主要指数历史 K 线序列
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可
⚠️ **响应结构特殊**：`data` 是 **4 个数组的数组**（每个元素是一条指数的历史序列），而非扁平列表。每条记录 12 字段：`tsCode`/`name`/`tradeDate`(ms)/`close`/`open`/`high`/`low`/`preClose`/`chg`/`pctChg`/`vol`/`amount`

### `POST /openapi/v1/stock/index/sw-heatmap` — 申万一级行业热力图
form: `OpenApiBaseForm`（无业务字段）· body `{}` 即可
⚠️ **当前返回空列表**（PG 数据迁移缺口，暂无可用数据）

---

## 九、基金 / ETF（fund — Max）

### `POST /openapi/v1/fund/etf/list` — ETF 列表
form: `FundListForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | – | ETF 代码（如 `"510300.SH"`） |
| `nameKeyword` | string | – | 名称模糊匹配。**注意 camelCase** |
| `fundType` | string | – | `"股票型"` / `"混合型"` / `"债券型"` 等 |
| `status` | string | – | `"D"` 存续 / `"I"` 发行中 / `"L"` 已上市 / `"S"` 已终止 |
| `market` | string | – | `"E"` 场内 / `"O"` 场外 |
| `exchange` | string | – | `"SH"` / `"SZ"` / `"BSE"`（⚠️ 用短形式，`"SSE"`/`"SZSE"` 无效返回 0 条） |
| `indexCode` | string | – | 跟踪指数代码（如 `"000300.SH"` 找跟踪沪深 300 的全部 ETF） |

完整字段（17个）：`tsCode`/`csName`(⚠️ ETF中文名，非简称)/`extName`(扩展名)/`cName`(⚠️ **简称，字段名大写N，不是`cname`**)/`indexCode`/`indexName`(跟踪指数名)/`setupDate`(成立日 YYYYMMDD)/`listDate`(上市日 YYYYMMDD)/`listStatus`("L"上市/"D"退市)/`exchange`("SH"/"SZ")/`mgrName`(管理人)/`custodName`(托管行)/`mgtFee`(管理费率)/`etfType`("纯境内"/"港股通"/"商品"/"货币"/"REITs"等)/`baseDate`(指数基期 YYYYMMDD)/`basePoint`(指数基点)/`publisher`(指数发布机构)

### `POST /openapi/v1/fund/list` — 公募基金列表
form: `FundListForm` (分页) · 同上字段（`indexCode` 不适用，`managerName` 一般不传）

响应字段（25 个）：`tsCode`/`name`/`management`(管理公司)/`custodian`(托管行)/`fundType`(如"债券型"/"混合型")/`foundDate`(成立日 YYYYMMDD)/`dueDate`(到期日，nullable)/`listDate`(上市日，nullable，**场外基金通常为 null**)/`issueDate`(发行日 YYYYMMDD)/`delistDate`(退市日，nullable)/`issueAmount`(发行规模，数据不全常为 0.0)/`durationYear`(存续年限，常为 0.0)/`minAmount`(最低申购额，常为 0.0)/`expReturn`(预期收益，常为 0.0)/`benchmark`(业绩基准描述)/`status`("L"存续/"D"退市)/`investType`(投资方向，如"灵活配置型")/`type`(基金类型，如"契约型开放式")/`trustee`(受托人，nullable)/`purcStartdate`(申购开始日 YYYYMMDD)/`redmStartdate`(赎回开始日 YYYYMMDD)/`market`("O"场外/"E"场内)/`mfee`(管理费率%)/`cfee`(托管费率%)/`pvalue`(面值，通常 1.0)
⚠️ 与 ETF list 字段集**完全不同**：此端点无 `indexCode`/`mgtFee`/`etfType`/`publisher`/`exchange`/`csName` 等 ETF 特有字段；日期字段均为 **YYYYMMDD 字符串**（不是毫秒时间戳）

### `POST /openapi/v1/fund/manager/list` — 基金经理列表
form: `FundListForm` (分页) · `tsCode` 与 `managerName` 至少一个必填
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | △ | 仅传 → 该基金的所有经理 |
| `managerName` | string | △ | 仅传 → 该经理管的所有基金。**字段名是 `managerName` 不是 `manager_name`** |

完整字段（10个）：`tsCode`/`annDate`(公告日 YYYYMMDD)/`name`(经理姓名)/`gender`("M"/"F")/`birthYear`/`edu`(学历，如"硕士")/`nationality`/`beginDate`(任职开始日 YYYYMMDD)/`endDate`(离任日 YYYYMMDD，在任为**空字符串**而非null)/`resume`(简历长文本)

### `POST /openapi/v1/fund/etf/kline/daily` — ETF 日 K + 复权因子
form: `FundDateRangeForm` (分页) · `{"tsCode": "510300.SH", "startDate": "20260101", "endDate": "20260430"}`。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段（12个）：`tsCode`/`tradeDate`(ms)/`open`/`high`/`low`/`close`/`preClose`/`chg`/`pctChg`/`vol`(⚠️ **成交量，单位：手，非万！**)/`amount`(⚠️ **成交额，单位：元，非万元！**)/`adjFactor`(复权因子，可空)

### `POST /openapi/v1/fund/etf/share-history` — ETF 份额历史
form: `FundDateRangeForm` (分页) · 字段同上。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段（8个）：`tsCode`/`tradeDate`(ms)/`etfName`(ETF名称)/`totalShare`(⚠️ **总份额，单位：份，非万份！**)/`totalSize`(⚠️ **总规模，单位：元，非万元！**)/`nav`(单位净值)/`close`(收盘价)/`exchange`

### `POST /openapi/v1/fund/nav/history` — 基金净值历史
form: `FundDateRangeForm` (分页) · 字段同上。完整字段（9个）：`tsCode`/`annDate`(公告日 YYYYMMDD)/`navDate`(净值日 YYYYMMDD)/`unitNav`(单位净值)/`accumNav`(累计净值)/`accumDiv`(累计分红)/`adjNav`(复权净值)/`netAsset`(资产净值元)/`totalNetasset`(合计净值元)；⚠️ `netAsset`/`totalNetasset` 常为 0（Tushare 不连续更新）；日期均为 YYYYMMDD 字符串

### `POST /openapi/v1/fund/dividend` — 基金分红
form: `FundDateRangeForm` (分页) · `tsCode` 必填。⚠️ 响应所有日期字段均为 YYYYMMDD 字符串（非毫秒）。完整字段（16个）：`tsCode`/`annDate`(公告日)/`impAnndate`(⚠️ **分红实施公告日，字段名小写d**)/`baseDate`(分红基准日)/`divProc`(进度，如"实施"/"预案")/`recordDate`(权益登记日)/`exDate`(除息日)/`payDate`(派息日)/`earpayDate`(⚠️ **收益支付日，字段名小写p，不是`earPayDate`**)/`netExDate`(净值除权日)/`divCash`(每份分红,元)/`baseUnit`(基准份额)/`earDistr`(已分配收益,元)/`earAmount`(分红总额,元)/`accountDate`(入账日)/`baseYear`(分红年度，如"2023"/"2024上半年")

### `POST /openapi/v1/fund/share/history` — 公募基金份额历史
form: `FundDateRangeForm` (分页) · `tsCode` + `startDate`/`endDate`。⚠️ 实际响应字段仅 3 个：`tsCode`/`tradeDate`(YYYYMMDD 字符串)/`fdShare`(份额，单位万份)；不含净值/规模等字段（净值用 `/fund/nav/history`）

### `POST /openapi/v1/fund/portfolio` — 基金前十大重仓股
form: `FundPortfolioForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 基金代码（如 `"110011.OF"` 易方达蓝筹；ETF 用 `"159919.SZ"` 等） |
| `endDate` | string | – | 报告期截止日 `YYYYMMDD`（季末日），不传默认最新已披露报告期 |

完整字段（8个）：`tsCode`(基金代码)/`annDate`(公告日 YYYYMMDD)/`endDate`(报告期截止日 YYYYMMDD)/`symbol`(持仓股票代码，如 `"300750.SZ"`)/`mkv`(持仓市值，单位：元)/`amount`(持仓量，单位：股)/`stkMkvRatio`(占基金净值比例%)/`stkFloatRatio`(占流通股比例%)

---

## 十、新闻 / 宏观（宏观 market — Pro；新闻 news — Max，已拆独立 scope）

### `POST /openapi/v1/market/news/list` — 站内新闻列表
form: `MarketNewsForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `type` | int | – | 新闻分类 ID（整数，实测常为 null；**不传不等于过滤掉 null**——不传 = 全量返回；不确定时省略） |
| `titleKeyword` | string | – | 标题模糊匹配。**字段名是 `titleKeyword` 不是 `title_keyword` 或 `q`** |
| `startDate` | string | – | `YYYYMMDD`，按 news_time 过滤 |
| `endDate` | string | – | `YYYYMMDD` |

完整响应字段（8 个）：`id`（Long）/`newsTime`（毫秒时间戳）/`newsTimeStr`（可读字符串如 `"2026-06-07 22:12:08"`，展示优先用这个）/`title`（可能 null）/`channels`（频道 CSV）/`src`（来源代码，如 "sina"/"cls"/"wallstreetcn"）/`type`（整数，可能 null，与请求 type 对应）/`score`（评分字符串）。⚠️ `title` 可能为 null；展示时以 `newsTimeStr` 优先。

### `POST /openapi/v1/market/news/types` — 新闻来源字典
无 body（HttpServletRequest 直入）· body 可省略或 `{}`。⚠️ **返回的是来源（source）字典，字段 `code`/`displayName`/`description`，`code` 匹配 `news/list` 响应中的 `src` 字段**（如 "sina"/"cls"/"eastmoney"），并非 `type` 整数值的字典。

### 宏观端点（共用 `MacroDateRangeForm`，分页）

下列宏观端点接受 `startDate` + `endDate`（日期范围）和/或 `page`/`size`（分页），日期格式因端点而异（详见下表）。不传日期 + `size=12` 即取最近 12 期，是 WF-3.7 宏观扫描的用法。

| 字段 | 类型 | 说明 |
|------|------|------|
| `startDate` | string | 月度端点：`YYYYMM`；季度端点：`YYYYQX`；日度端点：`YYYYMMDD`；可空 |
| `endDate` | string | 同上，可空 |
| `page` | int | 分页页码（默认 1） |
| `size` | int | 每页条数（默认 24，上限 100） |

| 端点 | 日期格式 | 响应关键字段 |
|------|---------|------|
| `/openapi/v1/market/macro/cpi` | `YYYYMM` | `month`(YYYYMM) + `ntVal`/`ntYoy`/`ntMom`/`ntAccu` 全国 + `townVal`/`townYoy`/`townMom`/`townAccu` 城市 + `cntVal`/`cntYoy`/`cntMom`/`cntAccu` 农村（`nt`=全国/`town`=城市/`cnt`=农村，`*Val`=值/`*Yoy`=同比/`*Mom`=环比/`*Accu`=累计） |
| `/openapi/v1/market/macro/ppi` | `YYYYMM` | `month`(YYYYMM) + `ppiYoy`/`ppiMom`/`ppiAccu` 总体 + `ppiMpYoy`(生产资料)/`ppiMpQmYoy`(采矿)/`ppiMpRmYoy`(原材料)/`ppiMpPYoy`(加工业) + `ppiCgYoy`(生活资料)/`ppiCgFYoy`(食品)/`ppiCgCYoy`(衣着)/`ppiCgAduYoy`(一般日用)/`ppiCgDcgYoy`(耐用消费品) |
| `/openapi/v1/market/macro/pmi` | `YYYYMM` | `month`(YYYYMM) + **数值型编码字段**：`pmi010000`(制造业综合)/`pmi010100`(生产)/`pmi010200`(新订单)/`pmi010300`(新出口)/`pmi020100`(大型企业)/`pmi020200`(中型)/`pmi020300`(小型)/`pmi030000`(非制造业综合) 等约 30+ 字段（均为数值，可直接读）；⚠️ 字段名是数字编码而非语义名 |
| `/openapi/v1/market/macro/gdp` | `YYYYQX`（如 `"2026Q1"`） | `quarter`(YYYYQX) + `gdp`/`gdpYoy`/`pi`/`piYoy`(第一产业)/`si`/`siYoy`(第二产业)/`ti`/`tiYoy`(第三产业)（单位：亿元） |
| `/openapi/v1/market/macro/money-supply` | `YYYYMM` | `month`(YYYYMM) + `m0`/`m0Yoy`/`m0Mom` + `m1`/`m1Yoy`/`m1Mom` + `m2`/`m2Yoy`/`m2Mom`（含环比 `*Mom`，单位：亿元） |
| `/openapi/v1/market/macro/social-finance` | `YYYYMM` | `month`(YYYYMM) + `incMonth`(社融增量本月)/`incCumval`(社融累计)/`rmbLoan`(人民币贷款)/`fxLoan`(外币贷款)/`entTrust`(委托贷款)/`entBill`(未贴现汇票)/`unbFinance`(未贴现银行承兑汇票)/`corpBond`(企业债券)/`nonFinStock`(非金融企业股票)/`govBond`(政府债券)（单位：亿元；多项可能为 null） |
| `/openapi/v1/market/macro/shibor` | `YYYYMMDD` | `date`(YYYYMMDD,**非 tradeDate**) + `onRate`(隔夜)/`w1`(1周)/`w2`(2周)/`m1`(1月)/`m3`/`m6`/`m9`/`y1`(1年) |
| `/openapi/v1/market/macro/lpr` | `YYYYMMDD` | `date`(YYYYMMDD,**非 tradeDate**) + `y1`(**1年期 LPR**)/`y5`(**5年期 LPR**)；⚠️ 字段名是 `y1`/`y5`，不是 `lpr1y`/`lpr5y` |
| `/openapi/v1/market/macro/monthly` | `YYYYMM` | `month`(YYYYMM) + 多宏观指标聚合（含 gdp/cpi/ppi/m2/社融等） |

---

## 十一、衍生品（derivative — Max）

### `POST /openapi/v1/derivative/futures/list` — 期货合约列表
form: `DerivativeListForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | – | 精确合约代码（如 `"CU2412.SHF"`） |
| `nameKeyword` | string | – | 名称模糊匹配 |
| `exchange` | string | – | `"CFFEX"` / `"SHFE"` / `"DCE"` / `"CZCE"` / `"INE"` / `"GFEX"` |
| `futCode` | string | – | 期货品种代码不带后缀（如 `"CU"` / `"AU"` / `"RB"`）。**字段名是 `futCode` 不是 `fut_code`** |
| `listStatus` | string | – | `"L"` 上市 / `"D"` 退市 / `"P"` 暂停 |

### `POST /openapi/v1/derivative/sge/list` — 上海黄金交易所产品列表
form: `DerivativeListForm` (分页) · 字段同上（`futCode` 不适用）

### `POST /openapi/v1/derivative/option/contracts` — 期权合约列表
form: `OptionContractQueryForm` (分页)

> **覆盖范围（2026-06 起全交易所，不再只有 ETF）**：ETF 期权（SSE/SZSE）+ 股指·国债期权（CFFEX：中证1000 MO / 沪深300 IO / 上证50 HO）+ 商品·能源期权（SHFE 铜金橡胶 / DCE 豆粕铁矿 / CZCE 白糖PTA / INE 原油 / GFEX 工业硅碳酸锂），共 **8 个交易所、2500+ 标的、21 万+ 合约**。

| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | – | 期权代码，**标的码或合约码均可**（服务端自动识别）。**标的码**→ 返回该标的全部在挂期权：ETF 用 ETF 码(`"510050.SH"` 50ETF)、股指用指数码(`"000852.SH"` 中证1000)、商品用期货合约码(`"JM2704.DCE"` 焦煤2704)；**合约码**(如 `"10011254.SH"` / `"MO2608-C-7500.CFX"`)→ 精确取该一张合约 |
| `optCodes` | string[] | – | 多标的批量，标的码带 `OP` 前缀。ETF `["OP510050.SH"]`、股指 `["OP000852.SH"]`、商品 `["OPJM2704.DCE","OPY2705.DCE"]`（= `OP`+期货合约码）。**单标的用上面的 `tsCode` 更省事** |
| `exchanges` | string[] | – | 交易所列表，8 选若干：`"SSE"`/`"SZSE"`(ETF) · `"CFFEX"`(股指/国债) · `"SHFE"`/`"DCE"`/`"CZCE"`/`"INE"`/`"GFEX"`(商品/能源)。例 `["DCE"]` = 大商所全部商品期权 |
| `dates` | string[] | – | 到期**月份** `YYYYMM`（**不是 YYYYMMDD**！）。例 `["202606"]`。不传=只返「到期月 ≥ 当前月」的在挂合约 |

> ✅ 「50ETF 期权」`{"tsCode":"510050.SH"}`；「中证1000股指期权」`{"tsCode":"000852.SH"}`；「大商所商品期权全量」`{"exchanges":["DCE"]}` 再自己筛品种。
> ⚠️ K 线端点（`option/kline/daily`、`option/kline/minutes`）的 `tsCode` 只认**合约**码（`"10011254.SH"` / `"MO2608-C-7500.CFX"` / `"Y2705-C-8400.DCE"`），不认标的码。
> ⚠️ **响应日期字段格式**：`sMonthDate` 是 **"yyyy-MM" 带横杠字符串**（如 `"2026-06"`，⚠️ 非 YYYYMM！）；`maturityDate`/`listDate`/`delistDate`/`lastEdate`/`lastDdate` 均是 **"YYYY-MM-DD" 带横杠字符串**；`callPut` 是定长空格补齐（`"C    "` / `"P    "`），**过滤前必须 trim()**；完整字段（18个）：`tsCode`/`exchange`(交易所)/`opName`(合约名)/`optCode`(=`"OP"+标的码`)/`optType`(品种类型)/`callPut`(认购/认沽，需trim)/`exerciseType`(行权类型)/`exercisePrice`(行权价)/`sMonthDate`(到期月份 "yyyy-MM")/`maturityDate`(到期日 "yyyy-MM-dd")/`listPrice`(挂牌基准价)/`listDate`(上市日 "yyyy-MM-dd")/`delistDate`(摘牌日 "yyyy-MM-dd")/`lastEdate`(最后行权日 "yyyy-MM-dd")/`lastDdate`(最后交易日 "yyyy-MM-dd")/`perUnit`(合约单位)/`quoteUnit`(报价单位)/`minPriceChg`(最小价格变动)

#### 🔑 带「具体日期 + 价格条件」的期权筛选 → 走**日 K 线**，不是本合约列表
合约列表（本端点）只有合约的**静态元数据**（行权价 / 到期日 / call-put / 合约单位），**没有任何某一天的价格**。
凡是问到「**某天的**最低 / 最高 / 开盘 / 收盘 / 结算 / 涨跌幅」或「按某日价格排序 / 跨日比较」的需求，一律查**期权日 K 线**——**问句里带日期 = 查日 K**，这是判断信号。**两条路，先看是单标的还是全市场：**

**A. 单一标的 / 少量合约**（如「50ETF 6 月某档期权」）→ `option/kline/daily`（单合约，必传 `tsCode` 合约码）：
1. `option/contracts` 圈合约拿每张 `tsCode`（合约码）。
2. 对每个 `tsCode` 调 `option/kline/daily`（`tsCode` + `startDate`/`endDate` `YYYYMMDD`），拿每日 `open/high/low/close/settle/preSettle/vol/oi`。

**B. 全市场 / 跨标的筛选**（如「**所有**期权里 6/3 最低÷6/2 收盘≤50% 的」）→ `option/kline/daily-by-date`（按交易日整拉全市场，**不要逐合约调几万次**）：
1. **按「交易所 × 日期」整拉**：`option/kline/daily-by-date`，传 `startDate`（**必填**；单日传 `startDate=endDate`）+ 可选 `exchange` 收窄。**单页上限 100 行**，用 `page=1,2,3…` 翻页直到返回空。要哪几天就各拉一次（如 6/2 一组、6/3 一组）。
2. **agent 侧跨日 join + 条件 + 排序**：把同一 `tsCode` 不同日的价格对齐，算比值 / 过滤 / 排序后输出（端点不做跨日逻辑）。
3. ⚠️ 排除「当天没成交」的假信号：某合约某天没交易时 `low/open/high=0`、`vol=0`——做比值前先剔掉 `low=0` 或 `vol=0` 的行，否则会把"没交易"误当成"暴跌到 0"。

> **期权 K 线字段三陷阱（跨日筛选前必看）**：
> - `tradeDate` 返回是**毫秒时间戳 long**（如 `1780329600000`），**不是 `"20260602"` 字符串**——跨日对齐按毫秒比对或先转换，别拿它做字符串 equals。
> - 未成交合约**也有行**：`open/high/low/vol/amount=0` 但 `close/settle` 仍是结算价（见上）。
> - `option/contracts` 的 `callPut` 是**定长空格补齐**（`"C    "` / `"P    "`），按认购/认沽过滤要先 `trim` 或前缀匹配，别 `== "C"`。

> 例：「找 6月3日最低价 ÷ 6月2日收盘价 ≤ 50%、且 6月2日最低价 > 10 的期权，按合约代码列最高/最低价」——
> ① 按交易所循环：`daily-by-date {"startDate":"20260602","exchange":"DCE","page":N}` 翻页拉 6/2 全量、再拉 6/3；商品期权价格高(>10)，主要落在 SHFE/DCE/CZCE/INE/GFEX。
> ② 按 `tsCode` 把 6/2、6/3 对齐 → 取 6/2 `close`、6/2 `low`、6/3 `low`，剔除 `low_0603=0` 的没成交行，按 `low_0603 / close_0602 ≤ 0.5 且 low_0602 > 10` 过滤，按 `tsCode` 排序输出。
> （这类"全市场扫一遍再筛"的活数据量大，能直接让后端跑就别让 agent 翻几百页——量大时建议加 `exchange` 逐所收窄。）

### 期货 / 期权 / SGE K 线 + 持仓 + 仓单 + 涨跌停（共用 `DerivativeDateRangeForm`，分页）

| 字段 | 类型 | 说明 |
|------|------|------|
| `tsCode` | string | 合约代码（K 线类用）。例 `"CU2412.SHF"` / `"10006281.SH"` / `"Au9999.SGE"` / `"CU.SHF"` 主力连续 |
| `symbol` | string | 期货品种代码不带后缀（`holding` / `wsr` 端点用）。例 `"CU"` |
| `startDate`, `endDate` | string | `YYYYMMDD` |
| `freq` | string | 周期：`"W"` / `"M"`（仅 `weekly-monthly` 端点用） |

端点列表：

- `/openapi/v1/derivative/futures/kline/daily` — 期货日 K（用 `tsCode`，如 `"CU.SHF"` 主力连续）。⚠️ `tradeDate` 是**毫秒时间戳**；完整字段（16个）：`tsCode`/`tradeDate`(ms) · 价格：`preClose`/`preSettle`(前结算)/`open`/`high`/`low`/`close`/`settle`(当日结算)/`change1`(close-preClose)/`change2`(settle-preSettle) · 成交：`vol`(手)/`amount`(万元) · 持仓：`oi`(手)/`oiChg`(手)/`delvSettle`(交割结算价)
- `/openapi/v1/derivative/futures/kline/weekly-monthly` — 期货周 / 月 K（`tsCode` + `freq`=`W`或`M`，均必填；当前库内该表数据稀疏，部分合约可能返空）
- `/openapi/v1/derivative/futures/kline/minutes` — 期货分钟 K（用 `tsCode`）
- `/openapi/v1/derivative/futures/holding` — 期货会员持仓（**用 `symbol` 不是 `tsCode`**，如 `"CU"`；⚠️ `tradeDate` 是**毫秒时间戳**；完整字段（10个）：`tradeDate`(ms)/`symbol`/`broker` · 成交：`vol`(⚠️成交量，单位：**手**)/`volChg`(成交量增减，手) · 持仓：`longHld`(多头持仓)/`longChg`(多头变化)/`shortHld`(空头持仓)/`shortChg`(空头变化)/`exchange`）
- `/openapi/v1/derivative/futures/wsr` — 期货仓单（**用 `symbol`**，如 `"CU"`；⚠️ `tradeDate` 是**毫秒时间戳**；完整字段（17个）：`tradeDate`(ms)/`symbol`(品种代码，入参回显) · 仓单：`futName`(品种名称)/`warehouse`(仓库名)/`whId`(仓库ID)/`preVol`(昨日仓单量)/`vol`(当日仓单量)/`volChg`(变化) · 属性：`area`(地区)/`year`/`grade`(等级)/`brand`(品牌)/`place`(产地)/`pd`(升贴水，Integer)/`isCt`(是否完税)/`unit`(单位)/`exchange`）
- `/openapi/v1/derivative/futures/main-contract` — 主力连续合约映射（用 `tsCode`，如 `"CU.SHF"`；⚠️ `tradeDate` 是**毫秒时间戳**；完整字段（3个）：`tsCode`(连续合约代码)/`tradeDate`(ms)/`mappingTsCode`(⚠️ 当日实际合约代码，如 `"CU2607.SHF"`——回测时用于把连续合约换算为真实合约)）
- `/openapi/v1/derivative/futures/settle` — 期货结算费用 + 保证金率（用 `tsCode`；⚠️ `tradeDate` 是 **YYYYMMDD 字符串**，与 `kline/daily` 的毫秒格式不同；完整字段（11个）：`tsCode`/`tradeDate`(YYYYMMDD)/`exchange` · 结算：`settle`(结算价)/`tradingFeeRate`(交易手续费率万分比)/`tradingFee`(元/手)/`deliveryFee`(交割手续费元/手)/`offsetTodayFee`(平今手续费元/手) · 保证金率：`longMarginRate`(多头投机)/`shortMarginRate`(空头投机)/`bHedgingMarginRate`(⚠️大写H，多头套保；旧文档误写 `bhedgingMarginRate`)/`sHedgingMarginRate`(⚠️大写H，空头套保；旧文档误写 `shedgingMarginRate`)）
- `/openapi/v1/derivative/futures/limit` — 期货合约每日涨跌停（用 `tsCode`；⚠️ `tradeDate` 是 **YYYYMMDD 字符串**，与 `kline/daily` 的毫秒不同；完整字段（7个）：`tsCode`/`tradeDate`(YYYYMMDD) · 价格：`preClose`(前收)/`preSettle`(前结算)/`upLimit`(涨停价)/`downLimit`(跌停价)/`marginRate`(保证金率)）
- `/openapi/v1/derivative/option/kline/daily` — 期权日 K（**单合约**，用 `tsCode`，如 `"10006281.SH"`）
- `/openapi/v1/derivative/option/kline/daily-by-date` — 期权日 K（**全市场**，按交易日不限合约：`startDate` 必填 + 可选 `exchange`，分页 100/页）。用于「某日全部期权按价格条件筛选 / 排序」，免逐合约调几万次
- `/openapi/v1/derivative/option/kline/minutes` — 期权分钟 K（用 `tsCode`）。⚠ **按需入库**：合约 5000+，分钟数据只对管理员手动回填过的合约存在，**空结果先判"该合约未回填"而非"无行情/接口坏了"**；需要时让用户联系管理员触发 `OptionMinutesTask`（参数 tsCode+日期区间），回填后即查即得
- `/openapi/v1/derivative/sge/kline/daily` — 上金所日 K（用 `tsCode`，如 `"Au(T+D)"` / `"Au99.99"` / `"Ag(T+D)"`；⚠️ 路径是 `sge/kline/daily` 不是 `sge/daily`；⚠️ `tradeDate` 是**毫秒时间戳**；完整字段（14个）：`tsCode`/`tradeDate`(ms) · OHLC：`open`/`high`/`low`/`close` · 特有：`priceAvg`(加权均价，元/克) · 涨跌：`chg`/`pctChange` · 成交：`vol`(千克)/`amount`(元)/`oi`(持仓量，千克) · 递延：`settleVol`(递延补偿成交量)/`settleDire`(**"B"**=多头补偿/**"S"**=空头补偿)）

---

## 十二、债券 / 可转债（bond — Max）

### `POST /openapi/v1/bond/cb/list` — 可转债列表
form: `BondListForm` (分页)
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | – | 可转债代码（如 `"113008.SH"` / `"123100.SZ"`） |
| `stkCode` | string | – | 正股代码（找正股是茅台的转债 → `"600519.SH"`）。**字段名是 `stkCode` 不是 `stk_code`** |
| `nameKeyword` | string | – | 简称模糊匹配 |
| `issueRating` | string | – | 信用评级 `"AAA"` / `"AA+"` / `"AA"` / `"AA-"` 等 |

响应字段（15 个）：`tsCode`/`bondFullName`(全称)/`bondShortName`(简称)/`stkCode`(正股代码)/`stkShortName`(正股简称)/`maturity`(存续年限，float)/`par`(面值，通常 100.0)/`issuePrice`(发行价)/`issueSize`(发行规模，**单位：元**)/`listDate`(上市日 **YYYYMMDD 字符串**，非ms)/`delistDate`(退市日 **YYYYMMDD 字符串**)/`convPrice`(当前转股价格，元/股)/`maturityDate`(到期日 **YYYYMMDD 字符串**)/`couponRate`(票面利率%)/`issueRating`(信用评级，nullable)
⚠️ 所有日期均为 **YYYYMMDD 字符串**（不是毫秒时间戳）；`issueSize` 单位是元（不是亿），如 `6000000000.0` = 60亿

### 单只债券时间序列（共用 `BondDateRangeForm`，分页）

| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 债券代码 |
| `startDate` | string | – | `YYYYMMDD` |
| `endDate` | string | – | `YYYYMMDD` |

端点列表：

- `/openapi/v1/bond/cb/daily` — 转债日 K + 转股溢价率 + 纯债溢价率（缺日期默认最近 60 天）。⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）**；端点在线可用但暂无可查询数据。预期字段：`tradeDate`(YYYYMMDD 字符串)/`tsCode`/`close`/`pctChg`/`bondValue`(纯债价值)/`bondOverRate`(纯债溢价率%)/`cbValue`(转股价值)/`cbOverRate`(转股溢价率%)——转债评估核心 4 指标
- `/openapi/v1/bond/cb/factor` — 转债技术因子（含 JSONB 动态因子）。⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）**
- `/openapi/v1/bond/cb/issue` — 转债发行（中签率等）。⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）**
- `/openapi/v1/bond/cb/call` — 转债强赎 / 回售。⚠️ **2026-06-08 实测 `data:[]`，底表暂无数据（PG 迁移缺口）**
- `/openapi/v1/bond/cb/rate` — 转债票面利率分档（各年利率阶梯；`tsCode` 必填）。日期均为 **YYYYMMDD 字符串**。字段（5个）：`tsCode`/`rateFreq`(付息频率，int，1=每年)/`rateStartDate`(YYYYMMDD)/`rateEndDate`(YYYYMMDD)/`couponRate`(票面利率%，如 0.2=0.2%)
- `/openapi/v1/bond/cb/price-chg` — 转股价变动（下修历史；`tsCode` 必填）。日期均为 **YYYYMMDD 字符串**。字段（7个）：`tsCode`/`bondShortName`(转债简称)/`publishDate`(YYYYMMDD 公告日)/`changeDate`(YYYYMMDD 变更执行日)/`convertPriceInitial`(初始转股价)/`convertpriceBef`(变更前转股价)/`convertpriceAft`(变更后转股价)。⚠️ **字段名陷阱**：`convertpriceBef`/`convertpriceAft` 中 `price` 全小写（不是 `convertPriceBef`！），与同端点的 `convertPriceInitial`（大写 P）命名不一致，容易写错
- `/openapi/v1/bond/cb/share` — 转股进度（⚠️ `publishDate`/`endDate` 是 **"YYYY-MM-DD" 带横杠字符串**；无 `tradeDate` 字段；camelCase 字段：`convertPriceInitial`/`convertPrice`/`convertVal`/`convertVol`/`convertRatio`/`accConvertVal`/`accConvertVol`/`accConvertRatio`（累计转股比例%）/`remainSize`（剩余规模）/`totalShares`；⚠️ 旧文档错写的 `acc_convert_ratio`/`remain_size` 是 snake_case，实际是 camelCase）
- `/openapi/v1/bond/repo/daily` — 国债逆回购日行情（如 `"204001.SH"` GC001；完整字段（12个）：`tsCode`/`tradeDate`(YYYYMMDD)/`repoMaturity`(品种名，如 `"GC001"`/`"GC007"` 等)/`preClose`/`open`/`high`/`low`/`close`/`weight`(加权平均价)/`weightR`(加权平均利率%)/`amount`(成交额，⚠️ **单位：千元**，不是万元)/`num`(成交笔数，Integer)）

### 横截面 / 收益率曲线 / 大宗（共用 `BondMarketForm`，分页）

| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tradeDate` | string | ✓ | **必填** 单日 `YYYYMMDD`（不传 size 内无日期过滤会返空）；或传 `startDate`/`endDate` 区间二选一 |
| `startDate` | string | – | 区间起始（与 `tradeDate` 二选一）|
| `endDate` | string | – | 区间结束 |
| `tsCode` | string | – | 债券代码（可选过滤单只） |
| `curveType` | string | – | 仅 `/yc`：`"0"` 到期收益率（最常用）/ `"1"` 即期 |
| `curveTerm` | string | – | 仅 `/yc`：期限（年）`"0.25"` / `"1"` / `"5"` / `"10"`。空 = 全期限曲线 |

端点列表：

- `/openapi/v1/bond/yc` — 国债收益率曲线（⚠️ 必须传日期 `tradeDate` 或 `startDate`/`endDate`，否则无过滤全库返空）。日期均为 **YYYYMMDD 字符串**。字段（6个）：`tradeDate`(YYYYMMDD)/`tsCode`(曲线代码，当前仅 `"1001.CB"` = 中债国债收益率曲线)/`curveName`(曲线全名)/`curveType`(类型，**字符串**，不是整数；`"0"`=到期收益率 / `"1"`=即期收益率)/`curveTerm`(期限年数，浮点，如 0.08=1个月/0.5=6个月/1.0=1年，当前范围 0.0~4.5)/`yieldRate`(收益率%，如 1.30=1.30%)。单日请求返 50 个期限点（全曲线快照），跨区间 + 固定 `curveTerm` 可做利率走势对比
- `/openapi/v1/bond/blk` — 转债大宗交易日汇总（`tsCode` 可选过滤，`tradeDate` 必填或用 `startDate`/`endDate`）。日期均为 **YYYYMMDD 字符串**。字段（6个）：`tradeDate`(YYYYMMDD)/`tsCode`/`name`(转债简称)/`price`(成交价)/`vol`(成交量，单位：**手**)/`amount`(成交额，单位：**万元**)
- `/openapi/v1/bond/blk-detail` — 转债大宗交易逐笔明细（每笔含买卖方营业部全名）。日期均为 **YYYYMMDD 字符串**。字段（8个）：`tradeDate`(YYYYMMDD)/`tsCode`/`name`(转债简称)/`price`(成交价)/`vol`(手)/`amount`(万元)/`buyDp`(买方营业部全名，长字符串)/`sellDp`(卖方营业部全名，长字符串)

---

## 十三、Token 自查（无 scope 要求）

### `POST /openapi/v1/whoami` — Token / 套餐 / scope 自查
无 body · 任何合法 token 都能调（仍校验 token / IP / 频率，但跳过 scope 校验）

完整字段（10个）：ownerName/tokenPrefix(脱敏前缀)/tier("FREE"/"PRO"/"MAX"/"ADMIN"/"CUSTOM")/tierLabel(套餐中文名)/scopes(**List\<String\>**，scope列表，通配符已展开)/adminWildcard(bool，是否含"\*")/rateLimitPerMin(int)/allowedPaths(路径白名单CSV，null=仅scope控制)/clientIp/llmHint(给LLM的中文权限说明，可直接拼入system prompt)

**用途**：每次进入新会话第一步调用此端点，知道当前 token 的 tier / scope / 频率上限，避免越权调用拿 403。

---

## 十四、港股（stock.hk — Max）

所有端点 form 均为 `HkQueryForm`（继承 `OpenApiPageForm`，**支持 `page`/`size`**）。日期 `startDate`/`endDate` 一律 `YYYYMMDD`；分钟端点改用 `startTime`/`endTime`（`YYYY-MM-DD HH:mm:ss`，**注意带 `-`、`:` 与空格，和其它端点的纯 `YYYYMMDD` 不同**）。tsCode 形如 `"00700.HK"`。

`HkQueryForm` 全字段一览（各端点用其中一个子集，传无关字段会被忽略）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `tsCode` | string | 港股代码，如 `"00700.HK"`。K 线 / 分钟 / 复权因子 / 三大表 / 财务指标**必填**；basic / tradecal 可空 |
| `startDate` | string | `YYYYMMDD`，可空 |
| `endDate` | string | `YYYYMMDD`，可空 |
| `startTime` | string | `YYYY-MM-DD HH:mm:ss`，**仅 minute 端点用** |
| `endTime` | string | `YYYY-MM-DD HH:mm:ss`，**仅 minute 端点用** |
| `freq` | string | 分钟频率 `"1min"` / `"5min"` / `"15min"` / `"30min"` / `"60min"`，**仅 minute 端点用**，默认 `"60min"` |
| `reportType` | string | **仅 fina-indicator 端点用**，精确等值匹配。值是带年份的完整报告期串，如 `"2024年中报"` / `"2023年年报"`（港股只有年报 / 中报，无季报）。⚠️ **不要**传 `"中报"` / `"年报"`（不带年份匹配不到，返回空）；不确定就别传 |
| `listStatus` | string | **仅 basic 端点用**：`"L"` 上市 / `"D"` 退市 / `"P"` 暂停。可空 |

### `POST /openapi/v1/stock/hk/basic` — 港股基础信息
form: `HkQueryForm` (分页) · `tsCode` 可空（不传列全市场），可选 `listStatus` 过滤。完整字段（12个）：tsCode/name(中文名)/fullname(全称)/enname(英文名)/cnSpell/market("主板"/创业板)/listStatus("L"上市/"D"退市/"P"暂停)/listDate(⚠️ **毫秒时间戳字符串**，如 `"1087315200000"`)/delistDate(⚠️ 退市则为毫秒字符串，**未退市为字符串 `"None"` 而非 null！**)/tradeUnit(交易单位字符串，如 `"100.0"`)/isin/currType("HKD"/"USD"等)

### `POST /openapi/v1/stock/hk/tradecal` — 港股交易日历
form: `HkQueryForm` (分页) · 判断港股是否交易日 / 算上一·下一交易日；`startDate` / `endDate` 可空。⚠️ **响应日期字段名是 `calDate`（不是 `tradeDate`！）** = **毫秒时间戳**；同时有 `pretradeDate`（上一交易日，也是毫秒）和 `isOpen`（1=交易日/0=非交易日）

### `POST /openapi/v1/stock/hk/kline` — 港股日 K 线（不复权）
form: `HkQueryForm` (分页) · `tsCode` **必填**。跨除权日比价请改用 `/kline-adj` 或配合 `/adj-factor` 自行换算。⚠️ 响应 `tradeDate` 是**毫秒时间戳**；完整字段（11个）：`tsCode`/`tradeDate`(ms)/`open`/`high`/`low`/`close`/`preClose`/`change`/`pctChg`/`vol`(⚠️ 成交量，单位：**股**，非万手)/`amount`(⚠️ 成交额，单位：**港元**)

### `POST /openapi/v1/stock/hk/kline-adj` — 港股日 K 线（复权 + 估值快照）
form: `HkQueryForm` (分页) · `tsCode` **必填**。⚠️ 响应 `tradeDate` 是**毫秒时间戳**；完整字段（18个）：`tsCode`/`tradeDate`(ms)/`close`/`open`/`high`/`low`/`preClose`/`change`/`pctChange`(⚠️ adj端点用`pctChange`，kline端点用`pctChg`)/`vol`(⚠️ 成交量，单位：**股**)/`amount`(⚠️ 成交额，单位：**港元**)/`vwap`(成交均价)/`adjFactor`(复权因子)/`turnoverRatio`(换手率%)/`freeShare`(流通股本，股)/`totalShare`(总股本，股)/`freeMv`(流通市值)/`totalMv`(总市值)

### `POST /openapi/v1/stock/hk/adj-factor` — 港股复权因子
form: `HkQueryForm` (分页) · `tsCode` **必填**。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段（4个）：tsCode/tradeDate(ms)/cumAdjfactor(**注意：港股/美股用 `cumAdjfactor`，A股用 `adjFactor`，字段名不同！**)/closePrice。用法：`HFQ_price = BFQ_price × cumAdjfactor / 当日最新 cumAdjfactor`

### `POST /openapi/v1/stock/hk/minute` — 港股分钟 K 线
form: `HkQueryForm` (分页) · `tsCode` **必填**。时间范围用 `startTime` / `endTime`（`YYYY-MM-DD HH:mm:ss`），`freq` 默认 `"60min"`
| 字段 | 类型 | 必填 | 说明 |
|------|------|----|------|
| `tsCode` | string | ✓ | 港股代码 |
| `freq` | string | – | `"1min"` / `"5min"` / `"15min"` / `"30min"` / `"60min"`（默认 `"60min"`） |
| `startTime` | string | – | `YYYY-MM-DD HH:mm:ss`（**不是 `YYYYMMDD`**） |
| `endTime` | string | – | `YYYY-MM-DD HH:mm:ss` |

### `POST /openapi/v1/stock/hk/income` — 港股利润表（long format）
form: `HkQueryForm` (分页) · `tsCode` **必填**。每行一个 `indName` → `indValue` 键值对，客户端自行透视成宽表

> **Long format 透视关键**：响应字段 `{tsCode, endDate, name, indName, indValue}`；`endDate` 是**毫秒时间戳 long**（与期权 tradeDate 一致，与美股 endDate 字符串相反）。按 `(endDate, indName)` pivot 得宽表。
> 覆盖范围：库内覆盖前 100 港股（按代码字母序）；00700.HK（腾讯）等旗舰可按需通过 `/run` 触发单只回填。数据量大，建议配合 `size` 分页使用。

### `POST /openapi/v1/stock/hk/balance-sheet` — 港股资产负债表（long format）
form: `HkQueryForm` (分页) · `tsCode` **必填**。同上 long format，透视键相同 `(endDate, indName)`

### `POST /openapi/v1/stock/hk/cash-flow` — 港股现金流量表（long format）
form: `HkQueryForm` (分页) · `tsCode` **必填**。同上 long format，透视键相同 `(endDate, indName)`

### `POST /openapi/v1/stock/hk/fina-indicator` — 港股财务指标（36 列）
form: `HkQueryForm` (分页) · `tsCode` **必填**；`reportType` 可选过滤（值用完整报告期串如 `"2024年中报"`）。⚠️ `endDate` 是**毫秒时间戳**；完整字段（36个）：`tsCode`/`name`(股票中文名)/`endDate`(ms)/`reportType`(年报/中报/季报)/`orgType`(行业分类)/`currency` · 每股：`bps`(净资产)/`basicEps`/`dilutedEps`/`perOi`(每股营业收入)/`perNetcashOperate`(每股经营现金流)/`epsTtm` · 盈利：`operateIncome`/`operateIncomeYoy`/`grossProfit`/`grossProfitRatio`/`netProfitRatio`/`holderProfit`/`holderProfitYoy` · 回报：`roeAvg`/`roeYearly`/`roicYearly`/`roa` · 现金流：`netcashOperate`/`netcashInvest`/`netcashFinance`/`endCash` · 资产负债：`totalAssets`/`totalLiabilities`/`debtAssetRatio`/`currentRatio` · 估值：`dividendRate`/`diviRatio`/`totalMarketCap`/`peTtm`/`pbTtm`

⚠️ 港股通持股（`stock_hk_hold`）**不在本 scope**，在 `stock.shareholder` scope 的 `/openapi/v1/stock/shareholder/hk-hold` 下。

> ℹ️ A/H 股比价（`stock_ah_comparison`）数据已入库，**暂无 OpenAPI 端点**；需要 A/H 溢价率时可通过 `/stock/hk/kline-adj`（港股）和 `/stock/kline/daily`（A 股）各取收盘价后自行计算。

---

## 十五、美股（stock.us — Max）

所有端点 form 均为 `UsQueryForm`（继承 `OpenApiPageForm`，**支持 `page`/`size`**）。日期 `startDate`/`endDate` 一律 `YYYYMMDD`。tsCode 是**裸 ticker**（`"AAPL"` / `"JPM"`），**无 `.O`/`.N` 后缀**（带后缀静默返空）；股份类别码保留原生点号（`"BRK.A"` / `"BF.B"`）。

`UsQueryForm` 全字段一览：

| 字段 | 类型 | 说明 |
|------|------|------|
| `tsCode` | string | 美股代码=裸 ticker，如 `"AAPL"` / `"MSFT"` / `"JPM"`（**无交易所后缀**）。K 线 / 复权因子 / 三大表 / 财务指标**必填**；basic / tradecal 可空 |
| `startDate` | string | `YYYYMMDD`，可空 |
| `endDate` | string | `YYYYMMDD`，可空 |
| `reportType` | string | **仅 fina-indicator 端点用**，精确等值匹配。值是东财口径完整报告期串，如 `"2025/Q1"` / `"2023/FY"`（`FY`=年报，`Q1/Q2/...`=季度累计）。⚠️ **不要**传 `"A"` / `"S1"` / `"Q1"` 这种纯代码（匹配不到，返回空）；不确定就别传 |
| `classify` | string | **仅 basic 端点用**：`"ADR"` / `"GDR"` / `"EQ"`。可空 |
| `listStatus` | string | basic 端点字段位（`"L"`/`"D"`/`"P"`），但**美股 us_basic 表无该列，basic 端点忽略**——保留仅为 form 一致性 |

### `POST /openapi/v1/stock/us/basic` — 美股基础信息
form: `UsQueryForm` (分页) · `tsCode` 可空（不传列全市场），可选 `classify` 过滤。完整字段（6个）：tsCode(如 `"AAPL.O"`)/name(⚠️ 中文名，**多数美股为字符串 `"None"` 而非真名称，实际名称用 `enname`**)/enname(英文名，如 `"APPLE"`)/classify("EQ"/"ADR"/"GDR"等)/listDate(⚠️ **毫秒时间戳字符串**)/delistDate(⚠️ **未退市为字符串 `"None"` 而非 null！**)

### `POST /openapi/v1/stock/us/tradecal` — 美股交易日历
form: `UsQueryForm` (分页) · 判断美股是否交易日 / 算上一·下一交易日；`startDate` / `endDate` 可空。⚠️ **响应字段名是 `calDate`（不是 `tradeDate`！）** = **毫秒时间戳**；`pretradeDate` 也是毫秒；`isOpen` = 1/0

### `POST /openapi/v1/stock/us/kline` — 美股日 K 线（不复权 + 估值快照）
form: `UsQueryForm` (分页) · `tsCode` **必填**。跨除权日比价请改用 `/kline-adj`。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段（16个）：tsCode/tradeDate(ms) · OHLC：open/high/low/close · preClose/change/pctChange · 成交：vol/amount · vwap(均价)/turnoverRatio(%)/totalMv · pe(市盈率)/pb(市净率)（含估值，一站式）

### `POST /openapi/v1/stock/us/kline-adj` — 美股日 K 线（复权 + 估值快照）
form: `UsQueryForm` (分页) · `tsCode` **必填**。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段（19个）：tsCode/tradeDate(ms) · OHLC：open/high/low/close · preClose/change/pctChange · 成交：vol/amount · vwap(均价)/adjFactor(复权因子)/turnoverRatio(%) · 股本：freeShare(流通)/totalShare(总) · 市值：freeMv(流通)/totalMv(总) · exchange("NAS"纳斯达克/"NYS"纽交所/"OTC")（⚠️ 无 pe/pb，需估值改用不复权的 `/kline`）

### `POST /openapi/v1/stock/us/adj-factor` — 美股复权因子
form: `UsQueryForm` (分页) · `tsCode` **必填**。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段（5个）：tsCode/tradeDate(ms)/exchange("NAS"/"NYS"/"OTC")/cumAdjfactor(**⚠️ 用 `cumAdjfactor`，不是 `adjFactor`！同港股**)/closePrice。用法：`HFQ_price = BFQ_price × cumAdjfactor / 当日最新 cumAdjfactor`

### `POST /openapi/v1/stock/us/income` — 美股利润表（long format）
form: `UsQueryForm` (分页) · `tsCode` **必填**。每行一个 `(indType, indName)` → `indValue` 键值对，客户端自行透视成宽表

> **Long format 透视关键**：响应字段 `{tsCode, endDate, indType, name, indName, indValue, reportType}`；⚠️ 美股 `endDate` 是**毫秒时间戳 integer**（实测 `1774627200000`，与港股 `endDate` 格式相同，**不是**字符串 "2024-12-31 00:00:00"——旧文档有误）。透视键 `(endDate, indType, indName)`，`indType` = 报告期标识（如 `"Q2"` `"Q4"` `"TTM"`）。

### `POST /openapi/v1/stock/us/balance-sheet` — 美股资产负债表（long format）
form: `UsQueryForm` (分页) · `tsCode` **必填**。同上 long format

### `POST /openapi/v1/stock/us/cash-flow` — 美股现金流量表（long format）
form: `UsQueryForm` (分页) · `tsCode` **必填**。同上 long format

### `POST /openapi/v1/stock/us/fina-indicator` — 美股财务指标（29 列）
form: `UsQueryForm` (分页) · `tsCode` **必填**。`reportType` 可选过滤（值用 `"2025/Q1"` / `"2023/FY"` 形式）；⚠️ `endDate` 是**毫秒时间戳**。完整字段（29个）：`tsCode`/`securityNameAbbr`(证券简称)/`endDate`(ms)/`reportType`/`indType`/`accountingStandards`/`currency` · 收入：`operateIncome`/`operateIncomeYoy`/`grossProfit`/`grossProfitYoy`/`parentHolderNetprofit`/`parentHolderNetprofitYoy`/`totalIncome` · 每股：`basicEps`/`dilutedEps`/`basicEpsYoy` · 比率：`grossProfitRatio`/`netProfitRatio`/`roeAvg`/`roa`/`debtAssetRatio`/`currentRatio`/`speedRatio`/`equityRatio` · 周转率：`totalAssetsTr`/`inventoryTr`/`accountsReceTr` · 分红：`payoutRatio`

---

## 十六、研报 / 卖方评级（stock.research — Plus）

所有端点 form 均为 `ResearchQueryForm`（继承 `OpenApiPageForm`，**支持 `page`/`size`**）。三端点 `tsCode` 均可空（行业 / 策略级研报 ts_code 为空串）。日期 `startDate`/`endDate` 一律 `YYYYMMDD`。

`ResearchQueryForm` 全字段一览：

| 字段 | 类型 | 说明 |
|------|------|------|
| `tsCode` | string | 股票代码带后缀，如 `"600519.SH"`。三端点均可空（不传按日期范围 / 月度返回） |
| `startDate` | string | `YYYYMMDD`，可空。broker-recommend 会自动截前 6 位转 `YYYYMM` 与 DB 的 `month` 列比对 |
| `endDate` | string | `YYYYMMDD`，可空 |
| `org` | string | 机构 / 券商名称过滤。可空。（report-rc 响应中对应字段是 `orgName`、broker-recommend 对应 `broker`、report 对应 `instCsname`） |
| `rating` | string | 评级过滤，**仅 report-rc 端点用**：如 `"买入"` / `"增持"` / `"中性"`。可空 |

### `POST /openapi/v1/stock/research/report` — 券商研究报告（含行业级研报）
form: `ResearchQueryForm` (分页) · `tsCode` 可空。按 `tradeDate DESC` 返回最新研报在前。⚠️ 响应 `tradeDate` 是**毫秒时间戳**。完整字段：`tsCode`/`name`(股票中文名)/`tradeDate`(ms)/`title`（报告文件名）/`abstr`（摘要长文本，可能数千字）/`reportType`（"个股研报"/"行业研报"）/`author`(分析师姓名)/`instCsname`（机构简称）/`indName`(行业名)/`url`（PDF 直链）

### `POST /openapi/v1/stock/research/report-rc` — 券商盈利预测 + 评级 + 目标价
form: `ResearchQueryForm` (分页) · `tsCode` 可空，`rating` 可选过滤。⚠️ 响应日期字段名是 **`reportDate`**（毫秒时间戳，非 `tradeDate`）；`createTime` 为字符串。完整字段（23 个）：`tsCode`/`name`/`reportDate`(ms)/`createTime`(字符串)/`reportTitle`/`reportType`/`classify`/`orgName`（机构名）/`authorName`/`quarter`/`opRt` 营收/`opPr` 利润/`tp`/`np`/`eps`/`pe`/`rd`/`roe`/`evEbitda`/`rating`/`maxPrice`/`minPrice`/`impDg` 评级变化。按 `reportDate DESC` 返回最近预测在前

> ⚠️ 数据覆盖：库内仅 ~170 只股票有记录（polling 每日增量采集，存量取决于 Tushare 权限）。旗舰标的（600519/000858 等）实测无数据；`tsCode` 不限制时按全库返回，限制到无记录股票则返回 `[]`。

### `POST /openapi/v1/stock/research/broker-recommend` — 券商月度金股推荐
form: `ResearchQueryForm` (分页) · `tsCode` 可空，`org` 按券商名过滤。`startDate`/`endDate` 自动截前 6 位转 `YYYYMM` 与 DB 的 `month` 列比对。响应字段只有 4 个：`month`（YYYYMM 字符串）/`broker`/`tsCode`/`name`，无 tradeDate/毫秒戳问题。按 `month DESC` 返回最近月份在前

---

## 十七、国际宏观（stock.intl-macro — Max）

所有端点 form 均为 `IntlMacroQueryForm`（继承 `OpenApiPageForm`，**支持 `page`/`size`**）。**所有业务字段均可空**——不传则按日期范围 / 默认窗口返回。日期 `startDate`/`endDate` 一律 `YYYYMMDD`。**注意路径前缀是 `/openapi/v1/intl-macro/...`（不带 `stock/`）**。
⚠️ **响应日期字段名为 `date`（不是 `tradeDate`），值是毫秒时间戳**（如 `1780588800000`）——9 个端点全部如此，展示时需转换。

`IntlMacroQueryForm` 全字段一览（仅 3 个字段，所有端点共用）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `startDate` | string | `YYYYMMDD`，可空 |
| `endDate` | string | `YYYYMMDD`，可空 |
| `currType` | string | **仅 libor 端点用**：`"USD"` / `"EUR"` / `"JPY"` / `"GBP"` / `"CHF"`，可空（默认 USD）。其它端点传了会被忽略 |

9 个端点（除 libor 外都只用 `startDate` / `endDate`）；**所有端点响应字段 `date` 均为毫秒时间戳**：

| 端点 | 关键响应字段 |
|------|------|
| `/openapi/v1/intl-macro/us-tycr` | `m1`/`m2`/`m3`/`m4`/`m6`/`y1`/`y2`/`y3`/`y5`/`y7`/`y10`/`y20`/`y30`（13 期限，单位 %）。算期限利差：`y10-m3` / `y10-y2` |
| `/openapi/v1/intl-macro/us-trycr` | `y5`/`y7`/`y10`/`y20`/`y30`（TIPS 实际收益率，5 期限）。与 us-tycr 同期限相减 ≈ 隐含通胀 |
| `/openapi/v1/intl-macro/us-tbr` | `w4Bd`/`w4Ce`/`w8Bd`/`w8Ce`/`w13Bd`/`w13Ce`/`w17Bd`/`w17Ce`/`w26Bd`/`w26Ce`/`w52Bd`/`w52Ce`（`Bd`=银行贴现率 / `Ce`=等价收益率；⚠️ `w17Bd`/`w17Ce` 常为 null） |
| `/openapi/v1/intl-macro/us-tltr` | `ltc`(长期综合) / `cmt`(CMT) / `efactor`(外推因子，常 null) |
| `/openapi/v1/intl-macro/us-trltr` | `ltrAvg`（长期实际利率均值，单一数值） |
| `/openapi/v1/intl-macro/hibor` | `onRate`(隔夜)/`w1`(1周)/`w2`(2周)/`m1`/`m2`/`m3`/`m6`/`m12`（港元，8 期限） |
| `/openapi/v1/intl-macro/libor` | `currType`(币种) + `onRate`/`w1`/`m1`/`m2`/`m3`/`m6`/`m12`（7 期限，⚠️ 2023-06 后多数已退役） |
| `/openapi/v1/intl-macro/gz-index` | `d10Rate`/`m1Rate`/`m3Rate`/`m6Rate`/`m12Rate`/`longRate`（广州民间借贷，6 期限） |
| `/openapi/v1/intl-macro/wz-index` | `compRate`(综合) + `centerRate`/`microRate`/`cmRate`/`sdbRate`/`omRate`/`aaRate` 7口径 + `m1Rate`/`m3Rate`/`m6Rate`/`m12Rate`/`longRate` 期限 |

⚠️ 全球财经事件日历（`macro_eco_cal`）和国家政策库（`macro_policy_npr`）**不在本 scope**，在 `market` scope 下，路径 `/openapi/v1/market/macro/eco-cal` / `/openapi/v1/market/macro/policy-npr`（已在「二十、其他端点速查」列出）。

---

## 十八、外汇（forex — Max）

两个端点 form 均为 `ForexQueryForm`（继承 `OpenApiPageForm`，**支持 `page`/`size`**）。日期 `startDate`/`endDate` 一律 `YYYYMMDD`。tsCode 形如 `"USDCNH.FXCM"` / `"EURUSD.FXCM"`。数据来源 Tushare `fx_obasic` / `fx_daily`（海外外汇 / CFD）。

`ForexQueryForm` 全字段一览：

| 字段 | 类型 | 说明 |
|------|------|------|
| `tsCode` | string | 外汇代码，如 `"USDCNH.FXCM"`。可空（daily 端点建议传，否则只按日期范围列全市场） |
| `startDate` | string | `YYYYMMDD`，可空（**仅 daily 端点用**） |
| `endDate` | string | `YYYYMMDD`，可空（**仅 daily 端点用**） |
| `classify` | string | 分类，**仅 obasic 端点用**：如 `"FX"` 外汇 / `"CFD"` 差价合约。可空 |
| `exchange` | string | 交易商，**仅 obasic 端点用**：如 `"FXCM"` / `"OANDA"`。可空 |

### `POST /openapi/v1/forex/obasic` — 外汇产品基础信息
form: `ForexQueryForm` (分页) · 可按 `tsCode` / `classify` / `exchange` 任意组合过滤；全空则按 ts_code 升序返回前 N 行。完整字段：`tsCode`/`name`(中文名)/`classify`("FX"/"CFD")/`exchange`("FXCM"/"OANDA")/`minUnit`/`maxUnit`/`pip`(最小价位步长)/`pipCost`(点值，常 null)/`targetSpread`(目标点差，常 null)/`minStopDistance`(最小止损距离，常 null)/`tradingHours`(交易时段文本)/`breakTime`(休市时段，常 null)

### `POST /openapi/v1/forex/daily` — 外汇日线行情
form: `ForexQueryForm` (分页) · `tsCode` 建议必填（不传则跨产品按 trade_date DESC 列）。⚠️ **响应 `tradeDate` 是毫秒时间戳**。完整字段：`tsCode`/`tradeDate`(ms)/`bidOpen`/`bidClose`/`bidHigh`/`bidLow`(买价 OHLC)/`askOpen`/`askClose`/`askHigh`/`askLow`(卖价 OHLC)/`tickQty`(报价笔数)/`exchange`(常 null)。点差 spread = askClose − bidClose，由调用方自行计算

---

## 十九、票房 / 影视（tmt — Ultra · 内部档，暂不外卖）

所有端点 form 均为 `TmtQueryForm`（继承 `OpenApiPageForm`，**支持 `page`/`size`**）。⚠️ **日期格式因端点而异**：BO（票房）/ film-record 用 `YYYYMMDD`；twincome / twincome-detail（台湾电子月营收）用 `YYYYMM`。**注意路径前缀是 `/openapi/v1/tmt/...`（不带 `stock/`）**。

`TmtQueryForm` 全字段一览（各端点用其中一个子集，传无关字段会被忽略）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `startDate` | string | 起始日期，可空。**BO / film-record 用 `YYYYMMDD`；twincome / twincome-detail 用 `YYYYMM`** |
| `endDate` | string | 结束日期，可空。同上格式规则 |
| `name` | string | 影片 / 剧目名称模糊匹配（bo-daily / bo-weekly / bo-monthly / film-record / teleplay-record 用） |
| `cName` | string | 影院名称模糊匹配，**仅 bo-cinema 端点用**（与 `name` 互斥） |
| `recNo` | string | 备案号精确匹配，**仅 film-record 端点用** |
| `licenseKey` | string | 许可证号精确匹配，**仅 teleplay-record 端点用** |
| `item` | string | 台湾电子产品代码，**仅 twincome / twincome-detail 用**，如 `"8001"` 合计 / `"8002"` 子分类 |
| `symbol` | string | 台湾电子公司代码，**仅 twincome-detail 端点用** |

### `POST /openapi/v1/tmt/bo-daily` — 电影日票房
form: `TmtQueryForm` (分页) · 单日电影维度票房榜（day_amount / total / list_day / wom_index / up_ratio / rank）。过滤：`startDate` / `endDate`（`YYYYMMDD`）+ `name` 影片名模糊。排序 date DESC + rank ASC

### `POST /openapi/v1/tmt/bo-weekly` — 电影周票房
form: `TmtQueryForm` (分页) · 单周电影维度票房榜（`date` = 周一日期），字段同 bo-daily（day_amount → week_amount）。`startDate` / `endDate` 用 `YYYYMMDD`

### `POST /openapi/v1/tmt/bo-monthly` — 电影月票房
form: `TmtQueryForm` (分页) · 单月电影维度票房榜（`date` = 月初日期），含 `listDate` 上映日期 + `mRatio` 月度环比。`startDate` / `endDate` 用 `YYYYMMDD`

### `POST /openapi/v1/tmt/bo-cinema` — 影院日票房
form: `TmtQueryForm` (分页) · 单日影院维度票房榜（aud_count 观影人次 / att_ratio 上座率 / day_showcount 排片场次，单位元）。过滤：`startDate` / `endDate`（`YYYYMMDD`）+ `cName` 影院名模糊

### `POST /openapi/v1/tmt/film-record` — 全国电影剧本备案
form: `TmtQueryForm` (分页) · 电影年度备案信息（备案号 / 影片名 / 备案单位 / 编剧 / 备案结果 / 备案地）。过滤：`startDate` / `endDate` 公示日期范围（`YYYYMMDD`）+ `recNo` 精确备案号 + `name` 影片名模糊

### `POST /openapi/v1/tmt/teleplay-record` — 全国电视剧备案
form: `TmtQueryForm` (分页) · 电视剧备案登记（许可证号 / 剧目名 / 题材 / 类型 / 制作机构 / 集数 / 拍摄日期，业务字段均 TEXT）。过滤：`licenseKey` 精确许可证号 + `name` 剧目名模糊（**此端点不按日期过滤**）

### `POST /openapi/v1/tmt/twincome` — 台湾电子产品月营收合计
form: `TmtQueryForm` (分页) · 台湾电子产品分类营收月度数据，`date` 格式 `YYYYMM`（VARCHAR 字符串比较）。`item` 产品代码（`"8001"` 合计 / `"8002"` 子分类等）。⚠️ `startDate` / `endDate` 用 **`YYYYMM`** 不是 `YYYYMMDD`

### `POST /openapi/v1/tmt/twincome-detail` — 台湾电子月营收明细
form: `TmtQueryForm` (分页) · 细化到公司代码 `symbol` 的月度营收 + 合并营业收入，`date` 格式 `YYYYMM`。⚠️ `startDate` / `endDate` 用 **`YYYYMM`**

> ⚠️ tmt 多数票房表数据可能为空（待补齐），调用前可先小窗口探测有无数据。

---

## 二十、其他端点速查（仅列路径——参数 / 返回结构见 api-full-spec.md）

> 以下 40 个端点同样在线可用（2026-06-07 全量实测：30+ 直接有数据）。调用前先查 [`api-full-spec.md`](./api-full-spec.md) 对应条目拿参数定义；通用约定（POST + JSON、`tsCode`/`startDate`/`endDate` 命名、`data:null` vs `[]` 语义）与上文一致。

| 路径（`/openapi/v1` 前缀省略） | scope | 一句话说明 |
|---|---|---|
| `/stock/basic/bse-mapping` | stock.basic | 北交所新旧代码对照。完整字段（4个）：name/oCode(**⚠️ 不是ocode，大写C**，旧代码如 `872931.BJ`)/nCode(**⚠️ 不是ncode，大写C**，新代码如 `920931.BJ`)/listDate(ms，北交所上市日期) |
| `/stock/kline/weekly-monthly` | stock.kline | 股票周/月线一体（不复权；参数：`tsCode` + 可选 `startDate`/`endDate` YYYYMMDD；⚠️ 响应 `tradeDate`/`endDate` 均为**毫秒时间戳**；完整字段（13个）：tsCode/tradeDate(ms)/endDate(ms，周期末日)/freq("week"/"month")/open/high/low/close/preClose/vol(手)/amount(千元)/change/pctChg(%)；⚠️ 底表为增量积累，历史数据可能稀疏，2026-06-08 前仅有近几周数据） |
| `/stock/kline/week-month-adj` | stock.kline | 股票周/月线复权一体（同上参数；⚠️ 响应 `tradeDate`/`endDate` 均为**毫秒时间戳**，`freq` 同上；一次返回 BFQ（`open/high/low/close`）+ QFQ（`openQfq/highQfq/lowQfq/closeQfq`）+ HFQ（`openHfq/highHfq/lowHfq/closeHfq`）三套 OHLC + `vol/amount/change/pctChg`） |
| `/stock/kline/index-minute` | stock.minute | 指数历史分钟 K 线（`tsCode` 必填传指数代码，如 `"000001.SH"` / `"000300.SH"` / `"399001.SZ"` 等；2026-06-05 起逐日积累，更早历史暂缺；⚠️ **响应日期字段名是 `tradeTime`（不是 `tradeDate`！）** = 毫秒时间戳；⚠️ **无 `freq` 字段也无 `preClose` 字段**（旧文档有误）；完整字段（8个）：tsCode/tradeTime(ms)/open/high/low/close/vol(手)/amount(千元)） |
| `/stock/indicator/idx-factor-pro` | stock.indicator | 指数因子专业版（89 列宽表，BFQ；`tsCode` 必填传指数代码如 `"000300.SH"`；⚠️ `tradeDate` 是**毫秒时间戳**；含 OHLCV + pctChange + MA5/10/20/30/60/90/250 + EMA5/10/20/30/60/90/250 + MACD/KDJ-K/D + RSI6/12/24 + BOLL/KTN/TAQ + DMI/CCI/ATR/OBV/PSY/WR/ROC/MTM + XSII 等 87 个 BFQ 量化因子） |
| `/stock/financial/forecast` | stock.financial | 业绩预告 ⚠️ **2026-06-08 实测 `data:[]`（PG 迁移缺口，底表暂无数据）**，`tsCode` 必填；暂不可用 |
| `/stock/financial/express` | stock.financial | 业绩快报（⚠️ **必填 tsCode**；⚠️ `annDate`/`endDate` 均是**毫秒时间戳**；完整字段（14个）：`tsCode`/`annDate`(ms)/`endDate`(ms) · 利润：`revenue`(营业收入元)/`operateProfit`(营业利润元)/`totalProfit`(利润总额元)/`nIncome`(净利润归母元) · 资产：`totalAssets`(总资产元)/`totalHldrEqyExcMinInt`(股东权益不含少数股东) · 每股：`dilutedEps`/`bps`(净资产) · 增长率：`dilutedRoe`(净资产收益率%)/`yoyNetProfit`(净利润同比%)/`yoySales`(营收同比%)；数据覆盖较全，主要上市公司有记录）|
| `/stock/financial/disclosure-date` | stock.financial | 业绩披露日历（⚠️ **必填 tsCode**；个股覆盖不均）。完整字段（6个）：tsCode/annDate(ms，公告日，⚠️ **不可靠**)/endDate(ms，报告期)/preDate(ms，预计披露日)/actualDate(ms，实际披露日，未披露则null)/modifyDate(ms，可null)；优先用 `preDate`/`actualDate`；**字段名 camelCase，不是 `pre_date`/`actual_date`** |
| `/stock/index/kline/weekly` | stock.index | 指数周线行情（⚠️ **输入** 用 `startDate`/`endDate` YYYYMMDD，**勿传 `tradeDate`** 请求参数——周线锚点日与日 K 精确日期不对齐，传了返空；⚠️ **响应 `tradeDate` 是毫秒时间戳**；响应字段（11 个）：`tradeDate`(ms)/`tsCode`/`open`/`high`/`low`/`close`/`preClose`/`change`/`pctChg`/`vol`/`amount`；⚠️ **`pctChg` 是小数形式**（0.0113 = 1.13%，需 × 100 才是百分比），与 `index/kline/daily` 的 `pctChg`（百分比形式，0.2339 = 0.2339%）**语义不同**；字段名也不同：周/月用 `change`，日用 `chg`） |
| `/stock/index/kline/monthly` | stock.index | 指数月线行情（⚠️ 同周线：勿传 `tradeDate` 请求参数，用 `startDate`/`endDate` YYYYMMDD；⚠️ **响应 `tradeDate` 是毫秒时间戳**；响应字段（11 个）：`tradeDate`(ms)/`tsCode`/`open`/`high`/`low`/`close`/`preClose`/`change`/`pctChg`/`vol`/`amount`；⚠️ `pctChg` 同周线——小数形式（0.0209 = 2.09%，需 × 100），字段名 `change`（不是 `chg`）） |
| `/stock/index/weight` | stock.index | 指数成分股与权重（月度，`tsCode` 传指数代码如 `"000300.SH"`；完整字段（4个）：`tradeDate`(ms，月度发布日)/`indexCode`(指数代码)/`conCode`(成分股代码)/`weight`(权重%)） |
| `/stock/index/dailybasic` | stock.index | 指数每日估值快照（完整字段（12个）：`tradeDate`(ms)/`tsCode` · 估值：`pe`/`peTtm`/`pb` · 市值：`totalMv`(总市值元)/`floatMv`(流通市值元) · 股本：`totalShare`/`floatShare`/`freeShare`(自由流通) · 换手：`turnoverRate`/`turnoverRateF`(基于自由流通股本)） |
| `/stock/index/global` | stock.index | 全球指数日 K 线（⚠️ 2026-06-08 实测 `data:[]`，底表暂无数据，勿当有效数据用） |
| `/stock/market/cyq-chips` | stock.sentiment | 每日筹码分布明细（`tsCode` 必填；⚠️ 响应 `tradeDate` 是**毫秒时间戳**；完整字段（4个）：tsCode/tradeDate(ms)/price(价格档位)/percent(该档筹码比例%)，可拼出筹码山图） |
| `/stock/market/hm-detail` | stock.lhb | 游资交易明细。字段（9个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`/`tsName`/`buyAmount`(元)/`sellAmount`(元)/`netAmount`(净买元)/`hmName`(游资名，如"温州帮")/`hmOrgs`(⚠️ **平文本字符串，一个营业部全名**，不是 JSON；与 `hm-list.orgs`（JSON 字符串数组）格式不同，**不要 JSON.parse**)/`tag`(通常 null，存在此字段但多为 null) |
| `/stock/market/ths-hot` | stock.plate | 同花顺 App 热榜。完整字段（11个）：tradeDate(ms)/dataType/tsCode/tsName/rank/pctChange/currentPrice/concept(JSON字符串数组，需JSON.parse)/hot(热度值)/rankTime("YYYY-MM-DD HH:mm:ss"字符串)/rankReason(可null) |
| `/stock/market/ths-index` | stock.plate | 同花顺指数列表（返回 `700xxx.TI` 代码系；`type` 含义：`I`=行业指数 / `BB`=宽基指数 / `ST`=风格指数 / `TH`=特色系列；⚠️ **与 `ths-concept`/`ths-hot` 的 `885xxx.TI` 概念板块代码系不同，不要混用**） |
| `/stock/market/ths-daily` | stock.plate | 同花顺指数日行情（`tsCode` 传 `700xxx.TI` 代码；⚠️ 响应 `tradeDate` 是**毫秒时间戳**；完整字段（14个）：tsCode/tradeDate(ms)/open/high/low/close/preClose/avgPrice/change/pctChange(%)/vol/turnoverRate(%，可为null)/totalMv(万元)/floatMv(万元)） |
| `/stock/market/tdx-index` | stock.plate | 通达信板块基础信息。完整字段（9个）：tradeDate(ms)/tsCode/name/idxType(板块类型)/idxCount(成分数，Integer)/totalShare/floatShare/totalMv/floatMv |
| `/stock/market/tdx-daily` | stock.plate | 通达信板块日行情。完整字段（35个）：tradeDate(ms)/tsCode/open/high/low/close/preClose/change/pctChange(%)/vol/amount/volRatio/turnoverRate(%)/swing(%)/upNum(Integer)/downNum(Integer)/limitUpNum(Integer)/limitDownNum(Integer)/luDays(Integer，连板天数)/return3Day(%)/return5Day(%)/return10Day(%)/return20Day(%)/return60Day(%)/mtd(%)/ytd(%)/return1Year(%)/floatMv/abTotalMv(**⚠️ 不是totalMv**，A+B股总市值)/floatShare/totalShare/bmBuyNet/bmBuyRatio(%)/bmNet/bmRatio(%) |
| `/stock/market/tdx-member` | stock.plate | 通达信板块成分股（`tsCode` 板块代码传参）。字段（4个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`(板块代码)/`conCode`(成分股代码)/`conName`(成分股名称) |
| `/stock/market/ci-daily` | stock.plate | 中信行业指数日行情（`tsCode` 格式如 `"CI005001.CI"`）。完整字段（11个）：tradeDate(ms)/tsCode/open/high/low/close/preClose/change/pctChange(%)/vol/amount |
| `/stock/market/ci-index-member` | stock.plate | 中信行业成分（无 `tradeDate` 字段；三级分类体系）。完整字段（11个）：l1Code/l1Name/l2Code/l2Name/l3Code/l3Name/tsCode/name/inDate(ms，纳入日期)/outDate(ms，剔除日期，可null)/isNew("Y"/"N") |
| `/stock/market/kpl-concept-cons` | stock.plate | 开盘啦题材成分（`tsCode` 题材代码，`nameKeyword` 承载个股代码反查）。字段（7个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`(题材代码，如 `"885589.TI"`)/`name`(题材名)/`conCode`(⚠️ **个股代码**，非题材代码，勿与 `tsCode` 混淆)/`conName`(个股名)/`description`(⚠️ **题材描述文字**，字段名为 `description`，原 Tushare `desc` 保留字重命名)/`hotNum`(人气值，int) |
| `/stock/market/limit-step` | stock.sentiment | 涨停连板天梯（`tradeDate` 传 YYYYMMDD）。字段（4个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`/`name`/`nums`（连板数，⚠️ **string 类型**，如 `"5"` = 5 连板，不是整数，排序/比较时须转换） |
| `/stock/market/limit-cpt-list` | stock.sentiment | 涨停最强板块统计（`tradeDate` 传 YYYYMMDD）。字段（9个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`(板块代码，如 `"885431.TI"`)/`name`/`days`（热度天数，int，如 28）/`upStat`（如 `"4天2板"`，string）/`consNums`（当前连续涨停次数，int）/`upNums`（历史总涨停次数，int）/`pctChg`（涨跌幅%，如 0.7535 = 0.75%）/`rank`（⚠️ **string 类型排名**，如 `"3"`，比较须转整数）|
| `/stock/market/st-daily` | stock.sentiment | ST 股票每日列表。完整字段（5个）：tradeDate(ms)/tsCode/name/type("ST"/"*ST"等)/typeName("风险警示板") |
| `/stock/market/st-warning` | stock.sentiment | ST 风险警示事件。字段（7个）：`tsCode`/`name`/`pubDate`(⚠️ **毫秒时间戳**，公告日)/`impDate`(⚠️ **毫秒时间戳**，执行日)/`stType`(风险类型，⚠️ **可为空字符串 `""` 而非 null**)/`stReason`(简短原因，一两句话)/`stExplain`(公告全文，**字段较长按需截取**) |
| `/stock/market/bak-basic` | stock.sentiment | 备用基础数据（每日股票快照，含估值/财务/股本/股东）。完整字段（24个）：tradeDate(ms)/tsCode/name/industry(行业)/area(地区)/pe/floatShare(流通股本万股)/totalShare(总股本万股)/totalAssets(万元)/liquidAssets(万元)/fixedAssets(万元)/reserved(公积金万元)/reservedPershare/eps/bvps/pb/listDate(ms，上市日期)/undp(未分配利润万元)/perUndp/revYoy(%)/profitYoy(%)/gpr(毛利率)/npr(净利率)/holderNum(股东户数，Integer) |
| `/stock/market/bak-daily` | stock.sentiment | 备用行情（⚠️ `tradeDate` 是**毫秒时间戳**；实际 31 字段，远比名字暗示的更丰富：`tsCode`/`name`/OHLC + `preClose`/`change`/`pctChange`/`vol`/`amount` + `volRatio`/`turnOver`/`swing` + `selling`/`buying` 卖买盘 + `totalShare`/`floatShare`/`pe`/`industry`/`area`/`floatMv`/`totalMv`/`avgPrice` + `strength`(强度)/`activity`(活跃度)/`avgTurnover`/`attack`(攻击)/`interval3`/`interval6` 动量；可作为轻量"全字段快照"使用） |
| `/stock/shareholder/ccass-hold` | stock.shareholder | CCASS 持股统计（按股票汇总；`tsCode` 传港股代码如 `"00700.HK"`）。字段（6个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`(港股代码)/`name`(股票名称)/`shareholding`(CCASS总持股量，股)/`holdNums`(持股机构数，int)/`holdRatio`(占已发行股份%) |
| `/stock/shareholder/ccass-detail` | stock.shareholder | CCASS 持股明细（按机构展开；同一日期股票含多行，每行对应一个 CCASS 参与者）。字段（7个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`(港股代码)/`name`(股票名称)/`colParticipantId`(机构编号)/`colParticipantName`(机构名称，如 "HSBC NOMINEES...")/`colShareholding`(该机构持股量，股)/`colShareholdingPercent`(占已发行股份%) |
| `/stock/shareholder/hk-hold` | stock.shareholder | 沪深港通持股明细（**含北向+南向**；`exchange=SH/SZ` = 北向资金持 A 股；`exchange=HK` = 南向资金持港股；查港股传 `tsCode` 如 `"00700.HK"`）。字段（7个）：`tradeDate`(⚠️ **毫秒时间戳**)/`tsCode`(TS代码)/`code`(纯数字代码，无后缀)/`name`(中文名)/`vol`(持股量，股)/`ratio`(持股占比%)/`exchange`(SH/SZ/HK；⚠️ 在 `stock.shareholder` scope，不在 `stock.hk`)|
| `/stock/shareholder/ggt-daily` | stock.shareholder | 港股通每日成交统计（市场级总量，无 tsCode；`buyAmount - sellAmount` = 净流入）。字段（5个）：`tradeDate`(⚠️ **毫秒时间戳**)/`buyAmount`(总买入成交金额亿元)/`buyVolume`(总买入成交笔数)/`sellAmount`(总卖出成交金额亿元)/`sellVolume`(总卖出成交笔数) |
| `/stock/shareholder/ggt-monthly` | stock.shareholder | 港股通每月成交统计（市场级，参数传 `{}` 取最近；`totalBuyAmt - totalSellAmt` = 月净流入）。字段（9个）：`month`(YYYYMM字符串，如"202504")/`dayBuyAmt`(日均买入额)/`dayBuyVol`(日均买入笔)/`daySellAmt`(日均卖出额)/`daySellVol`(日均卖出笔)/`totalBuyAmt`(月总买入额)/`totalBuyVol`(月总买入笔)/`totalSellAmt`(月总卖出额)/`totalSellVol`(月总卖出笔) |
| `/stock/shareholder/hsgt-list` | stock.shareholder | 沪深港通可交易股票名单。字段（5个）：`tsCode`/`tradeDate`(⚠️ **毫秒时间戳**，名单更新日)/`name`/`type`/`typeName`；`type` 4个值：`"HK_SH"`(沪股通，北向外资买上证A股)/`"HK_SZ"`(深股通，北向外资买深证A股)/`"SH_HK"`(港股通，沪市南向买港股)/`"SZ_HK"`(港股通，深市南向买港股)，不传 `type` 返全部 |
| `/market/macro/eco-cal` | market | 全球财经事件日历。字段（8个）：⚠️ `date`(**毫秒时间戳**，如 1780588800000)/`time`("HH:mm" 字符串，如 "13:00")/`currency`(货币/国家代码，如 "JPY"/"CNY")/`country`(⚠️ **非国名，是分类代码**，如 "economic_activity"，用 `currency` 辨别国家)/`event`(事件描述中文)/`value`(实际值，可为 null)/`preValue`(前值)/`foreValue`(预测值，可为 null) |
| `/market/macro/policy-npr` | market | 国家政策档案（⚠️ 响应 `pubtime` 是 `"YYYY-MM-DD HH:mm:ss"` 带横杠带冒号字符串，不是时间戳）。字段（7个）：`pcode`(政策文号，如 "国发〔2026〕14号")/`pubtime`("YYYY-MM-DD HH:mm:ss")/`title`/`url`(原文链接)/`puborg`(发布机构)/`ptype`(政策分类，斜杠分隔层级)/`contentHtml`(政策正文 HTML，**字段较大，按需截取**） |
| `/fund/sales/ratio` | fund | 各渠道公募基金销售保有占比（年度）；参数最稳传 `{}`；完整字段（6个）：year(Integer)/bank(%)/secComp(%)/fundComp(%)/indepComp(%)/rests(%) |
| `/fund/sales/vol` | fund | 销售机构公募基金保有规模 + 排名（季度）；参数最稳传 `{}`；完整字段（6个）：year(Integer)/quarter("Q1"-"Q4")/instName(机构名)/fundScale(非货基保有亿元)/scale(总规模亿元)/rank(季度排名，Integer) |
| `/derivative/futures/weekly-detail` | derivative | 期货主要品种交易周报（⚠️ **历史数据止于 2020-04，不含近期**）。字段（17个）：`exchange`(交易所，如 "CFFEX")/`prd`(品种代码，如 "IC"/"IF"/"IH")/`name`(品种中文名)/`vol`(当周成交量，手)/`volYoy`(成交量同比%)/`amount`(当周成交额，**亿元**)/`amoutYoy`(⚠️ **API 拼写错误**——`amout` 不是 `amount`，额同比%)/`cumvol`(年累计成交量)/`cumvolYoy`(年累计成交量同比%)/`cumamt`(年累计成交额亿元)/`cumamtYoy`(年累计额同比%)/`openInterest`(周五持仓量，手)/`interestWow`(持仓量环比%)/`mcClose`(主力合约收盘价)/`closeWow`(主力合约周涨跌%)/`week`("YYYYWW" 字符串，如 "202017" = 2020年第17周)/⚠️ `weekDate`(**毫秒时间戳**，对应该周五日期) |

---

## 套餐 → scope 累进式映射

> 2026-06-02 重排版（由低到高 free < plus < pro < max < ultra，付费 3 档 ↔ claw LOW/MID/HIGH）。
> 以 `/openapi/v1/whoami` 返回的 `tier`/`scopes` 为准——先 whoami 再决定调哪些端点。

| 套餐 | 含 Scope（累进） |
|------|---------|
| **Free（免费）** | `stock.basic` + `stock.kline` + `stock.indicator`（3） |
| **Plus（入门）** | + `stock.index` + `stock.minute` + `stock.financial` + `stock.research` + `stock.shareholder`（8） |
| **Pro（中级）** | + `stock.plate`（板块/指数）+ `stock.lhb`（龙虎榜）+ `stock.moneyflow`（资金流）+ `stock.sentiment`（情绪/ST/备用行情，URL 均 `/stock/market/...`）+ **`market`（国内宏观）**（14） |
| **Max（高级）** | + `derivative` + `fund` + `bond` + `stock.hk` + `stock.us` + **`stock.intl-macro`** + **`forex`** + **`news`**（18）⚠️ 以 `/openapi/v1/whoami` 返回的 scopes 为准（2026-06-08 实测 Max token 含以上全部） |
| **Ultra（内部 · 不对外）** | + `tmt` + `stock.selection`（20，不外卖） |
| **管理员** | `*`（所有 scope） |
