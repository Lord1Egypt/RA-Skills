# OpenClaw 重启安全流程（SOP, Sprint 4）

适用场景：任务中涉及 `openclaw gateway restart` / 配置变更后重启 / 需要重启后自动续跑。

## 目标
- 重启前发现配置风险，避免重启失败后人工排障。
- 重启后自动恢复任务并继续执行 pendingActions。
- 全流程具备可见回执、可诊断、可补偿、可升级。

## 标准流程
1. `doctor` 预检：`openclaw doctor --non-interactive`
2. checkpoint 落盘：写入 state/restart/<taskId>.json
3. 解析 `nextAction` 并入队 `pendingActions`
4. 发送重启前通知 + 任务清单（pre）
5. detached runner 执行重启
6. 重启后健康检查
7. 触发 resume 事件 + 重启完成通知
8. 发送重启后待处理任务清单（post-plan）
9. 执行任务续跑动作（resume actions）
10. 发送重启后任务执行结果（post-result）
11. done gate 判定，满足条件后置 `phase=done`

## done gate（严格）
必须同时满足：
- `healthOk=true`
- `resumeEventSent=true`
- `notifyPreSent=true`（若启用通知）
- `notifyPostSent=true`（若启用通知）
- `resumeStatus=success`

## `nextAction` 格式
- `notify:<text>`
- `notify-time`
- `notify-time:<TZ>`
- `cmd:<command>`
- `script:<path>`
- `json:[{...}]`
- 支持 `;` 串联（例如 `notify:重启完成;notify-time`）

## TaskPlan（Phase 1）
- 预览计划：
  - `scripts/restart-safe.sh plan --task-id <id> --next "notify:重启完成;notify-time"`
- 校验计划：
  - `scripts/restart-safe.sh validate --tasks-file skills/restart-safe-workflow/examples/plan-valid.json`
- 运行时使用任务文件：
  - `scripts/restart-safe.sh run --task-id <id> --tasks-file skills/restart-safe-workflow/examples/plan-valid.json`

## 补偿策略（reconcile）
- 对 `resume-failed/notify-failed/post-notified/...` 任务执行补偿
- 支持重试与退避：
  - `RECONCILE_MAX_RETRIES`（默认 3）
  - `RECONCILE_BACKOFF_SEC`（默认 5）
- 超限升级：
  - `escalationRequired=true`
  - `escalationReason=retry_exceeded`
  - 可见告警通知（若启用通知）

## 白名单策略
- 默认内置白名单（健康检查、状态查询、echo）
- 可通过 `ACTION_ALLOWLIST_FILE` 覆盖
- 白名单外命令拒绝执行并记为 `resume-failed`

## 诊断与排障
- 查看原始状态：
  - `scripts/restart-safe.sh status --task-id <id>`
- 查看摘要：
  - `scripts/restart-safe.sh report --task-id <id>`
  - `scripts/restart-safe.sh report --task-id <id> --verbose`（含 action 明细）
- 自动诊断：
  - `scripts/restart-safe.sh diagnose --task-id <id>`
- 手工触发补偿：
  - `scripts/restart-safe.sh reconcile --task-id <id>`

## 状态字段（Phase 2 扩展）
- `actionStates.<actionId>.status`：pending/running/success/failed/skipped
- `actionStates.<actionId>.attempts`
- `idempotencyLedger.<idempotencyKey>`：是否已执行
- `resumeCompletedActions`：已从队列出列的动作（含跳过/失败继续）

## 失败策略
- `onFailure=stop`：动作失败则流程失败
- `onFailure=continue`：动作失败后继续后续动作
- `onFailure=escalate`：动作失败后继续，并标记 `escalationRequired=true`

## 一键验收
- 默认（不真实重启）：
  - `scripts/restart-acceptance.sh`
- 真实重启链路：
  - `scripts/restart-acceptance.sh --with-restart --notify-channel feishu --notify-target user:<open_id> --notify-account master`

## 执行纪律
- No doctor, no restart.
- No checkpoint, no restart.
- No done without resume success.
