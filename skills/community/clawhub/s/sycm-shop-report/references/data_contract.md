> **适用范围**：本技能仅服务中国大陆天猫 / 淘宝商家，数据源限定生意参谋 MCP。
> **默认中文输出与 Asia/Shanghai 时区**是这一垂直领域的合理默认（生意参谋字段、千牛入口、类目命名都是中文语境），**不是策略强加**——若你的团队需要英文或别的时区，请自行改 SKILL.md 里字体、cron `tz` 与 narrative 文案。

# 数据契约：生意参谋接口 → 报表 JSON

所有 MCP 调用先用 `qwenwork_mcp_tool_get` 取 schema，再用 `qwenwork_mcp_tool_call`。
`toolName` 形如 `mcp__taobao-open-platform__openAtpSycm...`；参数一律包在 `{"param0":{"params":{"extMap":{...}}}}`（店铺绩效同理）。

## 一、要调哪些接口

| 用途 | 接口 | 关键参数 |
|---|---|---|
| 本期核心指标 + 环比 | `openAtpSycmTrafficDashboardOverviewQuery` | 日报 `dateType:"day", dateRange:"D|D"`；周报 `dateType:"week", dateRange:"起|止"`；月报 `dateType:"month"`。`device:"0"` |
| 近 7 日 / 每日走势 | `openAtpSycmTrafficDashboardTrendQuery` | 日报 `dateType:"recent7"`；周报用当周区间。返回 `statDate` + 各指标数组 |
| 同比 / 自定义对比 | `openAtpSycmCustomTrafficDashboardOverviewQuery` | `dateRange:"本期起|本期止,对比起|对比止"`。对比期填去年同期。返回各指标 `cycleCrc`＝同比 |
| 渠道结构（含同比） | `openAtpSycmCustomTrafficSourceOverviewQuery` | `dateType:"compareRange", dateRange:"本期,对比期"`。返回 `all/item/shop/live/content` 五组 |
| 渠道 + 同行同层 | `openAtpSycmOfflineTrafficSourceOverviewQuery` | `dateType:"day", dateRange, needCate:"true"`。返回 `rivalAvgUv/rivalGoodUv` 等 |
| 店铺绩效 + 同行 | `openAtpSycmShopPerformanceSummaryQuery` | `startDate/endDate`＝8 位整数 `YYYYMMDD`，`dateType:"day"`，`dateRange:"1d"|"7d"|"30d"|"1m"|"cz"`，`scopeType:"shop"`。返回 `current_sum` 与 `avg`/`exc`（同行）组 |
| 商品 TOP | `openAtpSycmOfflineItemRankingQuery` | `dateType, dateRange, page:"1", pageSize:"10", orderBy:"payAmt", order:"desc"` |

同比区间：日报＝去年同日历日；周报＝去年同 ISO 周（本期周一 −364 天）；月报＝去年同自然月。

## 二、字段映射（返回 → JSON）

指标名对照（接口字段 → 报表语义）：
`uv`＝进店人数、`pv`＝浏览量、`itmUv`＝商品页进店、`newUv/oldUv`＝新/老客人、`payAmt`＝销售额、`payByrCnt`＝买东西人数、`payRate`＝成交转化率、`payPct`＝客单价、`cartByrCnt`＝加购人数、`crtByrCnt`＝下单人数、`bounceRate`＝跳失率、`liveRoomUv`＝直播间人数、`shortVideoUv`＝短视频人数、`uvValue`＝每访客产值。

店铺绩效返回字段：`uv1d/pv1d/payAmt1d/payUsrCnt1d/payCnt1d/storeTcr1d/rfdAmt1d/realPayAmt1d`；同行取 `groupType=="avg"` 与 `=="exc"` 两组。

### daily_data.json
- `metrics.today` ← 本期概览各指标 `value`
- `metrics.crc` ← 本期概览各指标 `cycleCrc`（＝环比前一日）
- `metrics.prev_week` ← 上周同日概览（再调一次 Overview，`dateRange` 填上周同日）
- `metrics.last_year` ← 去年同期概览（`dateRange` 填去年同日）
- `metrics.uv_wow_crc` ← 自定义对比接口 `uv.cycleCrc`（本期 vs 上周同日）
- `trend7.days` ← 趋势接口，取最近 7 个点 `[标签, uv, pv, payAmt, payByrCnt, payRate]`
- `channels.rows[]` ← 渠道构成：`uv`＝本期，`uv_ly`＝本期/(1+`cycleCrc`)，`pay`/`pay_ly` 同理；`uv_wow_crc`/`pay_wow_crc` 用本期 vs 上周同日的自定义对比
- `funnel.now/ly` ← `[uv, itmUv, cartByrCnt, crtByrCnt, payByrCnt]` 本期与去年同期
- `items.rows[]` ← 商品排行 TOP：`title/uv(itmUv)/payAmt/payByrCnt/payItmCnt/payPct`
- `peer.self/avg/good` ← 店铺绩效 `current_sum` / `avg` / `exc`；`peer_ly.avg` ← 去年同期店铺绩效 `avg`

### weekly_data.json
- `metrics.self/prev/last_year` ← 周概览三次调用（本周 / 上周 / 去年同周，`dateType:"week"`）
- `compare3.*` / `growth_story.metrics` ← 由 `metrics` 三期数值算
- `week_trend.this_days/prev_days` ← 趋势接口当周与上周每日 `[标签, uv, payAmt]`
- `channels.rows[]` ← 渠道构成周区间（本期 vs 去年同周）：`uv/uv_prev/uv_ly/pay/pay_prev/pay_ly`
- `refund.*` ← 店铺绩效 `rfdAmt1d` 三期 + `payAmt` 三期
- `peer.uv_sum/pay_sum/byr_sum` ← 同行周累计（趋势接口 `rivalAvg*`/`rivalGood*` 七日累加）；`rate_avg/rate_good` ← 同行转化率

## 三、必填校验（生成前）
1. **环比双向核对**：`本期值 ÷ (1+cycleCrc)` 应≈上期趋势原值，误差 <0.5% 才可信。
2. **去重 vs 累加**：周/多日 `uv` 去重值 ≠ 各日累加；报表须标注（周去重用于「进店人数」，累加用于同行对照）。
3. **异常剔除**：`proportionCss` 与 `silentSalePro` 同时 100%、`ordAmt1d/ordUsrCnt1d` 为 0 却有销售额 → 判定接口异常，写入 `pitfalls`，不进结论。
4. **延迟字段**：`cstUsrCnt1d`（询单人数）延迟统计，返回 0 属正常，用 `cstUv1d` 代替。

## 四、叙述字段（每期由你重写，不要照抄样例）
`headline / signals / actions / actions_extra / pitfalls` 是**分析结论**，必须依据本期数据重写：
- `actions` 每条三段：`why`（引用本期具体数字）→ `how`（1~3 步 + 后台入口路径）→ `goal`（可验证量化目标）。
- 日报 3 条、周报 5 条、月报 6 条。
- 白话：术语首次出现括号解释（UV→进店人数）。
`kpi_cards[].deltas[].dir` 取 `up/down/flat` 决定颜色（涨绿跌红；退款率等「越低越好」指标涨时用 `down` 显红）。
