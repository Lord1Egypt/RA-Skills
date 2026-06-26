# 六层架构对照表

> **参考**: 终极鸽子王 (xiaoyi-claw-ultimate-pigeon-king) v2.2.2

---

## 完整对照

| 层级 | 鸽子王 | yaoyao-memory | 差距 |
|------|--------|---------------|------|
| **L1** | core (核心认知) | SOUL.md + IDENTITY.md + USER.md | ✅ 相当 |
| **L2** | memory_context | MEMORY.md + memory/*.md + vector_db | ✅ 相当 |
| **L3** | orchestration | fast_path.py + query_cache.py | 🆕 新增 |
| **L4** | execution | 63 scripts | ✅ 超额 |
| **L5** | governance | governance.py | 🆕 新增 |
| **L6** | infrastructure | infrastructure.py | 🆕 新增 |

---

## L1: Core (核心认知层)

### 鸽子王定义
```
职责: 定义"我是谁"、"用户是谁"、"如何工作"

核心文件:
- IDENTITY.md - 系统身份定义
- SOUL.md - 性格与价值观
- USER.md - 用户画像与偏好
- AGENTS.md - 行为规则与启动流程
```

### yaoyao-memory 实现
```
核心文件:
- /workspace/SOUL.md - 摇摇性格定义
- /workspace/IDENTITY.md - 摇摇身份定义
- /workspace/USER.md - 用户档案

✅ 已完整覆盖
```

---

## L2: Memory Context (记忆与上下文层)

### 鸽子王定义
```
职责: 提供"记住什么"、"理解上下文"

核心模块:
- MEMORY.md - 长期记忆索引
- data/ - 记忆数据存储
- retrieval/ - 记忆检索引擎
- management/ - 记忆生命周期管理
```

### yaoyao-memory 实现
```
核心模块:
- MEMORY.md - 长期记忆索引
- memory/*.md - 每日记忆文件 (7个)
- memory_stats.py - 统计分析
- predictive_cache.py - 预测性缓存 (v2.0)
- heat_tracker.py - 热度追踪
- forget_detector.py - 遗忘检测

✅ 已完整覆盖
```

---

## L3: Orchestration (任务编排层)

### 鸽子王定义
```
职责: 决定"做什么"、"如何调度"

核心模块:
- scheduler/ - 任务调度中心
- routing/ - 技能/模块路由
- policy/ - 执行策略引擎
- workflow/ - 工作流编排
```

### yaoyao-memory 实现
```
核心模块:
- fast_path.py - 简单查询快速路径
- query_cache.py - 查询缓存
- batch_search.py - 批量搜索优化
- conflict_detector.py - 冲突检测

🆕 部分实现 (快速路径 + 缓存)
```

---

## L4: Execution (能力执行层)

### 鸽子王定义
```
职责: 执行"具体任务"、"提供能力"

核心模块:
- runtime/ - 运行时环境
- automation/ - 自动化执行
- domain_agents/ - 领域智能体
- phone-engine/ - 手机操作引擎
```

### yaoyao-memory 实现
```
核心模块:
- 63个脚本模块
- memory.py - 主记忆引擎
- search.py - 统一搜索
- config_manager.py - 配置管理
- feature_flag.py - 特性开关

✅ 已超额实现
```

---

## L5: Governance (稳定性与治理层)

### 鸽子王定义
```
职责: 确保"安全"、"稳定"、"可审计"

核心模块:
- safety/ - 安全控制与护栏
- audit/ - 审计与证据链
- failover/ - 故障转移
- rollback/ - 回滚管理
```

### yaoyao-memory 实现
```
核心模块:
- governance.py - 治理主模块
  - AuditLogger - 审计日志
  - SecurityChecker - 安全检查
  - FailoverManager - 故障转移
  - RollbackManager - 回滚管理
- audit.py - 审计工具

🆕 新增
```

---

## L6: Infrastructure (基础设施与运维层)

### 鸽子王定义
```
职责: 提供"资产管理"、"运维支持"

核心模块:
- inventory/ - 资产与配置管理
- ops/ - 运维工具集
- backup/ - 备份与恢复
- monitoring/ - 监控与告警
```

### yaoyao-memory 实现
```
核心模块:
- infrastructure.py - 基础设施主模块
  - AssetManager - 资产管理
  - MonitoringMetrics - 监控指标收集
  - BackupManager - 备份管理

🆕 新增
```

---

## 接口对照

### 鸽子王标准接口
```json
L1_Output: { schema, timestamp, identity, personality, user, behavior }
L2_Output: { schema, timestamp, cognitive_context, memories, conversation }
L3_Output: { schema, timestamp, task_list, routing_target, execution_policy }
L4_Output: { schema, timestamp, task_results, state_changes, event_log }
L5_Output: { schema, timestamp, security_status, audit_records, recovery_actions }
L6_Output: { schema, timestamp, asset_updates, backup_status, monitoring_metrics }
```

### yaoyao-memory 接口
```json
Memory_Input: { schema, timestamp, request, context }
Memory_Output: { schema, timestamp, status, results, metadata }
Cache_Entry: { schema, key, ttl_seconds, created_at, data, stats }
Governance_Input: { schema, timestamp, operation, target, risk_level }
Governance_Output: { schema, timestamp, decision, reason, actions_taken }
Token_Budget: { total, allocated, used, status }
```

---

## 性能目标对照

| 指标 | 鸽子王目标 | yaoyao-memory 现状 |
|------|-----------|-------------------|
| 首Token延迟 | < 500ms | ~200ms ✅ |
| 总响应延迟 | < 3s | ~500ms ✅ |
| 缓存命中率 | > 90% | 86% 🟡 |
| 记忆检索延迟 | < 50ms | 0.04ms ✅ |
| Token利用率 | > 80% | ~70% 🟡 |

---

**最后更新**: 2026-04-10
