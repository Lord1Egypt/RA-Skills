# yaoyao-memory 架构文档 v4.0

> 六层架构记忆系统 - 让 AI 跨会话保持上下文、沉淀知识、持续进化

---

## 📐 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                      L6 基础设施层                          │
│   (paths.py, infrastructure.py, config/)                    │
├─────────────────────────────────────────────────────────────┤
│                      L5 治理层                              │
│   (security.py, governance.py, rbac.py)                    │
├─────────────────────────────────────────────────────────────┤
│                      L4 记忆管理层                          │
│   (memory.py, memory_*.py)                                │
├─────────────────────────────────────────────────────────────┤
│                      L3 索引层                              │
│   (search.py, vector_store.py, fts/)                       │
├─────────────────────────────────────────────────────────────┤
│                      L2 增强层                              │
│   (summarizer.py, forget_detector.py, auto_context.py)    │
├─────────────────────────────────────────────────────────────┤
│                      L1 捕获层                              │
│   (conversation_summarizer.py, intelligent_recall.py)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 目录结构

```
yaoyao-memory-v2/
├── SKILL.md              # 主文档（使用指南）
├── ARCHITECTURE.md       # 架构详解
├── CHANGELOG.md         # 版本历史
├── SECURITY.md          # 安全声明
├── FUNCTIONS.md         # 功能清单（103个）
│
├── src/                 # 源码
│   ├── core/            # 核心模块
│   │   └── __init__.py
│   │
│   ├── scripts/         # 工具脚本（103个）
│   │   ├── health_check.py
│   │   ├── sync_ima.py
│   │   ├── auto_fixer.py
│   │   └── ...
│   │
│   ├── config/         # 配置
│   │   └── feature_flags.json
│   │
│   └── tests/        # 测试
│       └── __init__.py
│
├── html/                # Web界面
└── references/          # 参考文档
```

---

## 🔢 核心模块

### L1 捕获层
负责从对话中捕获记忆

| 模块 | 功能 |
|------|------|
| `intelligent_recall.py` | 智能召回 |
| `auto_context.py` | 自动上下文追踪 |
| `conversation_summarizer.py` | 对话摘要 |

### L2 增强层
记忆后处理和增强

| 模块 | 功能 |
|------|------|
| `summarize.py` | 总结工具 |
| `forget_detector.py` | 遗忘检测 |
| `progressive_summary.py` | 渐进摘要 |

### L3 索引层
搜索和索引

| 模块 | 功能 |
|------|------|
| `search.py` | 主搜索引擎 |
| `vector_store.py` | 向量存储 |
| `query_cache.py` | 查询缓存 |

### L4 记忆管理层
记忆的 CRUD

| 模块 | 功能 |
|------|------|
| `memory.py` | 核心记忆操作 |
| `memory_stats.py` | 统计分析 |
| `memory_quality.py` | 质量评估 |
| `memory_graph.py` | 知识图谱 |

### L5 治理层
安全和权限

| 模块 | 功能 |
|------|------|
| `security.py` | 安全模块 |
| `governance.py` | 治理层 |
| `rbac.py` | 权限控制 |
| `context_guard.py` | 上下文守卫 |

### L6 基础设施层
系统基础服务

| 模块 | 功能 |
|------|------|
| `paths.py` | 路径管理 |
| `infrastructure.py` | 基础设施 |
| `config_manager.py` | 配置管理 |

---

## 🔌 依赖关系

```
用户请求
    │
    ▼
┌─────────────┐
│  cli.py    │ ← 入口
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  search.py │ ← 搜索引擎
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ memory.py   │ ← 核心CRUD
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ vector_store│ ← 向量存储
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  SQLite DB  │ ← 数据持久化
└─────────────┘
```

---

## ⚙️ 自动化流程

### 记忆沉淀流程
```
对话结束
    │
    ▼
conversation_summarizer.py
    │
    ▼
intelligent_recall.py
    │
    ▼
memory.py (写入)
    │
    ▼
sync_ima.py (同步云端)
```

### 健康检查流程
```
定时触发 (每6小时)
    │
    ▼
health_check.py
    │
    ├──▶ auto_fixer.py (自动修复)
    │
    └──▶ sync_ima.py (云端备份)
```

---

## 🛡️ 安全设计

1. **上下文隔离** - `<memory_block>` 标签防止记忆被当指令
2. **子Agent工具过滤** - 危险工具禁止列表
3. **Skill安全扫描** - 安装前恶意代码检测
4. **RBAC权限控制** - 基于角色的访问控制

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| FTS搜索延迟 | 0.02ms |
| 缓存命中率 | 100% |
| 数据库大小 | ~15MB |
| 记忆数量 | 95条 |

---

## 🚀 扩展指南

### 添加新模块
1. 在对应层级目录创建模块
2. 更新 `FUNCTIONS.md`
3. 更新 `SKILL.md`
4. 添加测试

### 版本发布
1. 更新 `CHANGELOG.md`
2. 更新 `SKILL.md` 版本号
3. 运行 `publish.sh`

---

_最后更新: 2026-04-14_
