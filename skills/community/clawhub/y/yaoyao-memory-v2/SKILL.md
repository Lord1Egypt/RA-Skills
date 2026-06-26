---
name: yaoyao-memory
version: 4.0.0
description: |
  六层架构记忆系统 - 让 AI 跨会话保持上下文、沉淀知识、持续进化
  【本地存储】SQLite 数据库
  【全文搜索】FTS5 搜索引擎
  【模块化】核心+可选模块，按需安装
---

# yaoyao-memory 🦞

> 六层架构记忆系统 - 你的第二大脑

---

## 快速开始

```bash
# 初始化
python3 scripts/init_memory.py

# 搜索记忆
python3 scripts/search.py "关键词"

# 健康检查
python3 scripts/health_check.py
```

---

## 核心功能

| 功能 | 说明 |
|------|------|
| 记忆存储 | SQLite 本地持久化 |
| 全文搜索 | FTS5 搜索引擎 |
| 向量搜索 | 可选的向量索引 |
| 云端同步 | IMA + NAS 双通道 |
| 自动遗忘检测 | v2多维度衰减+矛盾检测 |
| 知识图谱 | 记忆关联分析 |
| 硬件检测 | 自动识别AVX512/AMX/NEON |
| 预测维护 | 预测增长+维护计划 |
| 对话管理 | 多轮对话历史管理 |
| 批量操作 | 导入/导出/删除/更新 |
| 智能标签 | 自动标签/合并/清理 |
| WAL模式 | SQLite性能优化 |
| 命令行搜索 | quick_search CLI工具 |

---

## 六层架构

| 层级 | 功能 | 核心模块 |
|------|------|----------|
| L1 捕获 | 对话记忆捕获 | conversation_summarizer |
| L2 增强 | 遗忘检测/摘要 | forget_detector |
| L3 索引 | 搜索/向量 | search, vector_store |
| L4 管理 | 记忆 CRUD | memory |
| L5 治理 | 安全/权限 | security, governance |
| L6 基础 | 配置/路径 | paths, config |

---

## 目录结构

```
yaoyao-memory-v2/
├── SKILL.md              # 本文档
├── ARCHITECTURE.md       # 架构详解
├── CHANGELOG.md         # 版本历史
├── SECURITY.md          # 安全声明
├── FUNCTIONS.md         # 功能清单 (103个)
│
├── src/
│   ├── core/            # 核心模块
│   └── scripts/         # 工具脚本
│
├── html/                # Web界面
└── tests/              # 测试
```

---

## 常用命令

### 记忆操作
```bash
# 初始化
python3 scripts/init_memory.py

# 搜索
python3 scripts/search.py "查询内容"

# 统计
python3 scripts/memory_stats.py
```

### 系统维护
```bash
# 健康检查
python3 scripts/health_check.py

# 自动修复
python3 scripts/auto_fixer.py fix

# 性能优化
python3 scripts/benchmark.py
```

### 云同步
```bash
# IMA同步
python3 scripts/sync_ima.py

# NAS同步
python3 scripts/sync_to_nas.py
```

---

## 配置

配置文件：`~/.openclaw/workspace/memory/config/`

| 配置项 | 说明 |
|--------|------|
| `memory.db` | SQLite 主数据库 |
| `vectors.db` | 向量数据库 |
| `feature_flags.json` | 功能开关 |

---

## 安全

- ✅ 上下文隔离标签
- ✅ 子Agent工具过滤
- ✅ RBAC权限控制
- ✅ 安装前安全扫描
- ✅ subprocess timeout

文档：
- [SECURITY.md](./SECURITY.md) - 安全架构
- [SECURITY_FIX.md](./SECURITY_FIX.md) - 安全修复报告
- [RESEARCH.md](./RESEARCH.md) - 友商调研报告
- [MAINTENANCE.md](./MAINTENANCE.md) - 维护指南

---

## 变更记录

- [CHANGELOG.md](./CHANGELOG.md) - 完整版本历史
- [FUNCTIONS.md](./FUNCTIONS.md) - 103个功能清单

---

## 🔗 Hermes Bridge 集成

v4.0.0 集成 hermes-bridge 能力：

| 模块 | 功能 |
|------|------|
| error_classifier | API 错误分类 + 恢复决策 |
| smart_routing | 简单查询 → 便宜模型 |
| context_compressor | 结构化摘要压缩 |
| insights | 使用洞察生成 |
| trajectory | 对话轨迹记录 |
| redact | 敏感信息脱敏 |
| rate_limit | API 限流追踪 |

**API 端点**：`GET /api/hermes_status`

```bash
# 启动带 Hermes 的 API Server
python3 scripts/api_server.py --port 8765
```

---

_版本: 4.0.1 | 更新: 2026-04-15_
