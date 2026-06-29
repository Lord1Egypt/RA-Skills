# Resilience Skill

LLM API error tracking, classification, retry, and task recovery for OpenClaw.

> **⚠️ 必须先安装配套插件，否则此 Skill 完全无法工作**  
> 此 Skill **仅提供自然语言描述、示例和触发话术**。  
> **核心实现（工具注册、model_call_ended 自动错误记录 hook、重试引擎、Dashboard HTTP 服务、JSONL 日志与统计持久化）全部来自插件 `@leiJack-lo/resilience`**。  
> 只装 Skill 不装插件 → 工具不存在、调用失败、不会自动收集数据、Dashboard 也不会启动。

## 安装（必须按顺序）

```bash
clawhub login

# 1. 安装插件（必须带 --dangerously-force-unsafe-install）
# 原因：插件会使用 open 包打开浏览器、启动本地 HTTP server (默认 18765)、
# 注册 model_call_ended / agent_end 等敏感 hook、读写 ~/.openclaw/plugins/resilience/ 下的日志和配置。
# ClawHub 安全扫描因此标记为 "suspicious"（这是正常行为，不是恶意代码）。
openclaw plugins install clawhub:@leiJack-lo/resilience --dangerously-force-unsafe-install

# 2. 安装此 Skill（获得中文自然语言能力 + 工具描述）
openclaw skills install resilience-monitor

# 3. OpenClaw 2026.6.10+：允许 agent_end 会话恢复 hook 读取会话结束事件
# 不设置时，API 错误统计仍可用，但“会话失败统计 + 下一轮恢复指令”不会启用。
openclaw config set plugins.entries.resilience.hooks.allowConversationAccess true

# 4. 必须重启 Gateway，让插件的 hooks 和工具真正注册生效
openclaw gateway restart
```

安装成功后即可直接对 agent 说中文指令，例如：
- "查看今天报错统计"
- "打开 resilience 面板"
- "修改超时重试策略为指数退避"
- "生成今日错误日报"

**验证方法**：重启后问 agent "resilience 插件安装好了吗？" 或直接试一个工具调用。如果提示工具不存在，就说明插件没加载成功。

配置（面板端口、是否自动启动 Dashboard 等）放在 `~/.openclaw/openclaw.json` 的 `plugins.entries.resilience.config` 下；OpenClaw 2026.6.10+ 的会话恢复授权放在 `plugins.entries.resilience.hooks.allowConversationAccess` 下（见下方 dashboard 工具说明）。

## Overview

This skill adds natural language support and Chinese examples **on top of the Resilience plugin**. It lets your agent monitor API health, inspect per-model error patterns, adjust retry strategies, generate reports, and control the live dashboard using everyday language.

Use it to:

- Monitor API error rates and patterns
- View per-model performance statistics
- Configure retry strategies
- Generate error reports
- Track task recovery status
- Configure automatic session recovery prompts in Chinese or English

## Tools

### resilience_dashboard

Open the live web dashboard in your browser for real-time error stats and retry strategy management.

**Parameters:**
- `action`: `"open"` (default) | `"status"` | `"stop"`

**Features:**
- Live error overview (today / hour / active retries)
- Model breakdown table
- Recent errors feed
- Retry strategy cards — set default, adjust max retries
- Auto-refresh: **5s**, **60s**, **5min**, **1h**, or off

**URL:** `http://127.0.0.1:18765/` (default port, configurable via `dashboardPort`)

**Voice / natural language examples:**
- "打开错误统计页面" → `resilience_dashboard({ action: "open" })`
- "打开监控面板" → `resilience_dashboard({ action: "open" })`
- "打开 resilience 面板" → `resilience_dashboard({ action: "open" })`

The dashboard starts automatically when OpenClaw Gateway starts (unless `dashboardEnabled: false`).

**重要**：这些配置只有在**插件已正确安装并加载**后才生效（见最上面的安装前提）。

**Configuration** lives in `~/.openclaw/openclaw.json` under `plugins.entries.resilience.config` (not only `api.pluginConfig` at hook time). Example:

```json
"resilience": {
  "enabled": true,
  "hooks": {
    "allowConversationAccess": true
  },
  "config": {
    "dashboardPort": 18765,
    "dashboardEnabled": true,
    "instanceLabel": "my-workspace"
  }
}
```

At `gateway_start`, config is read from `ctx.config` + `ctx.workspaceDir`.

**Multi-instance:** Use the instance dropdown to view **all instances (aggregated)** or a single Gateway. Each instance stores data under `~/.openclaw/plugins/resilience/instances/<id>/`. Strategy edits apply only to the **local** Gateway instance.

### resilience_stats

View API error statistics by time period or model.

**Parameters:**
- `query` (optional): Natural language query
  - `"today"` or empty — today's full summary
  - `"hour"` — current hour stats
  - `"week"` — current week stats
  - Any model name (e.g., `"mimo-v2.5"`) — model-specific stats

