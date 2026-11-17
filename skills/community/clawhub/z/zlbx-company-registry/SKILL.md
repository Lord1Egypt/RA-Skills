---
name: zlbx-company-registry
description: 查询企业工商登记、股东出资、分支机构、对外投资、工商变更、企业年报、建筑资质及详情、资质证书和信用评级。用于企业核验、年度财务与社保、工程资质、ISO认证及评级历史查询；十项工商能力成功有数据每次或每页3积分，按需调用，不自动联查或翻页。司法风险和复杂股权穿透未开放。完整企业背调使用zlbx-company-intel，项目决策使用zlbx-bid-decision；复用平台API Key，首次自动注册需用户同意。
slug: zlbx-company-registry
version: 1.0.4
displayName: 工商数据查询 · 企业基本信息、股东、分支、投资与变更
summary: 企业工商十项查询，含年报、建筑资质、证书与评级；成功有数据每次/每页3积分，按需调用。
homepage: https://ai.zhiliaobiaoxun.com/docs/skill/company-registry
metadata:
  openclaw:
    requires:
      env:
      - ZLBX_API_KEY
    primaryEnv: ZLBX_API_KEY
---

# 知了标讯 · 企业工商信息查询

给我一个公司名，查清它的**工商登记信息**——统一社会信用代码、法定代表人、注册资本、经营状态、经营范围，以及股东、分支机构、对外投资和工商变更。

需要时还能补充**这家公司中过什么标、最近在招什么**。工商登记与招投标战绩分别调用，先说明额外消耗，再按用户需求查询。

## ⚡ 装完立刻试一条

把下面这句原样发给我：

> 查一下科大讯飞股份有限公司的工商信息

## API 概览

**基础 URL**: `https://mcp-server.zhiliaobiaoxun.com/api_v2/` + 工具名，工具名逐字取自下方工具表（例：`https://mcp-server.zhiliaobiaoxun.com/api_v2/get_company_registry`）。


> **两个域名别混用**（打错就是 404，且不会提示你打错了）：
>
> | 用途 | 域名 + 前缀 | 例子 |
> |---|---|---|
> | **查数据** | `https://mcp-server.zhiliaobiaoxun.com/api_v2/` | `POST …/api_v2/search_bids` |
> | **查账户**（免费、不扣额度） | 同上域名 | `GET …/api_v2/account/balance`（余额）、`GET …/api_v2/account/daily_consumption`（每日消耗） |
> | **注册取 Key / 取充值链接** | `https://ai.zhiliaobiaoxun.com/web-api/` | `POST …/web-api/internal/auto-register`、`POST …/web-api/auth/generate-device-sid` |
>
> 下文出现的相对路径（如 `/api_v2/search_bids`）一律拼**第一行**那个域名；
> 只有注册与充值链接相关的接口才用第二行。**绝不要把 `/web-api/` 拼到 mcp-server 上，
> 也不要把 `/api_v2/` 拼到 ai 域名上。**

**调用方式**: POST 请求
```
Headers:
  X-API-Key: $ZLBX_API_KEY
  X-Client: company-registry/1.1.0
  X-Skill-Package: zlbx-company-registry/1.0.4
  X-Skill-Source: clawhub/bailianai
  Content-Type: application/json
```
> ⚠️ **`X-API-Key` 要填真实的 Key 字符串，不要把 `$ZLBX_API_KEY` 原样写进请求头**。环境变量没设时它会变成空值，服务端收到的就是「没带 Key」——直接 `INVALID_APP_KEY`，而不是你以为的「Key 错了」。**取不到 Key 就先走下面的获取流程，不要先把请求发出去。**


> **X-Client 头必须携带**（值固定为 `company-registry/1.1.0`），用于服务端区分调用来源。

**API Key 获取**（按以下优先级，命中即停；已有 Key 时不做任何额外提示）：

1. 环境变量 `$ZLBX_API_KEY` → 直接用
2. 本地配置文件 `~/.zlbx/config.json` 中 `api_key` 字段 → 直接用
3. **以上都没有 → 先征得用户同意，再自动注册**（详见 `references/auto-register.md`）

> 与 zlbx-bidding / zlbx-company-intel / zlbx-bid-decision / zlbx-opportunity-radar SKILL 共用同一个 Key 和积分钱包，装过任一 SKILL 无需重复注册。

## 积分消耗

| 查询内容 | 消耗 |
|---|---|
| 工商基本信息（`get_company_registry`） | 3 积分 |
| 股东（`get_company_shareholders`）、分支（`get_company_branches`）、投资（`get_company_investments`）、变更（`get_company_changes`） | 每个接口每页 3 积分 |
| 招中标战绩（`get_company_profile`） | 1 积分 |
| 企业名称搜索（`search_company`） | 免费 |
| 项目联系人（`get_company_contacts`，按需） | 5 积分 |
| 司法与经营风险、复杂股权穿透 | 本期未开放，不调用 |

