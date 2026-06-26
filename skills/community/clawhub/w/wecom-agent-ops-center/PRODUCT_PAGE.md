# 企微 Agent Ops Center v2.4

**在企微群里看到你的 AI Agent 在做什么。** 不只是消息通道——实时心跳监控、异常秒级告警、每日健康报告、进程自动守护、敏感信息拦截、网络请求白名单，**让 AI 从「黑盒」变「透明」。

> 🚀 **ClawHub 首发**：WorkBuddy + OpenClaw 用户 2 分钟接入，为你的 AI 助手穿上「运维铠甲」。

## 一句话

> 为企微上的 AI Agent 提供统一的可观测性层。WorkBuddy 桌面用户和 OpenClaw 自托管用户都能用，2 分钟接入，0 学习成本。

## 与你有什么关系

| 角色 | 你的痛点 | 我们怎么解决 |
|------|---------|-------------|
| **WorkBuddy 用户** | Agent 挂了没人知道，任务失败第二天才发现 | 心跳检测 + 企微群自动告警 + 任务进度直播 |
| **OpenClaw 自托管用户** | 服务器上的实例不稳定，不知道什么时候挂了 | 自托管稳定性监控 + 资源告警（CPU/内存/磁盘） |
| **企业运维** | 几十个 Agent 跑在后台，完全黑盒 | 统一健康仪表板 + 日报推送 + 多 Agent 拓扑 |
| **业务负责人** | Agent 到底有没有在干活？花了多少钱？ | 调用统计 + 延迟追踪 + 审计日志 |
| **任何用 AI 的团队** | 不想用自己的 API Key，不想配 LLM | 我们只管监控，不管 AI（LLM 你自选） |

## 与"企微 AI 聊天机器人"的区别

| | AI 聊天机器人 | 企微 Agent Ops Center |
|---|---|---|
| 产品类型 | AI 对话服务 | **Agent 运维工具** |
| LLM 谁负责 | 服务商内置 | **你自己配**（DeepSeek / GPT / 自建） |
| 价值 | 能聊天 | **能看到 Agent 在干什么** |
| 类比 | 外包客服 | **给客服团队装监控 + 对讲机** |
| 粘性 | 换了损失对话历史 | **换了损失所有 Agent 健康数据** |

## 为什么是现在

- 企业微信已有 **15 万+** 企业在跑 AI Agent（数据来源：腾讯企微 2026 公开报告）
- 所有已部署 AI Agent 的企业都面临同一个问题：**「Agent 还在跑吗？」**
- 飞书生态的 `feishu-evolver-wrapper` 下载量 2.8 万，证明「AI 可观测性」是刚需
- 企微生态目前 **零同类产品**——这是一个空白品类

## 核心能力（v2.4 完整版）

```
你的 Agent      ←→   企微 Agent Ops Center    ←→   企微群
(WorkBuddy /          ┌─ 消息转发（L1 基础设施）
 OpenClaw /             ├─ 心跳监控（L2 可观测性）★ 核心
 ADP / 自建)            ├─ 异常告警（L2 通知）
                        ├─ 任务进度直播（L2 任务追踪）
                        ├─ 资源看板（L2 资源采集）
                        ├─ 审计日志（L2 审计追溯）
                        ├─ 进程守护 + 自动重启（L2 Lifecycle）★ NEW v2.4
                        ├─ 敏感信息扫描防护（L2 Secrets）★ NEW v2.4
                        ├─ 网络请求白名单（L2 NetworkGuard）★ NEW v2.4
                        ├─ 健康仪表板（L2 可视化）
                        └─ P2P 跨组织通信（Phase 2）
```

### L1 — 消息通道（免费，已有）
- WebSocket 长连接，零公网服务器
- 企微消息 ↔ Agent 双向透明转发
- 聊天历史不入库，不碰你的数据