**Examples:**
- "查看今天报错统计" → `resilience_stats({ query: "today" })`
- "查看 mimo-v2.5 的错误率" → `resilience_stats({ query: "mimo-v2.5" })`
- "查看本周错误率" → `resilience_stats({ query: "week" })`

### resilience_strategies

View, add, update, or reset retry strategies.

**Parameters:**
- `action`: `"list"` (default) | `"add"` | `"update"` | `"reset"`
- `strategyName`: Strategy name (required for add/update)
- `updates`: Fields to update (for add/update)

**Examples:**
- "查看当前所有策略配置" → `resilience_strategies({ action: "list" })`
- "修改超时重试策略为指数退避" → `resilience_strategies({ action: "update", strategyName: "default-exponential", updates: { type: "exponential" } })`
- "添加一个自定义重试策略" → `resilience_strategies({ action: "add", strategyName: "my-strategy", updates: { type: "custom", maxRetries: 3, intervals: [60000, 300000, 600000] } })`
- "重置策略为默认" → `resilience_strategies({ action: "reset" })`

### resilience_report

Generate detailed error reports.

**Parameters:**
- `reportType`: `"daily"` (default) | `"model"` | `"recovery"` | `"full"`
- `target`: Model name or date (YYYY-MM-DD)

**Examples:**
- "生成今日错误日报" → `resilience_report({ reportType: "daily" })`
- "查看 mimo-v2.5 的详细报告" → `resilience_report({ reportType: "model", target: "mimo-v2.5" })`
- "查看任务恢复状态" → `resilience_report({ reportType: "recovery" })`
- "生成完整状态报告" → `resilience_report({ reportType: "full" })`

### resilience_recovery

View or update automatic session recovery settings. Use this when the user wants to change the "continue the task" wording after a session failure, switch Chinese/English recovery language, or disable/enable automatic recovery.

**Parameters:**
- `action`: `"show"` (default) | `"update"` | `"reset"`
- `enabled`: `true` / `false`
- `language`: `"zh"` | `"en"`
- `prompt`: custom prompt overriding localized defaults
- `promptZh`: custom Chinese prompt
- `promptEn`: custom English prompt
- `ttlMs`: queued recovery context TTL
- `cooldownMs`: minimum interval between recovery injections per session
- `maxPerSession`: maximum automatic injections per session

**Examples:**
- "查看会话自动恢复设置" → `resilience_recovery({ action: "show" })`
- "把继续任务话术改成中文" → `resilience_recovery({ action: "update", language: "zh" })`
- "把继续任务话术改成英文" → `resilience_recovery({ action: "update", language: "en" })`
- "修改继续任务话术为：任务完成了吗？如果没完成请继续完成任务" → `resilience_recovery({ action: "update", language: "zh", prompt: "任务完成了吗？如果没完成请继续完成任务。" })`
- "关闭会话自动恢复" → `resilience_recovery({ action: "update", enabled: false })`

## Error Categories

| Category | Description | Retryable |
|----------|-------------|-----------|
| `rate_limit` | 429 Too Many Requests | ✅ |
| `server_overload` | 503 Service Unavailable | ✅ |
| `timeout` | Request timeout | ✅ |
| `auth_failed` | 401/403 Authentication failed | ❌ |
| `network_error` | Connection errors | ✅ |
| `model_unavailable` | Model not found or offline | ✅ |
| `context_too_long` | Context length exceeded | ❌ |
| `token_parse_error` | Tokenizer/token parsing failure | ❌ |
| `invalid_model_output` | Malformed model output / response format failure | ❌ |
| `session_runtime_error` | Non-API session runtime failure | ❌ |
| `unknown` | Unclassified errors | ❌ |

## Retry Strategies

### Strategy Types

- **fixed**: Fixed interval between retries (e.g., every 30s)
- **exponential**: Exponential backoff (1min → 2min → 4min → 8min...)
- **custom**: User-defined interval schedule (e.g., [1min, 3min, 5min, 15min])

### Default Strategies

| Name | Type | Max Retries | Intervals | Error Types |
|------|------|-------------|-----------|-------------|
| default-exponential | exponential | 5 | 1m→15m | rate_limit, server_overload, timeout, network_error |
| rate-limit-fixed | fixed | 3 | 30s | rate_limit |
| model-backoff | custom | 6 | 1m→2h | server_overload, model_unavailable |
| network-retry | exponential | 4 | 5s→1m | network_error |

## Data Storage

Per-instance data: `~/.openclaw/plugins/resilience/instances/<instance-id>/` (stats, logs, strategies, tasks). Legacy root layout is still read as `default`.

```
~/.openclaw/plugins/resilience/instances/<instance-id>/
├── meta.json
├── stats.json
├── strategies.json
├── recovery-settings.json
├── active-retries.json
├── logs/YYYY-MM-DD.jsonl
└── tasks/
```
