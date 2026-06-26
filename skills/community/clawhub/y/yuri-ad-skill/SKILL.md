---
name: yri-adx
description: "YRI AdX — Facebook ad automation via MCP API. Create campaigns, manage budgets, monitor performance, and scale ads. | 尤里改广告平台 MCP API — Facebook广告创建、投放管理、数据监控、预算调整、受众定位、文案素材管理。"
homepage: https://baiz.ai
primary_credential: BAIZ_API_TOKEN
env:
  BAIZ_API_TOKEN:
    description: "baiz.ai platform API Token. Generate it from the 'API Management' page in your baiz.ai dashboard. Format: xxx|xxx. Only valid for baiz.ai, not a raw Facebook Token. Use a minimal-permission test token. | baiz.ai 平台 API Token。在 baiz.ai 后台「API管理」页面生成，格式为 xxx|xxx。仅对 baiz.ai 有效，非 Facebook 原始 Token。建议使用最小权限的测试账户 Token。"
    required: true
    sensitive: true
---

# YRI AdX — 尤里改广告平台 / YRI Ad Exchange Platform

> **尤里改 (YRI)** — Intelligent Facebook Ad Management via MCP API

Manage Facebook ads through baiz.ai MCP API using curl commands. Create campaigns, target audiences, upload creatives, monitor performance, and scale — all from your terminal.

通过 curl 调用 baiz.ai MCP API 管理 Facebook 广告。创建广告计划、定位受众、上传素材、监控数据、扩量投放，一切尽在终端掌控。

## Security / 安全声明

**Operator / 运营方：** baiz.ai is a Facebook ad management SaaS platform — https://baiz.ai

**Credentials / 凭证声明：**
- This skill explicitly declares its credentials via `primary_credential: BAIZ_API_TOKEN` and `env.BAIZ_API_TOKEN`
- Tokens are generated in the baiz.ai dashboard under "API Management", format: `xxx|xxx`, marked `sensitive: true`
- Tokens are only valid for baiz.ai — they are NOT raw Facebook tokens. baiz.ai acts as a proxy layer for the Facebook Marketing API; token scope is controlled by baiz.ai
- Tokens are injected via environment variables and passed in HTTP headers — the skill never stores, caches, or writes them to disk
- Use a revocable, minimal-permission test token; avoid providing production credentials directly
- If any marketplace/registry listing fails to declare `BAIZ_API_TOKEN`, stop the installation and contact the publisher to update metadata before providing the token; treat the token as sensitive at all times and revoke it if you detect mismatches

**Platform Verification / 平台验证：**
- Official site: https://baiz.ai — provides user registration and ad management services
- baiz.ai serves as a proxy layer for Facebook Marketing API; users manage ad accounts through baiz.ai rather than interacting with Facebook API directly
- Before installation, visit https://baiz.ai to review its privacy policy, terms of service, and token permission scope

**Network Behavior / 网络行为：**
- All requests go to a single endpoint: `https://baiz.ai/mcp`, using standard HTTPS + JSON-RPC 2.0
- This skill is a pure prompt reference document — it contains no executable scripts, install hooks, or background processes

**High-Impact Operations / 高影响操作：**
- Mutation operations (`publish_campaign`, `stop_campaign`, `adjust_budget`, etc.) require explicit user initiation — the skill never triggers them automatically
- Each API call is a stateless single HTTP request with no session persistence
- Autonomous invocation is not recommended — use a restricted-scope token to minimize blast radius

**Installation Guide / 安装建议：**
1. Visit https://baiz.ai to verify platform legitimacy, privacy policy, and token permissions
2. Provide credentials via `BAIZ_API_TOKEN` env var — prefer revocable, minimal-permission test tokens
3. Test with sandbox/test ad accounts first; monitor API calls and billing
4. Only connect production tokens after confirming trust in the baiz.ai platform
5. To reduce risk, disable autonomous invocation or provide read-only tokens

## Pre-install Checklist / 安装前注意事项