### L2 — 监控与通知（新增 ★ 核心差异）
- **心跳检测**：每 30 秒检查 Agent 健康状态
- **秒级告警**：Agent 离线/降级 → 企微群推送告警卡片
- **每日报告**：自动生成健康日报，推送到指定企微群
- **状态仪表板**：`http://localhost:9527` 实时查看所有 Agent 状态
- **持久化历史**：Agent 运行数据本地保存，支持趋势分析

### L3 — P2P 跨组织通信（Phase 2）
- 配对码机制，零信任安全
- 跨公司 Agent 直连通信

## 快速开始

### 1. 安装

```bash
# 从 ClawHub 安装（推荐 — WorkBuddy / OpenClaw 用户）
clawhub install wecom-agent-ops-center

# 或从本地启动
git clone <repo> && cd wecom-connector
npm install
```

### 2. 获取企微凭证

```
企微管理后台 → 应用管理 → 智能机器人 → 复制 Bot ID 和 Secret
```

### 3. 配置

```bash
cp config.yaml.example config.yaml
# 编辑 config.yaml，填入 bot_id、bot_secret、你的 Agent 端点
```

**WorkBuddy 用户最小配置：**
```yaml
wecom:
  bot_id: "你的BotID"
  bot_secret: "你的BotSecret"

adapters:
  - type: "workbuddy"
    agent:
      id: "my-workbuddy"
      endpoint: "http://localhost:9527"  # WorkBuddy 本地端点
```

**OpenClaw 用户最小配置：**
```yaml
wecom:
  bot_id: "你的BotID"
  bot_secret: "你的BotSecret"

adapters:
  - type: "openclaw"
    agent:
      id: "my-openclaw"
      endpoint: "http://localhost:8080"  # OpenClaw 自托管端点
      selfHosted: true
```

### 4. 启动

```bash
node connector.js
```

### 5. 验证

- 在企微里 @机器人 发消息 → 你的 Agent 应回复
- 访问 `http://localhost:9527` → 查看 Agent 健康状态
- Agent 离线 3 次心跳后 → 企微群收到告警卡片

## 监控配置

```yaml
monitor:
  enabled: true
  heartbeat_interval: 30     # 心跳间隔（秒）
  offline_threshold: 3        # 连续失败次数 → 标记离线
  alert_cooldown: 300         # 告警冷却（秒），避免刷屏
  notify_chatid: "群聊ID"     # 告警推送到哪个企微群
  state_file: "./data/agent_states.json"

  # 可选：监控多个 Agent
  agents:
    - id: "customer-service"
      name: "AI客服Agent"
      endpoint: "http://localhost:3001/health"
    - id: "data-analyst"
      name: "数据分析Agent"
      endpoint: "http://localhost:3002/health"
```

## 告警卡片示例

**🟢 Agent 健康报告：**
```
📊 Agent 健康报告
更新时间：2026-05-30 10:30:00

🟢 3 正常  |  🟡 0 降级  |  🔴 0 离线
─────────────────
• 🟢 AI客服Agent — 120ms
• 🟢 数据分析Agent — 85ms
• 🟢 知识库Agent — 210ms
```

**🔴 异常告警：**
```
🚨 Agent 离线告警
─────────────────
| Agent | AI客服Agent |
| 连续失败 | 3 次 |
| 检查端点 | http://localhost:3001/health |
─────────────────
🔧 建议操作：
1. 检查 Agent 进程是否在运行
2. 手动测试：curl http://localhost:3001/health
```

## 架构

