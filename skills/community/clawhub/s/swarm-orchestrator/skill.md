---
name: swarm-orchestrator
display_name: "Swarm Orchestrator / 群智调度器"
description: AI Agent cluster orchestration platform - manage, schedule, and coordinate multiple AI agents locally with FastAPI backend and React dashboard
version: 0.1.0
author: OpenClaw Team
license: MIT
tags: [orchestration, multi-agent, ai-agents, swarm, automation, fastapi, python, react, local-first]

# Security & Requirements Declaration
requires:
  # System tools (must be pre-installed)
  tools:
    - name: python
      version: ">=3.11"
      purpose: Backend runtime
    - name: node
      version: ">=18"
      purpose: Frontend build and runtime
    - name: redis
      version: ">=6"
      purpose: Task queue and caching
    - name: docker
      version: ">=20"
      purpose: Optional containerized deployment
      optional: true

  # Environment variables (all optional)
  env:
    - name: DATABASE_URL
      description: Database connection string
      default: "sqlite+aiosqlite:///./data/swarm.db"
      required: false
      sensitive: false
    - name: REDIS_URL
      description: Redis connection URL
      default: "redis://localhost:6379"
      required: false
      sensitive: false
    - name: SECRET_KEY
      description: Application secret key for sessions
      default: "generated-on-first-run"
      required: false
      sensitive: true
    - name: OPENAI_API_KEY
      description: Optional OpenAI API key for LLM agents
      required: false
      sensitive: true
    - name: ANTHROPIC_API_KEY
      description: Optional Anthropic API key for Claude agents
      required: false
      sensitive: true

  # Package to install
  packages:
    - name: openclaw-swarm-orchestrator
      source: npm
      version: "0.1.0"
      verified_repo: https://github.com/ZhenRobotics/openclaw-swarm-orchestrator
      verified_commit: acae6e5
      install_command: "npm install -g openclaw-swarm-orchestrator"

# Network & Security Policy
network:
  external_servers:
    - description: "No external servers required for core functionality"
    - description: "Optional: OpenAI/Anthropic APIs if using LLM agents (user-controlled)"
  data_collection: none
  telemetry: none
  local_only: true

# Installation verification
verification:
  check_commands:
    - "swarm-orchestrator --version"
    - "curl http://localhost:8000/health"
  expected_files:
    - "~/.swarm-orchestrator/config.yml"
    - "./data/swarm.db"
---

# 🇨🇳 中文版

# Swarm Orchestrator 技能

**状态：** 🟢 本地优先的 AI 智能体编排平台
**类型：** 自托管，无需外部依赖
**隐私：** 100% 本地处理（可选的大模型 API 调用除外）

---

## 🔒 安全与信任

### 本技能的功能
- **本地运行** - 在您的机器上运行（后端 + 前端）
- **无遥测** - 不收集数据
- **无需外部服务器** - 核心功能无需外部依赖
- **可选 API 密钥** - 仅在使用大模型智能体时需要（OpenAI/Claude）
- **开源** - 所有代码可审计

### 本技能不会做的事
- ❌ 不向外部服务器发送数据（可选的大模型 API 除外）
- ❌ 不收集分析或遥测数据
- ❌ 不需要账号注册
- ❌ 不会未经许可访问您的文件
- ❌ 不会在您不知情的情况下运行后台进程

### 数据存储
- **数据库：** SQLite 文件存储在 `./data/swarm.db`（仅本地）
- **日志：** 文本文件存储在 `./logs/`（仅本地）
- **缓存：** 本地 Redis（仅本地）
- **无云同步** 或远程存储

---

## 📋 概述

OpenClaw Swarm Orchestrator 是一个**本地优先**的平台，用于构建和管理多智能体 AI 系统。可以把它想象成协调多个 AI 智能体协同工作的"控制塔"。

### 核心功能

- **智能体注册表** - 注册 LLM、工具、人类和自定义智能体
- **任务队列** - 基于优先级的任务分发与依赖管理
- **实时仪表板** - Web UI 监控智能体和任务
- **RESTful API** - 完整的 REST API 用于程序化控制
- **本地存储** - 所有数据保留在您的机器上

### 架构