1. **Registry vs Manifest —** Confirm the registry metadata matches `SKILL.md/_meta.json`, especially the `BAIZ_API_TOKEN` declaration, so the platform can inject the credential correctly / 上传或安装前确认注册表元数据与 `SKILL.md/_meta.json` 一致，尤其是 `BAIZ_API_TOKEN` 的声明，确保平台能正确注入凭证
2. **Token Scope —** Only provide revocable, minimal-permission test tokens until you have verified every workflow end-to-end / 在完全验证流程之前仅提供可撤销、最小权限的测试 Token
3. **Review baiz.ai Policies —** Visit https://baiz.ai to inspect privacy, billing, and terms, and understand how baiz.ai proxies calls to Facebook / 访问 https://baiz.ai 查看隐私、计费与条款，了解其如何代理调用 Facebook
4. **Read-only & No Autonomy —** Prefer read-only tokens for initial experiments and keep autonomous invocation disabled to avoid accidental mutations / 初次测试尽量使用只读 Token 并禁用自动调用，防止意外写操作
5. **Request Metadata Fixes —** If any listing omits required env vars, ask the publisher to update metadata before granting access / 若注册表遗漏所需环境变量，请先联系发布方补齐元数据再授予访问权限

## Configuration / 基础配置

- **Base URL**: `https://baiz.ai/mcp`
- **Auth**: Bearer Token (format: `xxx|xxx`, generate from baiz.ai dashboard "API Management")
- **Protocol**: JSON-RPC 2.0 over HTTPS

## Request Format / 通用调用格式

```bash
curl -s "https://baiz.ai/mcp" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"TOOL_NAME","arguments":{ARGUMENTS}},"id":1}'
```

## Tools / 工具列表

### 1. Balance / 查询余额
```bash
{"name":"get_balance","arguments":{}}
```
Returns: team_name, wallet_balance(USD), ad_account_balance(USD)

### 2. Accounts & Infrastructure / 账户与基础设施

```bash
# List Facebook accounts (三不限模式入口)
{"name":"list_accounts","arguments":{}}
# → id, username, account_id, status, c_user

# List BMs (二不限模式入口)
{"name":"list_businesses","arguments":{}}
# → id, name, bussiness_id

# Get BM detail (pages, pixels, ad account stats)
{"name":"get_business","arguments":{"id": BM_ID}}
# → owned_pages, client_pages, owned_pixels, ad_account_total, ad_account_active

# List ad accounts — filter by facebook_id (三不限) or bm_id (二不限)
{"name":"list_ad_accounts","arguments":{"facebook_id": ACCOUNT_ID}}
{"name":"list_ad_accounts","arguments":{"bm_id": BM_ID}}
# → id(系统ID), ad_account_id(FB ID), name, account_status, timezone_name, currency, balance, spend

# List pages — 三不限模式需传 facebook_id 实时拉取
{"name":"list_pages","arguments":{"facebook_id": ACCOUNT_ID}}
{"name":"list_pages","arguments":{}}
# → id(系统ID), name, page_id(FB ID), category
```

### 3. Offers / Offer 管理
```bash
# Create
{"name":"create_offer","arguments":{"name":"Product Name","url":"https://...","price":29.99,"ai_description":"产品描述供AI理解"}}

# List (filter: name, status, positioning)
{"name":"list_offers","arguments":{}}

# Get detail (includes related copywritings & campaigns)
{"name":"get_offer","arguments":{"id": OFFER_ID}}

# Update
{"name":"update_offer","arguments":{"id": OFFER_ID, "price": 39.99}}

# Delete
{"name":"delete_offer","arguments":{"id": OFFER_ID}}
```
Offer status: 0=draft, 1=active, 2=paused, 3=stopped

### 4. Targeting / 受众定位
```bash
# Create
{"name":"create_targeting","arguments":{
  "name": "US-25-55-All",
  "countries": ["US"],
  "gender": "all",
  "min_age": 25,
  "max_age": 55,
  "locate": ["6"],
  "interests": [],
  "behaviors": [],
  "device_platforms": ["mobile","desktop"],
  "publisher_platforms": ["facebook","instagram"],
  "advantage_audience": 1
}}

# List
{"name":"list_targetings","arguments":{}}

# Update
{"name":"update_targeting","arguments":{"id": TARGETING_ID, "max_age": 65}}

# Delete
{"name":"delete_targeting","arguments":{"id": TARGETING_ID}}
```
Gender: all / men / women | Age: 18-65 | advantage_audience: 1=on, 0=off