```
┌─ L3 企微 UI ─────────────────────────────────────┐
│  企微群 → 富卡片通知（告警/日报/任务进度/审计）   │
│  企微单聊 → 消息收发                              │
└──────────────┬───────────────────────────────────┘
               │ WebSocket
┌─ L2 监控通知 ★ ──────────────────────────────────┐
│  AgentMonitor → 心跳/健康检查/状态事件             │
│  TaskTracker  → 任务生命周期追踪（进度直播）        │
│  ResourceCollector → CPU/内存/队列监控             │
│  AuditLogger  → 决策点留痕 + 执行摘要              │
│  LinkTracker  → 多 Agent 链路拓扑 + 瓶颈定位       │
│  NotifyEngine → 卡片生成/防抖/分级告警             │
│  StateStore   → 状态持久化/历史追踪                │
└──────────────┬───────────────────────────────────┘
               │ EventBus
┌─ L1 统一抽象 ─────────────────────────────────────┐
│  AgentProfile / AgentStatus / TaskRecord          │
│  AuditEntry / CollaborationLink / MonitorEvent    │
└──────────────┬───────────────────────────────────┘
               │
┌─ L0 数据源适配 ★ ─────────────────────────────────┐
│  WorkBuddy Adapter  → 桌面 Agent（ClawHub 主力）  │
│  OpenClaw Adapter   → 自托管实例（ClawHub 主力）  │
│  ADP Claw Adapter   → 平台标准模式                │
│  ADP Multi Adapter  → 多 Agent 协作               │
│  ClawPro Adapter    → 企业平台                    │
│  Generic Adapter    → 通用 HTTP 心跳              │
│  A2A Adapter        → 标准协议兼容                │
└──────────────┬───────────────────────────────────┘
               │ HTTP / WebSocket / SDK
    ┌──────────┴──────────┐
    │                     │
WorkBuddy   OpenClaw   ADP/ClawPro
(桌面)      (自托管)    (云平台)
```

## 命令行

```bash
node connector.js              # 启动（监控 + 消息转发）
node connector.js pair         # 生成 P2P 配对码
node connector.js join <CODE>  # 加入 P2P 配对
node connector.js status       # 查看连接状态
node connector.js peers        # 查看已配对 Peers

# 环境变量
export WECOM_BOT_ID=xxx
export WECOM_BOT_SECRET=xxx
export AGENT_ENDPOINT=http://...
export MONITOR_NOTIFY_CHATID=群聊ID
node connector.js
```

## 技术栈

- **语言：** Node.js 18+
- **WebSocket：** `ws` 库（企微官方智能机器人协议）
- **监控：** 自建 AgentMonitor + NotifyEngine（无外部依赖）
- **持久化：** 本地 JSON 文件（StateStore）
- **消息转换：** 云端 API（www.hermesai.ltd）或本地降级
- **P2P 信令：** WebSocket 中继（可自建）

## 文件结构

```
wecom-connector/
├── ARCHITECTURE.md          # 完整架构设计（v3.0 四层 + 七适配器）
├── SKILL.md                 # 本文档（ClawHub 上架描述）
├── connector.js             # 主入口（v2.3）
├── config.yaml              # 用户配置（不提交）
├── config.yaml.example      # 配置模板（v2.3）
├── package.json             # v2.3.0
│
├── adapters/                # L0 — 数据源适配层 (v2.1)
│   ├── base-adapter.js      # 抽象基类
│   ├── generic-adapter.js   # 通用 HTTP 心跳 ★
│   ├── workbuddy-adapter.js # WorkBuddy 桌面 ★
│   └── openclaw-adapter.js  # OpenClaw 自托管 ★
│
├── core/                    # L2 — 核心监控引擎 (v2.3)
│   ├── agent-monitor.js     # Agent 健康监控 ★
│   ├── task-tracker.js      # 任务生命周期追踪 ★
│   ├── resource-collector.js # 资源指标采集 ★ (v2.2)
│   ├── audit-logger.js      # 审计日志 ★ (v2.3)
│   ├── notify-engine.js     # 通知卡片引擎 ★
│   ├── state-store.js       # 状态持久化 ★
│
├── integration/             # L1/L3 — 企微集成
│   ├── ws-client.js         # 企微 WebSocket
│   ├── agent-bridge.js      # Agent 通信桥接
│   ├── msg-converter.js     # 消息格式转换
│   └── dashboard-api.js     # 仪表板 API
│
├── dashboard/
│   └── dashboard.html       # 仪表板 UI
│
└── p2p/                     # P2P 子系统
    ├── p2p-router.js
    └── pairing-server.js
```