```
┌─────────────────┐
│  Web 仪表板     │  http://localhost:3000
│   (React UI)    │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI 服务器 │  http://localhost:8000
│  (后端 API)     │
└────────┬────────┘
         │
┌────────▼────────┐
│   本地存储      │
│ • SQLite 数据库 │  ./data/swarm.db
│ • Redis 缓存    │  localhost:6379
│ • 日志文件      │  ./logs/*.log
└─────────────────┘
```

---

## 🚀 安装

### 前置条件检查

安装前，请验证您已安装：

```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Redis
redis-cli ping  # 应该返回 PONG

# (可选) Docker
docker --version
```

### 方法一：使用 Docker（推荐 - 最简单）

**这是最安全的方法** - 所有内容都在容器中运行。

```bash
# 1. 克隆仓库（先检查代码！）
git clone https://github.com/ZhenRobotics/openclaw-swarm-orchestrator.git
cd openclaw-swarm-orchestrator

# 2. 启动前查看 docker-compose.yml
cat docker-compose.yml

# 3. 启动服务
docker-compose up -d

# 4. 验证
curl http://localhost:8000/health
# 应该返回: {"status": "healthy"}
```

访问：
- **前端：** http://localhost:3000
- **后端 API：** http://localhost:8000
- **API 文档：** http://localhost:8000/docs

### 方法二：本地安装（用于开发）

```bash
# 1. 通过 npm 安装（审查包后）
npm view openclaw-swarm-orchestrator  # 安装前查看
npm install -g openclaw-swarm-orchestrator

# 2. 验证安装
swarm-orchestrator --version

# 3. 启动服务（在不同终端中）

# 终端 1: 启动 Redis
redis-server

# 终端 2: 启动后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 终端 3: 启动前端
cd frontend
npm install
npm run dev
```

### 方法三：从源码安装（最透明）

```bash
# 1. 克隆并检查
git clone https://github.com/ZhenRobotics/openclaw-swarm-orchestrator.git
cd openclaw-swarm-orchestrator

# 2. 验证提交哈希（安全检查）
git log -1 --format="%H"
# 应该是: acae6e5... (或最新发布标签)

# 3. 运行前查看代码
cat backend/requirements.txt  # 检查依赖
cat package.json              # 检查 npm 依赖
cat docker-compose.yml        # 检查容器配置

# 4. 安装依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 5. 运行（详细步骤见方法二）
```

---

## ⚙️ 配置

### 最小配置（仅本地）

在项目根目录创建 `.env`：

```bash
# 最小配置 - 无需外部服务
DATABASE_URL=sqlite+aiosqlite:///./data/swarm.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-random-secret-key-here
DEBUG=true
```

### 可选：大模型智能体支持

如果您想使用大模型智能体（OpenAI、Anthropic），添加：

```bash
# 可选 - 仅在使用大模型智能体时需要
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**⚠️ 安全提示：**
- 仅在计划使用大模型智能体时添加 API 密钥
- 安全存储 `.env` 文件（不要提交到 git）
- API 密钥永远不会发送到我们的服务器（仅发送到官方大模型提供商）

---

## 💻 基本使用

### 1. 启动系统

```bash
# 使用 Docker
docker-compose up -d

# 或手动启动
redis-server &
cd backend && uvicorn app.main:app --reload &
cd frontend && npm run dev &
```

### 2. 创建您的第一个智能体

**通过 Web UI：**
1. 打开 http://localhost:3000
2. 转到"智能体"页面
3. 点击"新建智能体"
4. 填写：
   - 名称："我的助手"
   - 类型："llm"（或"tool"、"human"、"custom"）
   - 配置：`{"model": "gpt-4"}`（如果使用大模型）

**通过 API：**
```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "我的助手",
    "type": "llm",
    "config": {"model": "gpt-4"}
  }'
```

### 3. 创建任务

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "分析数据",
    "description": "处理销售报告",
    "priority": "high"
  }'
```

### 4. 监控状态

**Web 仪表板：** http://localhost:3000

**API：**
```bash
# 系统状态
curl http://localhost:8000/api/orchestrator/status

# 列出智能体
curl http://localhost:8000/api/agents

# 列出任务
curl http://localhost:8000/api/tasks
```

