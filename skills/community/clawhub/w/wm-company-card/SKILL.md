---
name: wm-company-card
display_name: "公司卡片"
version: 1.2.9
description: 公司一页纸摸底（行情+身份+估值成长）。深度研读/备忘请走 Role；全行业比价走 wm-industry-members。
---

# 公司卡片

公司摸底的 **L1 入口**（行情 + 基本面一页纸）。旧 `wm-quote-snapshot` 已市场下架。  
深度研读 / 生意全貌备忘 / 行业格局 → **不要停在本卡**，见下方「下一步」。

## 何时使用

- 「现在多少钱 / 今天涨跌」→ `include=quote` 或 `quote,kline`
- 「这家公司怎么样 / 一页纸」→ 默认 `include=default`（quote+identity+valuation+growth）
- 「看看走势 / 过往交易 / K线」→ 贴返回的 `company.kline` markdown；或只 `POST /v1/deeplinks/resolve`（不必跑全卡）
- 要股东 / 现金流负债 → 加 `shareholder` / `quality`，或 `include=full`
- **多只一起看**：`args.symbols`（≤50）

## 返回要点（给助手）

**寻址（HTTP 根，双读）：**
- 推荐：`data.card.*` / `data.freshness` / `data.deeplinks`（信封扁平后业务键在 `data`）
- 兼容：`data.result.card.*`（旧路径仍可用）

`identity` / default 路径字段在 **`card`** 内：

| 字段 | HTTP 路径（推荐） | 用途 |
|------|-------------------|------|
| `industry_l1` / `l2` / `l3` | `data.card.industry_l3` | 申万行业键，如 `industry.S340501` |
| `industry` | `data.card.industry` | 兼容字段（可能同 l3） |
| `pe_ttm` 等 | `data.card.pe_ttm` | 估值/行情 |

**比同行 / 拉竞争名单时**：取 `data.card.industry_l3`（或最细一层）→ 传给 `wm-industry-members.industry_code`。

## 下一步（必读，勿只停本卡）

| 用户意图 | 下一步 |
|----------|--------|
| 生意全貌 / 靠什么赚钱 | `wm-company-business` 或 **个股核对专家** |
| 读财务分析 / 进一步研读 / 值不值得继续看 | **公司深读专家**（`wm-analysis-nav`→`wm-analysis-run`） |
| 竞争对象 / 同业名单与估值中枢 | `industry_l3` → `wm-industry-members` |
| 行业阶段 / 天花板 / 竞争格局叙事 | **金融分析师**（配件 members + nav `theme=peer`）；**禁止外搜新闻当证据**；系统无 TAM 数据则如实说 |

对用户关键数字：标注来源技能 + **原样**贴返回的 `deeplinks[].markdown`（单票含 `company.card` + **`company.kline`（交易/K线）** + `analysis`；批量含 `company.compare`，逐票链在 `deeplinks_by_symbol` 或改调 `POST /v1/deeplinks/resolve`）；指标首次写中文+英文+代号（见管家 `output-hygiene`）。禁止手搓 `panel=` / `vs=`。

纯看 K 线 / 过往交易、不要全卡数据时：`POST /v1/deeplinks/resolve`，`items: [{ "id": "company.kline", "params": { "code": "600519" } }, …]`。

## 何时不要用

- 深度生意解读正文 → `wm-company-business`（可先本卡摸底）
- 行业全成分 → `wm-industry-members`
- 平台分析脚本树 → `wm-analysis-nav`

## 调用

`POST {WINMALE_API_BASE}/v1/skills/wm-company-card/run`

```json
{
  "symbol": "600519",
  "args": { "include": "default" }
}
```

轻量行情：

```json
{
  "args": {
    "symbols": ["600519", "000858"],
    "include": "quote,kline"
  }
}
```

| include | 含义 |
|---------|------|
| `default` | quote + identity + valuation + growth |
| `full` | 全部模块 |
| `quote` | 现价量额市值 |
| `quote,kline` | 再加均线与区间涨跌 |
| `…,shareholder` | 加上股东 |
| `…,quality` | 加上现金/负债 |

模块：`quote` `kline` `identity` `valuation` `growth` `quality` `shareholder`。

## 数据有效时间（`freshness`）

返回顶层与 `card.freshness`（同形）。HTTP：`data.freshness` 与 `data.card.freshness`（兼容 `data.result.*`）。

| 字段 | 含义 |
|------|------|
| `quote_date` / `quote_sas` | 现价·PE 等价格侧锚定的交易日（`$KLINE_DATE_LAST`） |
| `report_sas` | 成长/质量/估值报表侧最新期（`$SAS_LAST`） |

`quote_date` 在有行情/估值时**始终**返回（不要求 `include` 含 kline）。`kline_date` 与 `quote_date` 同值（兼容旧字段）。

`include` 含 `shareholder` 时另有域内日期（与 `report_sas` 不同期）：`free_holder_date`、`executive_hold_date`、`inst_report_date`、`northbound_asof_date` 等；`control_asof`=`MAX_DATE`（东财数据截至），`tags_synced_at`=equity-tags 平台同步时刻。停牌时可选 `suspend_start_date`。

## 禁止

- 新接入再装 `wm-quote-snapshot`（请用本技能）
- 多票循环 run；应一次 `symbols`
- 用本卡冒充实业「研读备忘」或「行业格局」长文（须交 Role / members）