## 版本与定价

| 版本 | 价格 | 目标用户 | 功能 |
|------|------|---------|------|
| **L0 免费** | ¥0 | WorkBuddy / OpenClaw 个人用户 | 1 个 Agent 心跳监控 + 消息收发 + 本地仪表板 |
| **L1 Pro** | ¥99/月 | 重度 WorkBuddy/OpenClaw 用户 | 5 个 Agent + 任务进度直播 + 日报推送 + 7 天历史 |
| **L2 P2P** | ¥299/月 | 多 Agent 协作团队 | P2P 跨组织通信 + 链路可视化 + 配对管理 |
| **L3 企业版** | ¥4,999+/月 | ClawPro / ADP 企业用户 | 私有化部署 + 无限 Agent + 审计合规 + SLA 保障 |

> **ClawHub 分发策略**：L0 免费版作为引流 Skill，L1 Pro 通过私域转化。

## 常见问题

**Q：和企微自带的 AI 有什么区别？**
A：企微自带的是「AI 聊天」。我们是「Agent 运维工具」——不管你的 AI 是谁家的，我们帮你监控它是否正常运行。

**Q：我的 Agent 不是 HTTP 端点怎么办？**
A：只需提供一个 health check URL（返回 200 即可）。消息转发可以走其他方式，监控走 HTTP。

**Q：消息内容会经过你们的服务器吗？**
A：消息转换（企微格式 ↔ 标准格式）走云端 API，不存储明文。监控数据全部存在本地。也可以设置 `converter.enabled: false` 完全本地运行。

**Q：不用你们监控，我只要消息转发行不行？**
A：可以。设置 `monitor.enabled: false` 降级为纯消息转发模式（L1 层）。

## 竞品对比（v2.4 更新）

| | 企微自带 AI | 通用 AI 聊天机器人 | feishu-evolver-wrapper | 企微 Agent Ops Center |
|---|---|---|---|---|
| AI 可替换 | ❌ | 部分 | ✅ | ✅ 任意 LLM |
| Agent 监控 | ❌ | ❌ | ✅ | ✅ 心跳 + 告警 + 日报 |
| 任务进度推送 | ❌ | ❌ | ❌ | ✅ 分节点实时卡片 |
| 支持 WorkBuddy | ❌ | ❌ | ❌ | ✅ ClawHub Skill 一键安装 |
| 支持 OpenClaw | ❌ | ❌ | ❌ | ✅ 自托管稳定性监控 |
| 数据本地化 | ❌ | ❌ | ⚠️ 部分 | ✅ 监控数据全本地 |
| 跨组织通信 | ❌ | ❌ | ❌ | ✅ P2P（Phase 2） |
| 开箱即用 | ✅ | ✅ | ✅ | ✅ 2 分钟配置 |
| 🆕 进程守护/自动重启 | ❌ | ❌ | ✅ watchdog + ensure | ✅ Lifecycle Manager（v2.4）|
| 🆕 Secrets 扫描防护 | ❌ | ❌ | ✅ SECRET_PATTERNS | ✅ SecretsScanner（v2.4）|
| 🆕 域名/IP 白名单 | ❌ | ❌ | ✅ open.feishu.cn 限定 | ✅ NetworkGuard（v2.4）|

> 🆕 = v2.4 新增，对标 feishu-evolver-wrapper 三大核心能力

## 路线图

