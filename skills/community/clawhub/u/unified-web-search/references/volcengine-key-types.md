# 火山引擎三种 Key 详解

## 概览

火山引擎有三套独立的认证体系，Key 互不通用。混淆使用会导致 401/403 错误。

| Key 类型 | 格式示例 | 环境变量 | 可用端点 | 获取方式 |
|----------|----------|----------|----------|----------|
| **联网搜索 API Key** | `<web-search-token>` | `WEB_SEARCH_API_KEY` | `open.feedcoopapi.com/search_api/web_search` | [联网搜索控制台](https://console.volcengine.com/search-infinity/api-key) 或 Agent Plan 控制台 |
| **agentplan key** | `ark-<agentplan-token>` | `ARK_API_KEY` | `/api/plan/v3/chat/completions` | Agent Plan 订阅自动分配 |
| **通用 ARK API Key** | `ark-<token>` | `ARK_API_KEY` | `/api/v3/responses`, `/api/v3/chat/completions` | [Ark 控制台](https://console.volcengine.com/ark/) 手动创建 |

## 详细说明

### 1. 联网搜索 API Key

- **用途**：仅用于联网搜索（Search Infinity API）
- **端点**：`https://open.feedcoopapi.com/search_api/web_search`
- **认证方式**：`Authorization: Bearer <web-search-token>`
- **请求头**：需加 `X-Traffic-Tag: skill_web_search_common`
- **额度**：个人用户每月 500 次免费；Agent Plan 用户按套餐额度
- **限制**：不能调任何 Ark 端点（`/api/v3/*`、`/api/plan/v3/*` 均返回 401）

### 2. agentplan key

- **用途**：仅用于 Agent Plan 套餐的模型推理
- **端点**：`https://ark.cn-beijing.volces.com/api/plan/v3/chat/completions`
- **协议**：OpenAI chat/completions 格式
- **限制**：不能调 `/api/v3/responses`（返回 401），不能调联网搜索 API（返回 401）
- **特点**：不支持缓存（cached_tokens 永远为 0）

### 3. 通用 ARK API Key

- **用途**：完整 Ark 平台功能
- **端点**：`/api/v3/responses`（含搜索工具）、`/api/v3/chat/completions` 等
- **限制**：需单独申请，非 Agent Plan 自动分配
- **特点**：支持 Responses API 的 `web_search` 工具，带 url_citation 引用

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 联网搜索 Key 调 `/api/v3/responses` → 401 | Key 不适用于 Ark 端点 | 改用 `open.feedcoopapi.com` |
| agentplan key 调 `/api/v3/responses` → 401 | agentplan 只能走 `/api/plan/v3` | 改用正确端点 |
| agentplan key 调联网搜索 API → 401 | key 类型不匹配 | 使用联网搜索 API Key |
| 通用 ARK Key 调 `/api/plan/v3` → 401/404 | plan 端点仅限 agentplan key | 使用正确的 key |

## 决策树

```
需要联网搜索？
├── 有 WEB_SEARCH_API_KEY → 调用 open.feedcoopapi.com 专用搜索端点（推荐）
├── 有通用 ARK API Key → 可走 /api/v3/responses + web_search 工具
└── 只有 agentplan key → 不能直接搜索，需要获取联网搜索 API Key

需要模型推理？
├── 有 agentplan key → 走 /api/plan/v3（OpenAI 格式）
├── 有通用 ARK API Key → 走 /api/v3/chat/completions
└── 有联网搜索 API Key → 不能用于模型推理
```
