---
name: spec-task
description: "结构化任务管理与生命周期强制执行。以下场景必须使用：(1) 任何被 coordinator 通过 sessions_spawn 派发的任务 (2) 可拆解步骤≥3 的复杂任务 (3) 工作区已存在 spec-task/ 目录时的后续任务 (4) 用户显式要求使用 spec-task (5) prependContext 明确提醒时。跳过 spec-task 会导致验收失败。"
metadata: {}
---

# Spec-Task 任务管理

## 核心原则

1. **所有非平凡任务必须通过 spec-task 管理**，不存在"太简单不需要"的例外。
2. 任务生命周期每一步都必须显式转换，不可跳过状态。
3. 四文档必须按拓扑序在 `running` 之前完成：`brief → spec → plan → checklist`。
4. 没有 checklist 的执行 = 不可追溯 = 验收失败。
5. 验收时所有 criteria 通过且任务为 running，自动转为 completed。

## 工作流程（8步）

```
1. config_merge    → 检查/合并项目配置
2. task_recall     → 搜索历史经验（keywords 必填，避免重复劳动）
3. task_create     → 创建任务（task_name 必填，生成 status.yaml）
4. 填充文档        → brief → spec → plan → checklist（按拓扑序）
5. task_transition → assigned → running（开始执行）
6. task_log        → 记录运行时事件（error/alert/add-block/remove-block/output/retry）
7. task_verify     → 验收管理（add-criterion → finalize；finalize 自动触发 completed）
8. task_archive    → 归档（生成 history + lessons，支持 dry_run）
```

## 状态机（8种状态 · 14条转换）

```
pending ──→ assigned ──→ running ──→ completed   (终态)
    │            │            │
    └── cancelled ← ─ ─ ─ ─ ┘
                      running → failed → running
                      running → blocked → pending
                      running → revised → running
                      running → revised → pending
                      running → running   (进度刷新)
```

| 起始状态 | 目标状态 | 说明 |
|---------|---------|------|
| pending | assigned | 任务分配 |
| pending | cancelled | 取消 |
| assigned | running | 开始执行 |
| assigned | cancelled | 取消 |
| running | completed | 完成（终态） |
| running | failed | 失败 |
| running | blocked | 阻塞 |
| running | cancelled | 取消 |
| running | revised | 需修订 |
| running | running | 进度刷新 |
| failed | running | 重试 |
| blocked | pending | 解除阻塞，回到待分配 |
| revised | running | 修订后重新执行 |
| revised | pending | 修订后回到待分配 |

## 四文档拓扑序

```
brief（无依赖）→ spec（依赖 brief）→ plan（依赖 brief）→ checklist（依赖 spec + plan）
```

- **brief.md**: 问题定义、目标、约束条件、成功标准
- **spec.md**: 技术方案、接口设计、数据结构
- **plan.md**: 实施计划、步骤分解、依赖关系
- **checklist.md**: 可执行检查项，格式：`- [x] 1.1 步骤描述`

## 5级检测器

| 级别 | 名称 | 条件 | 行为 |
|------|------|------|------|
| L1 | none | spec-task/ 不存在 | 自动初始化 |
| L2 | empty | 目录存在但无任务 | 等待任务创建 |
| L3 | skeleton | 有 status.yaml 但缺文档 | 提醒补全文档 |
| L4 | in_progress | 有非终态任务且文档完整 | 正常推进 |
| L5 | all_done | 所有任务终态 | 建议归档 |

## 子 Agent 合规

作为子 agent（被 coordinator 通过 sessions_spawn 派发）时：

1. **必须使用 spec-task**，不存在例外。
2. 第一步调用 `config_merge`，第二步调用 `task_recall`，第三步调用 `task_create`。
3. 创建后必须填充 brief → spec → plan → checklist 全部四文档。
4. 只有 checklist 中第一个步骤勾选后，才能开始实际执行。
5. 工作区已有 spec-task/ 目录时，优先用 `task_resume` 检查可恢复任务。

## Hook 系统

- **before_prompt_build**: 检测工作区状态，注入 prependContext 提醒。
- **before_tool_call**: 对 task_create、config_merge、task_archive、task_recall 自动注入 `project_root` 参数。

## 工具速查表

| 工具 | 必填参数 | 用途 |
|------|---------|------|
| `config_merge` | — | 合并项目配置（可选 project_root, format） |
| `task_recall` | keywords | 搜索历史经验（可选 project_root, agent_workspace, top） |
| `task_create` | task_name | 创建任务（可选 project_root, title, assigned_to, parent, depth） |
| `task_transition` | task_dir, status | 状态流转（可选 revision_type, trigger, summary, impact, resume_from, block_type, block_reason, assigned_to, changes, affected_steps） |
| `task_log` | task_dir, action | 记录事件；action: error / alert / add-block / remove-block / output / retry |
| `task_verify` | task_dir, action | 验收管理；action: add-criterion / finalize / get |
| `task_resume` | task_dir | 断点恢复，返回 next_action 决策 |
| `task_archive` | task_dir | 归档（可选 agent_workspace, project_root, agent_name, dry_run） |

## 验收状态

标准（criterion）状态：`pending | passed | failed`

验收流程：`add-criterion`（添加标准）→ `get`（查看结果）→ `finalize`（汇总确认）
finalize 时若全部 passed 且任务 status 为 running，自动转为 completed。

## 错误码

| 错误码 | 场景 |
|--------|------|
| `TASK_NOT_FOUND` | 任务目录不存在 |
| `TASK_ALREADY_EXISTS` | 同名任务已存在 |
| `INVALID_TRANSITION` | 非法状态转换 |
| `DUPLICATE_BLOCK` | 重复阻塞记录 |
| `BLOCK_NOT_FOUND` | 阻塞记录不存在 |
| `DUPLICATE_OUTPUT` | 重复产出记录 |
| `NO_CRITERIA` | 无验收标准时执行 finalize |
| `CONFIG_NOT_FOUND` | 配置文件不存在 |
| `INVALID_PARAMS` | 参数校验失败 |
| `INTERNAL_ERROR` | 内部错误 |
| `LOCK_ACQUIRE_FAILED` | 文件锁获取失败 |

## 配置参考（SpecTaskConfig）

```yaml
context: "项目描述（可选）"
runtime:
  allow_agent_self_delegation: true   # 允许 Agent 自行分配
  task_timeout: 3600                  # 任务超时（秒）
failure_policy:
  soft_block: true                    # 失败后是否允许继续
  hard_block: false                   # 失败后是否强制阻塞
  verify_failed: true                 # 验证失败是否触发策略
  on_exhausted: "cancel"              # 重试耗尽后的动作
archive:
  auto_archive: true                  # 是否自动归档
  record_history: true                # 是否记录历史
  generate_lessons: true              # 是否生成经验教训
```