---

## 🔧 智能体类型

### 1. LLM 智能体（需要 API 密钥）

使用外部大模型 API（OpenAI、Anthropic）。

```json
{
  "name": "GPT-4 助手",
  "type": "llm",
  "config": {
    "model": "gpt-4",
    "temperature": 0.7
  }
}
```

**需要：** `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`

### 2. 工具智能体（仅本地）

执行本地函数/脚本。

```json
{
  "name": "数据处理器",
  "type": "tool",
  "config": {
    "script_path": "./tools/process_data.py"
  }
}
```

**无需外部服务。**

### 3. 人类智能体（仅本地）

人在回路工作流。

```json
{
  "name": "管理员审批",
  "type": "human",
  "config": {
    "notification": "email"
  }
}
```

**无需外部服务。**

### 4. 自定义智能体（用户定义）

您定义行为。

```python
from swarm_orchestrator.base import BaseAgent

class MyCustomAgent(BaseAgent):
    async def execute(self, task):
        # 您的自定义逻辑
        return result
```

**无需外部服务。**

---

## 📊 监控与日志

### Web 仪表板

访问 http://localhost:3000：
- 实时智能体状态
- 任务队列监控
- 系统统计
- 执行日志

### 日志文件

所有日志本地存储：

```bash
# 应用日志
tail -f logs/swarm.log

# Docker 日志（如果使用 Docker）
docker-compose logs -f
```

---

## 🔐 安全最佳实践

### 1. API 密钥
- ✅ 存储在 `.env` 文件中（不在代码中）
- ✅ 设置文件权限：`chmod 600 .env`
- ✅ 将 `.env` 添加到 `.gitignore`
- ✅ 永远不要将 API 密钥提交到 git

### 2. 网络安全
- ✅ 防火墙：阻止端口 8000、3000 的外部访问
- ✅ 开发时仅使用 localhost（不是 0.0.0.0）
- ✅ 生产环境启用 HTTPS

### 3. 数据隐私
- ✅ 所有数据本地存储在 `./data/`
- ✅ 数据库文件权限：`chmod 600 data/swarm.db`
- ✅ 定期备份：`cp data/swarm.db backups/`

---

## 🐛 故障排除

### 后端无法启动

```bash
# 检查 Python 版本
python --version  # 必须是 3.11+

# 检查 Redis
redis-cli ping  # 必须返回 PONG

# 检查日志
tail -f logs/swarm.log
```

### 前端无法启动

```bash
# 检查 Node 版本
node --version  # 必须是 18+

# 清除缓存
cd frontend
rm -rf node_modules
npm install
```

### 端口冲突

```bash
# 检查端口
lsof -i :8000  # 后端
lsof -i :3000  # 前端
lsof -i :6379  # Redis

# 如需终止进程
kill -9 <PID>
```

---

## 📚 文档

- **主文档：** [README.md](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/README.md)
- **快速开始：** [QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/QUICKSTART.md)
- **API 参考：** http://localhost:8000/docs（启动后端后）

---

## 🤝 支持与社区

- **问题反馈：** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/issues
- **讨论：** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/discussions

---

## ✅ 安装前检查清单

使用本技能前：

- [ ] 在 GitHub 上查看源代码
- [ ] 验证提交哈希：`acae6e5`
- [ ] 检查 `requirements.txt` 和 `package.json`
- [ ] 阅读上述安全策略
- [ ] 了解数据存储位置
- [ ] 知道需要哪些 API 密钥（如果有）
- [ ] 首先在隔离环境中运行（可选）

---

**版本：** 0.1.0
**状态：** Alpha - 活跃开发中
**本地优先：** ✅ 所有核心功能离线工作
**隐私：** ✅ 数据不离开您的机器（可选的大模型调用除外）

---

# 🇬🇧 English Version

# Swarm Orchestrator Skill

**Status:** 🟢 Local-First AI Agent Orchestration Platform
**Type:** Self-hosted, no external dependencies required
**Privacy:** 100% local processing (except optional LLM API calls)

---

## 🔒 Security & Trust

### What This Skill Does
- **Runs locally** on your machine (backend + frontend)
- **No telemetry** or data collection
- **No external servers** required for core functionality
- **Optional API keys** only needed if you use LLM agents (OpenAI/Claude)
- **Open source** - all code is auditable

