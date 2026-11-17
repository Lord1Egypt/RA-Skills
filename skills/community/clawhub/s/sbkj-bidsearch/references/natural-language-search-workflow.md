# 自然语言搜索与条件编译

## 目标

把用户自然语言转换为普通搜索接口可接受的结构化参数。普通搜索接口不是自然语言接口，不能让 Agent 直接猜测所有字段。

## 调用链

```text
userQuery
  -> aiSearchSubmitPolling
  -> requestKey / status
  -> status=completed
  -> BidSearchCondition
  -> searchProjectApi
  -> 分页列表
```

## AI重写接口

端点：`/aiSearchSubmitPolling`

请求：

```json
{"userQuery":"湖北近30天物业服务，工程建筑中标结果，金额500万以上"}
```

结果中的关键字段：

- `data.requestKey`：处理任务标识；
- `data.status`：`processing`、`search_rewrite_done`、`area_code_done`、`industry_done`、`completed`、`failed`；
- `data.searchCondition`：日期、企业、主题、项目分类、采购分类、金额、分包标识；
- `data.areaCode`：省、市、区县编码；
- `data.industryCodes`：一级、二级、三级行业编码及路径名称；
- `data.errorMsg`：失败原因。

文档只明确说明需要使用 `requestKey` 轮询，没有明确轮询请求的具体参数格式。实现前必须确认这一点；不得猜测为重复提交 `userQuery` 或自行发明参数。

## 条件转换

| AI字段 | 普通搜索字段 | 处理规则 |
| --- | --- | --- |
| `searchStartTime` | `startDate` | 补 `00:00:00` |
| `searchEndTime` | `endDate` | 补 `23:59:59` |
| `subjects` | `keyword` | 默认 `|` 表示 OR；同时出现则用空格 |
| `enterpriseName` | `companyName` | 保留企业名称模糊查询语义 |
| `projectClassIds` | `projectClassID` | 多值英文逗号连接 |
| `purchaseTypeId` | `purchaseTypeID` | 直接映射 |
| `projectMoneyMin` | `projectMoneyMin` | 人民币元 |
| `projectMoneyMax` | `projectMoneyMax` | 人民币元 |
| `areaCode` | `areaCode` | 直接映射并校验六位编码或全国 `0` |
| `industryCodes` | `industryCode` | 分层合并去重 |
| `subcontractFlag` | 无明确字段 | 必须提示未透传 |

普通搜索默认补充：`pageId=1`、`pageNumber` 不超过 50、`searchType=1`、`searchMode=1`、`projectClassID=-100`、`purchaseTypeID=-100`、`fileFlag=-1`。实际项目应以用户已有配置和接口文档为准。

## 何时改用AI专用搜索

`SearchProjectForAI` 可用于简单自然语言快速查询或普通搜索条件编译暂不可用时的兜底，但要向调用方说明它是简化路径。复杂地区、行业、金额、项目分类、附件条件应优先使用“AI重写→普通搜索”。
