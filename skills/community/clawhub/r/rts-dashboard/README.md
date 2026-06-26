# RTS Dashboard ⚡

星际争霸/命令与征服风格的 OpenClaw 实时监控面板。

![Style: RTS Tactical Command Center]

## 功能

- **战术地图** — Agent 以节点形式分布，Skill 作为轨道粒子环绕
- **模型标识** — 每个 Agent 图标上方显示 🧠 当前大模型名称
- **系统面板** — CPU/内存/Gateway 状态/事件日志
- **会话详情** — 点击 Agent 查看模型、通道、技能、最近对话
- **定时任务** — Cron Job 在地图上随机游走显示
- **聊天** — 底部输入框直接发消息给 Agent
- **冷却机制** — Agent 离线后保持 5 分钟可见（琥珀色闪烁+倒计时）
- **CRT 效果** — 扫描线 + 雷达扫描 + 网格，军事 UI 美学

## 快速开始

```bash
cd rts-dashboard
npm install
node server.js
```

浏览器打开 http://127.0.0.1:4320

## 环境要求

- **Node.js** 18+
- **OpenClaw** 已安装并运行（默认端口 18789）

## 配置

全部可选，默认自动检测：

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `RTS_PORT` | `4320` | Dashboard 端口 |
| `OPENCLAW_GATEWAY_PORT` | `18789` | Gateway 端口 |
| `OPENCLAW_HOME` | `~/.openclaw` | OpenClaw 主目录 |
| `OPENCLAW_GATEWAY_TOKEN` | (自动读取) | Gateway 认证 Token |

## Gateway 配置

Dashboard 需要 Gateway 放行 WebSocket 来源：

```bash
openclaw config set gateway.controlUi.allowedOrigins '["http://127.0.0.1:4320"]'
```

## 认证

- 首次启动自动生成 Ed25519 设备密钥（保存在 `.device-keys.json`）
- Localhost 连接自动免配对
- 不需要开启任何安全降级选项

## 从 .skill 文件安装

```bash
mv rts-dashboard.skill rts-dashboard.zip
unzip rts-dashboard.zip -d rts-dashboard
cd rts-dashboard
npm install
node server.js
```

## 跨平台

- Windows / macOS / Linux 均可运行
- OpenClaw 安装路径自动检测（4 层降级策略）
- Agent/Skill 配置用 JSON.parse 解析，稳定可靠

## 文件结构

```
rts-dashboard/
├── README.md         # 本文件
├── SKILL.md          # Agent 自动化指令（给 AI 读的）
├── server.js         # Node.js 服务（HTTP + WebSocket）
├── package.json      # 依赖（仅 ws）
└── public/
    └── index.html    # 单文件前端（HTML + CSS + Canvas）
```

## License

MIT
