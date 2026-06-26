---
name: restart-safe-workflow
description: Safe OpenClaw gateway restart workflow with doctor precheck, checkpoint, restart-health-resume chain, task continuation, reconcile, and user-visible notifications.
---

# restart-safe-workflow

## 能力概览
- 安全重启主链：`doctor -> checkpoint -> restart -> health -> resume`
- 任务续跑：`pendingActions` + Action 状态机
- 语义动作：`notify-time[:TZ]`
- 计划能力：`plan` / `validate`（TaskPlan v1）
- 补偿与升级：`reconcile` + `retry_exceeded`
- 观测诊断：`report --verbose` / `diagnose`
- 一键验收：`restart-acceptance.sh`（支持 `--with-restart`，默认自守护 detached）

## 常用命令
```bash
# 安全重启
scripts/restart-safe.sh run --task-id <id> --next "notify:重启完成;notify-time"

# 计划预览 / 校验
scripts/restart-safe.sh plan --task-id <id> --next "notify:ok;notify-time"
scripts/restart-safe.sh validate --tasks-file examples/plan-valid.json

# 摘要 / 诊断
scripts/restart-safe.sh report --task-id <id>
scripts/restart-safe.sh report --task-id <id> --verbose
scripts/restart-safe.sh diagnose --task-id <id>

# 验收
scripts/restart-acceptance.sh
scripts/restart-acceptance.sh --with-restart --notify-channel feishu --notify-target user:<open_id>
```

## 推荐发布内容
- `SKILL.md`
- `README.md`
- `config-action-allowlist.txt`
- `schemas/taskspec-v1.schema.json`
- `examples/plan-valid.json`, `examples/plan-invalid.json`
- `scripts/restart-safe.sh`, `scripts/restart-acceptance.sh`
- `references/restart-safe-sop.md`
- `references/phase4-rollout-checklist.md`

## Changelog（最近两次）
- **v1.0.2**: 完成 Phase3/4，修复 TC10 升级触发，验收支持自守护 detached。
- **v1.0.1**: 完成 Phase1/2，新增 TaskPlan v1 与状态机能力。
