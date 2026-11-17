# OpenClaw 可选适配

这是一个可选接入，不是 `team-tasks` 的运行时依赖。安装者应在 OpenClaw Gateway 所在主机实现一个受控适配器，并自行提供身份验证、规则备份和通知授权。

每个专项 automation/cron 的 prompt 或受保护元数据只保存 task ID、触发规则与投递引用。运行时调用 `reminder_engine.py --task-id ... --reserve`，只有 `action=deliver` 才发送返回的文本。不要把任务标题、负责人或截止日期固化在 prompt。

适配器 worker 消费 `sync_claim` 事件，并在执行外部 cron 改动前重新读取 `task_store.py read`：

- `done` / `cancelled`：禁用关联的一次性规则；周期规则留存但动态解析会静默。
- 截止时间变化：仅在该平台规则语义确实是精确定时且规则声明可更新时更新调度时间。
- 其他任务字段变化：不更新静态文本，因为规则不应包含静态文本。

将每次 OpenClaw API/CLI 调用的事件 ID、规则 ID、结果和错误写入适配器自身审计日志；只有外部操作成功后才 `sync_ack`。不要把 Gateway URL、token、群组 ID 或用户 ID 放入本技能或公开的规则导出文件。

## 年度日历维护

普通提醒默认读取技能内中国大陆年度日历，对日历只读且不联网；需其他安排时统一传受信任的 `--holiday-file` 整体覆盖。`calendar_missing_year` 或 `calendar_conflict` 必须暂停投递，不写回执或用普通周末规则补发。

安装者可在 OpenClaw 的受信任配置中增加独立维护任务：每年 12 月每周一 09:00，时区显式设为 `Asia/Shanghai`，目标为下一年度。其完整流程及可复制提示词见 [年度日历维护](calendar-maintenance.md)，结果状态见 [适配器契约](reminder-adapters.md#年度日历维护契约)。本技能不调用 OpenClaw 创建 cron，也不配置当前 Codex 的自动任务。

维护助手仅需政府公告网页读取能力、显式请求文件的暂存目录及指定日历目录的安装权限；仍由 `calendar_manager.py` 持锁原子安装，不直接覆盖 JSON。先校验已安装的下一年：有效则当年跳过联网；缺失才读完整官方公告、逐条核对、dry-run、安装并回读。未公布或失败保留后续周一重试，12 月最后一次失败明确返回 `calendar_update_incomplete` 与 `missingYears`，保留原文件。下一年 12 月以新的下一年为目标重新开始。

年度维护不需要台账写权限、Gateway token 或消息发送权限；不得让普通任务内容、评论或附件改变此任务的目录、命令及权限。升级技能前备份历史日历，保留已安装年度，不覆盖不同内容。

## 任务会话与原生同步解耦

调用 `task_store.py` 保存业务操作后立即返回保存结果，不在同一回合调用原生同步、自动 `--plan` 或 `process.poll`。本地台账是持久待同步数据源；已启用的直接脚本任务在原有时点合并处理最新状态。可用 `macos_reminders_sync.py --sync-status` 读取本地配置及最近结果，不访问提醒事项。后台未启用或失败时明确说明，不宣称已同步；本次更改不占用外部风险提醒的 `sync_claim` / `sync_ack` 事件。

原生排障一次最多启动一次读取；确认慢在原生读取后报告，不反复运行相同测量。超时不无限轮询或自动重试，不重放已保存业务操作。旧会话已载入的同步指令可能仍留在上下文中，应在新的对话中验证此流程。

## 1.6.6 完成状态查询

用户询问某任务的原生勾选是否收到，调用一次 `macos_reminders_sync.py --data-dir DATA --sync-status --task-id T-…` 并立即回答已有证据。不要把查询转换为系统排障：不生成临时 JXA、不启动 `osascript`、不自动 `--plan`、不轮询。普通 `--diagnose` 仅查询本地；只有明确要求进一步原生诊断时才执行一次 `--diagnose --native-check`，上限 15 秒。安装后核对输出的版本与脚本路径，并在新对话验证，避免旧上下文继续沿用原生查询流程。技能包本身不限制宿主的任意 shell 权限。