- [x] v1.0 — WebSocket 连接 + 消息转发
- [x] v2.0 — 心跳监控 + 异常告警 + 健康仪表板
- [x] v2.1 — 任务生命周期追踪（task-tracker）+ 企微群进度直播卡片 + 适配器架构
- [x] v2.2 — WorkBuddy + OpenClaw 适配器 + 资源看板（CPU/内存/队列/磁盘监控）
- [x] v2.3 — 审计日志 + 执行摘要报告 + 决策点结构化记录 + 仪表板审计查询
- [x] **v2.4 — 进程守护自动重启 + Secrets 扫描防护 + 域名白名单** ★ 最新
- [ ] v3.0 — A2A 协议 + 多 Agent 链路拓扑 + 甘特图卡片
- [ ] v4.0 — ClawHub Skill 正式发布 + 可观测的智能协作控制台

## 链接

- 状态面板：`http://localhost:9527`
- 健康检查：`http://localhost:9527/health`
- 云端转换 API：`https://www.hermesai.ltd/health`
- 问题反馈：GitHub Issues

## v2.4 Dashboard API 端点

> 仪表板服务默认监听 `http://localhost:9527`，所有端点返回 JSON。

### 进程生命周期管理（Lifecycle Manager）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/lifecycle/processes` | 所有被管进程状态列表 |
| GET | `/api/lifecycle/:id` | 单个进程详情（状态/pid/重启次数/运行时长） |
| POST | `/api/lifecycle/:id/start` | 启动进程 |
| POST | `/api/lifecycle/:id/stop` | 停止进程（默认优雅关闭 SIGTERM） |
| POST | `/api/lifecycle/:id/restart` | 重启进程 |
| POST | `/api/lifecycle/ensure` | 手动触发 ensure 检查（请求体可选 `{ "procId": "..." }`） |

**启动/停止请求体（可选）：**
```json
// POST /api/lifecycle/:id/stop
{ "graceful": false }   // true=SIGTERM, false=SIGKILL

// POST /api/lifecycle/ensure
{ "procId": "my-agent" }  // 不传 = ensure 所有进程
```

**响应示例：**
```json
// GET /api/lifecycle/processes
{
  "processes": [
    {
      "id": "my-agent",
      "name": "My AI Agent",
      "state": "running",
      "pid": 12345,
      "restartCount": 0,
      "uptime": 3600000,
      "lastHealthStatus": "healthy"
    }
  ],
  "count": 1
}
```

### 敏感信息扫描（Secrets Scanner）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/secrets/stats` | 扫描器统计（规则数/分类/严重级别分布/当前模式） |
| GET | `/api/secrets/rules` | 查看所有启用的扫描规则（名称/分类/严重级别） |
| POST | `/api/secrets/test` | 测试一段文本是否含敏感信息 |

**测试请求体：**
```json
POST /api/secrets/test
{
  "text": "my key is sk-abc123...",
  "context": { "source": "test" }
}
```

**响应示例：**
```json
{
  "safe": false,
  "blocked": false,
  "findings": [
    {
      "rule": "OpenAI API Key",
      "category": "api_key",
      "severity": "high",
      "matched": "sk-abc123...",
      "context": "...my key is sk-abc..."
    }
  ],
  "text": "my key is sk-abc123..."
}
```

### 网络请求守卫（Network Guard）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/network/status` | 守卫状态（模式/拦截统计/最近阻断记录/允许列表） |
| POST | `/api/network/test` | 测试某个 URL/域名/IP 是否被允许 |

**测试请求体：**
```json
POST /api/network/test
{ "url": "https://api.openai.com/v1/chat" }
```

**响应示例：**
```json
{ "allowed": false, "reason": "api.openai.com 不在白名单中" }
```

**允许列表（GET `/api/network/status` 返回）：**
```json
{
  "installed": true,
  "mode": "block",
  "total": 42,
  "allowed": 15,
  "blocked": 27,
  "blockedLog": [ { "host": "api.openai.com", "reason": "...", "timestamp": 1717056000000 } ],
  "allowed": {
    "domains": ["*.work.weixin.qq.com", "www.hermesai.ltd"],
    "ips": [],
    "cidrs": ["127.0.0.0/8", "10.0.0.0/8"]
  }
}
```

---

## License

MIT
