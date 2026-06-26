# RMN Visualizer — 递归记忆神经网络可视化

> 一键查看你的 AI Agent 大脑结构 🧠

## 安装

```bash
clawhub install rmn-visualizer
```

## 快速开始

告诉你的 Agent：

> "可视化我的记忆网络"

或者手动运行：

```bash
node rmn-visualizer/scripts/launch.js
```

Agent 会自动：
1. 扫描你的记忆文件（MEMORY.md, memory/*.md, .issues/*）
2. 解析为 5 层递归神经网络
3. 启动可视化服务 + Cloudflare Tunnel
4. 把公网链接发到聊天窗口，点击即可查看

## 前置要求

- Node.js 18+
- `cloudflared`（[安装指南](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)）
- 没有 cloudflared？用本地模式：`node rmn-visualizer/scripts/serve.js`，打开 http://localhost:3459

## 你会看到什么

D3.js 力导向图，5 层彩色节点：

- 🔴 Identity — 身份、核心原则（永不衰减）
- 🟠 Semantic — 知识、教训（缓慢衰减）
- 🟡 Episodic — 事件、日志（中等衰减）
- 🟢 Working — 当前任务（快速衰减）
- 🔵 Sensory — 感知数据（最快衰减）

支持：拖拽节点 · 缩放平移 · 层级过滤 · 悬停看详情 · 实时统计面板

## 自定义

```bash
RMN_WORKSPACE=/path/to/workspace node rmn-visualizer/scripts/launch.js
RMN_PORT=3459 node rmn-visualizer/scripts/launch.js
```

## 零依赖

纯 Node.js，D3.js 从 CDN 加载。不需要 npm install。

## License

MIT — 完全免费开源
