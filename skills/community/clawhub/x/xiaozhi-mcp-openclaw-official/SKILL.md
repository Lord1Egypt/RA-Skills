---
name: 小智AI-Xiaozhi Mcp Openclaw Official
description: 按小智官方 MCP 接入方式，把小智 AI 设备通过 MCP 接到 OpenClaw / OpenAI-compatible 后端。适用于已经有小智 MCP 接入点（wss://api.xiaozhi.me/mcp/?token=...）的场景。提供一个 `openclaw_query(message)` MCP 工具，让小智在需要外部能力、复杂推理、联网查询或外部智能辅助时调用。 Official XiaoZhi MCP bridge for OpenClaw / OpenAI-compatible backends. Use when you already have a XiaoZhi MCP endpoint and want XiaoZhi to call an external assistant tool such as `openclaw_query(message)`.
---

# xiaozhi-mcp-openclaw-official

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

### 作用
这是一个按小智官方文档方式接入的最小可用 MCP 原型。

数据流：
```text
小智
→ MCP 接入点
→ mcp_pipe.py
→ openclaw_mcp.py
→ OpenAI/OpenAI-compatible 后端
→ 回复文本
→ 小智播报
```

### 提供的工具
- `openclaw_query(message)`
  - 当用户提到“龙虾机器人”“龙虾”或需要外部能力时，调用这个工具
  - 返回适合语音播报的简短中文结果

### 启动步骤
1. 安装依赖：
```bash
pip install -r requirements.txt
```
2. 复制配置：
```bash
cp .env.example .env
```
3. 修改 `.env`：
- `MCP_ENDPOINT`
- `OPENAI_BASE`
- `OPENAI_KEY`
- `MODEL`
4. 启动：
```bash
python3 mcp_pipe.py openclaw_mcp.py
```

### 关键配置项
- `MCP_ENDPOINT`：小智 MCP 接入点
- `OPENAI_BASE`：OpenAI/OpenAI-compatible 后端地址
- `OPENAI_KEY`：后端 key
- `MODEL`：模型名（如 `gpt-5.4`）

### 注意事项
- 不要把真实 `.env` 连同密钥一起分享
- 这是一个原型桥接项目，后续可以继续增强成真正的 OpenClaw 多工具接入版

---

## English

### Purpose
This is a minimal working MCP prototype that follows XiaoZhi's official MCP integration style.

Flow:
```text
XiaoZhi
→ MCP endpoint
→ mcp_pipe.py
→ openclaw_mcp.py
→ OpenAI/OpenAI-compatible backend
→ reply text
→ XiaoZhi speaks it
```

### Provided tool
- `openclaw_query(message)`
  - Use when the user mentions “龙虾机器人 / Lobster Robot” or when an external capability is needed
  - Returns a short Chinese reply suitable for voice playback

### Startup
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Copy config:
```bash
cp .env.example .env
```
3. Update `.env`:
- `MCP_ENDPOINT`
- `OPENAI_BASE`
- `OPENAI_KEY`
- `MODEL`
4. Start:
```bash
python3 mcp_pipe.py openclaw_mcp.py
```

### Key config values
- `MCP_ENDPOINT`: XiaoZhi MCP endpoint
- `OPENAI_BASE`: OpenAI/OpenAI-compatible backend URL
- `OPENAI_KEY`: backend API key
- `MODEL`: model name (for example `gpt-5.4`)

### Notes
- Do not publish your real `.env` or secrets
- This is a prototype bridge and can later be extended into a richer OpenClaw multi-tool integration