### What This Skill Does NOT Do
- ❌ Does not send data to external servers (except optional LLM APIs)
- ❌ Does not collect analytics or telemetry
- ❌ Does not require account registration
- ❌ Does not access your files without permission
- ❌ Does not run background processes without your knowledge

### Data Storage
- **Database:** SQLite file in `./data/swarm.db` (local only)
- **Logs:** Text files in `./logs/` (local only)
- **Cache:** Redis on localhost (local only)
- **No cloud sync** or remote storage

---

## 📋 Overview

OpenClaw Swarm Orchestrator is a **local-first** platform for building and managing multi-agent AI systems. Think of it as a "control tower" for coordinating multiple AI agents working together.

### Core Features

- **Agent Registry** - Register LLM, Tool, Human, and Custom agents
- **Task Queue** - Priority-based task distribution with dependencies
- **Real-time Dashboard** - Web UI to monitor agents and tasks
- **RESTful API** - Complete REST API for programmatic control
- **Local Storage** - All data stays on your machine

### Architecture

```
┌─────────────────┐
│  Web Dashboard  │  http://localhost:3000
│   (React UI)    │
└────────┬────────┘
         │
┌────────▼────────┐
│  FastAPI Server │  http://localhost:8000
│  (Backend API)  │
└────────┬────────┘
         │
┌────────▼────────┐
│ Local Storage   │
│ • SQLite DB     │  ./data/swarm.db
│ • Redis Cache   │  localhost:6379
│ • Log Files     │  ./logs/*.log
└─────────────────┘
```

---

## 🚀 Installation

### Prerequisites Check

Before installing, verify you have:

```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Redis
redis-cli ping  # Should return PONG

# (Optional) Docker
docker --version
```

### Method 1: Using Docker (Recommended - Easiest)

**This is the safest method** - everything runs in containers.

```bash
# 1. Clone repository (inspect code first!)
git clone https://github.com/ZhenRobotics/openclaw-swarm-orchestrator.git
cd openclaw-swarm-orchestrator

# 2. Review docker-compose.yml before starting
cat docker-compose.yml

# 3. Start services
docker-compose up -d

# 4. Verify
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

Access:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Method 2: Local Installation (For Development)

```bash
# 1. Install via npm (after reviewing package)
npm view openclaw-swarm-orchestrator  # Review before installing
npm install -g openclaw-swarm-orchestrator

# 2. Verify installation
swarm-orchestrator --version

# 3. Start services (in separate terminals)

# Terminal 1: Start Redis
redis-server

# Terminal 2: Start backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 3: Start frontend
cd frontend
npm install
npm run dev
```

### Method 3: From Source (Most Transparent)

```bash
# 1. Clone and inspect
git clone https://github.com/ZhenRobotics/openclaw-swarm-orchestrator.git
cd openclaw-swarm-orchestrator

# 2. Verify commit hash (security check)
git log -1 --format="%H"
# Should be: acae6e5... (or latest release tag)

# 3. Review code before running
cat backend/requirements.txt  # Check dependencies
cat package.json              # Check npm deps
cat docker-compose.yml        # Check container config

# 4. Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 5. Run (see Method 2 for detailed steps)
```

---

## ⚙️ Configuration

### Minimal Configuration (Local Only)

Create `.env` in project root:

```bash
# Minimal config - no external services needed
DATABASE_URL=sqlite+aiosqlite:///./data/swarm.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-random-secret-key-here
DEBUG=true
```

### Optional: LLM Agent Support

If you want to use LLM agents (OpenAI, Anthropic), add:

```bash
# Optional - only if using LLM agents
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**⚠️ Security Note:**
- Only add API keys if you plan to use LLM agents
- Store `.env` file securely (not in git)
- API keys are never sent to our servers (only to official LLM providers)

---

## 💻 Basic Usage

### 1. Start the System

```bash
# Using Docker
docker-compose up -d

# Or manually
redis-server &
cd backend && uvicorn app.main:app --reload &
cd frontend && npm run dev &
```

### 2. Create Your First Agent

