# 违规案例周报字段参考

## 目录

1. 时间和数量口径
2. 字段来源
3. 质量状态
4. Markdown 版式
5. 多页合并

## 1. 时间和数量口径

- 日期字段：`LC_ViolatiEventNew.LatestInfoPublDate`。
- 展示名称：公告日期/发布时间。
- 区间：`window_start 00:00:00 <= LatestInfoPublDate < window_end+1日 00:00:00`。
- `case_count`：主表事件数。
- `company_count`：去重证券代码数。
- `party_count`：各案例内按 `PartyName` 归并后的处罚对象数；同一对象的多种处罚类型不重复计数。

## 2. 字段来源

| 输出字段 | 聚源来源 | 说明 |
|---|---|---|
| `company.stock_code` | `InvolvedSecurity` | 股票代码 |
| `company.short_name` | `SecuMain.SecuAbbr` | 公司简称 |
| `company.full_name` | `SecuMain.ChiName` | 公司名称 |
| `company.bankuai` | `ListedSector + SecuMarket` | 不按代码前缀猜测 |
| `trigger_institutions` | `PenalOrgs/PenalOrg` | 通过 `LB=1978` 解码 |
| `violation_matters` | `EventContent/ViolationStatement` | 违规事实原文及分项 |
| `event_level_types` | `TranslatedCodeLabels` | 事件级规范违规类型 |
| `penalty_situation` | `EventContent/PenalStatement` | 案例整体处罚段 |
| `admin_numbers` | `AdminNumbers` | 处罚文号 |
| `case_penalties` | `LC_ViolatiParty` | 同一案例内按 `PartyName` 归并，多种处罚类型合并到同一对象 |
| 对象身份 | 若处罚对象名称与本案公司简称或全称一致，则为“上市公司”；否则取最终展示的 `violation_matters.text` 中、处罚对象姓名附近的原文职务 | 非上市公司对象未出现职务时显示“——”；不得从 `PartyType`、主体信息或处罚段补写 |
| 对象违规类型 | `ViolationStatement` + 事件类型 | 仅事件级时标记 `event_level` |
| 对象处罚类型 | `PenalTypeNew/PenalType` | 通过 `LB=2475` 解码 |
| 处罚期限 | `PenalStatement` 明示期限；其明确存在期限语义时可结合 `BeginDate/EndDate` | 仅有日期值但原文无“期限/市场禁入/不得担任/限制”等期限语义时不视为处罚期限；未载明时为 `null` |
| 法规依据 | `ViolationClauses/ViolationClause/EventContent` | 不外部补法条 |

板块映射：

| 条件 | 板块 |
|---|---|
| `ListedSector=7` | 科创板 |
| `ListedSector=6` | 创业板 |
| `ListedSector=8` | 北交所 |
| `ListedSector=1, SecuMarket=90` | 深主板 |
| `ListedSector=1, SecuMarket=83` | 沪主板 |

## 3. 质量状态

### `verified`

公司映射、触发机构、违规事项、处罚情况、对象明细和法规依据均已取得，且无冲突。

### `partial`

聚源原字段或可解析正文缺少部分信息。查看 `missing_fields`，保留案例并明确缺失，不自行补齐。

### `review_required`

事件级与对象级字段冲突、代码无法解码，或身份/期限/法规结构无法可靠对应。保留原字段并提示人工复核。

### `source_degraded`

聚源主表可能查询成功，但派生结构化缓存不可用。仍可返回数据库字段；违规事实、处罚段、身份或期限的派生完整度可能下降。该状态仅用于内部校验和机器数据；对外交付的 Word 周报不展示结构化缓存、降级生成、质量状态、完整度、缺失字段或复核提示。

## 4. Markdown 版式

固定顺序：

1. 标题、统计区间和时间口径；
2. 案例数、公司数、对象数、触发机构和违规类型概览；
3. 逐案例展示公司信息、发布时间和触发机构；
4. 违规事项；
5. 处罚情况；
6. 案例处罚情况表；
7. 法规依据；
8. 数据质量、缺失字段和降级说明（仅 Markdown/JSON；Word 不显示）。

案例处罚情况表基础列：

```text
处罚对象名称 | 对象身份 | 违规类型 | 处罚类型
```

仅当该案例至少一个处罚对象存在非空 `penalty_term` 时，追加“处罚期限”列；否则整列隐藏。

## 5. 多页合并

1. 以第一页 `report_meta` 和全局 `total` 为准。
2. 逐页收集 `cases[]`。
3. 以 `case_id` 去重。
4. 按 `publish_time DESC, case_id DESC` 排序。
5. 重新统计公司数、对象数和质量状态；不要把单页 `statistics` 直接相加，避免去重公司重复计数。
6. 若任一页 `source_degraded=true`，整份周报标记为降级。
