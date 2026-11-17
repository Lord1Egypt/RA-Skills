# 调度适配器契约

`team-tasks` 不发送团队消息通知。风险提醒的调度平台适配器负责保存规则、调用提醒解析器和投递消息；台账仍是提醒内容及状态的事实源。

macOS 宿主另有 [原生提醒事项适配](macos-reminders.md)，将全部活动与归档任务镜像到「团队待办（team-tasks）」，并原子回写可靠的勾选完成。其 [定时同步](periodic-sync.md) 优先采用平台的直接命令调度，缺少这项能力时使用本机用户 LaunchAgent；周期运行不调用模型。它不领取或确认 `sync_claim` / `sync_ack`，也不使用风险筛选或工作日日历。原生事项的到期展示由 macOS 管理；此适配不代替下文的风险调度规则、动态解析与消息投递，也不修改既有催办任务或其任务 ID。

## 规则与关联

适配器应在自身受保护的配置存储中维护关联，不写入任务对象：

```json
{
  "taskId": "T-260918-001",
  "reminderJobIds": ["scheduler-job-123"],
  "oneShot": false
}
```

专项规则只能保存 `taskId`、调度表达式、投递目标引用和 `oneShot`；不得缓存标题、负责人、截止日期、状态或提醒正文。规则触发时调用：

```sh
python3 scripts/reminder_engine.py --data-dir /local/team-tasks \
  --task-id T-260918-001 --slot 2026-09-18T14:00+08:00 \
  --delivery-reference channel-ref --reserve
```

仅当 JSON 输出的 `action` 为 `deliver` 时发送 `text`。`silent`（任务结束、暂停、消失、非工作日、重复占位或状态竞争）必须不投递旧文本。`taskId + slot` 是外部发送方的幂等键。

## 工作日日历

常规和专项提醒默认只读加载技能包内 `references/calendars/CN/YYYY.json`，无需 `--holiday-file`。内置日历使用 `Asia/Shanghai`：当前时间、计划时间、进展时间和历史统计区间均按北京时间确定日期；日期范围所需的年度文件必须全部存在。适配器不因宿主机器的时区不同而改变判日。

需要自定义日历时，所有常规及专项调用应显式传入同一份受信任的 `--holiday-file`，整体覆盖内置日历。该参数兼容旧的日期数组，也支持：

```json
{"holidays":["2026-10-01"],"makeupWorkdays":["2026-10-10"]}
```

适配器不得自行重复周末/调休判断。脚本返回 `ok: false` 时不投递，不生成替代文本、不调用 `remind` 或占用时间槽。日历相关错误包括：

| code | 附加字段 | 处理 |
|---|---|---|
| `calendar_missing_year` | `missingYears`，如 `[2024]` | 暂停本次提醒，按官方完整公告补录全部缺失年度后重试；不退回普通周末规则 |
| `calendar_conflict` | `conflicts`，冲突日期数组 | 保留原文件并核对官方公告，修复配置前不投递；不猜测哪个数组优先 |

默认覆盖 2025–2026；任务历史跨入 2024 或计划日期跨入 2027 时，缺年度同样暂停。显式 `--holiday-file` 延续旧格式行为，按调用方时区判日且不执行年度覆盖校验；文件缺失、无效或日期冲突时也须停止。年度 JSON 含元数据，不能直接作为覆盖输入；如需导出覆盖文件，应合并所有受信任年度的休假、补班日期，去重并检查冲突，只保留 `holidays` 和 `makeupWorkdays` 两个键。

## 年度日历维护契约

接入平台默认每年 12 月每周一 09:00（`Asia/Shanghai`）触发维护助手，目标是触发年份的下一年。将其配置为独立受信任任务，避免在创建普通任务时扩大权限。助手应能读取政府公告，日常提醒继续完全离线。

执行 [年度日历维护](calendar-maintenance.md) 中的完整流程：先 `calendar_manager.py validate --year YEAR`；已有有效日历返回 `already_complete` 并跳过联网；缺失年度才读取官方完整通知、核对全部日期，再进行 `install --request FILE --dry-run`、正式安装和回读校验。脚本仅作本地校验和安装；结构校验不能代替助手对公告完整性的核对。

助手/适配器输出以下状态，它们不是脚本联网检查的结果：

| status | 含义 | 后续触发 |
|---|---|---|
| `already_complete` | 目标年度已存在且通过校验 | 当年后续运行先校验后直接跳过联网 |
| `updated` | 新年度已安装并回读通过校验 | 与上项相同，保留历史文件 |
| `not_published` | 尚未找到完整官方通知 | `retry: true`，下一次 12 月周一重试 |
| `error` | 网页无法读取、日期不完整、已有文件无效或安装失败 | 保留原文件，`retry: true`，下一次触发重试 |

12 月最后一个周一 09:00 的检查仍未成功，输出 `status: "error"`、`code: "calendar_update_incomplete"` 和 `missingYears: [目标年]`，说明实际失败原因；不自动延伸到其他月份的无限重试。下一年 12 月重新以新的下一年度为目标。已安装文件即为当年完成依据，无须另写完成标记。

维护助手可访问政府公告网页，并通过安装工具写指定日历目录的年度文件、锁和临时文件；不授予技能根目录泛化写权限、台账写权限或通知发送权限。此契约不自行创建平台调度任务；可复制任务提示词见上述维护说明。

## 同步 outbox

`create`、`update`、`status`、`reopen`、`comment` 成功提交时，会与任务变更原子地把事件写入主台账的 `_reminderSyncEvents`。原生 `complete_external` 提交时产生两条普通事件：`status` / `changedFields:["status"]` 和 `comment` / `changedFields:["comments"]`；重复完成凭据不再产生事件。适配器 worker 使用：

```json
{"op":"sync_claim","actor":"scheduler-adapter","limit":20,"leaseSeconds":300}
```

处理成功后才确认：

```json
{"op":"sync_ack","actor":"scheduler-adapter","eventIds":["event-id"]}
```

租约过期后事件可由其他 worker 重试；适配器必须按事件 ID 去重自己的外部修改日志。处理事件时再读取当前台账，不应相信事件中的旧字段。结束任务的 one-shot 规则应禁用；周期规则可保留，但每次运行前仍需动态解析。仅改标题、负责人或评论时不改写规则正文。

本 outbox 的确认会结束该事件的待处理状态，不是多订阅者广播。macOS 全量同步不得领取或确认这些事件，否则会使调度 worker 漏掉任务变更；本机适配使用独立幂等标记及锁，失败时独立重试。

## 迁移 dry-run

适配器先导出规范化规则 JSON，例如：

```json
{"rules":[{"id":"job-1","taskId":"T-260918-001","oneShot":true,"dynamic":false}]}
```

再运行：

```sh
python3 scripts/reminder_migration.py --data-dir /local/team-tasks --rules exported-rules.json
```

它只输出报告，不访问、创建、禁用或删除任何规则。无显式 `taskId`、或 ID 在活动台账中不存在的规则被列为孤儿并建议暂停；绝不根据标题猜测关联。适配器应先备份规则，人工确认报告后再执行变更并保留回退副本。
