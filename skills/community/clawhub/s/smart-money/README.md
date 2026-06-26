[🇺🇸 English](#english) · [🇨🇳 中文](#chinese)

---

<a name="english"></a>

# Smart Money Tracker

> AI Agent on-chain whale tracking skill. Track smart money wallets, get real-time trading signals including LP pool entries and custom address subscriptions.

**v1.2**: Add up to 5 personal wallets for real-time monitoring. Same address shared across agents uses one subscription stream (Reference Counting) — no duplicate billing.  
**v1.1**: Whale LP activity tracking — detect when smart money adds/removes liquidity on Uniswap V2/V3.

## Install

```bash
openclaw skill install https://github.com/AntalphaAI/smart-money
```

## Architecture

```
Agent (OpenClaw)  ──MCP──►  Antalpha Server  ──►  On-chain Data Provider
                              │                    (Streams + REST)
                  agent_id    ├── smart_money_watchlist
                              ├── agent_watched_wallets   ← v1.2 new
                              └── sm_stream_registry      ← v1.2 new (RC)
```

- **MCP remote mode**: Backend on Antalpha server, agents call via MCP protocol
- **Multi-tenant isolation**: Each agent gets a unique `agent_id`, custom watchlists are isolated per agent
- **Zero config**: No local API keys required for MCP mode
- **RC-based Streams**: Same wallet address across multiple agents shares one subscription stream

## Quick Start

```
# Step 1: Register (once)
Tool: antalpha-register
→ Save agent_id + api_key to ~/.smart-money/agent.json

# Step 2: Get whale signals
Tool: smart-money-signal
Args: { agent_id: "...", level: "high" }

# Step 3 (v1.2): Add your own address
Tool: smart-money-custom
Args: { agent_id: "...", action: "add", address: "0x...", label: "My Whale" }
→ On-chain subscription registered, stream_id back-filled

# Step 4: Query merged signals (public + your custom)
Tool: smart-money-signal
Args: { agent_id: "...", level: "all" }
```

## MCP Server

```
https://mcp-skills.ai.antalpha.com/mcp
```

## MCP Tools

| Tool | v | Description |
|------|---|-------------|
| `antalpha-register` | v1 | Register agent, get `agent_id` + `api_key` (call once) |
| `smart-money-signal` | v1.2 | Get trading signals — public pool **+** your custom addresses merged |
| `smart-money-watch` | v1 | View a specific wallet's recent activity |
| `smart-money-list` | v1 | List all monitored wallets (public + custom) |
| `smart-money-custom` | v1.2 | **Add / remove / list** custom addresses with auto on-chain subscription RC |
| `smart-money-pool` | v1.1 | Query whale LP activity on Uniswap V2/V3 |

## User Scenarios

### 🔍 Scenario 1 — Daily whale signal check

> "What are smart money wallets buying today?"

```
smart-money-signal { agent_id, level: "high", limit: 20 }
```

Response:
```
🔴 HIGH Signal | Paradigm Fund
Buy PEPE — $127.5K · First position ever
TX: 0xabc...def | 2026-04-17 08:00 UTC

🟡 MEDIUM Signal | Wintermute
Accumulating ARB — $45K · 3rd buy in 24h
TX: 0x123...456 | 2026-04-17 06:20 UTC

Powered by Antalpha AI
```

---

### 👁 Scenario 2 — Track a specific wallet's activity

> "Show me what Paradigm has been doing lately"

```
smart-money-watch { agent_id, address: "0xParadigm...", limit: 10 }
```

---

### ➕ Scenario 3 — Add a personal wallet to monitor (v1.2.1)

> "Track this address for me: 0xABC... — it's my target whale"

```
# Step 1: Add to custom list (on-chain subscription auto-registered)
smart-money-custom {
  agent_id,
  action: "add",
  address: "0xABC...",
  label: "Target Whale"
}

# Step 2: Check current signals (auto-triggers a fresh scan + baseline)
smart-money-signal { agent_id, level: "all" }
```

> ⚠️ **After Step 1, agent MUST show this warning:**
>
> *The data provider is now tracking `0xABC...` in real time. However, MCP cannot push notifications to you — signals are stored server-side only. **Without a scheduled Cron task, you will NEVER receive alerts.***
>
> *Strongly recommended: create a 15-min Cron task now — I will execute it for you automatically. Skipping this means you will not receive any alerts.*

```bash
# Step 4 (recommended — after user confirms):
openclaw cron add \
  --name "smart-money-alert" \
  --cron "*/15 * * * *" \
  --session isolated \
  --message "Call smart-money-signal agent_id <id> level high since <last_check>. Alert if new signals. Reply HEARTBEAT_OK if none."
```

**Result**: Address is monitored via on-chain data subscription. Combined signals (public pool + custom) returned by `smart-money-signal`. Cron closes the notification loop.

---

### 📋 Scenario 4 — List and manage custom addresses (v1.2)

> "Which addresses am I watching? How many slots are left?"

```
smart-money-custom { agent_id, action: "list" }
```

Response:
```json
{
  "private_count": 2,
  "remaining_slots": 3,
  "wallets": [
    { "address": "0xABC...", "label": "Target Whale", "stream_id": "abc-123", "added_at": "2026-04-17T08:00:00Z" },
    { "address": "0xDEF...", "label": "Fund X",       "stream_id": "def-456", "added_at": "2026-04-16T12:00:00Z" }
  ]
}
```

---

### ➖ Scenario 5 — Remove a custom address (v1.2)

> "Stop tracking 0xABC..."

```
smart-money-custom { agent_id, action: "remove", address: "0xABC..." }
```

**Result**: Address removed, on-chain subscription cancelled (if no other agents are watching the same address via Reference Counting).

---

### 🏊 Scenario 6 — Whale LP pool activity

> "Is Paradigm adding liquidity anywhere recently?"

```
smart-money-pool {
  agent_id,
  address: "0xParadigm...",
  event_type: "POOL_IN",
  dex: "uniswap_v3",
  limit: 5
}
```

Response:
```
🔴 HIGH Signal | Paradigm Fund
POOL_IN — USDC/ETH (Uniswap V3) · $215K
Pool: 0x88e6A...  TX: 0xabc...def | 2026-04-14 04:00 UTC
```

---

### ⏰ Scenario 7 — Set up recurring monitoring (OpenClaw)

> "Alert me every hour if any high-level signals appear"

> ⚠️ **Why this matters**: The on-chain data provider pushes events to the MCP Server in real time, but MCP cannot push to you. Without this Cron, signals accumulate silently and you receive zero notifications.

```bash
# Recommended: 15-min interval for responsive alerts with reasonable token cost
openclaw cron add \
  --name "smart-money-alert" \
  --cron "*/15 * * * *" \
  --session isolated \
  --message "Call smart-money-signal with agent_id <id>, level high, since <last_check_iso>. If new signals found, notify me with a summary. If none, reply HEARTBEAT_OK."
```

*Cost note*: `--session isolated` + `HEARTBEAT_OK` on no-signal runs minimizes token usage. Each silent check ≈ 500 tokens; only pays full cost when real signals appear.

---

### 🔄 Scenario 8 — Multiple agents, same address (RC behavior)

> Agent A and Agent B both add `0xVitalik...`

- Agent A adds → on-chain subscription created, `ref_count = 1`
- Agent B adds → **same subscription reused**, `ref_count = 2`, no duplicate billing
- Agent A removes → `ref_count = 1`, subscription still active
- Agent B removes → `ref_count = 0`, subscription cancelled automatically

---

## Signal Levels

**Transfer / Swap signals:**

| Level | Trigger |
|-------|---------|
| 🔴 HIGH | Large buy > $50K, or first-time token position |
| 🟡 MEDIUM | Accumulation (≥2 buys of same token in 24h), or large sell > $50K |
| 🟢 LOW | Regular transfers $1K–$50K |

**Pool signals (POOL_IN / POOL_OUT):**

| Level | Trigger |
|-------|---------|
| 🔴 HIGH | Pool entry > $100K |
| 🟡 MEDIUM | Pool entry $10K–$100K |
| 🟢 LOW | Pool entry < $10K |

## Public Pool (19 wallets)

VC Funds: Paradigm, a16z, Polychain Capital, Dragonfly Capital, DeFiance Capital  
Market Makers: Wintermute, Jump Trading, Cumberland DRW  
Whales: Vitalik.eth, Justin Sun, James Fickel  
DeFi: Uniswap V2 ETH/USDT, Lido stETH, 0x Protocol  
Exchanges: Binance Hot Wallet 14, Robinhood  
Other: Nansen Smart Money 1, Alameda Research (Remnant), Celsius (Remnant)

## Data Source

- **On-chain data provider** — ERC20 transfers, native transfers, token prices
- **Real-time event streams** (v1.1+) — LP events + custom address webhook ingestion
- **ETH Mainnet only** (V1)

## Security Notes

- Agent identity via UUID — no private keys involved
- `api_key` is secret; store securely, never expose in logs or prompts
- Custom watchlist addresses are isolated per `agent_id` (multi-tenant)
- On-chain subscription cancelled automatically on `remove` (no zombie subscriptions, RC-guarded)
- All data comes from public blockchain; no user funds are touched

## Changelog

### v1.2.2 (2026-06-15)
- Fixed: removed the decommissioned `smart-money-scan` tool (no longer on the live MCP), which broke the "first scan / baseline" workflow step. Tool count 7 → 6.
- Changed: its on-demand scan is now folded into `smart-money-signal` (auto scan-if-stale + custom-address backfill on every call); workflows call `smart-money-signal` directly for the baseline.

### v1.2.1 (2026-04-17)
- Mandatory Cron setup prompt after `smart-money-custom action=add`
- Strong-nudge copy: "without Cron you will NEVER be notified" (EN + ZH)
- Recommended interval: 15 min with `--session isolated` flag
- Scenario 3 and 7 updated with actionable Cron commands

### v1.2.0 (2026-04-17)
- `smart-money-custom` upgraded: supports `add` / `remove` / `list` with on-chain subscription auto-management
- Reference Counting (RC): same address across multiple agents shares ONE subscription stream; auto-cleanup when last reference released
- New DB tables: `agent_watched_wallets`, `sm_stream_registry`
- `smart-money-signal` merges public pool + agent custom addresses in one response

### v1.1.0 (2026-04-14)
- New: `smart-money-pool` — whale LP add/remove events (Uniswap V2/V3)
- New: `POOL_IN` / `POOL_OUT` signal types in `smart-money-signal`
- New: Real-time on-chain event stream integration for LP webhook ingestion

### v1.0.2
- Add: monitoring setup guide, agent behavior rules

### v1.0.1 (2026-03-28)
- Various bugfixes and address normalization

### v1.0.0 (2026-03-28)
- Initial release

## License

MIT

---

<a name="chinese"></a>

# Smart Money 聪明钱追踪器

> AI Agent 链上鲸鱼追踪技能。追踪聪明钱钱包动向，获取实时交易信号（含 LP 入池信号与自定义地址订阅）。

**v1.2 新增**：自定义地址订阅 — 最多添加 5 个个人监控地址，通过实时数据订阅服务推送信号。相同地址跨多个 Agent 共享一个订阅流（引用计数），避免重复计费。  
**v1.1 新增**：鲸鱼 LP 行为追踪 — 当聪明钱在 Uniswap V2/V3 添加流动性时自动生成高强度信号。

## 安装

```bash
openclaw skill install https://github.com/AntalphaAI/smart-money
```

## 架构

```
Agent (OpenClaw)  ──MCP──►  Antalpha 服务器  ──►  On-chain Data Provider
                              │                    (Streams + REST)
                  agent_id    ├── smart_money_watchlist
                              ├── agent_watched_wallets   ← v1.2 新增
                              └── sm_stream_registry      ← v1.2 新增（引用计数）
```

- **MCP 远程模式**：后端部署在 Antalpha 服务器，Agent 通过 MCP 协议调用
- **多租户隔离**：每个 Agent 获得唯一 `agent_id`，自定义监控列表相互隔离
- **零配置**：MCP 模式无需本地 API Key
- **引用计数 Stream**：多 Agent 监控同一地址时共享一个订阅流

## 快速上手

```
# 第一步：注册（仅需一次）
工具：antalpha-register
→ 保存 agent_id + api_key 到 ~/.smart-money/agent.json

# 第二步：获取鲸鱼信号
工具：smart-money-signal
参数：{ agent_id: "...", level: "high" }

# 第三步（v1.2）：添加自定义地址
工具：smart-money-custom
参数：{ agent_id: "...", action: "add", address: "0x...", label: "目标鲸鱼" }
→ 链上订阅自动创建，stream_id 回填

# 第四步：查询合并信号（公共池 + 自定义地址）
工具：smart-money-signal
参数：{ agent_id: "...", level: "all" }
```

## MCP 服务器

```
https://mcp-skills.ai.antalpha.com/mcp
```

## MCP 工具

| 工具 | 版本 | 说明 |
|------|------|------|
| `antalpha-register` | v1 | 注册 Agent，获取 `agent_id` + `api_key`（仅需一次） |
| `smart-money-signal` | v1.2 | 获取交易信号（公共池 **+** 自定义地址合并） |
| `smart-money-watch` | v1 | 查看指定钱包的近期活动 |
| `smart-money-list` | v1 | 列出所有监控钱包（公共 + 自定义） |
| `smart-money-custom` | v1.2 | **添加 / 删除 / 查看**自定义地址，自动管理链上订阅（引用计数） |
| `smart-money-pool` | v1.1 | 查询鲸鱼 LP 活动（Uniswap V2/V3 入池/退池） |

## 用户场景

### 🔍 场景一 — 日常鲸鱼信号查看

> "今天聪明钱在买什么？"

```
smart-money-signal { agent_id, level: "high", limit: 20 }
```

返回示例：
```
🔴 高强度信号 | Paradigm Fund
买入 PEPE — $127.5K · 首次建仓
TX: 0xabc...def | 2026-04-17 08:00 UTC

🟡 中强度信号 | Wintermute
累积 ARB — $45K · 24h 内第 3 次买入
TX: 0x123...456 | 2026-04-17 06:20 UTC

由 Antalpha AI 提供聚合服务
```

---

### 👁 场景二 — 查看特定钱包动向

> "Paradigm 最近在做什么？"

```
smart-money-watch { agent_id, address: "0xParadigm...", limit: 10 }
```

---

### ➕ 场景三 — 添加个人监控地址（v1.2.1）

> "帮我追踪这个地址：0xABC...，这是我盯的目标鲸鱼"

```
# 第一步：添加到自定义列表（链上订阅自动创建）
smart-money-custom {
  agent_id,
  action: "add",
  address: "0xABC...",
  label: "目标鲸鱼"
}

# 第二步：查看当前信号（自动触发一次扫描 + 建立基线）
smart-money-signal { agent_id, level: "all" }
```

> ⚠️ **添加完成后，Agent 必须显示以下强提示：**
>
> *服务商已开始实时监控 `0xABC...`，但 MCP 协议无法主动推送通知——链上信号会存入数据库，但你**永远收不到提醒**。不创建定时检查任务将无法收到任何告警。*
>
> *建议现在创建 15 分钟定时任务（见场景七）。不创建也可以，但业务龙头可能已过。*

```bash
# 第四步（用户确认后创建）：
openclaw cron add \
  --name "smart-money-alert" \
  --cron "*/15 * * * *" \
  --session isolated \
  --message "使用 agent_id <id> 调用 smart-money-signal，level 为 high，since 为 <上次检查时间>。有新信号则通知我，无新信号则静默回复 HEARTBEAT_OK。"
```

**效果**：自定义地址通过实时数据订阅监控，Cron 定时拉取信号，信号到达即时通知用户。

---

### 📋 场景四 — 查看并管理自定义地址（v1.2）

> "我现在在追踪哪些地址？还剩几个名额？"

```
smart-money-custom { agent_id, action: "list" }
```

返回示例：
```json
{
  "private_count": 2,
  "remaining_slots": 3,
  "wallets": [
    { "address": "0xABC...", "label": "目标鲸鱼", "stream_id": "abc-123", "added_at": "2026-04-17T08:00:00Z" },
    { "address": "0xDEF...", "label": "Fund X",   "stream_id": "def-456", "added_at": "2026-04-16T12:00:00Z" }
  ]
}
```

---

### ➖ 场景五 — 取消监控某个地址（v1.2）

> "不想追踪 0xABC... 了"

```
smart-money-custom { agent_id, action: "remove", address: "0xABC..." }
```

**效果**：地址从列表中移除，对应链上订阅自动注销（引用计数归零时才真正取消）。

---

### 🏊 场景六 — 鲸鱼 LP 入池检测

> "Paradigm 最近有没有往流动性池里加钱？"

```
smart-money-pool {
  agent_id,
  address: "0xParadigm...",
  event_type: "POOL_IN",
  dex: "uniswap_v3",
  limit: 5
}
```

返回示例：
```
🔴 高强度信号 | Paradigm Fund
POOL_IN — USDC/ETH（Uniswap V3）· $215K
池子：0x88e6A...  TX: 0xabc...def | 2026-04-14 04:00 UTC
```

---

### ⏰ 场景七 — 设置定时监控（OpenClaw）

> "每小时提醒我一次高强度信号"

> ⚠️ **为什么必须创建**：数据服务商实时将信号推送到 MCP Server，但 MCP 无法主动通知你。不设置 Cron，信号将静默积庋，你永远收不到提醒。

```bash
# 推荐间隔：15 分钟（响应速度与 Token 消耗的平衡点）
openclaw cron add \
  --name "smart-money-alert" \
  --cron "*/15 * * * *" \
  --session isolated \
  --message "使用 agent_id <id> 调用 smart-money-signal，level 为 high，since 为 <上次检查时间 ISO 格式>。有新信号则摘要通知我，无新信号则静默回复 HEARTBEAT_OK。"
```

*成本说明*：`--session isolated` + 无信号时静默回复 `HEARTBEAT_OK` 大幅减少 Token 消耗。只有实际有信号时才会消耗完整回复的 Token。

---

### 🔄 场景八 — 多 Agent 共享地址的引用计数行为（v1.2）

> Agent A 和 Agent B 都添加了 `0xVitalik...`

- Agent A 添加 → 链上订阅创建，`ref_count = 1`
- Agent B 添加 → **复用同一 Stream**，`ref_count = 2`，无重复计费
- Agent A 删除 → `ref_count = 1`，Stream 继续存活
- Agent B 删除 → `ref_count = 0`，Stream 自动删除

---

## 信号等级

**转账 / 交换信号：**

| 等级 | 触发条件 |
|------|---------|
| 🔴 高 | 单笔买入 > $50K，或首次持仓某 Token |
| 🟡 中 | 24h 内同一 Token 累计买入 ≥ 2 次，或单笔卖出 > $50K |
| 🟢 低 | 常规转账 $1K–$50K |

**LP 池子信号（POOL_IN / POOL_OUT）：**

| 等级 | 触发条件 |
|------|---------|
| 🔴 高 | 入池金额 > $100K |
| 🟡 中 | 入池金额 $10K–$100K |
| 🟢 低 | 入池金额 < $10K |

## 公共监控池（19 个钱包）

VC 基金：Paradigm、a16z、Polychain Capital、Dragonfly Capital、DeFiance Capital  
做市商：Wintermute、Jump Trading、Cumberland DRW  
巨鲸：Vitalik.eth、孙宇晨、James Fickel  
DeFi 协议：Uniswap V2 ETH/USDT、Lido stETH、0x Protocol  
交易所：Binance 热钱包 14、Robinhood  
其他：Nansen Smart Money 1、Alameda Research（残余）、Celsius（残余）

## 数据来源

- **数据服务商** — ERC20 转账、原生代币转账、Token 价格
- **实时事件订阅**（v1.1+）— LP 事件 + 自定义地址 Webhook 落库
- **仅支持以太坊主网**（V1）

## 安全说明

- Agent 身份通过 UUID 标识，不涉及私钥
- `api_key` 为私密凭据，请安全存储，切勿在日志或提示词中暴露
- 自定义监控列表按 `agent_id` 隔离（多租户）
- `remove` 操作自动注销链上订阅（引用计数保护，无僵尸订阅）
- 所有数据均来自公开链上数据，不涉及用户资金

## 更新日志

### v1.2.2（2026-06-15）
- 修复：移除已下线的 `smart-money-scan` 工具（线上 MCP 已无此工具），它曾导致"首次扫描/建立基线"工作流步骤失败。工具数 7 → 6。
- 变更：其按需扫描能力已并入 `smart-money-signal`（每次调用自动 scan-if-stale + 回填自定义地址）；工作流改为直接调用 `smart-money-signal` 建立基线。

### v1.2.1（2026-04-17）
- 新增：`smart-money-custom action=add` 完成后强制提示创建 Cron 定时任务
- 新增：强提示警示文案（中英双语）：“不创建 Cron 则永远收不到通知”
- 新增：推荐间隔 15 分钟，增加 `--session isolated` 参数
- 场景三、场景七均已更新为可直接执行的 Cron 命令

### v1.2.0（2026-04-17）
- 升级：`smart-money-custom` 支持 `add` / `remove` / `list`，自动管理链上订阅
- 新增：引用计数（RC）— 多 Agent 监控同一地址共享一个订阅流，最后一个引用释放时自动取消
- 新增：数据表 `agent_watched_wallets`、`sm_stream_registry`
- 升级：`smart-money-signal` 合并公共池 + 自定义地址两路结果，统一返回

### v1.1.0（2026-04-14）
- 新增：`smart-money-pool` 工具，查询鲸鱼 LP 添加/移除活动（Uniswap V2/V3）
- 新增：`POOL_IN` / `POOL_OUT` 信号类型
- 新增：实时事件订阅集成，接收 LP 事件

### v1.0.2
- 新增监控设置指南和 Agent 行为规则

### v1.0.1（2026-03-28）
- 多项 Bug 修复及地址规范化

### v1.0.0（2026-03-28）
- 初始版本

## 许可证

MIT
