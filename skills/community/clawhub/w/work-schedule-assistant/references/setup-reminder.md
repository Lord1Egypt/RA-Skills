# 配置每日工作提醒

## 推荐方式

在用户实际使用提醒的聊天渠道中，让 OpenClaw 执行：

```text
请使用 work-schedule-assistant，为当前聊天设置每天早上8:30的工作日程提醒，时区为 Asia/Shanghai。
```

从活动聊天中创建定时任务，更容易保留当前企业微信会话的投递目标。

## 终端配置

先确认 Gateway 正常：

```bash
openclaw status
```

然后在 Skill 目录运行：

```bash
python3 scripts/setup_reminder.py \
  --time 08:30 \
  --timezone Asia/Shanghai \
  --channel wecom \
  --to "<企业微信目标ID>"
```

如果从活动聊天中调用并希望沿用当前路由：

```bash
python3 scripts/setup_reminder.py \
  --time 08:30 \
  --timezone Asia/Shanghai \
  --channel last
```

Cron 修改需要 `operator.admin` 权限。

## 检查任务

```bash
openclaw cron list
```

手动测试时，从列表中取得任务 ID：

```bash
openclaw cron run <任务ID>
```

查看运行记录：

```bash
openclaw cron runs --id <任务ID> --limit 20
```

## 重要条件

- Gateway 必须持续运行。
- `cron.enabled` 必须启用。
- 不得设置 `OPENCLAW_SKIP_CRON`。
- 确认 `--tz` 与实际工作时区一致。
- 企业微信渠道必须处于 `running, works` 状态。
- 若 Cron 正常执行但没有收到消息，检查 `channel`、`to` 和企业微信权限。

## 修改提醒时间

为避免重复提醒，先用 `openclaw cron list` 找到名称为“每日工作日程提醒”的旧任务，再使用 `openclaw cron edit` 修改，或者移除旧任务后重新运行配置脚本。