### 5. Copywriting / 文案管理
```bash
# Create
{"name":"create_copywriting","arguments":{"primary_text":"Ad body text","headline":"Headline","description":"Description","tag":"tag"}}

# List
{"name":"list_copywritings","arguments":{}}

# Update
{"name":"update_copywriting","arguments":{"id": COPY_ID, "headline": "New Headline"}}

# Delete
{"name":"delete_copywriting","arguments":{"id": COPY_ID}}
```

### 6. Files / 素材管理
```bash
# Upload via URL
{"name":"create_file","arguments":{"url":"https://...","name":"filename","tag":"mcp","comment":"备注"}}

# List (filter: tag, name)
{"name":"list_files","arguments":{}}

# Delete
{"name":"delete_file","arguments":{"id": FILE_ID}}
```

### 7. Strategy / 投放策略 (Optional)
```bash
# Create strategy — defines channel, objective, budget type, bid, ad structure
{"name":"create_strategy","arguments":{
  "name": "FB-Sales-CBO-Auto",
  "channel": "facebook",
  "objective": "OUTCOME_SALES",
  "call_to_action_type": "LEARN_MORE",
  "conversion_location": "WEBSITE",
  "budget_type": "daily",
  "campaign_budget": 50,
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "method": "auto",
  "adsets_per_campaign": 3,
  "ads_per_adset": 2,
  "selected_hours": ["0-23"]
}}

# List
{"name":"list_strategies","arguments":{}}

# Get detail
{"name":"get_strategy","arguments":{"id": STRATEGY_ID}}
```

Objectives: OUTCOME_SALES / OUTCOME_TRAFFIC / OUTCOME_ENGAGEMENT / LEAD_GENERATION / OUTCOME_APP_PROMOTION
CTA types: LEARN_MORE / SHOP_NOW / ORDER_NOW / BUY_NOW / SIGN_UP / APPLY_NOW / DOWNLOAD / CONTACT_US
Budget: daily (CBO) / adset_budget (per ad set)
Bid: LOWEST_COST_WITHOUT_CAP / COST_CAP / LOWEST_COST_WITH_BID_CAP
Structure: auto (by quantity) / custom (manual adset config)

### 8. Campaign / 广告计划
```bash
# Create — auto-triggers publish flow
{"name":"create_campaign","arguments":{
  "name": "Campaign Name",
  "objective": "OUTCOME_SALES",
  "call_to_action_type": "LEARN_MORE",
  "start_time": "2026-03-20 00:00:00",
  "end_time": "2026-03-27 23:59:59",
  "selected_hours": ["0-23"],
  "copywriting_ids": [COPY_ID],
  "targeting_ids": [TARGETING_ID],
  "file_ids": [FILE_ID],
  "offer_ids": [OFFER_ID],
  "facebook_business_id": BM_SYSTEM_ID,
  "facebook_page_id": PAGE_SYSTEM_ID,
  "ad_account_ids": [AD_ACCOUNT_SYSTEM_ID],
  "budget_type": "daily",
  "limit_daily_amount": 20
}}
# Optional: facebook_pixel_id, lead_form_id, thumb_ids, limit_amount, comment

# List (filter: bm_id, ad_account_id, status, name)
{"name":"list_campaigns","arguments":{}}

# Get detail (includes related copywritings, targetings, files, offers, accounts)
{"name":"get_campaign","arguments":{"id": CAMPAIGN_ID}}

# Update (name, time, budget — budget changes auto-sync to Facebook)
{"name":"update_campaign","arguments":{"id": CAMPAIGN_ID, "limit_daily_amount": 30}}

# Publish / retry (only for status 0=draft or 10=failed)
{"name":"publish_campaign","arguments":{"id": CAMPAIGN_ID}}

# Stop (pauses all ads under this campaign)
{"name":"stop_campaign","arguments":{"id": CAMPAIGN_ID}}

# Start (resume paused campaign)
{"name":"start_campaign","arguments":{"id": CAMPAIGN_ID}}

# Delete (stops FB ads first, then soft-deletes)
{"name":"delete_campaign","arguments":{"id": CAMPAIGN_ID}}

# Adjust budget (increase/decrease/set, auto-sync to Facebook)
{"name":"adjust_budget","arguments":{"id": CAMPAIGN_ID, "action": "increase", "amount": 20, "budget_field": "limit_daily_amount"}}
```

