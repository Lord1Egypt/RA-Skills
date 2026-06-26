# 🇨🇳 中文版

# OpenClaw Swarm Orchestrator

**本地优先的 AI 智能体集群编排平台**

[![版本](https://img.shields.io/badge/版本-0.1.0-blue.svg)](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator)
[![许可证](https://img.shields.io/badge/许可证-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 概述

OpenClaw Swarm Orchestrator 是一个功能强大的 AI 智能体集群编排平台，灵感来自 OpenAI Swarm 架构。它提供了一个本地优先的解决方案，用于构建、管理和协调多智能体 AI 系统。

### 为什么选择 Swarm Orchestrator？

- **🔒 本地优先** - 所有数据和处理都在您的机器上进行
- **🚀 快速设置** - 使用 Docker 5 分钟内启动运行
- **🔧 灵活架构** - 支持多种智能体类型（LLM、工具、人类、自定义）
- **📊 实时监控** - 现代化 React 仪表板实时更新
- **🔐 隐私保护** - 无遥测、无数据收集、无云同步
- **🌐 完整 API** - RESTful API 可集成到任何应用

---

## 主要特性

### 智能体管理
- 注册和配置多种类型的 AI 智能体
- 支持 LLM（OpenAI、Anthropic）、工具、人类和自定义智能体
- 实时健康监控和状态跟踪
- 基于能力的智能体选择

### 任务调度
- 优先级队列任务分发
- 任务依赖管理
- 自动负载均衡
- 失败重试机制

### 实时监控
- Web 仪表板实时更新
- 详细的执行日志
- 系统性能指标
- 任务执行可视化

### RESTful API
- 完整的 CRUD 操作
- OpenAPI/Swagger 文档
- 异步处理支持
- WebSocket 实时通知（即将推出）

---

## 技术架构

### 后端
- **Python 3.11+** - 现代 Python 特性
- **FastAPI** - 高性能异步 Web 框架
- **SQLAlchemy** - 强大的 ORM
- **Redis** - 消息队列和缓存
- **Pydantic** - 数据验证

### 前端
- **React 18** - 现代 UI 框架
- **TypeScript** - 类型安全
- **TailwindCSS** - 实用优先的 CSS
- **shadcn/ui** - 精美的组件库
- **React Query** - 数据获取

### 存储
- **SQLite** - 轻量级关系数据库
- **Redis** - 内存数据存储
- **本地文件系统** - 日志和配置

---

## 快速开始

### 使用 Docker（推荐）

```bash
# 克隆仓库
git clone https://github.com/ZhenRobotics/openclaw-swarm-orchestrator.git
cd openclaw-swarm-orchestrator

# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 手动安装

**后端设置：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**前端设置：**
```bash
cd frontend
npm install
npm run dev
```

---

## 使用示例

### 创建智能体

```python
import requests

# 创建 LLM 智能体
agent = {
    "name": "GPT-4 助手",
    "type": "llm",
    "config": {
        "model": "gpt-4",
        "temperature": 0.7
    }
}

response = requests.post(
    "http://localhost:8000/api/agents",
    json=agent
)
```

### 提交任务

```python
# 创建任务
task = {
    "title": "分析销售数据",
    "description": "处理本月的销售报告",
    "priority": "high"
}

response = requests.post(
    "http://localhost:8000/api/tasks",
    json=task
)
```

### 监控状态

```python
# 获取系统状态
status = requests.get("http://localhost:8000/api/orchestrator/status")
print(status.json())

# 列出所有智能体
agents = requests.get("http://localhost:8000/api/agents")
print(agents.json())
```

---

## 配置

在项目根目录创建 `.env` 文件：

```bash
# 基本配置
DATABASE_URL=sqlite+aiosqlite:///./data/swarm.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
DEBUG=true

# 可选：大模型 API 密钥
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 项目结构

```
openclaw-swarm-orchestrator/
├── backend/              # Python FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── models/      # 数据库模型
│   │   ├── services/    # 业务逻辑
│   │   └── core/        # 核心配置
│   └── requirements.txt
├── frontend/            # React TypeScript 前端
│   ├── src/
│   │   ├── components/  # React 组件
│   │   ├── pages/       # 页面组件
│   │   └── services/    # API 客户端
│   └── package.json
├── data/                # SQLite 数据库
├── logs/                # 应用日志
└── docker-compose.yml   # Docker 配置
```

---

## 智能体类型

### 1. LLM 智能体
使用大语言模型（OpenAI、Anthropic）处理任务。

**特点：**
- 自然语言理解
- 上下文感知
- 灵活推理能力

**需要：** API 密钥（OpenAI 或 Anthropic）

### 2. 工具智能体
执行特定的本地函数或脚本。

**特点：**
- 快速执行
- 可预测结果
- 无需外部 API

**需要：** 本地脚本或函数

### 3. 人类智能体
人在回路中的工作流程。

**特点：**
- 人工审批
- 质量控制
- 复杂决策

**需要：** 通知系统（邮件、Webhook 等）

### 4. 自定义智能体
用户定义的智能体逻辑。

**特点：**
- 完全可定制
- 无限可能性
- 可与任何系统集成

---

## 安全与隐私

### 数据保护
- ✅ 所有数据本地存储
- ✅ 无云同步或远程存储
- ✅ 无遥测或分析
- ✅ 开源可审计

### API 密钥安全
- ✅ 存储在 `.env` 文件中
- ✅ 永远不提交到版本控制
- ✅ 仅在需要时使用
- ✅ 仅发送到官方 API 端点

### 网络安全
- ✅ 默认本地主机访问
- ✅ 可配置 CORS
- ✅ 生产环境 HTTPS
- ✅ 无外部依赖（核心功能）

---

## 开发

### 运行测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

### 代码质量

```bash
# 后端 Lint
cd backend
black app/
flake8 app/

# 前端 Lint
cd frontend
npm run lint
```

---

## 路线图

- [x] 基本智能体管理
- [x] 任务队列系统
- [x] Web 仪表板
- [x] RESTful API
- [x] Docker 支持
- [ ] WebSocket 实时更新
- [ ] 高级调度算法
- [ ] 多智能体对话
- [ ] 插件系统
- [ ] 分布式部署
- [ ] 指标和分析

---

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/CONTRIBUTING.md) 了解详情。

---

## 支持

- **问题反馈：** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/issues
- **讨论：** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/discussions
- **文档：** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/README.md

---

## 许可证

MIT License - 详见 [LICENSE](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/LICENSE) 文件

---

## 致谢

灵感来自 OpenAI Swarm 架构和现代多智能体系统。

---

**版本：** 0.1.0
**状态：** Alpha - 活跃开发中
**作者：** OpenClaw Team

---

# 🇬🇧 English Version

# OpenClaw Swarm Orchestrator

**Local-First AI Agent Cluster Orchestration Platform**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## Overview

OpenClaw Swarm Orchestrator is a powerful AI agent cluster orchestration platform inspired by OpenAI Swarm architecture. It provides a local-first solution for building, managing, and coordinating multi-agent AI systems.

### Why Swarm Orchestrator?

- **🔒 Local-First** - All data and processing happens on your machine
- **🚀 Quick Setup** - Up and running in 5 minutes with Docker
- **🔧 Flexible Architecture** - Support for multiple agent types (LLM, Tool, Human, Custom)
- **📊 Real-time Monitoring** - Modern React dashboard with live updates
- **🔐 Privacy-Focused** - No telemetry, no data collection, no cloud sync
- **🌐 Complete API** - RESTful API for integration with any application

---

## Key Features

### Agent Management
- Register and configure multiple types of AI agents
- Support for LLM (OpenAI, Anthropic), Tool, Human, and Custom agents
- Real-time health monitoring and status tracking
- Capability-based agent selection

### Task Scheduling
- Priority queue task distribution
- Task dependency management
- Automatic load balancing
- Failure retry mechanisms

### Real-time Monitoring
- Web dashboard with live updates
- Detailed execution logs
- System performance metrics
- Task execution visualization

### RESTful API
- Complete CRUD operations
- OpenAPI/Swagger documentation
- Async processing support
- WebSocket real-time notifications (coming soon)

---

## Technical Architecture

### Backend
- **Python 3.11+** - Modern Python features
- **FastAPI** - High-performance async web framework
- **SQLAlchemy** - Powerful ORM
- **Redis** - Message queue and caching
- **Pydantic** - Data validation

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type safety
- **TailwindCSS** - Utility-first CSS
- **shadcn/ui** - Beautiful component library
- **React Query** - Data fetching

### Storage
- **SQLite** - Lightweight relational database
- **Redis** - In-memory data store
- **Local File System** - Logs and configuration

---

## Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/ZhenRobotics/openclaw-swarm-orchestrator.git
cd openclaw-swarm-orchestrator

# Start all services
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Installation

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

---

## Usage Examples

### Create an Agent

```python
import requests

# Create LLM agent
agent = {
    "name": "GPT-4 Assistant",
    "type": "llm",
    "config": {
        "model": "gpt-4",
        "temperature": 0.7
    }
}

response = requests.post(
    "http://localhost:8000/api/agents",
    json=agent
)
```

### Submit a Task

```python
# Create task
task = {
    "title": "Analyze sales data",
    "description": "Process monthly sales report",
    "priority": "high"
}

response = requests.post(
    "http://localhost:8000/api/tasks",
    json=task
)
```

### Monitor Status

```python
# Get system status
status = requests.get("http://localhost:8000/api/orchestrator/status")
print(status.json())

# List all agents
agents = requests.get("http://localhost:8000/api/agents")
print(agents.json())
```

---

## Configuration

Create a `.env` file in project root:

```bash
# Basic configuration
DATABASE_URL=sqlite+aiosqlite:///./data/swarm.db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
DEBUG=true

# Optional: LLM API keys
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Project Structure

```
openclaw-swarm-orchestrator/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── core/        # Core configuration
│   └── requirements.txt
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   └── services/    # API clients
│   └── package.json
├── data/                # SQLite databases
├── logs/                # Application logs
└── docker-compose.yml   # Docker configuration
```

---

## Agent Types

### 1. LLM Agents
Use Large Language Models (OpenAI, Anthropic) to process tasks.

**Features:**
- Natural language understanding
- Context awareness
- Flexible reasoning

**Requires:** API key (OpenAI or Anthropic)

### 2. Tool Agents
Execute specific local functions or scripts.

**Features:**
- Fast execution
- Predictable results
- No external APIs needed

**Requires:** Local scripts or functions

### 3. Human Agents
Human-in-the-loop workflows.

**Features:**
- Manual approval
- Quality control
- Complex decision making

**Requires:** Notification system (email, webhook, etc.)

### 4. Custom Agents
User-defined agent logic.

**Features:**
- Fully customizable
- Unlimited possibilities
- Can integrate with any system

---

## Security & Privacy

### Data Protection
- ✅ All data stored locally
- ✅ No cloud sync or remote storage
- ✅ No telemetry or analytics
- ✅ Open source and auditable

### API Key Security
- ✅ Stored in `.env` file
- ✅ Never committed to version control
- ✅ Only used when needed
- ✅ Only sent to official API endpoints

### Network Security
- ✅ Default localhost access
- ✅ Configurable CORS
- ✅ HTTPS in production
- ✅ No external dependencies (core features)

---

## Development

### Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend lint
cd backend
black app/
flake8 app/

# Frontend lint
cd frontend
npm run lint
```

---

## Roadmap

- [x] Basic agent management
- [x] Task queue system
- [x] Web dashboard
- [x] RESTful API
- [x] Docker support
- [ ] WebSocket real-time updates
- [ ] Advanced scheduling algorithms
- [ ] Multi-agent conversations
- [ ] Plugin system
- [ ] Distributed deployment
- [ ] Metrics and analytics

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/CONTRIBUTING.md) for details.

---

## Support

- **Issues:** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/issues
- **Discussions:** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/discussions
- **Documentation:** https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/README.md

---

## License

MIT License - see [LICENSE](https://github.com/ZhenRobotics/openclaw-swarm-orchestrator/blob/main/LICENSE) file for details

---

## Acknowledgments

Inspired by OpenAI Swarm architecture and modern multi-agent systems.

---

**Version:** 0.1.0
**Status:** Alpha - Active Development
**Author:** OpenClaw Team
