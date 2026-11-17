<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: zlbx-bidding/2.5.0
X-Skill-Package: tender-bid-tracker/1.0.0
X-Skill-Source: clawhub/bailianai
```
<!-- request-identity:end -->

# 工商工具速查

POST `https://mcp-server.zhiliaobiaoxun.com/api_v2/` + 工具名。所有请求包括免费余额及展示回执均使用当前包规定的完整请求头；不要只带Key和X-Client。

```text
X-API-Key: 当前已配置的平台Key
X-Client: zlbx-bidding/2.5.0
X-Skill-Package: tender-bid-tracker/1.0.0
X-Skill-Source: clawhub/bailianai
Content-Type: application/json
```

另两个固定头 `X-Skill-Package`、`X-Skill-Source` 见本文件的请求身份块。不向客户端分发供应商Token。

五个工商接口成功有数据每次/每页 **3积分**，无结果和失败不扣费。有效会员先扣当日额度，不足时按用户的钱包续扣设置执行。只调用用户需要的能力。

## 主体参数

主体参数只使用 `company_name`：准确企业全称、统一社会信用代码或注册号。不要传入平台主体ID；公共响应不返回数据源内部ID，也不通过额外接口查找这类ID。
简称通过免费主体库消歧，有多个候选时返回 `QUERY_EMPTY` 和候选列表，需用户确认，不付费猜测。

## get_company_registry — 工商基本信息

```json
{"company_name":"北京百度网讯科技有限公司"}
```

返回 `query`、`matched_by`（exact/bidding_index/identifier）、`matched_name`、`company`、`other_candidates`。
`company` 包括：

- `name`、`unifiedSocialCreditCode`、`businessRegistrationNumber`、`organizationCode`、`organizationType`、`legalRepresentative`。
- `registeredCapital`、`paidInCapital`：数值单位统一为万（元/亿按单位换算，币种不变），未知单位为null；币种见 `registeredCapitalCurrency` / `paidInCapitalCurrency`。`registeredCapitalDetail` / `paidInCapitalDetail` 包含raw/amount/unit/currency，不擅自汇率换算。
- `establishmentDate`、`approvalDate`、`operatingPeriod`（startDate/endDate，缺失日期为空）。
- `businessStatus`、`registrationAuthority`、`provinceCode`（省份简称码）、`city`、`area`、`address`、`industry`、`businessScope`、`usedName`、`nickNames`、`staffNumRange`。
- `sourceUpdatedAt`：源数据更新时间原始毫秒时间戳，缺失时不猜测。

本期工商基本信息接口不含联系方式、商标或官网。使用自有库查询时应标明数据口径与更新时间，不将历史信息称为实时数据。

## 四个分页接口

```json
{"company_name":"北京百度网讯科技有限公司","page_num":1,"page_size":20}
```

每次只查一页；`page_size`为1至20，默认20；`page_num`从1开始。返回 `total`、`items`、`page_num`、`page_size`、`has_more`、`query`、`matched_by`、`matched_name`、`queried_identifier`。以信用代码/注册号查列表时 `matched_name` 可为空，不额外采购基本信息以填名。

| 工具 | items字段 |
|---|---|
| `get_company_shareholders` | name/type/typeName、subscribedCapitalRecords/paidInCapitalRecords历史记录数组（amount/method/date/percent）、firstShareholdingDate、hkCapital |
| `get_company_branches` | name/businessStatus/legalRepresentative/registeredCapital（数值，单位万）/registeredCapitalCurrency/registeredCapitalDetail/establishmentDate/provinceCode |
| `get_company_investments` | 分支通用字段，加unifiedSocialCreditCode/amount/amountSuffix/percent/subscriptionDate/paidInDate/organizationType/businessScope |
| `get_company_changes` | changeDate/changeItem/before/after/recordCreatedDate |

股东额外参数 `source=1`（工商登记，默认）或 `source=2`（最新公示）；响应 `shareholder_source` / `shareholder_source_name` 标明口径。type=1企业、2自然人、3其他。出资数组可能有多条历史记录，不能求和或认定首条就是当前比例。
分支不承诺信用代码；投资不等于控股；变更日期不等于记录创建日期。司法风险及复杂股权穿透本期未开放。

## 来源、时间与缓存

对外来源统一写“知了标讯工商数据”，同时注明 `shareholder_source_name` 的工商登记/最新公示口径。供应商名称、品牌、域名、内部来源标识及其翻译名都不出现在对话、报告、表格、链接或错误解释中；不得从ID字段名称反推出供应商品牌。公共响应不返回数据源内部ID，不自行改名为平台ID。

响应包含 `source`（平台工商业务标识 `company_registry`，不展示技术值）、`data_freshness`（`snapshot` 为取得的数据快照，`static` 为静态库，均不保证实时）、`cached`、`fetched_at`（原始取数时间）、`queried_at`（本次查询时间）。缓存默认关闭；启用后命中仍按成功查询3积分计费。取数时间不等于源数据更新时间。
供应商故障不冒充空结果，不自动重试超时请求。

## 股东结果解读边界

旧响应只在新字段缺失时读取 `subscribedCapital` / `paidInCapital` 历史数组别名；不是企业详情中的资本数值，不能重复读取并累加。

- 默认给查询口径、`total`、本页条数和记录表。只有已返回记录才可写进表；页内自然人数量写“本页”，未查完不能说“全部仅有”。未返回的股东名称、类型和比例均未知。
- `subscribedCapitalRecords`/`paidInCapitalRecords` 多条历史记录逐条列金额、单位、日期及对应比例；不能取首条、累加历史出资或按日期猜成当前持股比例。记录比例列标题用“出资记录比例”；无法确认当前比例时明确说明接口记录未给出可确认的当前持股比例。
- 不根据名称、注册地址、出资日期或单页比例推断持股平台、创始人间接持股、控制权、所属集团、投资人关系和融资轮次。不把“没有超过50%”改写成“无控股股东”；未取得股权穿透数据就说明无法判断。
- 合计只使用同口径、同时间、同单位且未重复的已查询记录，用代码或计算工具求和并保留精度。不用 `100%-本页合计` 填补未查询股东的比例，不猜“其余均不足1%”。不具备可比记录时不计算总比例。
- 不使用Web搜索或模型记忆补齐未返回股东、投资人关系和控制权。需要更多字段或下一页时先说明范围及每页3积分，由用户决定。

## 招投标补充（按需）

用户只问股东时只调 `get_company_shareholders`。允许每会话首次免费余额检查、必要的免费主体消歧及展示回执；不付费联查基本信息、画像、中标次数、联系人、投资、分支、变更或风险。单次只查用户指定的一页，不自动翻页或故障重试。

| 工具 | 场景 | 积分 |
|---|---|---|
| get_company_profile | 招标/中标次数，company传全称 | 1 |
| search_company | 免费主体候选查询 | 0 |
| get_company_contacts | 招投标联系人；按原返回隐私层级展示 | 5 |
| query_bids_advanced | 中标记录，match_modes=["winner"] | 2 |
| get_company_partners | 合同客户/供应商，与企业股东不同 | 3 |

返回url原样展示，不删改免登录签名；联系人工具的脱敏号码不得自行补全。

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: tender-bid-tracker/1.0.0
X-Skill-Source: clawhub/bailianai
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
