# 小智AI-Xiaozhi Mcp Openclaw Official

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

### 目标
这是一个**按小智官方 MCP 文档方式**接入 OpenClaw / OpenAI-compatible 后端的最小可用原型。

### 架构
```text
小智
→ MCP 接入点 (wss://api.xiaozhi.me/mcp/?token=...)
→ mcp_pipe.py
→ openclaw_mcp.py (FastMCP 工具)
→ OpenAI / OpenAI-compatible 后端
→ 返回结果给小智
```

### 提供的 MCP 工具
- `openclaw_query(message)`：把一段文本发给后端处理，并返回适合播报的简短文本

### 快速开始
1. 安装依赖：
```bash
pip install -r requirements.txt
```
2. 配置环境变量：
```bash
cp .env.example .env
nano .env
```
3. 启动：
```bash
python3 mcp_pipe.py openclaw_mcp.py
```

### 关键环境变量
- `MCP_ENDPOINT`：小智提供的 MCP 接入点
- `OPENAI_BASE`：模型后端地址
- `OPENAI_KEY`：模型 key
- `MODEL`：模型名（例如 `gpt-5.4`）

### 适用场景
- 小智已经拿到了官方 MCP 接入点
- 不想改小智源码
- 想给小智增加“龙虾机器人 / OpenClaw”外挂能力

### 注意事项
- 不要把真实 `.env` 或密钥发布出去
- 这是原型桥接，后续还可以继续增强成多工具版

---

## English

### Goal
This is a minimal working prototype for integrating XiaoZhi AI with OpenClaw / OpenAI-compatible backends using the **official XiaoZhi MCP approach**.

### Architecture
```text
XiaoZhi
→ MCP endpoint (wss://api.xiaozhi.me/mcp/?token=...)
→ mcp_pipe.py
→ openclaw_mcp.py (FastMCP tool)
→ OpenAI / OpenAI-compatible backend
→ return response to XiaoZhi
```

### Provided MCP tool
- `openclaw_query(message)`: send a text query to the backend and return a short reply suitable for voice playback

### Quick start
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Configure environment:
```bash
cp .env.example .env
nano .env
```
3. Start the bridge:
```bash
python3 mcp_pipe.py openclaw_mcp.py
```

### Key environment variables
- `MCP_ENDPOINT`: XiaoZhi MCP endpoint
- `OPENAI_BASE`: backend base URL
- `OPENAI_KEY`: backend API key
- `MODEL`: model name (for example `gpt-5.4`)

### Good fit for
- You already have an official XiaoZhi MCP endpoint
- You do not want to modify XiaoZhi source code
- You want to add OpenClaw / external assistant capability to XiaoZhi

### Notes
- Do not publish the real `.env` file or secrets
- This is a prototype bridge and can be extended later into a richer multi-tool version
