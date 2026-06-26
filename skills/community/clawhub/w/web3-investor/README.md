# Web3 Investor Skill

> **English** | [中文](#chinese)

AI-friendly DeFi investment intelligence skill. Discover, analyze, and compare yield opportunities across Ethereum, Base, Arbitrum, and Optimism — powered by Antalpha's remote MCP server. No API keys needed.

---

## Installation

```bash
openclaw skill install https://github.com/AntalphaAI/web3-investor
```

### Install via ClawHub

```bash
clawhub install web3-investor
```

> Requires [OpenClaw](https://www.antalpha.com/) with Python 3.7+.  
> No environment variables required — all data is fetched from the remote MCP server.

---

## Features

### 1. Opportunity Discovery (`discover`)
Search for DeFi yield opportunities across chains with flexible filters:
- Filter by chain: `ethereum`, `base`, `arbitrum`, `optimism`
- Filter by minimum / maximum APY
- Stablecoin-only mode
- Natural language query support (e.g. "I want safe yields on Base")
- Session-aware: remembers your preferences across calls

### 2. Deep Analysis (`analyze`)
Get a detailed breakdown of any single investment product:
- Basic / detailed / full depth levels
- Historical performance data
- LLM-generated insights
- Optional: skip history for faster response

### 3. Multi-Product Comparison (`compare`)
Side-by-side comparison of 2 or more products:
- Unified metrics table
- Comparative analysis
- Final recommendation

### 4. Intent Clarification Flow (`confirm-intent` / `get-intent`)
When a query is ambiguous, the server returns a clarification request. The agent:
1. Presents clarification options to the user
2. Calls `confirm-intent` to lock in preferences (risk profile, capital nature, liquidity need)
3. Re-runs discovery with the stored intent

### 5. Feedback Loop (`feedback`)
Submit feedback on any recommendation:
- Outcomes: `helpful`, `not_helpful`, `invested`, `dismissed`
- Optional free-text reason
- Feeds back into server-side recommendation quality

---

## Commands & Usage

### discover
```bash
python3 scripts/mcp_client.py discover \
  --chain <ethereum|base|arbitrum|optimism> \
  --min-apy <number> \
  [--max-apy <number>] \
  [--stablecoin-only] \
  [--limit <1-10>] \
  [--session-id <id>] \
  [--natural-language "<query>"]
```

### analyze
```bash
python3 scripts/mcp_client.py analyze \
  --product-id <id> \
  [--depth basic|detailed|full] \
  [--no-history]
```

### compare
```bash
python3 scripts/mcp_client.py compare \
  --ids <id1> <id2> [<id3> ...]
```

### feedback
```bash
python3 scripts/mcp_client.py feedback \
  --product-id <id> \
  --feedback <helpful|not_helpful|invested|dismissed> \
  [--reason "<text>"]
```

### confirm-intent
```bash
python3 scripts/mcp_client.py confirm-intent \
  --session-id <id> \
  --type <intent_type> \
  --risk <conservative|moderate|aggressive> \
  [--capital-nature <nature>] \
  [--liquidity-need <need>]
```

### get-intent
```bash
python3 scripts/mcp_client.py get-intent \
  --session-id <id>
```

---

## MCP Tools Reference

| Tool | Purpose | Key Response Fields |
|------|---------|---------------------|
| `investor_discover` | Find yield opportunities | `recommendations[]`, `intent{}`, `search_stats` |
| `investor_analyze` | Deep analysis of one product | `product{}`, `historical_data`, `llm_insights` |
| `investor_compare` | Compare multiple products | `products[]`, `comparisons[]`, `recommendation` |
| `investor_feedback` | Submit feedback | `acknowledged` |
| `investor_confirm_intent` | Lock in user intent | `acknowledged`, `session_id` |
| `investor_get_stored_intent` | Retrieve stored intent | `found`, `intent{}` |

---

## Example Sessions

**Find and analyze:**
```
User: Find ETH lending on Base with >5% APY
→ discover --chain base --min-apy 5

User: Analyze the top result
→ analyze --product-id aave-eth-base --depth detailed
```

**Compare two products:**
```
→ compare --ids aave-usdc-base compound-usdc-ethereum
```

**Intent clarification:**
```
User: I want to invest in DeFi
→ discover --natural-language "I want to invest in DeFi"
  [Server returns NEEDS_CLARIFICATION]

User: Stablecoin, moderate risk, 1 month horizon
→ confirm-intent --session-id <id> --type stablecoin --risk moderate
→ discover --session-id <id>
```

---

## Architecture

```
web3-investor/
├── scripts/
│   └── mcp_client.py     # Thin MCP client wrapper
├── config/
│   └── config.json       # MCP server endpoint config
└── SKILL.md              # Agent skill definition
```

- All business logic runs on the remote MCP server: `https://mcp-skills.ai.antalpha.com/mcp`
- The local client handles only: MCP session handshake, request routing, SSE response parsing
- No local API keys, no local data storage

## Security

- All API keys managed server-side
- No sensitive data stored locally
- MCP session protocol: `initialize` → `notifications/initialized` → `tools/call` (with `Mcp-Session-Id` header)

---

## Changelog

### v2.0.3 — 2026-04-08
- Add `homepage` metadata for provenance and ClawHub trust signals
- No functional changes

### v2.0.2 — 2026-04-08 ⭐ *Recommended baseline*
- **Fix critical connection bug**: "No valid session ID provided" error resolved
- Add `MCPClient` class with proper session management
- Implement full MCP 2024-11-05 handshake: `initialize` → `notifications/initialized`
- Parse `mcp-session-id` from response headers and reuse across calls
- Add SSE (`text/event-stream`) response parsing
- Type hints, improved docstrings, singleton pattern
- Timeouts: initialize 60s, tools 120s

### v2.0.1 — 2026-04-08
- **Security fix**: Remove all `localhost:3000` signer API references
- Remove `DUNE_API_KEY` environment variable dependency
- Strip all trading/execution code and legacy local modules
- Simplify config to MCP endpoint only
- Confirm `env: []` — no local API keys required

### v2.0.0 — 2026-04-08 ⚠️ *Breaking change*
- Full architecture rewrite: local discovery/trading modules → thin MCP client wrapper
- New commands: `discover`, `analyze`, `compare`, `feedback`, `confirm-intent`, `get-intent`
- Natural language query support
- Intent clarification flow
- Remove all local API key dependencies

### v0.5.x — 2026-03-29 to 2026-03-30
- Legacy versions with local service architecture (deprecated)
- Various metadata format fixes for ClawHub compatibility

---

## License

MIT — [Antalpha AI Team](https://www.antalpha.com/)

---

---

<a name="chinese"></a>

# Web3 Investor Skill（中文文档）

AI 驱动的 DeFi 收益发现与分析技能。支持在 Ethereum、Base、Arbitrum、Optimism 四条链上发现、分析和对比投资机会，所有数据通过 Antalpha 远端 MCP 服务器获取，**无需本地 API Key**。

---

## 安装

```bash
openclaw skill install https://github.com/AntalphaAI/web3-investor
```

### 通过 ClawHub 安装

```bash
clawhub install web3-investor
```

> 依赖 [OpenClaw](https://www.antalpha.com/)，Python 3.7+。  
> 无需配置任何环境变量。

---

## 功能介绍

### 1. 机会发现（`discover`）
在多条链上搜索 DeFi 收益机会，支持灵活过滤：
- 按链筛选：`ethereum`、`base`、`arbitrum`、`optimism`
- 按最低 / 最高 APY 筛选
- 仅限稳定币模式
- 自然语言查询（如"帮我找 Base 上安全稳健的收益"）
- 会话感知：跨调用记忆你的偏好

### 2. 深度分析（`analyze`）
对单一投资产品进行详细解析：
- 支持 basic / detailed / full 三个分析深度
- 历史表现数据
- LLM 生成的投资洞察
- 可跳过历史数据以加速响应

### 3. 多产品对比（`compare`）
同时对比 2 个及以上投资产品：
- 统一指标横向对比
- 综合分析报告
- 最终推荐建议

### 4. 意图澄清流程（`confirm-intent` / `get-intent`）
当查询语义不明时，服务端返回澄清问题，Agent 会：
1. 向用户展示选项
2. 调用 `confirm-intent` 锁定偏好（风险等级、资金属性、流动性需求）
3. 携带已存储意图重新执行发现

### 5. 反馈回路（`feedback`）
对任何推荐结果提交反馈：
- 结果类型：`helpful`（有帮助）、`not_helpful`（无帮助）、`invested`（已投资）、`dismissed`（忽略）
- 可附加文字原因
- 反馈数据用于服务端推荐质量优化

---

## 命令与用法

### discover — 发现机会
```bash
python3 scripts/mcp_client.py discover \
  --chain <ethereum|base|arbitrum|optimism> \
  --min-apy <数字> \
  [--max-apy <数字>] \
  [--stablecoin-only] \
  [--limit <1-10>] \
  [--session-id <id>] \
  [--natural-language "<查询语句>"]
```

### analyze — 深度分析
```bash
python3 scripts/mcp_client.py analyze \
  --product-id <产品ID> \
  [--depth basic|detailed|full] \
  [--no-history]
```

### compare — 多产品对比
```bash
python3 scripts/mcp_client.py compare \
  --ids <id1> <id2> [<id3> ...]
```

### feedback — 提交反馈
```bash
python3 scripts/mcp_client.py feedback \
  --product-id <产品ID> \
  --feedback <helpful|not_helpful|invested|dismissed> \
  [--reason "<原因文字>"]
```

### confirm-intent — 确认用户意图
```bash
python3 scripts/mcp_client.py confirm-intent \
  --session-id <id> \
  --type <意图类型> \
  --risk <conservative|moderate|aggressive> \
  [--capital-nature <属性>] \
  [--liquidity-need <需求>]
```

### get-intent — 获取已存储意图
```bash
python3 scripts/mcp_client.py get-intent \
  --session-id <id>
```

---

## MCP 工具一览

| 工具 | 用途 | 关键返回字段 |
|------|------|-------------|
| `investor_discover` | 发现收益机会 | `recommendations[]`, `intent{}`, `search_stats` |
| `investor_analyze` | 单产品深度分析 | `product{}`, `historical_data`, `llm_insights` |
| `investor_compare` | 多产品横向对比 | `products[]`, `comparisons[]`, `recommendation` |
| `investor_feedback` | 提交反馈 | `acknowledged` |
| `investor_confirm_intent` | 锁定用户意图 | `acknowledged`, `session_id` |
| `investor_get_stored_intent` | 获取已存储意图 | `found`, `intent{}` |

---

## 使用示例

**发现并分析：**
```
用户：帮我找 Base 上 APY > 5% 的 ETH 借贷
→ discover --chain base --min-apy 5

用户：分析排名第一的产品
→ analyze --product-id aave-eth-base --depth detailed
```

**对比两个产品：**
```
→ compare --ids aave-usdc-base compound-usdc-ethereum
```

**意图澄清流程：**
```
用户：我想投资 DeFi
→ discover --natural-language "我想投资 DeFi"
  [服务端返回 NEEDS_CLARIFICATION]

用户：稳定币，中等风险，1个月期限
→ confirm-intent --session-id <id> --type stablecoin --risk moderate
→ discover --session-id <id>
```

---

## 架构说明

```
web3-investor/
├── scripts/
│   └── mcp_client.py     # 轻量 MCP 客户端封装
├── config/
│   └── config.json       # MCP 服务端地址配置
└── SKILL.md              # Agent 技能定义文件
```

- 所有业务逻辑运行在远端 MCP 服务器：`https://mcp-skills.ai.antalpha.com/mcp`
- 本地客户端仅负责：MCP 会话握手、请求路由、SSE 响应解析
- 无本地 API Key，无本地数据存储

## 安全说明

- 所有 API Key 由服务端统一管理
- 本地不存储任何敏感数据
- MCP 会话协议：`initialize` → `notifications/initialized` → `tools/call`（携带 `Mcp-Session-Id` header）

---

## 版本更新说明

### v2.0.3 — 2026-04-08
- 添加 `homepage` 元数据，改善 ClawHub 信任评分
- 无功能性变更

### v2.0.2 — 2026-04-08 ⭐ *推荐基准版本*
- **修复关键连接 Bug**：彻底解决 "No valid session ID provided" 错误
- 新增 `MCPClient` 类，实现完整会话管理
- 实现标准 MCP 2024-11-05 握手流程：`initialize` → `notifications/initialized`
- 从响应头提取并复用 `mcp-session-id`
- 新增 SSE（`text/event-stream`）响应解析
- 完善类型注解、文档字符串，采用单例模式
- 超时配置：初始化 60s，工具调用 120s

### v2.0.1 — 2026-04-08
- **安全修复**：移除所有 `localhost:3000` 签名 API 引用
- 移除 `DUNE_API_KEY` 环境变量依赖
- 删除所有交易执行代码和历史遗留本地模块
- 简化 config 仅保留 MCP 端点配置
- 确认 `env: []`，无需任何本地 API Key

### v2.0.0 — 2026-04-08 ⚠️ *破坏性变更*
- 架构全量重写：本地发现/交易模块 → 轻量 MCP 客户端封装
- 新增 6 条命令：`discover`、`analyze`、`compare`、`feedback`、`confirm-intent`、`get-intent`
- 支持自然语言查询
- 支持意图澄清流程
- 移除所有本地 API Key 依赖

### v0.5.x — 2026-03-29 至 2026-03-30
- 旧版本，采用本地服务架构（已废弃）
- 多次修复 ClawHub 元数据格式兼容性问题

---

## 开源协议

MIT — [Antalpha AI 团队](https://www.antalpha.com/)
