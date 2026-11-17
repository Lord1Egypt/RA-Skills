<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: company-intel/1.0.2
X-Skill-Package: zhiliao-company-intel/1.0.6
X-Skill-Source: clawhub/zhiliaobiaoxun
```
<!-- request-identity:end -->

# 工具速查（企业情报所用子集）

> 与 zlbx-bidding SKILL 同一套 api_v2 接口，此处只收录本 SKILL 用到的 9 个工具的关键参数。
> `POST https://mcp-server.zhiliaobiaoxun.com/api_v2/` + 工具名（例：`https://mcp-server.zhiliaobiaoxun.com/api_v2/get_company_profile`），Header 带 `X-API-Key` + `X-Client: company-intel/1.0.2`。

## 通用概念

**company 参数**：公司类工具统一接受 `company`（公司全称/简称/ID）或 `company_url`（知了标讯公司页链接），两者至少填一个。①步拿到 id 后优先传 id，避免重名歧义。**例外：`find_competitors` 只认公司名称，必须传全称**（生产实测：传 id 会被当成名称检索，0 结果且照扣积分）。

**match_modes**（关键词在哪个字段匹配）：

| 值 | 含义 | 情报分析中的用途 |
|---|------|-----------------|
| `winner` | 中标方 | 查主体的中标履历（④步核心） |
| `winner_tender` | 中标或投标 | 零中标时看有无投标参与记录 |
| `caller` | 招标方/采购单位 | 主体是采购方型公司时查其采购史 |
| `sm` / `title` / `brand` / `fulltext` | 标的物/标题/品牌/全文 | 品类过滤 |

**bid_process 公告阶段**：1=采购意向 2=预招标 4=招标 7=中标结果 8=合同。查中标履历用 `[7,8]`。

**组合逻辑**（仅 `query_bids_advanced` / `aggregate_bids_advanced` 支持 keyword_groups）：
- `keywords`（OR） AND `keyword_groups` 每组（组内 OR） AND NOT `exclude_keywords`
- 例·公司×品类交集：`{"keywords": ["公司全称"], "match_modes": ["winner"], "keyword_groups": [{"keywords": ["视频监控"], "match_modes": ["sm","title"]}]}`

**金额参数已统一**：所有筛项目金额的工具都用 `min_amount`/`max_amount`，单位一律**万元**（用户说「500 万以上」就传 `500`）。旧的 `min_money`/`max_money`（单位元）已移除，不再用于金额筛选；REST可能忽略未知字段，MCP可能报参数错误，不要继续使用旧参数。只有价格类工具例外：`get_top_brands`/`get_price_trends` 用 `min_price`/`max_price`，单位是**元**（产品单价，不是项目金额）。传错的后果是空结果**且照常扣积分**。

**响应**：`{"success": true, "data": {...}, "meta": {"cost_units": 1}}`；分页 `page`/`page_size`（默认 20，最大 50；search_company 最大 20）。

**链接**：所有返回的 `url`（公司页/公告页）带 `sk` 免登录签名，**原样输出，严禁删改**。

## 工具清单

### search_company — ① 公司名称解析（免费，不计积分）
`{"company_name": "简称或别名", "province": "可选", "city": "可选", "page_size": 10}`
→ `items`: `id`、`fullname`、`name`（简称）、`province`/`city`、`win_count`（中标次数）、`cal_count`（招标次数）、`org_count`、`url`（公司页，带 sk）。按 org_count 降序。短语匹配无结果时自动降级模糊匹配。

### get_company_profile — ② 公司画像
`{"company": "全称或ID"}` 或 `{"company_url": "..."}`
→ `fullname`、`org_base_type`、`industry`/`industry_l1`/`industry_l2`、`province`/`city`/`county`、`capital`（注册资本）、`size`（企业规模）、`business_status`、`establishment_date`、`business_scope`、`caller_count`（招标次数）、`winner_count`（中标次数）、`url`（公司页）。

