# OpenClaw 定时任务

本参考仅在用户要求配置 OpenClaw 定时订阅任务时读取。配置前必须已经运行过 `qslazy task status 剧名`，并根据资源发布时间向用户确认过“时间优先”或“画质优先”策略。

## 推荐流程

1. 用 `qslazy task status 剧名 --env <skills-dir>/quark-lazy-cli/.env` 查看网盘状态和资源发布时间。
2. 询问用户偏好：
   - 时间优先：最早有效资源发布时间 + 4 小时。
   - 画质优先：最后一批高质量资源发布时间 + 4 小时。
3. 用户确认后，再创建 OpenClaw 定时任务。
4. 简单、命名规范的资源默认用 `LAZY_CLI_ADVISOR=code`，避免每次唤醒大模型。

## 定时任务模板

```bash
openclaw cron add \
  --name "凡人修仙传-定时更新" \
  --cron "30 2 * * 0" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --agent AgentName \
  --announce \
  --channel feishu \
  --account bot-AgentName \
  --to "USER_OPEN_ID" \
  --message "bash -c 'LAZY_CLI_ADVISOR=code qslazy update all 凡人修仙传 --env <skills-dir>/quark-lazy-cli/.env'\n\n仅根据 stdout 汇报结果，除非排错，不要读取 log 或报告文件。"
```

替换项：

- `凡人修仙传-定时更新`：任务显示名。
- `30 2 * * 0`：定时表达式（cron 格式）。
- `AgentName`：执行任务的 OpenClaw Agent。
- `bot-AgentName`：通知账号。
- `USER_OPEN_ID`：通知目标。
- `<skills-dir>/quark-lazy-cli/.env`：实际 Skill 安装目录中的 `.env`。

## 常用时间

```text
每周一 22:00 -> 0 22 * * 1
每周六 14:00 -> 0 14 * * 6
每周日 02:30 -> 30 2 * * 0
每天 09:00 兜底 -> 0 9 * * *
```

## 汇报格式

定时任务执行后，只根据 stdout 汇报。建议包含：

```text
订阅：
当前：
目标：
偏好：
更新结果：
新增集数：
补全剧集：
```

## 维护命令

```bash
openclaw cron list
openclaw cron run <job-id>
openclaw cron edit <job-id> --cron "0 22 * * 1"
openclaw cron edit <job-id> --disable
openclaw cron edit <job-id> --enable
openclaw cron rm <job-id>
```

执行 `edit`、`rm` 等变更操作前，先向用户确认。
