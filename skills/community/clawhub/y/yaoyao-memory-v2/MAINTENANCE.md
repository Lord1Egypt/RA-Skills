# yaoyao-memory 维护指南 v4.0

> 最后更新: 2026-04-14

---

## 📊 监控阈值

| 指标 | 阈值 | 说明 |
|------|------|------|
| 系统健康度 | ≥90分 | 低于此值告警 |
| 记忆数量 | - | 越多越好 |
| 错误类型记忆 | <10条 | 超过告警 |
| 搜索延迟 | <100ms | 超过告警 |
| 缓存命中率 | >60% | 低于此值告警 |
| L0覆盖 | ≥60% | 对话历史覆盖 |
| L1覆盖 | ≥95% | 结构化记忆覆盖 |
| 数据库大小 | <100MB | 定期清理 |

---

## 🔧 手动维护任务

### 1. 完整维护（每周）
```bash
python3 scripts/health_check.py
python3 scripts/auto_fixer.py fix
python3 scripts/benchmark.py
```

### 2. 覆盖率检查（每日）
```bash
python3 scripts/check_coverage.py
```

### 3. FTS重建（搜索失效时）
```bash
python3 scripts/memory_wal.py checkpoint  # 执行检查点
python3 scripts/optimize_vector_system.py rebuild  # 重建索引
```

### 4. 向量优化（数据库过大时）
```bash
python3 scripts/optimize_vector_system.py status
python3 scripts/optimize_vector_system.py vacuum
```

### 5. 预测性维护（每周）
```bash
python3 scripts/predictive_maintenance.py
```

---

## 📝 自动任务

| 任务 | 调度 | 说明 |
|------|------|------|
| 健康检查 | 每6小时 | 自动检查+修复 |
| 性能优化 | 每6小时 | 自动优化 |
| 记忆沉淀 | 每日 | 自动沉淀 |
| IMA同步 | 每日 | 云端备份 |
| NAS同步 | 每4小时 | 本地备份 |

---

## 🚨 故障排查

### 搜索失效
1. 检查 `python3 scripts/health_check.py`
2. 运行 `python3 scripts/memory_wal.py status`
3. 执行 `python3 scripts/memory_wal.py checkpoint`

### 性能下降
1. 检查 `python3 scripts/benchmark.py`
2. 运行 `python3 scripts/auto_optimizer.py`
3. 检查 `python3 scripts/predictive_maintenance.py`

### 数据库过大
1. 运行 `python3 scripts/memory_wal.py checkpoint`
2. 执行 VACUUM: `python3 scripts/optimize_vector_system.py vacuum`
3. 清理: `python3 scripts/batch_operations.py cleanup_dup`

### IMA同步失败
1. 检查API限额（200次/天）
2. 等待次日重置
3. 检查网络连接

---

## 📁 日志位置

| 日志 | 路径 |
|------|------|
| 健康检查 | `memory/heartbeat-state.json` |
| 同步状态 | `memory/.ima_sync.json` |
| NAS同步 | `memory/.samba_sync_state.json` |
| 预测缓存 | `memory/.predictive_cache.json` |

---

## ⚠️ 重要原则

1. **自动化优先** - 大部分任务自动执行，无需手动干预
2. **有问题先检查** - `health_check.py` 是第一排查工具
3. **保留痕迹** - 所有操作都记录到每日记忆

---

_有问题先问 health_check.py_