### get_company_business_keywords — ② 主营业务词云
`{"company": "...", "begin_date": "2023-01-01", "limit": 20}`（可加 end_date/provinces/cities；limit 默认 10 最大 50）
→ `keywords`: 每项 `{"keyword": "服务器", "count": 150, "amount": 50000000}`（从中标记录提炼，count=中标次数，amount=金额·元）。

### get_company_partners — ③ 合作客户与供应商
`{"company": "...", "partner_type": "客户|供应商|全部"(必填), "keywords": [品类过滤,可选], "begin_date": "可选", "min_amount": 可选, "limit": 20}`（limit 默认 20 最大 100）
→ `partners`: 每项 `company_name`、`company_id`、`cooperation_count`（合作次数）、`cooperation_amount`/`cooperation_amount_wan`、`last_cooperation_time`、`products`（合作品类）。

### query_bids_advanced — ④ 中标履历明细
`{"keywords": ["公司全称"], "match_modes": ["winner"], "bid_process": [7,8], "begin_date": "3年前", "sort_field": "money", "sort_order": "desc", "page_size": 20}`
支持 `keyword_groups`/`exclude_keywords`；金额筛选参数为 `min_amount/max_amount`（万元）。
→ `total` + `items`: `bid_id`、`title`、`pub_time`、`money`/`money_wan`、`caller_name`、`winner_names`、`sm_names`、`url`（公告页，带 sk）。

### search_bids — ④ 备用常规搜索
`keywords`(必填) + `match_modes` + `bid_type`(招标/中标/全部) + `bid_process` + `begin_date/end_date` + `provinces/cities` + `min_amount/max_amount`（**万元**）。快速单条件查询时用；需要排序/排除词时用 query_bids_advanced。

### aggregate_bids_advanced — ④ 聚合统计（中标实力的量化底座）
`{"filters": {"keywords": ["公司全称"], "match_modes": ["winner"], "bid_type": 2, "begin_date": "3年前"}, "group_by": ["year"]}`
- `group_by` 可选：`month`/`quarter`/`year`/`province`/`city`/`industry`/`brand`/`company_type`/`bid_method`；`compare_with`: `yoy`/`qoq`。
- filters 的金额参数为 `min_amount/max_amount`（万元）；`bid_type`: 1=招标 2=中标。
→ `total_count`、`total_amount`/`total_amount_wan` + `buckets`: 每桶 `key`、`count`、`sum_amount`/`sum_amount_wan`、`avg_amount`（带 compare 时含 `yoy_count`/`yoy_amount`）。

### find_competitors — ⑤ 竞争对手（投标重叠度）
`{"company": "公司全称（勿传数字ID）", "limit": 10}`（limit 默认 10 最大 50；3 积分/次）
→ `total_projects`、`total_competitors` + `competitors`: 每家 `company_name`、`company_id`、`co_bid_count`（共同投标次数）、`latest_co_bid_time`、`top_co_bid_products`（交锋品类）、`top_co_bid_callers`（共同客户）、`top_co_bid_provinces`（交锋地区）。`top_co_bid_*` 的元素是 `{"name": "...", "count": N}` 对象（非字符串），取 `name` 展示、`count` 排序。

### get_company_contacts — ⑦ 项目联系人（按需步骤，5 积分/次）
`{"company": "...", "keywords": [品类过滤,可选], "role": 0, "limit": 5}`
- `role`: 1=招标联系人 2=中标联系人 0=全部（默认）；limit 默认 5 最大 20；可加 begin_date/end_date、match_modes。
→ `contacts`: 每条 `phone`、`name`（部分脱敏，如"李*"）、`bid_count`、`last_pub_time`、`last_bid_url`；外层 `contact_privacy`: `"full"`（付费账户，电话完整）| `"masked"`（免费/试用账户，电话脱敏）。
- ⚠️ **铁律 6**：电话按返回形态**原样展示**，不自行打码、不补全、不成批导出。`masked` 时附升级提示（充值后重新查询即得完整电话）。

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: zhiliao-company-intel/1.0.6
X-Skill-Source: clawhub/zhiliaobiaoxun
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
