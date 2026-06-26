# Status.yaml 格式参考

status.yaml 是每个任务的运行时状态文件，跟踪任务的生命周期。每个任务一份。

## 文件位置

`spec-task/<task-name>/status.yaml`

## 完整字段定义

```yaml
task_id: <string>                      # 任务唯一标识
title: <string>                        # 任务标题
created: <ISO 8601 datetime>           # 创建时间
updated: <ISO 8601 datetime>           # 最后更新时间（每次 saveStatus 自动更新）

# ─── 状态 ───
status: <状态值>                       # 见下方 8 种状态定义
assigned_to: <string>                  # 负责执行的 agent 名称，默认 "agent"
started_at: <ISO 8601 datetime | null> # 第一次转为 assigned 时自动设置
completed_at: <ISO 8601 datetime | null> # 转为 completed 时自动设置

# ─── 进度 ───
progress:
  total: <number>                      # checklist 中带步骤编号的 checkbox 总数
  completed: <number>                  # 已勾选（- [x]）的步骤数
  current_step: <string>               # 当前步骤编号（如 "2.3"）
  percentage: <number>                 # 完成百分比

# ─── 嵌套关系 ───
parent: <string | null>                # 父任务路径，null = 顶层任务
depth: <number>                        # 嵌套深度（0 = 顶层任务）
children: <string[]>                   # 子任务路径列表

# ─── 产出物 ───
outputs: <string[]>                    # 产出物文件的绝对路径列表

# ─── 时间统计 ───
timing:
  estimated_minutes: <number | null>   # 预估时间（来自 plan.md）
  elapsed_minutes: <number | null>     # 实际耗时（task_transition 时自动计算）

# ─── 错误记录 ───
errors:                                # 执行过程中遇到的错误
  - step: <string>                     # 出错的步骤编号
    message: <string>                  # 错误描述
    retry_count: <number>              # 已重试次数
    timestamp: <ISO 8601 datetime>      # 发生时间

# ─── 告警 ───
alerts:                                # 需要注意的异常情况
  - type: <string>                     # depth_exceeded | timeout | other
    message: <string>                  # 告警描述
    timestamp: <ISO 8601 datetime>      # 发生时间

# ─── 阻塞信息 ───
blocked_by:                            # 当前任务被哪些任务阻塞
  - task: <task-path>                  # 阻塞任务路径
    reason: <string>                   # 阻塞原因

# ─── 验收 ───
verification:
  status: <验收状态>                   # pending | passed | failed
  criteria:                            # 逐条验收结果
    - criterion: <string>              # Success Criteria 条目
      result: <string>                 # passed | failed
      evidence: <string>               # 证据（产出物路径或描述）
      reason: <string>                 # 通过/失败原因
  verified_at: <ISO 8601 datetime>     # 验收时间
  verified_by: <string>                # 验收者（agent 名称）

# ─── 变更历史 ───
revisions:                             # 所有变更记录，只追加不修改
  - id: <number>                       # 递增编号（从 1 开始）
    type: <变更类型>                    # 见下方 RevisionType 定义
    timestamp: <ISO 8601 datetime>      # 变更时间
    trigger: <string>                  # 触发原因
    summary: <string>                  # 变更摘要
    block_type: <string>               # soft_block | hard_block（仅 auto_adapt 时有值）
    block_reason: <string>             # 阻碍原因（仅 auto_adapt 时有值）
    impact: <string>                   # minor | major | full_reset
    changes:                            # 变更的构件
      - artifact: <string>             # brief | spec | plan | checklist
        action: <string>               # added | modified | removed
        detail: <string>               # 变更详情
    affected_steps:                     # 受影响的步骤
      invalidated: <string[]>          # 失效的步骤编号
      modified: <string[]>             # 需要修改的步骤编号
      added: <string[]>                # 新增的步骤编号
    resume_from: <string>              # 从哪个步骤继续（步骤编号）
    status_before: <string>            # 变更前状态
    status_after: <string>             # 变更后状态
```

## 枚举类型速查

### TaskStatus（8 种）

| 状态 | 含义 |
|------|------|
| `pending` | 任务已创建，等待分配 |
| `assigned` | agent 已接受任务 |
| `running` | 正在执行 |
| `completed` | 全部完成 + 验收通过 |
| `failed` | 执行失败或验收不通过（重试耗尽） |
| `blocked` | 需要其他任务先完成 |
| `cancelled` | 用户主动中止 |
| `revised` | 用户变更需求，正在评估影响（临时状态） |

### VerificationStatus（3 种）

`pending` | `passed` | `failed`

### RevisionType（6 种）

`created` | `user_request` | `auto_adapt` | `verify_retry` | `cancel` | `status_change`

### ImpactLevel（3 种）

| 级别 | 含义 |
|------|------|
| `minor` | 小调整，不影响现有步骤 |
| `major` | 影响多个步骤，需修改 checklist |
| `full_reset` | 需要重新规划 |

## 进度计算规则

ProgressCalculator 自动从 `checklist.md` 解析进度，**只有带步骤编号的 checkbox** 才计入 `total`：

- ✅ 计入：`- [ ] 1.1 收集需求`、`- [x] 2.3.1 编写测试`
- ❌ 不计入：`- [ ] 常规备注`、`- [x] 附加说明`

`percentage` 由 ProgressCalculator 自动计算，agent 无需手动更新 progress 字段。

## 时间计算

`elapsed_minutes` 在每次 `task_transition` 时自动计算（基于 `started_at` 或上次转换时间到当前时间的差值），agent 无需手动维护。
