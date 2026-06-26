# yaoyao-memory 脚本索引

> 92个脚本按用户场景分类 - 最后更新：2026-04-10

---

## 🎯 按用户场景

### 👤 日常使用（高频）
| 脚本 | 功能 |
|------|------|
| `memory.py` | 核心记忆存储 |
| `search.py` | 记忆搜索 |
| `memory_stats.py` | 统计概览 |
| `health_check.py` | 健康检测 |
| `auto_fixer.py` | 自修复 |
| `config_manager.py` | 配置管理 |

### 🔍 搜索查询（中频）
| 脚本 | 功能 |
|------|------|
| `smart_query.py` | 智能查询推荐 |
| `memory_search_enhanced.py` | 增强搜索（模糊/正则/布尔）|
| `query_predictor.py` | 查询预测 |
| `batch_search.py` | 批量搜索 |
| `intelligent_recall.py` | 智能召回 |

### 📊 分析洞察（中频）
| 脚本 | 功能 |
|------|------|
| `memory_trends.py` | 趋势分析 |
| `memory_graph.py` | 记忆图谱 |
| `memory_insights.py` | 洞察提取 |
| `conversation_summarizer.py` | 对话摘要 |
| `forget_detector.py` | 遗忘检测 |
| `conflict_detector.py` | 冲突检测 |

### 🔧 系统维护（低频）
| 脚本 | 功能 |
|------|------|
| `memory_archive.py` | 归档管理 |
| `memory_snapshot.py` | 快照管理 |
| `memory_snapshot.py` | 快照管理 |
| `cleanup.py` | 清理 |
| `performance_monitor.py` | 性能监控 |
| `alert_manager.py` | 告警管理 |

### 🔐 安全治理（管理员）
| 脚本 | 功能 |
|------|------|
| `security.py` | 安全检查 |
| `rbac.py` | 权限管理 |
| `context_guard.py` | 上下文守卫 |
| `skills_guard.py` | Skill安全 |
| `subagent_isolation.py` | 子Agent隔离 |
| `circuit_breaker.py` | 熔断器 |

### 🔄 同步备份 → 独立 Skill

> 云端备份功能已独立为 `yaoyao-cloud-backup` Skill

| 脚本 | 功能 | 位置 |
|------|------|------|
| `sync_ima.py` | IMA云同步 | yaoyao-cloud-backup |
| `sync_samba.py` | Samba同步 | yaoyao-cloud-backup |
| `backup_manager.py` | 备份管理 | yaoyao-cloud-backup |
| `backup_restore.py` | 备份恢复 | yaoyao-cloud-backup |
| `memory_exporter.py` | 导出功能 | yaoyao-cloud-backup |
| `migrate.py` | 迁移工具 | yaoyao-cloud-backup |

### 🧠 智能增强（可选）
| 脚本 | 功能 |
|------|------|
| `embedding.py` | 向量化 |
| `progressive_summary.py` | 渐进摘要 |
| `memory_enhancer.py` | 记忆增强 |
| `psychology_adapter.py` | 心理学适配 |
| `behavior_learner.py` | 行为学习 |
| `persona_learner.py` | 画像学习 |

### 🛠️ 开发者工具（高级）
| 脚本 | 功能 |
|------|------|
| `api_server.py` | API服务 |
| `cli.py` | 命令行 |
| `benchmark.py` | 性能基准 |
| `check_coverage.py` | 覆盖率 |
| `token_tracker.py` | Token追踪 |
| `retry.py` | 重试机制 |

### 📦 内部模块（开发者）
| 脚本 | 功能 |
|------|------|
| `vector_store.py` | 向量存储 |
| `dedup.py` | 去重 |
| `router.py` | 路由 |
| `rewriter.py` | 改写 |
| `understand.py` | 理解 |
| `langdetect.py` | 语言检测 |
| `explainer.py` | 解释 |
| `feedback.py` | 反馈 |

---

## 📊 统计

| 场景 | 数量 | 使用频率 |
|------|------|----------|
| 日常使用 | 6 | ⭐⭐⭐ 高频 |
| 搜索查询 | 5 | ⭐⭐ 中频 |
| 分析洞察 | 6 | ⭐⭐ 中频 |
| 系统维护 | 6 | ⭐ 低频 |
| 安全治理 | 6 | ⭐ 管理员 |
| 同步备份 | 5 | ⭐ 按需 |
| 智能增强 | 6 | ⭐ 可选 |
| 开发者工具 | 6 | ⭐ 高级 |
| 内部模块 | 8 | 🔧 开发 |
| **总计** | **98** | |

---

## 🔑 功能开关（Feature Flags）

| 开关 | 默认 | 说明 |
|------|------|------|
| `memory.silent_mode` | False | 静默模式（需确认）|
| `search.hybrid` | True | 混合搜索 |
| `search.cache` | True | 搜索缓存 |
| `memory.auto_promote` | True | 自动升级 |
| `memory.llm_enhance` | False | LLM增强 |
| `shell.enabled` | True | Shell嵌入 |
| `ux.detailed_errors` | True | 详细错误 |

---

## 🚀 快速命令

```bash
# 搜索记忆
python3 scripts/memory.py search <关键词>

# 查看统计
python3 scripts/memory.py stats

# 健康检测
python3 scripts/health_check.py

# 自修复
python3 scripts/auto_fixer.py fix

# 配置管理
python3 scripts/config_manager.py list
```