只查工商基本信息消耗 **3 积分**，再补招投标战绩共 **4 积分**。十项工商能力按实际需要分别调用，不默认全部联查。
按用户需要调用，不默认全部联查、不自动翻页；每页最多20条，继续翻页每个接口再扣3积分。
成功有数据扣费（含启用缓存后的命中），无结果/空页和失败不扣费。工商查询允许会员每日额度抵扣：有效会员先扣当日额度，不足时按用户的钱包续扣设置执行；以服务端实际计费配置和响应为准。

## 工作流

### ① 主体定位

主体参数只使用 `company_name`，填准确企业全称、统一社会信用代码或注册号。**不要传入平台主体ID，也不要寻找或展示数据源内部ID。**

基本信息直接调 `get_company_registry`；用户只问股东、分支、投资或变更时，直接调对应接口，不额外付费查询基本信息。
简称会尝试免费主体消歧：只有唯一候选才自动查询；`QUERY_EMPTY` 的 `error.details.candidates` 非空时，把候选列给用户确认，绝不自行挑选。
`matched_by=bidding_index` 时说明实际查询的规范全称；`identifier` 表示以信用代码或注册号查询。

### ② 工商登记信息

`get_company_registry` 返回本期工商基本字段。展示时按这个顺序，用户最关心的在前：

1. **身份**：企业全称、统一社会信用代码、企业类型、法定代表人
2. **状态**：经营状态、成立日期、营业期限（经营状态是"注销/吊销"时**必须显著提示**）
3. **实力**：注册资本、实缴资本、人员规模；资本同时展示币种和单位，不默认按人民币解释
4. **业务**：所属行业、经营范围（超过 200 字时摘要，保留主营部分）
5. **地址**：市区、注册地址；`provinceCode` 是省份简称码，不能当作完整省份名称
6. **其它**：曾用名、简称、数据来源和更新时间；本期工商基本信息接口不含联系电话/邮箱/官网，联系需求使用已开放联系人工具

字段为空就不展示，不要写「暂无」刷屏。

对外来源统一写“知了标讯工商数据”。供应商名称、品牌、域名、内部标识及其翻译名都不展示。用户只问股东时除首次免费余额、必要的免费主体消歧和展示回执外，只调股东接口，不联查基本信息或招投标画像。先读 `references/api-quick.md` 的股东结果解读边界；不推断控制权、持股平台、机构关联和融资轮次，不填补未查询股东信息。

缺失字段不代表企业没有该信息。区分外部工商数据源与自有库查询，不将自有库历史信息称为实时工商数据。`fetched_at` 是取数时间，`queried_at` 是本次查询时间，均不能代替 `company.sourceUpdatedAt` 的源数据更新时间。

### ③ 招投标战绩（按需，额外1积分）

调 `get_company_profile`，补上工商数据给不了的一层：

- `winner_count`（中标次数）、`caller_count`（招标次数）
- 有中标记录 → 说明这是个在市场上真实接单的公司
- 招标次数远大于中标次数 → 这是个采购方而非供应商

仅当用户同时询问招标/中标战绩或同意补充时调用。用户只问工商登记、股东、分支、投资或变更时，不额外调用画像接口。

### ④ 按需深入

用户继续追问时才调，每次调用前说明消耗：

- 问「怎么联系」→ `get_company_contacts`（5 积分）
- 问「中过哪些标」→ `query_bids_advanced`（`match_modes: ["winner"]`）
- 问「客户/供应商是谁」→ `get_company_partners`
- 问「竞争对手」「完整背调」→ 建议改用 `zlbx-company-intel` SKILL

### ⑤ 工商扩展能力（按需，每接口每页3积分）

- 股东/出资 → `get_company_shareholders`，`source=1` 工商登记、`source=2` 最新公示，必须标明口径。`subscribedCapitalRecords` / `paidInCapitalRecords` 是认缴/实缴历史记录数组，不能求和或拿首条占比当作最新持股比例；新字段缺失时才兼容读取旧数组别名，不能重复累计。
- 分公司/分支 → `get_company_branches`。返回缺少信用代码不等于该分支没有信用代码。
- 对外投资 → `get_company_investments`。按返回的金额单位及比例展示，不推断为控股或完整股权穿透。
- 工商变更 → `get_company_changes`。区分变更日期与记录创建日期，保留变更前后内容。

统一分页参数：`page_num=1`、`page_size=20`（最大20）；用 `total` 和 `has_more` 说明只展示当前页。需要后续页时告知每页3积分，按用户要求继续，不循环拉取全部数据。