### 9. Monitoring / 数据监控
```bash
# Ad-level data (realtime from Facebook API via BM token)
{"name":"list_campaign_ads","arguments":{"id": CAMPAIGN_ID}}
# → metrics: total_spend, impressions, clicks, reach, purchase, cpm, cpc, ctr, cpa
# → ads[]: ad_id, name, status, spend, impressions, clicks, reach, frequency,
#           link_clicks, landing_page_views, add_to_cart, purchase, initiate_checkout, view_content, lead

# Ad set-level data
{"name":"list_campaign_adsets","arguments":{"id": CAMPAIGN_ID}}
# → adsets[]: adset_id, name, status, daily_budget, bid_strategy, spend, impressions, clicks, purchase

# Pause/activate an ad set
{"name":"update_adset_status","arguments":{"id": CAMPAIGN_ID, "adset_id": "FB_ADSET_ID", "status": "PAUSED"}}

# Pause/activate a single ad
{"name":"update_ad_status","arguments":{"id": CAMPAIGN_ID, "ad_id": "FB_AD_ID", "status": "PAUSED"}}
```

### 10. Scale / 扩量
```bash
# Copy entire campaign (deep copy: campaign + ad sets + ads, default PAUSED)
{"name":"copy_campaign","arguments":{"id": CAMPAIGN_ID, "status_option": "PAUSED"}}

# Copy ad set within same campaign (default PAUSED)
{"name":"copy_adset","arguments":{"id": CAMPAIGN_ID, "adset_id": "FB_ADSET_ID", "status_option": "PAUSED"}}
```

## Campaign Status Codes / 广告状态码

| Code | EN | 中文 |
|------|----|------|
| 0 | Draft | 草稿 |
| 1 | Under Review | 审核中 |
| 2 | Learning/Active | 学习中/投放中 |
| 3 | Rejected | 被拒 |
| 4 | Unprofitable | 不盈利 |
| 5 | Budget Depleted | 预算耗尽 |
| 6 | Archived | 归档 |
| 7 | Stopped | 已停止 |
| 8 | Disabled | 已禁用 |
| 9 | Expired | 已过期 |
| 10 | Failed | 发布失败 |

## Workflow / 完整广告发布与管理流程

### Phase 1: Preparation / 准备阶段
1. `get_balance` — Confirm sufficient budget / 确认余额充足
2. `list_accounts` (三不限) or `list_businesses` (二不限) — Get Facebook accounts or BMs / 获取账号或BM
3. `list_ad_accounts(facebook_id/bm_id)` — Get available ad accounts / 获取可用广告户
4. `list_pages(facebook_id)` — Get pages / 获取主页

### Phase 2: Creative Setup / 素材准备
5. `create_offer` or `list_offers` — Prepare landing page/product link / 准备落地页
6. `create_targeting` or `list_targetings` — Define audience / 创建受众定位
7. `create_copywriting` or `list_copywritings` — Create ad copy / 创建文案
8. `create_file` or `list_files` — Upload creatives / 上传素材
9. `create_strategy` or `list_strategies` — Define delivery strategy (optional) / 创建投放策略(可选)

### Phase 3: Launch / 发布阶段
10. `create_campaign` — Assemble all components & auto-trigger publish / 组装创建广告计划(自动触发发布)
11. `get_campaign` — Poll publish status (async: 0→1→2 or →10) / 轮询发布状态
12. `publish_campaign` — Retry if failed (status=10) / 发布失败可重试

### Phase 4: Optimization / 优化阶段
13. `list_campaign_ads` — Realtime ad performance from Facebook API / 实时广告数据
14. `list_campaign_adsets` — Ad set level performance / 广告组级别数据
15. `update_adset_status` / `update_ad_status` — Pause underperformers / 暂停低效广告组或广告
16. `adjust_budget` — Scale budget based on performance / 根据表现调整预算
17. `update_campaign` — Modify campaign settings (budget auto-syncs to FB) / 修改计划设置

### Phase 5: Scale / 扩量阶段
18. `copy_campaign` — Duplicate winning campaigns / 复制优质广告计划
19. `copy_adset` — Duplicate winning ad sets / 复制优质广告组
20. `stop_campaign` / `start_campaign` — Control delivery / 控制投放开关
21. `delete_campaign` — Clean up (stops FB ads first) / 清理(先停止再删除)
