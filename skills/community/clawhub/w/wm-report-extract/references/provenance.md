# 溯源契约

每个提取值必须可独立复核：任何人拿着 `page` 翻到 PDF 对应页，能找到与 `quote` 一致的原文。

## 输出目录结构（result-{ts}/）

```json
{
  "manifest.json": {
    "layout": "split_tables",
    "catalog": {
      "tables": [{"id": "key_financials", "file": "tables/key_financials.json"}],
      "narratives": [{"id": "mda_outlook", "file": "narratives/mda_outlook.json"}],
      "fields": [{"id": "contract_liabilities", "file": "fields/contract_liabilities.json"}],
      "derived": []
    },
    "gaps_file": "gaps.json",
    "quality_file": "quality.json",
    "promote_candidates_file": "promote_candidates.json"
  }
}
```

## 按需字段（FieldRecord）

按需字段是 L1/L2 的“字段级目录”。任何外部 Agent 只要读取 `result-{ts}/manifest.json -> catalog.fields[]`，就能枚举该次 resolve 已落盘的字段与其文件路径。

### FieldRecord 必备契约

- `field_id`：字段 id（由字段名/用户 need 推导，建议仅用小写 a-z/0-9/_）。
- `label`：用户可读字段名（自然语言原文/近似）。
- `value`：该字段在报告中的确定值（字符串，保留原始数字形态即可）。
- `unit`：单位（来自表头/单位行或 records 的 unit；可为空字符串）。
- `period`：期间标签（来自 records 的 `values[].period` 或可回溯的表头语义；必要时为空）。
- `layer`：`L1`（来自 `quality.json` 中 `verdict=pass` 的 typed 表）、或 `L2`（来自 records / 正文 locate / extract-query）。
- `method`：`record_map | locate | extract-query | text_scan` 等，表示取值路径。
- `status`：`found` / `not_found` / `ambiguous`（字段级）。
- `source.quote`：必须是“PDF 页内可复核”的原文摘录（建议 ≤120 字），并且 `source.page` 必须对应到 PDF 物理页序号。

建议结构示例：

```json
{
  "field_id": "contract_liabilities",
  "label": "合同负债",
  "value": "131.57",
  "unit": "亿元",
  "period": "2025-12-31",
  "layer": "L2",
  "method": "record_map",
  "status": "found",
  "source": {
    "page": 17,
    "table": 12,
    "quote": "合同负债 131.57 亿元",
    "file": "tables/balance_sheet.json"
  }
}
```

### 落盘位置与索引

- `fields/*.json`：每个字段一份 FieldRecord。
- `result-{ts}/manifest.json`：新增 `manifest.catalog.fields[]`，每个条目包含 `{id, file}`。

## 单表结构（tables/*.json）

- 必须含 `table_id`、`title`、`description`、`method=record_map`、`group`。
- 必须含 `schema.columns[]`，每列包含 `{key,label,type,description}`，保证数据自解释。
- 每行必须附 `source{page,table,quote}`，`quote` 建议 ≤120 字并保留关键数字。
- `unit_default` 优先取原表单位（表头/单位行），不要覆盖为全局单位。
- 对 `meta.tables[].type is None` 但有稳定行列结构的表，允许落为 `source_type=generic_table`，`description` 必须明确“未定型通用表，供上层消费判读”。
- **无 `quality.json` 不得把 typed 表交给下游。** 污染表必须 `demote` 回 generic（或 `split` 只留匹配行）；只消费 `verdict=pass` 的稳定 `table_id`。`status=fail` 表示发生过 demote/split，不代表所有 typed 表都不可用。
- Agent 晋升的同类型多张物理表使用 `{type}` 与 `{type}_p{page}_i{index}`，不要把多源表拼成一张。

## 叙述结构（narratives/*.json）

- 无表格对应内容统一走 `method=text_scan`，例如 `mda_business/mda_industry/mda_outlook/risk_factors`。
- 叙述块必须包含 `narrative_id`、`title`、`description`、`anchor`、`page_range`、`bullets[]`。
- `bullets[]` 每条需含 `{label,text,quote,page,status}`，支持 `found|not_found|not_disclosed`。

