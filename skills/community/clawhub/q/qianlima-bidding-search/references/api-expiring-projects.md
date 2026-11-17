# 临期项目接口

## 搜索

`POST /api/search/expiring`

查询即将到期的周期性项目基础信息，用于早期商机（合同到期、续约机会）挖掘。临期项目主要面向已有中标结果、合同周期、服务开始时间和服务到期时间的项目。

请求体不能为空，且必须包含至少一个非空 `keywords`；空请求体或不符合必填约束时返回参数错误（错误码 `10004`），不会进入额度校验或搜索流程。

### 入参字段

- `keywords`：关键词数组，必填。最多 10 个，且至少包含一个非空关键词，用于检索项目、产品、服务、行业词等。
- `keywordsSearchType`：关键词匹配方式。`1` 表示任一关键词命中；`2` 表示所有关键词同时命中，默认 `1`。
- `excludeWords`：排除词数组，可选。最多 10 个，命中任意排除词的公告会被过滤掉。
- `matchScopes`：匹配范围列表，可选。控制关键词匹配的位置，不传默认匹配标题+正文。与普通标讯共用匹配范围枚举（采购意向仅支持其中 1、2、8、10），支持 `1`（全部：标题+正文+附件）、`2`（标题）、`3`（项目编号）、`4`（采购单位）、`5`（中标单位）、`6`（代理机构）、`7`（联系人）、`8`（正文）、`9`（标的物）、`10`（附件），支持组合多选。格式为数字数组，枚举见 `enums.md`。
- `beginServiceExpireTime`：服务到期时间范围开始日期，可选。格式 `yyyy-MM-dd`。只有开始和结束日期同时有值才会按该范围查询。若服务到期时间范围完全不传，默认查询未来 90 到 180 天。
- `endServiceExpireTime`：服务到期时间范围结束日期，可选。格式 `yyyy-MM-dd`。只有开始和结束日期同时有值才会按该范围查询。若服务到期时间范围完全不传，默认查询未来 90 到 180 天。
- `contractPeriodType`：原合同周期类型，可选，枚举见 `enums.md`。传该字段时，会转换为对应的合同周期天数范围查询。
- `areaIds`：地区 ID 数组，可选。支持省、市、区/县，取值来自 `area.json`；不传时按全国查询。 先按 [地区规则](../SKILL.md#地区) 取得已确定参数；`[]` 为显式取消筛选，运行时移除该字段，未知编号、布尔值与小数不接受。
- `beginContractAmount`：合同金额下限，可选，单位为元。
- `endContractAmount`：合同金额上限，可选，单位为元。
- `procurementMethod`：原招标方式，可选，枚举见 `enums.md`。
- `purchasingUnitTypes`：采购单位类型数组，可选，枚举见 `enums.md`。
- `sortType`：排序字段，可选。临期项目支持 `1`（时间倒序）、`2`（综合排序）、`6`（相关性倒序），默认值为 `2`。
- `currentPage`：页码，必传，从 1 开始。
- `numPerPage`：每页数量，可选。默认 30，最大 100。

服务到期起止范围最多 5 个日历年，包含周年边界日，闰日周年落在非闰年时取 2 月末日；这是查询跨度，不是仅能查询距今 5 年内的数据，也不是 `contractPeriodType` 的合同期限。超限由本地返回 `TIME_SPAN_EXCEEDED`，不会执行搜索；说明上限并请用户调整，不静默截短或自动拆分。单端条件仍要求补齐另一端，完全不传的默认范围不变。

合同周期类型说明：

| 类型值 | 含义 | 周期范围 |
| --- | --- | --- |
| `1` | 1年以下 | 小于 360 天 |
| `2` | 1年 | 360-550 天 |
| `3` | 2年 | 551-900 天 |
| `4` | 3年 | 901-1300 天 |
| `5` | 5年 | 1400-2000 天 |
| `6` | 5年以上 | 大于 2001 天 |

### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `rowCount` | integer | 符合条件的项目总数。 |
| `pageCount` | integer | 按当前每页数量计算出的总页数。用于判断是否还有下一批。 |
| `list` | array | 当前页返回的临期项目列表。 |

临期项目卡片字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | integer | 项目唯一标识。 |
| `title` | string | 项目名称，也可理解为公告标题。 |
| `areaName` | string | 项目所属地区，通常为"省-市-区/县"格式。 |
| `purchasingUnit` | string | 招标单位、采购单位或发布项目的单位。 |
| `publishTime` | string | 发布时间，格式通常为 `yyyy-MM-dd`。 |
| `serviceStartTime` | string | 服务开始时间。 |
| `serviceExpireTime` | string | 服务到期时间。 |
| `contractAmount` | string | 合同金额，单位为元。为空表示未公示。 |
| `contractPeriod` | string | 合同周期，表示在位供应商的服务签约时长。 |
| `budgetAmount` | string | 项目招标预算，单位为元。为空表示未公示。 |
| `winningBidderUnit` | string | 中标单位，即当前合同周期内的在位供应商。 |
| `url` | string | 千里马项目详情页链接。用于查看正文和附件。 |

## 详情

`GET /api/expiring/detail/{id}`

已知真实临期公告 ID 直接 `detail --id ID --result-type expiring_project`，不要求搜索名单、会话或有效/可写缓存；来源链接加 `--fields sourceUrl`。序号/标题先由对应结果唯一定位；来源不明只澄清，不尝试其他接口。

### 入参字段

- `id`：公告 ID，路径参数。用于精确定位临期项目。

### 返回字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | integer | 项目唯一标识。用于确认详情返回的是当前结果中的同一项目。 |
| `title` | string | 项目名称，也可理解为公告标题。 |
| `areaName` | string | 项目所属地区，通常为"省-市-区/县"格式。 |
| `purchasingUnit` | string | 招标单位、采购单位或发布项目的单位。 |
| `publishTime` | string | 发布时间。 |
| `serviceStartTime` | string | 服务开始时间。 |
| `serviceExpireTime` | string | 服务到期时间。 |
| `contractAmount` | string | 合同金额，单位为元。为空表示未公示。 |
| `contractPeriod` | string | 合同周期，表示在位供应商的服务签约时长。 |
| `budgetAmount` | string | 项目招标预算，单位为元。为空表示未公示。 |
| `purchasingUnitLinkName` | string | 招标单位或采购单位联系人。 |
| `purchasingUnitLinkPhone` | string | 招标单位或采购单位联系方式。 |
| `winningBidderUnit` | string | 中标单位，即当前合同周期内的在位供应商。 |
| `winningBidderUnitLinkName` | string | 中标单位联系人。为空表示未公示。 |
| `winningBidderUnitLinkPhone` | string | 中标单位联系方式。为空表示未公示。 |
| `agencyUnit` | string | 代理机构。 |
| `agencyUnitLinkName` | string | 代理机构联系人。 |
| `agencyUnitLinkPhone` | string | 代理机构联系方式。 |
| `url` | string | 千里马项目详情页链接。用于查看正文和附件。 |
| `targetKeywords` | array | 标的物关键词列表。面向用户时可称为“标的物”。 |


检索匹配范围支持 1–10，不表示详情会返回这些位置的字段。临期项目可取自身详情和 `/api/sourceUrl/{id}` 来源链接，不调用普通项目正文、附件或时间线接口。公开临期详情页可展示正文和附件，但不等于存在临期独立资源 API。
