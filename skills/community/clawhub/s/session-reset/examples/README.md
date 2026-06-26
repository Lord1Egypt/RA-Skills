# 使用示例目录

本目录包含 `session-reset` skill 的各种使用示例脚本。

## 示例列表

| 示例 | 脚本 | 使用场景 |
|------|------|----------|
| **首次初始化** | [00-first-time-setup.sh](./00-first-time-setup.sh) | **新安装后必做！** 配置默认 agents |
| 日常维护 | [01-daily-maintenance.sh](./01-daily-maintenance.sh) | 定期清理过期 sessions |
| SOUL 更新后 | [02-after-soul-update.sh](./02-after-soul-update.sh) | 修改配置后让配置生效 |
| 批量重置 | [03-reset-all-agents.sh](./03-reset-all-agents.sh) | 批量重置六部+秘书 |
| 备份管理 | [04-backup-management.sh](./04-backup-management.sh) | 查看和恢复备份 |
| 高级用法 | [05-advanced-usage.sh](./05-advanced-usage.sh) | 自定义清理策略 |

## 使用步骤

```bash
# 1. 首次使用（必做！）
./00-first-time-setup.sh
openclaw session-reset --init

# 2. 后续使用其他示例
./01-daily-maintenance.sh
./02-after-soul-update.sh
# ...
```

## 注意事项

- **必须先执行初始化** (`--init`)，否则 `--scope agents` 无法使用
- 大多数示例默认使用 `--dry-run` 预览模式
- 需要实际执行时，请取消脚本中的注释
- 建议在执行前仔细查看预览输出