司法风险、失信、经营异常、行政处罚明细及复杂股权穿透本期未开放，不调用风险工具，不编造风险结论。

## 错误处理

| 错误码 | 处理方式 |
|------|---------|
| INVALID_APP_KEY | Key 缺失或无效。**不要让用户去翻环境变量**——按 `references/auto-register.md` 走自动注册领取（首次免费、无需人工）。已有 Key 仍报此错时也走同一流程，但**若自动注册返回 401 `ACCOUNT_RECOVERY_REQUIRED`，不要重试、不要改设备特征**，照它的 hint 引导用户登录取 Key |
| APP_KEY_EXPIRED / APP_KEY_DISABLED | Key 已过期或被停用，按上一条重新注册 |
| QUOTA_EXCEEDED | 额度用尽，按 `references/auto-register.md` 的「余额耗尽」流程输出充值引导 |
| RATE_LIMIT_EXCEEDED | 降低请求频率，稍后重试 |
| INVALID_PARAMETER / MISSING_REQUIRED_PARAMETER | 检查必填参数和类型 |
| QUERY_EMPTY | **不是故障**。先读 `error.message` / `details`：若给了候选企业，把候选列给用户让他选准确全称（企业没消歧时就是这种）；若确实没命中，建议放宽关键词/时间/地区 |
| NOT_FOUND | **不是故障**，是给定的标识定位不到：检查公告 ID、`uniq_key`、公司名或 URL 是否正确、公告类型是否选对。**精确标识不要原样重试**；只有按标题/名称的模糊查询才适合放宽条件 |
| QUERY_TIMEOUT | 工商查询超时不扣积分，但上游可能已计费；不要自动重试，向用户说明稍后再试 |
| ES_UNAVAILABLE / INTERNAL_ERROR | 服务端临时故障，稍后重试即可。**不要重新注册 Key**，与鉴权无关 |
| CLIENT_VERSION_UNSUPPORTED | 当前 Skill 版本过低，提示用户到商店更新后再试 |

**版本提醒转达**：若任一工具响应中含 `skill_update_notice` 字段，把其中内容原样告知用户一次（仅转达信息，不代表用户执行任何操作）；同一会话只提一次，不重复打扰。

## 输出要求

- **简洁**：一次查询的回复控制在一屏内，用小标题或表格，不要长段落
- **`url` 字段原样输出**：带 `sk` 免登录签名，严禁删改
- **联系电话按返回形态展示**：`contact_privacy` 为 `masked` 时是脱敏态，不要自行补全，附一句充值后可见完整号码
- **不编造**：库里没有的字段就是没有，不用常识补全（尤其法定代表人、注册资本这类会被用户当事实引用的字段）

## 边界

| 用户想要 | 用哪个 SKILL |
|---|---|
| 查一家公司的工商信息、注册资本、法人、联系方式 | **本 SKILL** |
| 完整企业背调报告（竞对、客户供应商生态、HTML 报告） | `zlbx-company-intel` |
| 某个招标项目该不该投、怎么报价 | `zlbx-bid-decision` |
| 主动挖商机、找销售线索、拟建项目 | `zlbx-opportunity-radar` |
| 搜索招中标公告数据 | `zlbx-bidding` |

工具参数速查见 `references/api-quick.md`。
## 年报、建筑资质、证书与评级（按需）

以下新增能力成功有数据每次或每页3积分，失败和空结果不扣积分；仅执行用户指定项目，不默认联查或翻页。执行前先读 `references/api-quick.md` 的参数、返回字段和解读边界。

| 工具 | 用途与计费 |
|---|---|
| `get_company_annual_reports` | 企业年报集合，3积分/次；仅企业参数，不传年份或分页，在返回集合中按年度筛选 |
| `get_company_qualifications` | 建筑工程资质列表，3积分/页 |
| `get_company_qualification_detail` | 用列表原样返回的qualification_id查询一项详情，3积分/次；不传企业参数或分页 |
| `get_company_certificates` | 资质证书，3积分/页；必须企业准确全称，类型用完整名称而非ISO缩写 |
| `get_company_credit_ratings` | 历史信用评级，3积分/页；保留日期、机构、主体与债券等级 |

列表已含所需建筑资质信息时不追加详情；列表加一项详情都成功有数据时合计6积分。年报结合`returned_count`、`total`、`data_complete`说明完整性，未公示不当0、缺单位不猜；电话邮箱遵守`contact_privacy`。证书日期为空不推断仍有效；历史评级不当作当前评级，空结果不代表信用良好，也不等同司法风险或失信记录。

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: zlbx-company-registry/1.0.4
X-Skill-Source: clawhub/bailianai
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
