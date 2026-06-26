# 🧠 Agent Memory v12.2.0

> Give your AI agents a memory that thinks — not just stores.

[![Security Audit](https://img.shields.io/badge/security-192%20fixes-brightgreen)](https://github.com/agent-memory/agent-memory/security) [![GDPR](https://img.shields.io/badge/compliance-GDPR-blue)](https://github.com/agent-memory/agent-memory) [![Circuit Breaker](https://img.shields.io/badge/resilience-circuit%20breaker-orange)](https://github.com/agent-memory/agent-memory)

Agent Memory is a production-grade memory layer for AI agents. It goes beyond simple vector storage with **5-way retrieval**, **temporal reasoning**, **proactive management**, and **enterprise-grade privacy**.

## ✨ Why Agent Memory?

| Feature | Agent Memory | Mem0 | Zep | LangChain Memory |
|---------|-------------|------|-----|------------------|
| 5-way retrieval (FTS+BM25+Semantic+Entity+Causal) | ✅ | ❌ | ❌ | ❌ |
| Dual-timeline fact management | ✅ | ❌ | ❌ | ❌ |
| Proactive Spirit butler | ✅ | ❌ | ❌ | ❌ |
| Chinese native support (12 PII types) | ✅ | ❌ | ❌ | ❌ |
| Enterprise compliance (GDPR + SOC2) | ✅ | ❌ | ❌ | ❌ |
| Self-hosted / Docker | ✅ | ✅ | ✅ | ✅ |

## 🚀 Quick Start

### Install

```bash
pip install agent-memory
```

### 5-Minute Demo

```python
from agent_memory import Memory

# Initialize — zero config
mem = Memory()

# Remember
result = mem.remember("Alice is a data scientist working on NLP projects")
print(result.memory_id)  # mem_abc123

# Recall
results = mem.recall("NLP projects")
for r in results.items:
    print(r["content"])

# Forget
mem.forget(result.memory_id)  # Soft delete, restorable within 30 days

# PII Detection & Redaction
from agent_memory.privacy.guard import PrivacyGuard
guard = PrivacyGuard()
redacted = guard.redact("Contact: 13812345678")
# → "Contact: [手机号]"

# Health Check
info = mem.status()
print(f"Healthy: {info.get('healthy')} | Total: {info.get('total_memories')}")
```

### Docker

```bash
docker compose up -d
# API available at http://localhost:8988
```

### Playground

```bash
pip install "agent-memory[web]"
python -m agent_memory.playground.app
# Open http://localhost:8988
```

## 🏗 Architecture

```
┌─────────────────────────────────────────────┐
│  Adapters: SDK / REST API / MCP / CLI       │
├─────────────────────────────────────────────┤
│  Spirit: Proactive Butler + Safety Protocol │
├─────────────────────────────────────────────┤
│  Cognition: Digital Twin + Metacognition    │
├─────────────────────────────────────────────┤
│  Engines: Ingest / Recall / Maintain / Graph│
├─────────────────────────────────────────────┤
│  Storage: SQLite + FTS5 + sqlite-vec       │
└─────────────────────────────────────────────┘
```

## 📦 Installation Options

```bash
# Core (minimal dependencies)
pip install agent-memory

# With web API
pip install "agent-memory[web]"

# With semantic search
pip install "agent-memory[semantic]"

# With Chinese NLP
pip install "agent-memory[chinese]"

# With observability
pip install "agent-memory[observability]"

# Everything
pip install "agent-memory[all]"
```

## 🔑 Core Features

### TEMPR 5-Way Retrieval
FTS5 full-text + BM25 + Semantic vector + Entity expansion + Causal chain, fused with Reciprocal Rank Fusion.

### Dual-Timeline Facts
`valid_from` / `valid_until` / `occurrence_time` / `mention_time` — track when facts are true, not just when stored.

### Spirit Proactive Butler
Dual-LLM safety protocol, proactive health checks, conflict detection, and memory consolidation.

### Privacy & Compliance
5-level sensitivity, PII detection (12 Chinese types), GDPR/SOC2 compliance framework, encrypted storage.

### Enterprise-Ready
Multi-tenant with quotas, billing engine, feature flags, audit logging, knowledge distillation.

### Chinese Native
jieba tokenization, 12 PII types (身份证/手机/银行卡/护照/军官证...), sentiment analysis, intent detection.

## 🌐 API

### REST API (50+ endpoints)

```bash
# Remember
curl -X POST http://localhost:8988/v1/memories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"content": "Important fact to remember"}'

# Recall
curl -X POST http://localhost:8988/v1/recall \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"query": "important fact"}'
```

### Python SDK

```python
from agent_memory import Memory

mem = Memory()  # Zero config

# Remember
result = mem.remember("Hello world", importance="high")
print(result.memory_id)

# Recall
results = mem.recall("hello")
for r in results.items:
    print(r["content"])

# Forget
mem.forget(result.memory_id)

# Advanced: access full engine
mem.engine  # AgentMemory instance
```

### MCP Server

11 tools for AI agent integration: remember, recall, context_for, correct, delete, spirit_check, etc.

## 🖥️ Complete CLI Reference

### 核心操作

| Command | Description |
|---------|-------------|
| `agent-memory init` | 首次运行引导 — 初始化记忆系统 |
| `agent-memory remember <content>` | 写入记忆 |
| `agent-memory recall <query>` | 检索记忆 |
| `agent-memory context <query>` | 组装上下文 |
| `agent-memory stats` | 查看统计 |
| `agent-memory maintain` | 执行维护 |
| `agent-memory compress` | 压缩记忆 |
| `agent-memory graph` | 生成图谱 |
| `agent-memory feedback <id>` | 记录反馈 |
| `agent-memory feedback-v2 <id>` | 记录反馈 v2（持续学习） |
| `agent-memory learn` | 应用反馈学习 |
| `agent-memory forget <id>` | 删除单条记忆 |
| `agent-memory restore <id>` | 恢复软删除的记忆 |
| `agent-memory purge-deleted` | 永久清理软删除记忆 |
| `agent-memory flush` | L1→L2 沉淀 |
| `agent-memory heal` | 自我修复 |
| `agent-memory update <id>` | 更新记忆内容（版本化） |
| `agent-memory versions <id>` | 查看记忆版本历史 |
| `agent-memory batch-remember` | 批量写入记忆 |
| `agent-memory export` | 导出为 Markdown |
| `agent-memory conflicts` | 检测记忆冲突 |
| `agent-memory notifications` | 查看待处理的主动通知 |
| `agent-memory reactor-scan` | 手动触发 reactor 全量扫描 |

### 知识管理

| Command | Description |
|---------|-------------|
| `agent-memory distill` | 执行记忆蒸馏 |
| `agent-memory distill-stats` | 查看蒸馏系统统计 |
| `agent-memory encyclopedia` | 查看个人百科 |
| `agent-memory entities` | 查看知识实体 |
| `agent-memory topic-summaries` | 查看主题摘要 |
| `agent-memory doc` | 文档精读（上传/检索/列表/回溯） |
| `agent-memory validate <id>` | 验证单条记忆 |
| `agent-memory validate-all` | 验证所有记忆 |
| `agent-memory awareness` | 查询知识感知度 |
| `agent-memory sync` | 从 MEMORY.md 同步记忆 |
| `agent-memory auto-context` | 自动组装上下文 |

### 时间旅行

| Command | Description |
|---------|-------------|
| `agent-memory snapshot` | 创建记忆快照 |
| `agent-memory snapshots` | 列出所有快照 |
| `agent-memory diff` | 对比两个时间点的记忆差异 |
| `agent-memory blame` | 追溯记忆来源 |
| `agent-memory timeline-stats` | 时间旅行系统统计 |
| `agent-memory traces` | 查看推理追踪历史 |
| `agent-memory trace-detail` | 查看单次推理详细步骤 |
| `agent-memory trace-log` | 查看结构化追踪日志 |

### 自我认知

| Command | Description |
|---------|-------------|
| `agent-memory whoami` | 我是谁 — 第一人称自我叙述 |
| `agent-memory identity` | 查看身份画像 |
| `agent-memory narrative` | 构建叙事 |
| `agent-memory worldview` | 查看世界观 |
| `agent-memory self-concept` | 查看完整自我概念 |
| `agent-memory self` | 统一自我状态仪表盘 |
| `agent-memory mood` | 查看 Agent 当前内在状态 |
| `agent-memory persona` | 构建数字孪生人格画像 |
| `agent-memory persona-get` | 获取最新的数字孪生人格画像 |
| `agent-memory personality` | 人格分析 |
| `agent-memory confidence` | 查看置信度历史 |
| `agent-memory reflect` | 查看自我反思历史 |
| `agent-memory uncertainty` | 查看不确定因素模式分析 |
| `agent-memory meta-recall` | 带反思的检索 |
| `agent-memory evaluate` | 评估检索结果质量 |
| `agent-memory gaps` | 查看知识空白 |

### Spirit 管家

| Command | Description |
|---------|-------------|
| `agent-memory spirit` | 自然语言指令 — 通过 Spirit 管家解析并执行 |
| `agent-memory health` | 运行健康检查 |
| `agent-memory daily-report` | 生成每日记忆报告 |
| `agent-memory weekly-report` | 生成每周记忆报告 |
| `agent-memory annual-report` | 生成记忆年报 |
| `agent-memory curiosity` | 好奇心引擎 |
| `agent-memory curious` | 查看好奇驱动的探索任务 |

### 增长

| Command | Description |
|---------|-------------|
| `agent-memory achievements` | 查看成就徽章 |
| `agent-memory growth-feedback` | 提交检索反馈 |
| `agent-memory share-card` | 生成可分享的洞察卡片 |

### 分布式

| Command | Description |
|---------|-------------|
| `agent-memory federation` | 跨 Agent 知识联邦 |
| `agent-memory sync-peers` | 列出所有同步对等节点 |
| `agent-memory sync-with` | 与指定对等节点同步 |
| `agent-memory sync-all` | 与所有对等节点同步 |
| `agent-memory sync-checkpoint` | 创建同步检查点 |
| `agent-memory sync-stats` | 查看同步引擎统计 |

### 角色 & 模型

| Command | Description |
|---------|-------------|
| `agent-memory roles` | 列出所有可用的角色模板 |
| `agent-memory role-get` | 获取特定角色模板 |
| `agent-memory role-apply` | 应用角色风格到个人人格 |
| `agent-memory role-create` | 创建新角色模板 |
| `agent-memory role-delete` | 删除角色模板 |
| `agent-memory role-from-media` | 从媒体文件创建角色模板 |
| `agent-memory model-server` | 管理模型守护进程 |

## 🔧 Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `AGENT_MEMORY_DB_PATH` | Database file path | `./memory.db` |
| `AGENT_MEMORY_JWT_SECRET` | JWT signing key (REQUIRED in production) | — |
| `AGENT_MEMORY_WEB_PORT` | Web server port | `8988` |
| `AGENT_MEMORY_ENV` | Environment (production/development/test) | `production` |

See [DEPLOYMENT.md](DEPLOYMENT.md) for full configuration.

## 📊 Benchmarks

Run the benchmark suite:

```bash
python -m agent_memory.benchmarks.benchmark_suite
```

## 📄 License

MIT License
