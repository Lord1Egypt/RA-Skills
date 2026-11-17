# 企业情报接口

## 搜索公司候选

`POST /api/searchCompany`；命令 `search-company --query-json '<JSON>'`，可选 `--session-id`。

请求只含 `companyName/currentPage/pageSize`：名称可为全称、片段、简称或别名，去首尾空格后非空；页码默认 1；每页默认 10、最大 20。不使用 `numPerPage`。

响应 data 保留 `total/currentPage/pageSize/list`，脚本候选为 `rows`：`companyId/companyName/registeredAddress/winningCount/tenderingCount`。次数可为 0，不据此断言没有实际业务。非空候选 1 积分；无匹配为 total 0 和空列表，不扣分。

候选搜索返回独立 `follow_up`，翻页用 `search-company --next --result-set-id RESULT`，可省略或更换会话。缓存不可用时用完整 `--context-json`，复制原成功输出的 `effective_query`，必须包含 `companyName/currentPage/pageSize`，只递增页码。缺项才澄清，不自动重查或猜页码，超过 20 的原页大小先纠正、不静默缩小。完整样例见 [企业能力](capabilities/enterprise-intelligence.md)。不调用项目 next、refine 或 detail；选定主体后分析只传 `companyName`，不得增加 `companyId` 或确认标志。

## 通用规则

每个企业端点只传该端点支持的字段，不共用一套通用入参。合作供应商、合作甲方、采购地区和中标地区支持 `companyName/beginTime/endTime/sortType`；直接和潜在竞对只支持 `companyName/beginTime/endTime`；工商信息只支持 `companyName`；联系电话只支持 `companyName/phoneType/currentPage/numPerPage`。

下列企业分析不保存项目结果集，不能接项目 `next`、`refine`、`detail`。后续查询重新调用 `enterprise` 并带上 `companyName` 和 `kind`。

## kind 与端点

| `kind` | 接口 | 返回内容 |
| --- | --- | --- |
| `partners` | `POST /api/enterprise/partners` | 合作供应商、合作次数、合作金额 |
| `area-distribution` | `POST /api/enterprise/areaDistribution` | 采购地区、合作次数、合作金额 |
| `principals` | `POST /api/enterprise/principals` | 合作甲方、合作次数、合作金额 |
| `winning-area-distribution` | `POST /api/enterprise/winningAreaDistribution` | 中标地区、中标次数、中标金额 |
| `co-bidder-competitors` | `POST /api/enterprise/coBidderCompetitors` | 直接竞争对手、同场竞标次数、中标次数、中标金额、竞争力等级 |
| `potential-competitors` | `POST /api/enterprise/potentialCompetitors` | 潜在竞争对手、中标次数、中标金额、竞争力等级 |
| `business-info` | `GET /api/enterprise/businessInfo` | 工商基本信息 |
| `contacts` | `POST /api/enterprise/contacts` | 联系人、电话类型、联系电话 |

## 逐端点入参

| 字段 | 含义与传参规则 |
| --- | --- |
| `companyName` | 工商/机构登记全称，必填 |
| `beginTime` / `endTime` | 合作、地区和竞对接口可用，`YYYY-MM-DD`；不传时默认近一年 |
| `sortType` | 仅合作供应商、合作甲方、采购地区和中标地区可用，`1` 按次数、`2` 按金额 |
| `currentPage` / `numPerPage` | 仅联系电话支持；页码默认 1，每页默认 30，最大 100 |
| `phoneType` | 仅联系电话支持；`1` 手机、`2` 座机 |

## 返回和展示

合作供应商与电话 API data 含 `rowCount/pageCount/list`；采购地区、合作甲方和中标地区 data 含 `list`，最多返回 30 条；两类竞对 data 含 `list`。工商 API data 为工商字段对象。不要据返回列表推断全量规模。

企业情报脚本返回 `rows`。不同 `kind` 的行字段不同：

- `contacts`：`linkMan`、`phoneType`、`phone`。
- `partners` / `principals`：`companyName`、`cooperationCount`、`cooperationAmount`。
- `area-distribution`：`areaName`、`cooperationCount`、`cooperationAmount`。
- `winning-area-distribution`：`areaName`、`winningCount`、`winningAmount`。
- `co-bidder-competitors` / `potential-competitors`：`competitorName`、`winningCount`、`winningAmount`、`competitivenessLevel`；直接竞争对手还可返回 `coBidderCount`。
- `business-info`：使用 `name/regStatus/companyOrgType/legalPersonName/regCapital/estiblishTime/regNumber/orgNumber/creditCode/industry/businessTerm/approvedTime/regInstitute/regLocation/businessScope`，按中文标签展示。

金额类字段展示为万元。字段缺失时按“未公示”或原始返回为空处理，不补猜。

## 核心概念边界

- 合作供应商：`partners` 的返回企业，适合“某甲方常合作哪些供应商”。
- 合作甲方 / 客户：`principals` 的返回企业，适合“某供应商服务过哪些甲方/客户”。
- 采购地区分布：`area-distribution`，看企业采购合作地区。
- 中标地区分布：`winning-area-distribution`，看企业中标地区。
- 直接竞争对手：`co-bidder-competitors`，面向“同场竞标过的对手”。
- 直接和潜在竞争对手的 `competitivenessLevel` 只按接口原值“高级/中级/低级”展示。接口综合竞标/中标次数和中标金额计算，Skill 不补写等级阈值，也不改成“强/中/弱”。
- 企业联系电话：`contacts`，只有明确追问联系方式时调用。