**Via Web UI:**
1. Open http://localhost:3000
2. Go to "Agents" page
3. Click "New Agent"
4. Fill in:
   - Name: "My Assistant"
   - Type: "llm" (or "tool", "human", "custom")
   - Config: `{"model": "gpt-4"}` (if using LLM)

**Via API:**
```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Assistant",
    "type": "llm",
    "config": {"model": "gpt-4"}
  }'
```

### 3. Create a Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Analyze data",
    "description": "Process the sales report",
    "priority": "high"
  }'
```

### 4. Monitor Status

**Web Dashboard:** http://localhost:3000

**API:**
```bash
# System status
curl http://localhost:8000/api/orchestrator/status

# List agents
curl http://localhost:8000/api/agents

# List tasks
curl http://localhost:8000/api/tasks
```

---

## 🔧 Agent Types

### 1. LLM Agents (Requires API Key)

Uses external LLM APIs (OpenAI, Anthropic).

```json
{
  "name": "GPT-4 Assistant",
  "type": "llm",
  "config": {
    "model": "gpt-4",
    "temperature": 0.7
  }
}
```

**Required:** `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

### 2. Tool Agents (Local Only)

Executes local functions/scripts.

```json
{
  "name": "Data Processor",
  "type": "tool",
  "config": {
    "script_path": "./tools/process_data.py"
  }
}
```

**No external services needed.**

### 3. Human Agents (Local Only)

Human-in-the-loop workflows.

```json
{
  "name": "Manager Approval",
  "type": "human",
  "config": {
    "notification": "email"
  }
}
```

**No external services needed.**

### 4. Custom Agents (User-Defined)

You define the behavior.

```python
from swarm_orchestrator.base import BaseAgent

class MyCustomAgent(BaseAgent):
    async def execute(self, task):
        # Your custom logic
        return result
```

**No external services needed.**

---

## 📊 Monitoring & Logs

### Web Dashboard

Access at http://localhost:3000:
- Real-time agent status
- Task queue monitoring
- System statistics
- Execution logs

### Log Files

All logs stored locally:

```bash
# Application logs
tail -f logs/swarm.log

# Docker logs (if using Docker)
docker-compose logs -f
```

---

## 🔐 Security Best Practices

### 1. API Keys
- ✅ Store in `.env` file (not in code)
- ✅ Set file permissions: `chmod 600 .env`
- ✅ Add `.env` to `.gitignore`
- ✅ Never commit API keys to git

### 2. Network Security
- ✅ Firewall: Block ports 8000, 3000 from external access
- ✅ Use localhost only (not 0.0.0.0) for development
- ✅ Enable HTTPS in production

### 3. Data Privacy
- ✅ All data stored locally in `./data/`
- ✅ Database file permissions: `chmod 600 data/swarm.db`
- ✅ Regular backups: `cp data/swarm.db backups/`

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Must be 3.11+

# Check Redis
redis-cli ping  # Must return PONG

# Check logs
tail -f logs/swarm.log
```

### Frontend won't start

```bash
# Check Node version
node --version  # Must be 18+

# Clear cache
cd frontend
rm -rf node_modules
npm install
```

### Port conflicts

```bash
# Check ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :6379  # Redis

# Kill processes if needed
kill -9 <PID>
```

---

## 📚 Documentation

- **Main Docs:** [README.md](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/README.md)
- **Quick Start:** [QUICKSTART.md](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/QUICKSTART.md)
- **API Reference:** http://localhost:8000/docs (after starting backend)

---

## 🤝 Support & Community

- **Issues:** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/issues
- **Discussions:** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/discussions

---

## ✅ Pre-Installation Checklist

Before using this skill:

- [ ] Review source code on GitHub
- [ ] Verify commit hash: `acae6e5`
- [ ] Check `requirements.txt` and `package.json`
- [ ] Read security policy above
- [ ] Understand data storage locations
- [ ] Know which API keys you need (if any)
- [ ] Run in isolated environment first (optional)

---

**Version:** 0.1.0
**Status:** Alpha - Active Development
**Local-First:** ✅ All core features work offline
**Privacy:** ✅ No data leaves your machine (except optional LLM calls)

---

*Built with privacy and transparency in mind. Inspect the code before you trust it.*
