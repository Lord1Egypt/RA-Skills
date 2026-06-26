---

name: china-company-search-wendaoyun
description: 问道云企业信息查询工具，支持通过问道云 API 查询企业基本信息、经营信息、财务信息、舆情信息、企业各类风险指标等功能，当用户需要查询企业相关信息时触发。

---

# 问道云 (WenDaoYun) 企业信息查询

## 配置说明

1. 获取 API Key：打开 <https://open.wintaocloud.com/home，登录后在个人中心或开发者中心获取>
2. 在 config.json 文件中配置 WENDAOYUN_API_KEY, 例如："WENDAOYUN_API_KEY": "your_api_key"
3. 每日调用额度 200 次

> ⚠️ API Key 属于敏感信息，请妥善保管，不要泄露给他人。发现泄露请及时在问道云开放平台作废。

***

## 查询流程

前提：确保在 config.json 文件中配置了 WENDAOYUN_API_KEY ,读取这个文件获取这个 WENDAOYUN_API_KEY的值进行接口调用认证
所有查询都遵循：搜索企业 → 用户确认 → 查询详情
情况一：
第 1 步.用户提示(如"查询XX企业)
第 2 步.调用 `fuzzy-search-org` 搜索企业，列出前 5 条；如果 total 超过 5 条，告知用户可以"查下一页或指定页码"

情况二:
第 1 步：用户提出需求（如"查XX的行政处罚"）
第 2 步：调用 `fuzzy-search-org` 搜索企业，列出前 5 条；如果 total 超过 5 条，告知用户可以"查下一页或指定页码"
第 3 步：**必须等待用户确认具体企业**，不要跳过！
第 4 步：调用对应详细信息接口

***

## 接口速查

| 用户说法              | 接口                            | 状态 |
| ----------------- | ----------------------------- | -- |
| 查询 XX 企业          | `fuzzy-search-org`            | ✅  |
| XX 的行政处罚          | `get-punishments`             | ✅  |
| XX 是不是老赖 / 失信被执行人 | `get-dishonest`               | ⏳  |
| XX 经营异常           | `get-abnormal`                | ✅  |
| XX 股权质押           | `get-equity-pledge`           | ✅  |
| XX 环保处罚           | `get-environmental-penalties` | ✅  |
| XX 欠税公告           | `get-tax-notice`              | ✅  |
| XX 简易注销           | `get-simple-cancel`           | ✅  |
| XX 土地抵押           | `get-land-mortgage`           | ✅  |
| XX 清算信息           | `get-clear-info`              | ✅  |
| XX 公示催告           | `get-public-inform`           | ✅  |
| XX 劳动仲裁送达报告       | `get-labour-arb`              | ✅  |
| XX 担保信息           | `get-gua-info`                | ✅  |
| XX 开庭公告           | `get-open-court-arb`          | ✅  |
| XX 税收违法           | `get-tax-violation`           | ⏳  |
| XX 债券信息           | `get-bond-info`               | ✅  |
| XX 海关进出口信用        | `get-import-export-credit`    | ✅  |
| XX 被执行信息          | `get-execute-info`            | ✅  |
| XX 失信被执行          | `get-dishonest-debtors`       | ✅  |
| XX 股权冻结           | `get-share-blocking`          | ✅  |
| XX 限制高消费          | `get-consumption-limits`      | ✅  |
| XX 裁判文书           | `get-judge-doc`               | ✅  |
| XX 破产重整           | `get-bankruptcy-regroup`      | ✅  |
| XX 司法拍卖           | `get-judicial-sale`           | ✅  |
| XX 开庭公告           | `get-open-court`              | ✅  |
| XX 立案信息           | `get-case-filing`             | ✅  |
| XX 诉前调解           | `get-pre-mediate`             | ✅  |
| XX 询价评估           | `get-inq-eval`                | ✅  |
| XX 送达公告           | `get-deliver-notice`          | ✅  |
| XX 终本案件           | `get-cases-terminated`        | ✅  |
| XX 限制出境           | `get-exit-ban`                | ✅  |
| XX 法院公告           | `get-judicial-notice`         | ✅  |
| XX 风险信息           | `get-risk`                    | ✅  |

***

## API 基础信息

- **Base URL**: `https://h5.wintaocloud.com/prod-api/api/invoke`
- **认证**: Header 填写(`Bearer后面一定要追加一个空格`): `Authorization: Bearer {api_key}`
- **请求方式**: GET
- **URL 拼接方式**: `Base URL + / + 接口名称 + ? + 参数`
  - Base URL = `https://h5.wintaocloud.com/prod-api/api/invoke`
  - 接口名称 = 各接口的名称（如 `fuzzy-search-org`、`get-equity-pledge`），直接拼接在路径中，**不是** query 参数
  - 有参数时拼接在 `?` 后，格式为 `key=value&key=value`
  - 正确示例：`https://h5.wintaocloud.com/prod-api/api/invoke/fuzzy-search-org?searchKey=XXX&pageNum=1&pageSize=5`
- **金额字段**: punishAmount、assureAmount、mortgageAmount 等单位为**分**，展示时÷100换算为元
- **金额字段可能返回 null，展示时应显示"未知"而非 null**

***

## fuzzy-search-org - 企业模糊搜索

**请求参数**：

| 参数        | 类型      | 必填 | 说明             |
| --------- | ------- | -- | -------------- |
| searchKey | string  | 是  | 关键词（最少 2 字符）   |
| pageNum   | integer | 否  | 页码，默认 1，每页 5 条 |

**响应字段**：

| 字段           | 类型     | 说明           |
| ------------ | ------ | ------------ |
| orgId        | string | 企业ID         |
| orgName      | string | 企业名称         |
| usCreditCode | string | 统一社会信用代码     |
| incDate      | string | 成立日期         |
| legalName    | string | 法定代表人        |
| status       | string | 企业状态（存续/在业等） |
| address      | string | 企业地址         |

**使用说明**：结果可能很多（如"腾讯"返回近万条），始终只展示前 5 条，展示时必须包含序号、企业全称、法定代表人、成立日期、状态。必须询问用户确认。

***

## get-punishments - 行政处罚

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段           | 类型      | 说明                    |
| ------------ | ------- | --------------------- |
| punishNo     | string  | 行政处罚决定文书号             |
| illegalFact  | string  | 违法事实                  |
| punishResult | string  | 处罚结果                  |
| unitName     | string  | 作出处罚单位名称              |
| punishTime   | string  | 处罚日期                  |
| punishAmount | integer | 处罚金额（单位：分，换算需÷100才是元） |

***

## get-abnormal - 经营异常

**请求参数**：

| 参数        | 类型     | 必填 | 说明   |
| --------- | ------ | -- | ---- |
| searchKey | string | 是  | 企业全称 |

**响应字段**：
\| 字段 | 类型 | 说明 |
\|------|------|------|------|
\| department | string | 列入部门 |
\| abnormalDate | string | 列入日期 |
\| abnormalReason | string | 列入原因 |
\| removeDepartment | string | 移出部门 |
\| removeDate | string | 移出日期 |
\| removeReason | string | 移出原因 |

***

## 以下接口请求参数均为

| 参数        | 类型      | 必填 | 说明             |
| --------- | ------- | -- | -------------- |
| searchKey | string  | 是  | 企业全称           |
| pageNum   | integer | 否  | 页码，默认1         |
| pageSize  | integer | 否  | 每页条数，默认10，最大20 |

### get-equity-pledge - 股权质押

**响应字段**：

| 字段              | 类型     | 说明                    |
| --------------- | ------ | --------------------- |
| pledgeeNameList | list   | 质权人列表 \[{name, type}] |
| riskState       | string | 股权质押状态                |
| publicTime      | string | 公告日期                  |
| pledgeName      | string | 出质人名称                 |

### get-environmental-penalties - 环保处罚

**响应字段**：

| 字段                | 类型      | 说明         |
| ----------------- | ------- | ---------- |
| punishBehavior    | string  | 违法事实       |
| punishAmount      | integer | 处罚金额（单位：分） |
| punishInstitution | string  | 作出处罚单位名称   |
| publishDate       | string  | 发布日期       |
| punishDate        | string  | 处罚日期       |
| punishNumber      | string  | 环保处罚决定书文号  |

### get-tax-notice - 欠税公告

**响应字段**：

| 字段               | 类型      | 说明              |
| ---------------- | ------- | --------------- |
| taxDepartment    | string  | 发布单位            |
| publishDate      | string  | 发布日期            |
| taxCategory      | string  | 欠税税种            |
| newOwnTaxBalance | integer | 当前发生新欠税余额（单位：分） |
| ownTaxBalance    | integer | 欠税余额（单位：分）      |

### get-simple-cancel - 简易注销

**响应字段**：

| 字段            | 类型     | 说明                                              |
| ------------- | ------ | ----------------------------------------------- |
| result        | string | 简易注销结果                                          |
| publicDate    | string | 公告日期                                            |
| regInstitute  | string | 登记机关                                            |
| usCreditCode  | string | 统一社会信用代码                                        |
| orgName       | string | 企业名称                                            |
| objectionList | list   | 异议信息 \[{objectionDate, content, objectionName}] |
| promiseUrl    | string | 全体投资人承诺书Url                                     |

### get-land-mortgage - 土地抵押

**响应字段**：

| 字段                | 类型      | 说明         |
| ----------------- | ------- | ---------- |
| mortgageAmount    | integer | 抵押金额（单位：分） |
| mortgageBeginTime | string  | 抵押开始日期     |
| mortgageEndTime   | string  | 抵押结束日期     |
| mortgageArea      | string  | 抵押面积       |
| address           | string  | 地址         |

### get-public-inform - 公示催告

**响应字段**：

| 字段               | 类型      | 说明     |
| ---------------- | ------- | ------ |
| publishAuthority | string  | 发布机关名称 |
| billType         | string  | 票据类型   |
| faceValue        | integer | 票面金额   |
| publishDate      | string  | 公告日期   |
| orgName          | string  | 企业名称   |
| billNumber       | string  | 票据号    |

### get-labour-arb - 劳动仲裁送达报告

**响应字段**：

| 字段             | 类型     | 说明   |
| -------------- | ------ | ---- |
| publishDate    | string | 公告日期 |
| applicantName  | string | 原告名称 |
| respondentName | string | 被告名称 |
| caseNo         | string | 案号   |

### get-gua-info - 担保信息

**响应字段**：

| 字段                | 类型      | 说明                    |
| ----------------- | ------- | --------------------- |
| assureAmount      | integer | 担保金额（单位：分，换算需÷100才是元） |
| assureBeginTime   | string  | 担保起始日                 |
| assureEndTime     | string  | 担保终止日                 |
| assureTerm        | string  | 担保期限（年）               |
| assureName        | string  | 担保方式                  |
| currency          | string  | 币种                    |
| performState      | string  | 履行状态                  |
| isRpt             | string  | 是否关联交易                |
| assuredEntityName | string  | 被担保方名称                |
| assureEntityName  | string  | 担保方名称                 |
| reportDate        | string  | 报告期                   |
| transactionDate   | string  | 交易日期                  |
| assureDealTime    | string  | 处理日期                  |

### get-open-court-arb - 开庭公告（劳动仲裁）

**响应字段**：

| 字段              | 类型     | 说明     |
| --------------- | ------ | ------ |
| courtOpenTime   | string | 开庭日期   |
| caseReason      | string | 案由     |
| plaintiffName   | string | 原告名称   |
| defendantName   | string | 被告名称   |
| caseNo          | string | 案号     |
| undertakeDept   | string | 承办部门名称 |
| dataOpenCourtId | long   | 开庭公告ID |

### get-bond-info - 债券信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段         | 类型     | 说明                   |
| ---------- | ------ | -------------------- |
| issueScale | string | 发行规模（亿元）             |
| remainTerm | string | 剩余期限（年）              |
| bondTerm   | string | 债券期限（年）              |
| expireDate | string | 到期日期（如 "2022-01-01"） |
| issueDate  | string | 发行日期（如 "2022-01-01"） |
| bondType   | string | 债券类型                 |
| bondName   | string | 债券简称                 |
| bondNo     | string | 债券编号                 |

### get-import-export-credit - 海关进出口信用信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段            | 类型     | 说明                   |
| ------------- | ------ | -------------------- |
| identifyCode  | string | 认证证书编码               |
| creditLevel   | string | 信用等级                 |
| eCommerceType | string | 跨境贸易电子商务类型           |
| industryType  | string | 行业种类                 |
| validityDate  | string | 报关有效期                |
| annualReport  | string | 年报情况                 |
| cancelFlag    | string | 海关注销标志               |
| specialArea   | string | 特殊贸易区域               |
| economicArea  | string | 经济地区                 |
| area          | string | 行政地区                 |
| regCode       | string | 海关注册编码               |
| regDate       | string | 注册日期（如 "2022-01-01"） |
| busType       | string | 经营类别                 |
| regGov        | string | 注册海关                 |

### get-execute-info - 被执行信息（强制执行）

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段                   | 类型      | 说明                    |
| -------------------- | ------- | --------------------- |
| dataExecuteId        | string  | 被执行人ID                |
| registerDate         | string  | 立案日期                  |
| caseNo               | string  | 案号                    |
| executeOrgName       | string  | 执行法院名称                |
| executeAmount        | integer | 执行标的（单位：分，换算需÷100才是元） |
| possibleExecutorName | string  | 疑似申请执行人名称             |

### get-dishonest-debtors - 失信被执行信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段                  | 类型      | 说明                    |
| ------------------- | ------- | --------------------- |
| caseNo              | string  | 案号                    |
| executeCourtName    | string  | 执行法院名称                |
| performStatus       | string  | 被执行人履行情况              |
| releaseTime         | string  | 发布日期                  |
| executeAccordNo     | string  | 执行依据文号                |
| dishonestySituation | string  | 失信被执行人行为具体情形          |
| caseAmount          | integer | 涉案金额（单位：分，换算需÷100才是元） |

### get-share-blocking - 股权冻结信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段                 | 类型      | 说明                    |
| ------------------ | ------- | --------------------- |
| executedPersonName | string  | 被执行人名称                |
| stockOrgName       | string  | 冻结股权标的企业名称            |
| executeAmount      | integer | 股权数额（单位：分，换算需÷100才是元） |
| executeCourtName   | string  | 执行法院名称                |
| executeNoticeNo    | string  | 执行通知文书号               |
| freezeState        | string  | 状态                    |
| freezeBeginTime    | string  | 冻结开始日期                |
| freezeEndTime      | string  | 冻结结束日期                |
| dataFreezeId       | long    | 冻结信息ID                |

### get-consumption-limits - 限制高消费信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段               | 类型     | 说明                    |
| ---------------- | ------ | --------------------- |
| executeCourtName | string | 执行法院名称                |
| caseAmount       | string | 涉案金额（单位：分，换算需÷100才是元） |
| limitHighObjName | string | 限制令对象名称（企业）           |
| applicantName    | string | 申请人名称                 |
| releaseTime      | string | 发布日期                  |
| registerTime     | string | 立案日期                  |
| relatePersonName | string | 关联人名称                 |
| caseNo           | string | 案号                    |
| dataLimitHighId  | string | 限制高消费ID               |

### get-judge-doc - 裁判文书信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段          | 类型      | 说明                    |
| ----------- | ------- | --------------------- |
| dataCaseId  | string  | 关联案件ID                |
| caseNo      | string  | 案号                    |
| caseReason  | string  | 案由                    |
| caseAmount  | integer | 案件金额（单位：分，换算需÷100才是元） |
| judgeResult | string  | 裁判结果                  |
| judgeTime   | string  | 裁判日期                  |
| publishTime | string  | 公布日期                  |
| memberList  | list    | 案件关联方信息               |
| caseType    | string  | 案件类型                  |

**memberList - 案件关联方信息**：

| 字段   | 类型     | 说明                                |
| ---- | ------ | --------------------------------- |
| list | list   | 关联信息 \[{name, type, judgeResult}] |
| name | string | 人员身份名称                            |

**list - 关联信息**：

| 字段          | 类型     | 说明              |
| ----------- | ------ | --------------- |
| name        | string | 名称              |
| type        | int    | 关联类型（1-企业，2-人员） |
| judgeResult | string | 裁判结果            |

### get-bankruptcy-regroup - 破产重整信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段             | 类型     | 说明     |
| -------------- | ------ | ------ |
| caseNo         | string | 案号     |
| beApplyMembers | list   | 被申请人信息 |
| applyMembers   | list   | 申请人信息  |

**beApplyMembers - 被申请人信息**：

| 字段   | 类型     | 说明            |
| ---- | ------ | ------------- |
| name | string | 名称            |
| type | int    | 类型（1-企业，2-人员） |

**applyMembers - 申请人信息**：

| 字段   | 类型     | 说明            |
| ---- | ------ | ------------- |
| name | string | 名称            |
| type | int    | 类型（1-企业，2-人员） |

### get-judicial-sale - 司法拍卖信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段                    | 类型      | 说明                   |
| --------------------- | ------- | -------------------- |
| auctionName           | string  | 拍卖名称                 |
| caseNo                | string  | 案号                   |
| dealOrgName           | string  | 处置单位名称               |
| dataJudicialAuctionId | string  | 司法拍卖ID               |
| startPrice            | integer | 起拍价（单位：分，换算需÷100才是元） |
| evaluationPrice       | integer | 评估价（单位：分，换算需÷100才是元） |
| auctionTime           | string  | 拍卖时间段                |

### get-open-court - 开庭公告（司法）

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段              | 类型     | 说明      |
| --------------- | ------ | ------- |
| memberList      | list   | 相关方信息   |
| courtOpenTime   | string | 开庭时间    |
| courtName       | string | 法院名称    |
| caseReason      | string | 案由      |
| caseNo          | string | 案号      |
| dataOpenCourtId | string | 开庭信息表ID |

**memberList - 相关方信息**：

| 字段   | 类型     | 说明      |
| ---- | ------ | ------- |
| list | list   | 相关方信息列表 |
| name | string | 相关方身份名称 |
| code | string | 相关方身份编码 |

**list - 相关方信息列表**：

| 字段   | 类型     | 说明               |
| ---- | ------ | ---------------- |
| name | string | 相关方名称            |
| type | int    | 相关方类型（1-企业，2-人员） |
| id   | string | 相关方主键            |

### get-case-filing - 立案信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段             | 类型     | 说明     |
| -------------- | ------ | ------ |
| memberList     | list   | 当事人信息  |
| caseReason     | string | 案由     |
| registerDate   | string | 立案日期   |
| courtName      | string | 法院名称   |
| caseNo         | string | 案号     |
| dataRegisterId | string | 立案信息ID |

**memberList - 当事人信息**：

| 字段   | 类型     | 说明      |
| ---- | ------ | ------- |
| code | string | 身份编码    |
| name | string | 身份名称    |
| list | list   | 当事人信息列表 |

**list - 当事人信息列表**：

| 字段   | 类型     | 说明                   |
| ---- | ------ | -------------------- |
| id   | string | 实体主键                 |
| type | int    | 实体类型（1-企业，2-人员，0-其他） |
| name | string | 实体名称                 |

### get-pre-mediate - 诉前调解信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段               | 类型     | 说明        |
| ---------------- | ------ | --------- |
| memberList       | list   | 诉前调解相关方信息 |
| caseReason       | string | 案由        |
| registerDate     | string | 立案日期      |
| courtName        | string | 法院名称      |
| caseNo           | string | 案号        |
| dataPreMediateId | string | 诉前调解ID    |

**memberList - 诉前调解相关方信息**：

| 字段   | 类型     | 说明        |
| ---- | ------ | --------- |
| list | list   | 相关方信息     |
| code | string | 相关方身份CODE |
| name | string | 相关方身份名称   |

**list - 相关方信息**：

| 字段   | 类型     | 说明                |
| ---- | ------ | ----------------- |
| type | int    | 相关方类型（1-企业，2-自然人） |
| id   | string | 相关方主键             |
| name | string | 相关方名称             |

### get-inq-eval - 询价评估信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段            | 类型     | 说明       |
| ------------- | ------ | -------- |
| partyList     | list   | 当事人信息    |
| ownerList     | list   | 标的物所有人信息 |
| inqResult     | string | 询价结果（元）  |
| subjectMatter | string | 标的物      |
| caseNo        | string | 案号       |

**partyList - 当事人信息**：

| 字段             | 类型     | 说明               |
| -------------- | ------ | ---------------- |
| entityName     | string | 当事人名称            |
| entityCategory | int    | 当事人类型（1-企业，2-人员） |
| entityId       | string | 当事人主键            |

**ownerList - 标的物所有人信息**：

| 字段             | 类型     | 说明               |
| -------------- | ------ | ---------------- |
| entityCategory | int    | 所有人类型（1-企业，2-人员） |
| entityId       | string | 所有人主键            |
| entityName     | string | 所有人名称            |

### get-deliver-notice - 送达公告信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段                  | 类型     | 说明      |
| ------------------- | ------ | ------- |
| memberList          | list   | 相关方信息列表 |
| releaseTime         | string | 发布日期    |
| courtName           | string | 法院名称    |
| caseReason          | string | 案由      |
| caseNo              | string | 案号      |
| noticeName          | string | 公告名称    |
| dataDeliverNoticeId | string | 送达公告ID  |

**memberList - 相关方信息列表**：

| 字段   | 类型     | 说明      |
| ---- | ------ | ------- |
| list | list   | 相关方实体信息 |
| name | string | 相关方身份名称 |
| code | string | 相关方身份编码 |

**list - 相关方实体信息**：

| 字段   | 类型     | 说明            |
| ---- | ------ | ------------- |
| type | int    | 类型（1-企业，2-人员） |
| id   | string | 主键            |
| name | string | 名称            |

### get-cases-terminated - 终本案件信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段               | 类型     | 说明                     |
| ---------------- | ------ | ---------------------- |
| noExecuteAmount  | long   | 未履行金额（单位：分，换算需÷100才是元） |
| executeAmount    | long   | 执行标的（单位：分，换算需÷100才是元）  |
| finalTime        | string | 终本日期                   |
| executeCourtName | string | 执行法院名称                 |
| caseNo           | string | 案号                     |
| dataCaseId       | string | 案件ID                   |
| dataCaseFinalId  | string | 终本案件ID                 |

### get-exit-ban - 限制出境信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段               | 类型     | 说明                    |
| ---------------- | ------ | --------------------- |
| caseNo           | string | 案号                    |
| releaseTime      | string | 发布日期                  |
| phone            | string | 联系电话                  |
| executeCourtName | string | 执行法院名称                |
| executeAmount    | long   | 执行标的（单位：分，换算需÷100才是元） |
| applicationList  | list   | 申请人信息                 |
| executeList      | list   | 被执行人信息                |
| limitList        | list   | 限制出境对象信息              |
| dataLimitExitId  | string | 限制出境ID                |

**applicationList - 申请人信息**：

| 字段   | 类型     | 说明            |
| ---- | ------ | ------------- |
| type | int    | 类型（1-企业，2-人员） |
| id   | string | 主键            |
| name | string | 名称            |

**executeList - 被执行人信息**：

| 字段   | 类型     | 说明            |
| ---- | ------ | ------------- |
| type | int    | 类型（1-企业，2-人员） |
| id   | string | 主键            |
| name | string | 名称            |

**limitList - 限制出境对象信息**：

| 字段   | 类型     | 说明            |
| ---- | ------ | ------------- |
| type | int    | 类型（1-企业，2-人员） |
| id   | string | 主键            |
| name | string | 名称            |

### get-judicial-notice - 法院公告信息

**请求参数**：

| 参数        | 类型      | 必填 | 说明               |
| --------- | ------- | -- | ---------------- |
| searchKey | string  | 是  | 企业全称             |
| pageNum   | integer | 否  | 页码，默认 1          |
| pageSize  | integer | 否  | 每页条数，默认 10，最大 20 |

**响应字段**：

| 字段                | 类型     | 说明          |
| ----------------- | ------ | ----------- |
| publishDate       | string | 刊登日期        |
| noticeOrgName     | string | 公告人/公告机构名称  |
| caseReason        | string | 案由          |
| caseNo            | string | 案号          |
| memberList        | list   | 法院公告相关方信息集合 |
| dataCourtNoticeId | string | 法院公告ID      |

**memberList - 法院公告相关方信息集合**：

| 字段   | 类型     | 说明      |
| ---- | ------ | ------- |
| list | list   | 相关方实体列表 |
| code | string | 身份编码    |
| name | string | 身份名称    |

**list - 相关方实体列表**：

| 字段   | 类型     | 说明                 |
| ---- | ------ | ------------------ |
| name | string | 相关方名称              |
| id   | string | 主键ID               |
| type | int    | 类型（1-企业，2-人员，0-其他） |

### get-risk - 企业风险信息

**请求参数**：

| 参数    | 类型     | 必填 | 说明                      |
| ----- | ------ | -- | ----------------------- |
| orgId | string | 是  | 企业ID（orgId，非 searchKey） |

> ⚠️ 此接口使用 `orgId` 而非 `searchKey`，orgId 从 `fuzzy-search-org` 接口结果中获取

**响应字段**：

| 字段            | 类型     | 说明   |
| ------------- | ------ | ---- |
| operationRisk | object | 经营风险 |
| lawRisk       | object | 法律风险 |
| financeRisk   | object | 财务风险 |
| opinionRisk   | object | 舆情风险 |
| riskDynamic   | object | 风险动态 |

**operationRisk / lawRisk / financeRisk / opinionRisk - 风险结构**：

| 字段           | 类型     | 说明         |
| ------------ | ------ | ---------- |
| totalRiskCnt | long   | 风险条数       |
| riskInfo     | string | 最近一次风险简述   |
| riskDetail   | string | 最近一次风险明细   |
| riskTime     | string | 最近一次风险记录时间 |

**riskDynamic - 风险动态**：

| 字段       | 类型     | 说明           |
| -------- | ------ | ------------ |
| riskInfo | string | 最近一次风险动态简述   |
| riskTime | string | 最近一次风险动态记录时间 |

***

## get-clear-info - 清算信息

**请求参数**：

| 参数        | 类型     | 必填 | 说明   |
| --------- | ------ | -- | ---- |
| searchKey | string | 是  | 企业全称 |

**响应字段**：

| 字段                 | 类型     | 说明       |
| ------------------ | ------ | -------- |
| liquidationLeader  | string | 清算组负责人名称 |
| liquidationMembers | string | 清算组成员    |

***

## 待接入接口

- `get-dishonest` - 失信被执行人
- `get-tax-violation` - 税收违法

***

## 关键原则

- ✅ 所有详细查询都必须先搜索、再确认、后查询
- ❌ 不要在未确认企业时直接调用详细信息接口
- ⚠️ 金额字段单位为分，展示时需÷100换算为元；返回 null 时显示"未知"
- ⚠️ 当 code=200 但数据为空时，展示消息为"暂无数据"，而非直接显示接口原始返回