### 叙述 KPI 硬门（qa-tables 强制）

关键词命中 **不等于** 提取成功。对 `manifest.catalog.narratives` 已落盘文件及 `gaps.json` 中 `status=required` 项：

1. `status=found` 的 bullet / 字段：**必须**非空 `quote` + 正整数 `page`；缺任一则记 `narrative_kpi_gate` → gaps `suspect`，不得当下游事实。
2. 报告未披露：显式 `status=not_disclosed`（或 gaps `not_disclosed`），禁止静默省略。
3. 尚待 Agent 补全：保持 gaps `pending`/`required`，不得伪造数值。

行业高频叙述 KPI 示例（无 typed 落盘时）：装机容量正文、利用小时、来水/水库、综合成本率、NBV margin 文字口径、去化率。

### FieldRecord 口径维度（建议强制）

在必备契约之外，行业敏感字段应填写：

- `scope`：`合并` / `母公司` / `权益口径` / `全口径` / `控股` / `权益装机` 等
- `basis`（可选）：`原保险` / `已赚` / `监管口径` / `会计口径`
- 缺 `scope` 且清单要求口径区分时，应进 `gaps`（如 `equity_vs_full_scope`、`controlling_vs_equity_capacity`），不得混入口径输出

若表格行本身缺解释列，允许对单行用 `text_scan` 回补；此时建议补 `reason_method: "text_scan"` 或在 `source.section` 标注来源段落。

## MD&A 变动原因（D 组强制形态）

`type=variance_reasons` 的行不得只输出金额。在通用字段之外附加：

```json
{
  "group": "D_mda",
  "field": "销售费用",
  "value": "11,273,114,891.99",
  "unit": "元",
  "period": "2025年度",
  "yoy_pct": "43.93",
  "reason": "主要系报告期公司加速构建直连用户的新渠道模式，以及加大新车型、新技术的上市宣传及品牌提升所致",
  "status": "found",
  "source": {"page": 31, "table": 29, "quote": "销售费用 11,273,114,891.99 7,832,252,812.60 43.93"}
}
```

- `reason`：逐字来自「原因说明 / 情况说明 / 变动原因」列（或紧随金额的脚注），禁止改写。
- 叙述型归因（银行净息差「主要原因如下」等无独立列表）同样用此三元组，`source.section` 指向 `mda_overview`。
- 费率/毛利率走独立字段（如「销售费用占营业收入比例」），不要塞进 automobile 扩展组。

## derived 规则

- 仅当用户明确要计算值，或清单要求比率（如净利率）时才产出。
- `value` 给计算结果，`source.quote` 换成 `formula`："净利率 = 归母净利润/营业收入"，并附 `inputs: [字段引用…]`。
- 输入字段必须先以 `found` 状态存在；任一输入缺失则 derived 不产出。

## not_found 纪律（应提尽提的闭环）

1. plan 方法失败 → 用 `fallback` 方法重试。
2. 仍失败 → `locate` 换同义锚点（如「货币资金」→「现金及存放中央银行款项」）重扫。
3. 仍失败 → 确认该科目是否适用该公司（银行无「存货」不是缺失，是结构差异，`not_found` + `reason: "不适用/未披露"`）。
4. 输出 `gaps: [{field, searched_pages: [..], anchors_tried: [..], reason}]`。

**禁止**：编造数值/页码；用第三方数据源（东财/同花顺/wind）补数；把 derived 伪装成 found。

## 正文渲染（给人）

- 关键数字表每行带页码角标：`营业收入 3,375.32 亿元（p12）`。
- `degraded` 值加「⚠ 需复核」。
- 结尾 footer（逐字生成，格式对齐全仓约定）：

```
> 数据来源：{source.title}（报告期 {source.report_date}；PDF 页码见正文角标；Docling 预处理，cache {cache_id}）
```

## 页码语义

- `page` = **PDF 物理页序**（`<!-- page:N -->`），非年报印刷页码（两者常差 2-4 页：封面/目录）。用户问「第 N 页」时先澄清是哪种；默认给 PDF 物理页并在正文注明。
