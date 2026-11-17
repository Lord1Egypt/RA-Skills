# 查询条件与执行策略

意图、分词、位置、扩词读 [普通项目](project-search.md)；负责参数编译。

模式见[游客规则](../guest-access.md)。

## 何时预检

按能否准确表达判断，不按条件数量决定；同一字段上下限算一项范围。

- **直接调用**：单源可落为组内 OR／组间 AND 加独立字段，各组可有不同位置。明确替换／取消独立字段、修改唯一词组也直接执行，继承未改条件。意向／临期遵循各自全局关键词和位置协议。
- **预检一次**：嵌套 AND/OR、配对分支、跨位置 OR、多源，或 refine 需重组逻辑和分支。能等价合成就一个操作，否则为每个完整分支建操作。
- **澄清或停止**：关键含义／待改对象不明、条件冲突、地区未定位或原条件无法完整恢复；已明确但需要拆查询不属于澄清理由。

每日任务复用已确认方案；单源只改时间或独立字段可直接调用，多源、分支、嵌套仍预检。
选数据源 → 列全部明确条件与分支逻辑 → 安排最少必要操作 → `preflight-complex` → 只执行 `approved_operations`。预检不调 API；冲突记入 `unresolved_conditions`，只停受影响分支。多分支结果和接口总数分别展示，不相加称去重总数。

## 语义计划

提交 `conditions/operations`：条件 `id/type/value`，操作 `id/action/data_source`。不填条件的 `normalized/applies_to`、操作的 `condition_ids/query`。嵌套加 `logic_groups/root_group_id`，组以 `id/operator/condition_ids/group_ids` 引用，根须有效。共同条件省 `operation_ids`；分支条件标对应操作，每支保留必要条件。金额在“和/以及”前一般只属前支，“都/各”才共享。

普通 `keyword_group` 表达 OR，多个条件默认 AND。例：`{"id":"c1","type":"keyword_group","value":{"keywords":["空调","新风"],"matchScopes":[2]}}`。需编译时读 [执行样板](../execution-patterns.md)。

| 语义 type | value / 对应含义 |
| --- | --- |
| `keyword_group` | 普通项目 `{keywords:[...],matchScopes:[...]}`，独立 OR 组 |
| `keyword` | 词数组；普通新查询默认 `[2,9]`；refine 唯一业务组继承位置；采购意向/临期生成自身关键词字段 |
| `project_title/project_id` | 词数组；标题 2，普通编号 `[8,10]`，临期编号 3，意向无编号位置；非公告 ID 直查 |
| `organization_role` | 普通项目 `{role:"purchasing_unit"或"winning_unit"或"agency",keywords:[机构名]}`，对应 4/5/6 |
| `match_scope` | 明确位置数组；普通项目用于一般 keyword 的位置，独立 keyword_group/角色/标题/编号保持自己的位置 |
| `area/organization_type/stage` | 地区 ID 数组、单位类型、普通项目阶段映射 |
| `exclude_words` | 排除词数组，全局生效 |
| `procurement_category/funds_source` | 普通项目分类/资金来源数组 |
| `procurement_method` | 普通项目采购方式数组；临期单值；采购意向不支持 |
| `has_annex/has_agency/registration_status/has_bidding_phone/has_winning_phone` | 普通项目 0 或 1，保留 0 |
| `publish_time` | 项目/采购意向发布时间；秒级与单端只适用于普通项目 |
| `planned_purchase_date/service_expiry` | 采购意向月份 / 临期服务到期日期 |
| `amount_min/amount_max/amount_range` | 元；普通项目为预算或中标金额任一满足的范围，其他源写预计采购/合同金额字段 |
| `contract_period/sort/quantity` | 合同周期、排序、数量，按对应源支持范围 |
| `company_name/enterprise_time/phone_type` | 企业名称、企业统计日期、电话类型；operations 加 `enterprise_kind` |

相对时间附 `current_date`：普通近N月向前同日，意向未来N月从下月起，临期从当天起。复杂细化用 `result_set_id` 继承原条件与金额，可省会话。

同位置复杂词组可等价编译时一次完成。类型与设备配对、不同位置的 OR 不能简单合并；原意明确就分支执行。仅缺条件或冲突的分支停止。不改 AND 为 OR，不用分区列表冒充交集。

## 三类数据源的区别

- 普通项目只发 `keywordGroups`，各组必须有位置；采购意向/临期保留顶层 `keywords/keywordsSearchType/matchScopes`，关键词最多 10 个、排除词最多 10 个。普通项目不自创关键词组数或组内词数上限。
- 普通/临期支持 1–10，采购意向仅 `[1,2,8,10]`：1 标题+正文+附件；2 标题；3 编号；4 采购单位；5 中标单位；6 代理；7 联系人；8 正文；9 标的物；10 附件。“全部”不包含所有十种专用索引，但正文和附件可以含这些信息。
- 意向/临期 `keywordsSearchType`：1 任一、2 全部，位置是全局共享，独立词位置不能套普通分组协议。
- 结构化地区、时间、金额、单位类型、阶段、分类、方式、资金和二值筛选不混进关键词。支持位置检索不意味着详情返回对应字段。

## 业务判断与编译边界

角色、粒度、召回见 [普通项目](project-search.md)。角色位置不是公司 ID 精确过滤；不得因用户原话未说“标题”就删默认位置。核实标准由 Agent 保留，不填未知字段；预检通过不等于业务满足。

意向/临期省略位置默认标题+正文。意向不套用角色/编号位置，无法等价表达时说明限制。“定向采购”按原语义对应邀请、谈判磋商、单一来源；普通一次传方式 `[1,2,3]`，临期单值方式才分支。无有效关键词先补充。

## 取消条件

普通 `refine` 取消条件的 value 用 null，如 procurement_method、has_annex。批准 patch 原样传入；未改继承，回第一页。

可取消地区、排除词、阶段、单位类型、分类、方式、资金、有无属性、报名、金额、排序／数量（恢复默认）。不能清空必填关键词／位置或用空时间冒充不限。清除仅用于明确普通 refine 的 AND，不进入 OR／NOT。

## 地区、金额与停止

地区按 [地区规则](../../SKILL.md#地区) 确定参数。七地区先按入口处理限制；其他地区区县第一次只查区县；零结果需用户同意才扩大市级，其他条件不变；未回复或已有结果时不扩大。

采购意向两组时间各最多 3 年，默认预计采购时间，仅“最近发布”用公告日期；临期按服务到期时间，最多 5 年，不发 `beginTime/endTime`。标讯最多 3 年，单端补月，“以来”传双端，不支持不限时间。超限请用户调整，不截短或拆分；续查和预检同样校验。

金额元，500 万写 5000000。新/改正金额小于 10000 时，Agent 首次自行核对原话换算；正确保留，不自动改下限。继承已执行金额不额外确认单位。金额/时间逆序不交换，澄清冲突。

首页 1；新查询未指定数量不主动传每页数。三源默认 30、最大 100；公司默认 10、最大 20，用 `pageSize`。续查精确承接页码/页大小，完整/缓存超限先纠正、不静默缩小。“最新”排序 1，“最相关”6；普通项目不承诺按金额全量排序。状态失效按 [连续追问](follow-up-and-results.md) 恢复；对象、源、条件、页码仍不明才停止。
