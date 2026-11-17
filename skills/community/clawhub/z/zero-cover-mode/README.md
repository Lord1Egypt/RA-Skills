# Zero Cover Mode — 零稀泥模式

> v1.0.0 — 保证每次 bug 修复都执行根因分析→测试验证→闭环归档→上线验证 四阶段闭环。
> 同一类型 bug 重复出现时自动拉重构警报。

## 快速开始

```bash
# 查看当前状态
cd skills/zero-cover-mode
python lib/state_manager.py info

# 注册修复 session
python lib/state_manager.py register <session_id> <bug_id>

# 运行完整修复管线
python lib/orchestrator.py run-pipeline --bug-id <bug_id> --test-cmd "pytest tests/"

# 查看根因深度
python lib/root_cause_validator.py check bugs/{bug_id}/BUG_ROOT_CAUSE.md

# 生成周报
python lib/weekly_report.py generate FIX_CLOSURE_LOG.ndjson 2026-W26 reports/my_report.md
```

## 组件概览

| 组件 | 用途 | 关键特性 |
|------|------|---------|
| `lib/orchestrator.py` | 四阶段编排层（入口） | UoW 事务保护, checkpoint 断线恢复, 全局超时, 熔断自愈 |
| `lib/persistence_facade.py` | 持久化门面（唯一写入入口） | 单次扫描去重+行数统计, 指数退避重试, 运维可观测计数器 |
| `lib/state_manager.py` | 状态管理 + 跨进程文件锁 | 原子写入, session 管理, ndjson 单源重建 |
| `lib/repository.py` | 持久化仓库 | 委托 PersistenceFacade 双写, 批量保存, 完整性校验+自动恢复 |
| `lib/ndjson_schema.py` | ndjson 校验/追加/轮转 | Pydantic 严格校验, 安全轮转带备份 |
| `lib/fake_data_detector.py` | L1-L3 假数据检测 | AST 文档字符串跳过, 26 关键词模式 |
| `lib/sensitive_filter.py` | 敏感信息脱敏 | API key/JWT/GitHub PAT/Windows 路径 |
| `lib/loop_detector.py` | 重复 bug 根因检测 | Jaccard token 相似度 |
| `lib/weekly_report.py` | 周报自动生成 | 隔离数据分析 |
| `lib/refactoring_alert.py` | 重构警报聚合 | 按 bug_type 聚类截断, 根源模式加权 |
| `lib/backend_checker.py` | 后端可用性 + 活代码验证 | Ollama 并发检查, LIBRARY_TEST 短路 |
| `lib/root_cause_validator.py` | 5-Whys 深度检测 | 循环论证检测, 最小内容长度 |
| `lib/ndjson_migrate_v1_to_v2.py` | ndjson schema 迁移 | bug_types 数组→字符串, 微秒截断 |

## 架构特性

| 维度 | 说明 |
|------|------|
| **事务完整性** | Phase 0/1/2/3 全部 UoW 保护，失败自动回滚 |
| **契约锁死** | Pydantic 构造时 + 运行时双重校验 |
| **单一写入门面** | 所有 ndjson 写入经 PersistenceFacade |
| **幂等性保障** | bug_id 去重 + OSError 保守策略 |
| **并发安全** | OS 原子操作 + 文件锁 + checkpoint 事务一致性 |
| **自愈机制** | 熔断器 60s 自动恢复 + undo 带锁保护 |
| **容错与重试** | 指数退避重试（MAX_RETRIES=3） |
| **全局超时** | PIPELINE_TIMEOUT 每个 Phase 前检查 |

## 文档

详见 `SKILL.md` 了解完整工作流程和四阶段闭环规范。
