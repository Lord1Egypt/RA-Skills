# yaoyao-memory 架构文档

> **版本**: v3.9.0 | **参考**: 鸽子王六层架构

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [LAYER_INTERFACES.md](./LAYER_INTERFACES.md) | 层间接口规范 |
| [SIX_LAYER_MAPPING.md](./SIX_LAYER_MAPPING.md) | 六层对照表 |

---

## 架构总览

```
┌─────────────────────────────────────────────────────────────┐
│                    yaoyao-memory 架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  L1: Identity (身份层)                                       │
│      └── SOUL.md, IDENTITY.md, USER.md                      │
│                                                             │
│  L2: Memory Context (记忆层)                                  │
│      └── MEMORY.md, memory/*.md, predictive_cache.py        │
│                                                             │
│  L3: Orchestration (编排层) ← NEW                           │
│      └── fast_path.py, query_cache.py                       │
│                                                             │
│  L4: Execution (执行层)                                      │
│      └── 63 scripts, memory.py, search.py                   │
│                                                             │
│  L5: Governance (治理层) ← NEW                               │
│      └── governance.py, audit.py, security.py               │
│                                                             │
│  L6: Infrastructure (基础设施层) ← NEW                       │
│      └── infrastructure.py, backup_manager.py, monitoring    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 六层对照 (vs 鸽子王)

| 鸽子王层级 | yaoyao-memory 实现 | 状态 |
|-----------|-------------------|------|
| L1 core | SOUL.md + IDENTITY.md + USER.md | ✅ 完整 |
| L2 memory_context | MEMORY.md + memory/*.md | ✅ 完整 |
| L3 orchestration | fast_path.py + query_cache.py | 🆕 新增 |
| L4 execution | 63个脚本模块 | ✅ 完整 |
| L5 governance | governance.py + audit.py | 🆕 新增 |
| L6 infrastructure | infrastructure.py + backup_manager.py | 🆕 新增 |

---

## 核心模块

### 记忆系统
- `memory.py` - 主记忆引擎
- `search.py` - 统一搜索入口
- `predictive_cache.py` - 预测性缓存 (v2.0 with TTL)

### 性能优化
- `token_optimizer.py` - Token预算控制
- `fast_path.py` - 简单查询快速路径
- `query_cache.py` - 查询缓存

### 治理与安全
- `governance.py` - 治理主模块
- `audit.py` - 审计日志
- `security.py` - 安全检查

### 基础设施
- `infrastructure.py` - 基础设施主模块
- `backup_manager.py` - 备份管理
- `health_check.py` - 健康检测

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v3.9.0 | 2026-04-10 | 新增六层架构对照、Token预算、快速路径、治理层、基础设施层 |
