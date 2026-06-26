# Skill Feedback Collector

基于 MCP 协议的人类反馈收集器，通过 WebSocket 连接前端 UI 实现 AI 与人类的交互式协作。

支持 OpenClaw 等 AI Agent 平台，让 AI 在完成任务后等待用户确认，实现高效的人机协作工作流。

## 核心原理

```
┌─────────────┐     stdio      ┌──────────────────┐    WebSocket     ┌──────────────┐
│  AI Agent   │◄──────────────►│  MCP Server      │◄───────────────►│  浏览器 UI    │
│  (OpenClaw) │  MCP Protocol  │  (Node.js)       │   Port 18061    │  (index.html) │
└─────────────┘                └──────────────────┘                  └──────────────┘
```

1. AI 完成任务后调用 `ask_human_feedback` 工具，传入工作摘要
2. MCP Server 通过 WebSocket 将问题推送到浏览器前端
3. AI 线程被 **挂起**（Promise pending）—— 等待期间不消耗 Token
4. 用户在浏览器中阅读问题并输入反馈
5. 反馈通过 WebSocket 返回 → MCP Server 释放 Promise → AI 继续工作

## 快速开始

### 安装

```bash
git clone git@github.com:2019-02-18/skill-feedback-collector.git
cd skill-feedback-collector
npm install
npm run build
```

### 配置 MCP

在你的 AI 客户端（Cursor / OpenClaw 等）的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "feedback-collector": {
      "command": "node",
      "args": ["build/index.js"],
      "cwd": "/path/to/skill-feedback-collector"
    }
  }
}
```

### 访问前端

服务启动后，在浏览器中打开：

```
http://你的服务器IP:18061
```

## 功能特性

| 特性 | 说明 |
|------|------|
| MCP 线程挂起 | 通过 Promise 挂起 AI 线程，等待期间零 Token 消耗 |
| WebSocket 实时通信 | 问题推送与反馈回传全部通过 WebSocket 实时完成 |
| HTTP 轮询降级 | WebSocket 不可用时自动降级为 HTTP Long-Polling |
| 反馈模式开关 | 支持通过 UI 或 MCP 工具随时开关反馈确认模式 |
| WebSocket 心跳 | 30 秒 ping/pong 保活，自动检测和清理死连接 |
| 浏览器通知 | AI 提问时弹出桌面通知 + 音效提醒，无需盯着页面 |
| Token 认证 | 可选的 `FEEDBACK_TOKEN` 环境变量保护 API 访问 |
| Markdown 渲染 | AI 消息支持 `**加粗**` 和 `` `代码` `` 格式化 |
| 对话历史持久化 | 自动保存到 `feedback-history.json`，最多 500 条 |
| 历史导出 | 一键导出完整对话记录为 JSON 文件 |
| 快捷回复 | 内置"继续"、"好的"、"重做"、"结束"快捷按钮 |
| 自动重连 | 断线后自动重连，不会丢失待处理的问题 |
| 服务器部署 | 绑定 `0.0.0.0`，支持外网浏览器访问 |

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `FEEDBACK_PORT` | `18061` | HTTP + WebSocket 服务端口 |
| `FEEDBACK_TOKEN` | （空） | 可选的认证 Token，设置后所有 API 和 WebSocket 连接需要携带 Token |

```bash
# 自定义端口
FEEDBACK_PORT=9090 node build/index.js

# 启用认证
FEEDBACK_TOKEN=my-secret-token node build/index.js
# 访问时需要：http://服务器IP:18061/?token=my-secret-token
```

## 项目结构

```
skill-feedback-collector/
├── SKILL.md              # OpenClaw/ClawHub 技能定义文件
├── package.json           # 依赖管理
├── tsconfig.json          # TypeScript 配置
├── src/
│   └── index.ts           # MCP Server 核心逻辑
├── client/
│   └── index.html         # 前端交互面板
└── feedback-history.json  # 对话历史（运行后自动生成，已 gitignore）
```

## MCP 工具

### `ask_human_feedback`

挂起 AI 线程，等待人类输入。反馈模式关闭时直接返回不挂起。

**参数：**
- `reason`（string，必需）：工作摘要和需要用户确认的内容

**返回：** 用户输入的文本（或关闭模式下的 bypass 消息）

**使用场景：**

```
✅ 任务完成后 → 询问用户是否继续
❓ 遇到不确定参数 → 请用户决定
🔧 修复错误后 → 请用户验证
📝 完成阶段性工作 → 确认下一步方向
```

### `set_feedback_mode`

开关反馈确认模式。

**参数：**
- `enabled`（boolean，必需）：`true` 开启，`false` 关闭

**使用场景：**

```
用户说"自由模式" → 调用 set_feedback_mode(enabled: false)
用户说"确认模式" → 调用 set_feedback_mode(enabled: true)
也可以直接在浏览器 UI 上切换开关
```

## 对话流程示例

```
AI: [完成任务] → 调用 ask_human_feedback("✅ 登录 API 已完成，需要继续吗？")
    ⏸️ AI 线程挂起，不消耗 Token
用户: [在浏览器中输入] → "继续，帮我加上注册接口"
AI: [收到反馈] → 开始编写注册接口
AI: [完成任务] → 调用 ask_human_feedback("✅ 注册接口完成，还需要什么？")
    ⏸️ 再次挂起
用户: "没有了，结束吧"
AI: [收到反馈] → 结束对话
```

## 适用场景

- **Coding Plan** — 在一轮对话中完成更多任务，提升交互效率
- **任何需要人工确认的 AI 工作流** — 防止 AI 猜测导致返工
- **OpenClaw Skill 生态** — 符合 ClawHub 标准，可发布分享

## 安全说明

- **网络访问**：服务默认绑定 `0.0.0.0`，建议通过防火墙限制可访问的 IP 范围
- **认证保护**：在公网或共享网络环境部署时，务必设置 `FEEDBACK_TOKEN` 环境变量
- **历史记录**：对话历史存储在本地 `feedback-history.json` 文件中，包含敏感信息时请定期清理
- **无外部请求**：本技能不会发起任何对外网络请求、不下载外部资源、不执行 shell 命令
- **代码透明**：所有源码均在 `src/index.ts` 中，可自行审查

## 技术栈

- **TypeScript** + **Node.js**
- **@modelcontextprotocol/sdk** — MCP 协议 SDK
- **ws** — WebSocket 实现
- **原生 HTTP** — 静态文件服务 + REST API

## 许可证

MIT
