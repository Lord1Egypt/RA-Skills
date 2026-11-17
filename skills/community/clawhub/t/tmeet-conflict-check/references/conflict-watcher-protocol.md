# 会议冲突监测协议

## 目标

让确定性脚本轮询腾讯会议列表，只在新增或改期会议产生新冲突时唤醒模型。脚本不直接向用户解释或发送消息。

## 执行模式

macOS/Linux 使用本文的 Bash 示例。Windows x64 必须改用 [windows-execution.md](windows-execution.md) 中的 PowerShell、LocalAppData 状态路径和 Windows 验收流程。

### 默认时间策略

- 时区：用户当前时区（`--timezone local`）。
- 工作日：周一至周五（`--weekdays 1,2,3,4,5`）。
- 办公时间：09:00–18:00，包含 18:00 槽位，不包含 18:30。
- 检查槽位：每个整点和半点（`--schedule-minutes 0,30`）。
- 默认允许调度器晚到 120 秒，超过后该次启动静默退出。

这些是“检查时间”。只有检测到新冲突时才“提醒用户”，不在每个槽位例行发消息。

用户要求开启监测却没有给出时间配置时，直接使用上述默认值，不需要为时间再追问一轮。

### 调度器单次执行（被动触发）

```bash
python3 scripts/watch_meeting_conflicts.py \
  --state-file "<PRIVATE_STATE_DIR>/conflict-watch.json"
```

参数默认为 `--trigger scheduled`。外部调度器应在整点和半点启动。脚本会再做一次办公时间和槽位校验；即使宿主误在夜间、周末或非槽位启动，也会在调用 `tmeet` 之前静默退出。

标准输出为空时，宿主必须直接丢弃结果，不创建 Agent 回合、不发用户消息。只有输出 `meeting.conflict.detected` NDJSON 时，才将该行作为新 Agent 回合的输入。

### 常驻执行（被动触发）

```bash
python3 scripts/watch_meeting_conflicts.py \
  --watch \
  --state-file "<PRIVATE_STATE_DIR>/conflict-watch.json"
```

脚本不再按固定短间隔空轮询，而是休眠到下一个有效槽位。宿主运行时持续消费标准输出。脚本无新冲突时不输出心跳，不得因进程仍在运行而反复唤醒 Agent。

### 用户主动查询

用户主动说“查一下我的会议冲突”时，Agent 应立即调用 `tmeet meeting list/search` 并当场计算，不等待下一个整点或半点，也不受办公时间限制。无冲突时也要向用户返回“未发现当前账号腾讯会议之间的时间冲突”。

`--trigger manual` 可用于脚本调试或人工建立快照，会立即执行而绕过时间门禁；但脚本仍只输出“新冲突事件”，不能代替上述面向用户的即时查询回复。

## 自定义检查时间

自定义时区、工作日、办公时间，但仍每小时整点/半点检查：

```bash
python3 scripts/watch_meeting_conflicts.py \
  --watch \
  --timezone "Asia/Shanghai" \
  --weekdays "1,2,3,4,5" \
  --office-start "08:30" \
  --office-end "19:00" \
  --schedule-minutes "0,30" \
  --state-file "<PRIVATE_STATE_DIR>/conflict-watch.json"
```

只在用户指定的离散时间检查；`--schedule-times` 会覆盖 `--schedule-minutes`，且所有时间必须位于办公时间内：

```bash
python3 scripts/watch_meeting_conflicts.py \
  --watch \
  --office-start "08:30" \
  --office-end "19:00" \
  --schedule-times "09:15,12:00,17:45" \
  --state-file "<PRIVATE_STATE_DIR>/conflict-watch.json"
```

更改时间配置后，使用新参数重启常驻进程，或更新宿主调度器的启动参数。

## 初始化与去重

- 首次执行只建立基线，默认不提醒已存在冲突。
- 需要首次也告警时显式传入 `--alert-existing`。
- 状态文件保存会议签名和活跃冲突指纹。同一冲突不重复提醒；冲突解除后再次出现时可重新提醒。
- 状态文件及事件文件使用私有目录，不提交到 Git。
- Windows 上使用当前用户的 `%LOCALAPPDATA%\tmeet-conflict-check\`；文件模式 `0600` 仅是 POSIX 保护，不作为 Windows ACL 保证。

## 事件格式

```json
{
  "event": "meeting.conflict.detected",
  "event_time": "2026-08-13T02:05:00Z",
  "source": "tmeet-conflict-check",
  "query_window": {
    "start": "2026-08-13T01:05:00Z",
    "end": "2026-08-27T02:05:00Z"
  },
  "changed_meetings": [
    {
      "subject": "客户评审",
      "meeting_code": "222222222",
      "start_time": "2026-08-14T02:30:00Z",
      "end_time": "2026-08-14T03:30:00Z"
    }
  ],
  "conflicts": [
    {
      "kind": "hard",
      "meetings": [],
      "overlap_start": "2026-08-14T02:30:00Z",
      "overlap_end": "2026-08-14T03:00:00Z",
      "overlap_minutes": 30
    }
  ]
}
```

`kind` 取值：

- `hard`：两场会议存在实际重叠时段。
- `soft`：前后会议无重叠，但间隔小于 `--soft-gap-minutes`。
- `multi`：同一时段至少有三场会议并发。

事件不包含 `meeting_id` 等内部标识。

## Agent 处理规则

1. 仅对 `event=meeting.conflict.detected` 触发用户提醒。
2. 直接使用事件中的会议时间和冲突计算结果，不重新拉取全部会议。
3. 提醒中说明这是“当前账号可见的腾讯会议冲突”，不声称覆盖完整日程。
4. 展示冲突会议、重叠或间隔时长，不自行取消会议或代替用户选择。
5. 脚本连续失败或退出时，将其视为监测失效，单独告知用户；不声称仍在监测。
6. 每次用户可见结果末尾都要告知用户可自定义检查时间。已启用默认监测时使用：“当前冲突监测时间可自定义；默认在当前时区的工作日 09:00–18:00（含 18:00），整点和半点由脚本检查，只有新冲突才提醒你并唤醒 Agent。”只做即时查询或其他场景时，将开头改为“可启用冲突监测，检查时间可自定义”，不声称已在运行。已自定义时改为回显实际配置。

## 边界

- 这是脚本级低成本轮询，不是腾讯会议服务端实时邀请事件。
- 脚本进程或调度器停止期间不会检查。
- OAuth 失效、CLI 不可用或网络中断时，脚本输出错误并在连续失败达到阈值后退出。
- 默认最多有约 30 分钟的新邀请冲突发现延迟；自定义更密的槽位会增加 CLI/API 请求量。
