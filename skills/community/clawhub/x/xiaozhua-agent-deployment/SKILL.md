---
name: agent-deployment
description: "AI Agent 部署与管理。在 WSL2/Linux 上安装 OpenClaw，配置 GitHub Copilot 认证，启动 Gateway，初始化 workspace（SOUL.md/USER.md/TASKS.md）。支持多 Agent 部署、端口配置、认证排错。使用场景：部署新 Agent、重启 Agent、认证过期修复、配置更新。"
---

# Agent 部署

## 部署新 Agent（WSL2 + OpenClaw）

### 前置条件
- WSL2 已安装（需管理员权限：`wsl --install`）
- Ubuntu 发行版

### 安装步骤
```bash
# 1. 安装 nvm + Node.js（绕过 sudo）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.nvm/nvm.sh
nvm install 24

# 2. 安装 OpenClaw
npm install -g openclaw

# 3. 初始化
openclaw setup

# 4. GitHub Copilot 认证
openclaw login-github-copilot
# 注意：device code 每次超时就失效，可能需要多试几次

# 5. 配置模型和端口
# 编辑 ~/.openclaw/openclaw.json
# gateway.port: <YOUR_PORT>（避免和主 Agent 冲突）
# model: github-copilot/claude-sonnet-4-20250514

# 6. 启动
openclaw gateway
```

### 启动已有 Agent
```bash
wsl -d Ubuntu
source ~/.nvm/nvm.sh
openclaw gateway
```
- 端口：<YOUR_PORT>
- Token：`<YOUR_TOKEN>`
- 浏览器打开 http://127.0.0.1:<YOUR_PORT>

## Workspace 初始化
新 Agent 上线后写入：
- **SOUL.md** — 身份、职责、性格
- **USER.md** — Lei 的信息和偏好
- **TASKS.md** — 任务清单
- **COLLABORATION.md** — 协作协议

## 常见问题
- **device code 超时** — 每次生成新 code，快速在浏览器完成认证
- **端口冲突** — 改 openclaw.json 的 gateway.port
- **config overwrite** — Gateway 启动时可能重写配置，启动后检查端口是否正确
- **关机后重启** — 需要手动启动 WSL + Gateway，AI 没有管理员权限自动启动
