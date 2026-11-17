# 安全存储接口

## 运行方式

Python 3.9+，仅使用标准库，支持 macOS/Linux 本地文件系统。所有读写者必须使用同一个规范化数据目录；不要把实际台账部署在 iCloud、Dropbox、NFS 等同步或共享目录。技能包可以复制到运行机器，台账需放在该机器的本地目录。

调用方先完成身份和业务权限检查。`actor` 仅作审计标签，不是身份凭据。`task_store.py` 是存储层，不使用网络，不验证聊天平台身份，不计算提醒频率、节假日或 snooze 上限，也不发送消息；风险筛选及内置年度日历判日由同技能的 `scripts/reminder_engine.py` 完成，调度和通知由接入方负责。

macOS 提醒事项由独立的 `scripts/macos_reminders_sync.py` 同步：它通过本存储入口 `read` 读取活动及全部归档的一致快照，写入「团队待办（team-tasks）」，并以 `complete_external` 原子回写可靠的勾选完成。存储层不调用原生应用，原生适配不领取或确认调度 outbox。调用与权限见 [macOS 提醒事项同步](macos-reminders.md)。

```sh
python3 /path/to/team-tasks/scripts/task_store.py \
  --data-dir /absolute/local/data/team-tasks \
  --request /path/to/request.json
```

也可省略 `--request`，通过标准输入传入一个 JSON 操作对象。请求文件不能是正式台账。数据目录应预先创建；首次使用显式发送 `{"op":"init"}`，现有台账不能初始化覆盖。

Python 接入可导入 `TaskStore`，调用 `TaskStore(directory).execute(request)`；不要调用内部 `commit`、`mutate` 等方法。失败抛出 `StoreError` 或 `OSError`，CLI 会将其转换为结构化 JSON。

日历不属于任务台账模型，不由 `task_store.py` 管理，也不进入台账备份/恢复事务。日常任务与提醒对技能内 `references/calendars/CN/` 只读；提醒缺少所需年度或发现休假/补班冲突时先失败，不调用 `remind` 登记回执。只有独立年度维护流程可执行 `calendar_manager.py install` 写入指定日历目录；权限及接口见 [年度日历维护](calendar-maintenance.md)。不要为此开放整个技能根目录或在任务操作中触发联网。

## 操作请求

| op | 参数 | 行为 |
|---|---|---|
| `init` | 无 | 仅在没有活动文件和归档时创建空台账 |
| `read` | 无 | 返回 `ledgers`，文件名映射到完整文档；查询和导出在其副本上进行 |
| `validate` | 无 | 校验活动文件及全部归档，返回各文件任务数 |
| `create` | `actor`, `fields` | 脚本生成 ID、默认字段及初始历史；返回 `id` |
| `update` | `actor`, `id`, `changes`, `expected` | 在最新对象上应用允许字段的修改，追加历史 |
| `status` | `actor`, `id`, `status`, `expected` | 状态为 `pending/done/cancelled`；同步完成和取消时间 |
| `complete_external` | `actor`, `id`, `expected`, `source` | 以完成凭据和状态历史指纹原子提交完成、来源评论及两条普通 outbox 事件；重复凭据无变化 |
| `comment` | `actor`, `id`, `content`, `meaningfulProgress?` | 追加非空评论和历史，不替换数组；标记有效进展时原子更新 `lastProgressAt` |
| `remind` | `id`, `slot` | 原子增加提醒计数并记录时间槽；返回 `duplicate` |
| `sync_claim` | `actor`, 可选 `limit`, `leaseSeconds` | 租约领取待处理的提醒同步事件；返回 `events` |
| `sync_ack` | `actor`, `eventIds` | 仅确认由该 actor 租约领取且已成功处理的同步事件 |
| `archive` | `month` | 将该月及以前完成/取消的活动任务完整移入该月归档；月份必须早于本月 |
| `reopen` | `actor`, `id`, `expected` | 从活动文件或归档检索任务，恢复 pending，清除完成/取消时间，追加历史 |
| `restore` | `backup`, `expectedHash`, 可选 `target` | 显式恢复指定文件，默认目标 `team-tasks.json`；先保留原文件证据 |

不支持整表替换、直接删除任务或覆盖评论/历史。未知请求参数也会被拒绝。

任务 `create`、`update`、`status`、`reopen` 和 `comment` 与 `_reminderSyncEvents` 中的同步事件在同一事务内提交。事件是“重新读取当前任务并同步外部规则”的可靠提示，不是过期任务字段的副本。调度适配器领取事件后应重新 `read`，成功处理其外部规则后才确认；租约超时可重试，适配器应按事件 ID 做外部操作去重。`sync_claim` 与 `sync_ack` 不修改任务及其历史。

`create.fields` 允许：`title`（必填）、`description`、`priority`、`isBlocking`、`tags`、`assignee`、`assigneeId`、`creator`、`creatorId`、`dueDate`、`dueTime`、`sourceType`、`sourceId`、`notifyTargetId`、`snoozedUntil`、`lastProgressAt`。

`update.changes` 允许上述字段中的业务可变字段，排除 `creator`、`creatorId`、`sourceType`、`sourceId`。ID、创建时间、状态、评论、历史和提醒字段不能通过普通更新修改。已有未知字段完整保留，但不开放任意扩展字段写入。

普通更新的 `expected` 必须恰好包含此次修改的所有字段，值为读取时的旧值。对未存在的可选字段使用 `null`；存储层将缺失与 `null` 视为等价。状态操作及重开必须传入 `{"status":"读取到的旧状态"}`；`complete_external` 使用下述专用预期结构。冲突时整个操作拒绝，不部分应用。

```json
{
  "op": "update",
  "actor": "user-123",
  "id": "T-260908-001",
  "changes": {"priority": "high", "dueDate": "2026-09-15"},
  "expected": {"priority": "medium", "dueDate": null}
}
```

```json
{"op":"comment","actor":"user-123","id":"T-260908-001","content":"已联系供应商"}
```

当评论代表实际推进时，接入方应显式标记，避免自动日志或“暂无进展”错误重置停滞计时：

```json
{"op":"comment","actor":"user-123","id":"T-260908-001","content":"供应商已确认交付时间","meaningfulProgress":true}
```

```json
{"op":"remind","id":"T-260908-001","slot":"2026-09-08T14:00+08:00"}
```

时间槽须由所有提醒调用方使用同一规范，包含日期与时区，不能只写 `14:00`。脚本将其作为不透明幂等键。顶层可选 `_reminderReceipts` 为 `{任务ID: [时间槽, ...]}`，脚本自动维护、不自动清理，保证较早时间槽的延迟重试也不重复计数。它不会替换任务对象，归档后保留回执供重开使用。成功发送外部消息与记录回执不构成分布式事务；消息重试用平台幂等键，平台不支持时需单一发送者和结果核查。

## 原生完成回写

`complete_external` 请求结构如下；两处 64 位十六进制值由适配器生成，指纹由 `status_history_fingerprint(task)` 取得：

```json
{
  "op": "complete_external",
  "actor": "macOS 提醒事项",
  "id": "T-260908-001",
  "expected": {
    "status": "pending",
    "historyFingerprint": "读取任务时的64位小写SHA-256"
  },
  "source": {
    "kind": "macos-reminders",
    "namespace": "数据目录命名空间的64位小写SHA-256",
    "reminderId": "原生提醒事项ID",
    "completionDate": "2026-09-08T14:10:00+08:00",
    "receiptId": "该次原生完成凭据的64位小写SHA-256"
  }
}
```

`source` 恰好包含以上五个字段；`kind` 固定为 `macos-reminders`，原生 ID 非空，完成时间须为包含时区的有效 ISO 时间。`expected` 恰好包含 `status:"pending"` 和合法指纹。指纹是任务历史中 `create`、`status`、`reopen` 条目的规范 JSON（`sort_keys=True`、`ensure_ascii=False`、`separators=(',',':')`）UTF-8 的 SHA-256。普通字段修改或追加评论不会使其失效，完成后重开会使其改变；回写不能仅比较当前 `pending` 状态。

存储层在现有锁内先查目标任务历史 `detail.externalCompletion` 中的 `receiptId`，归档同样查询。凭据及完整来源一致时返回 `duplicate:true, changed:false`；同凭据但来源不同则返回 `conflict`。未提交过的凭据仅能修改活动台账中的 `pending` 任务，且指纹必须仍一致。来源完成时间是否可靠、是否发生在同步基线之后，由原生适配器判断，不得用不可靠的旧勾选构造请求。

首次提交在同一事务中设置 `done`、`completedAt` 为台账提交时间，追加保存原生完成时间与 ID 的来源评论、`status` 和 `comment` 历史，以及两条普通 outbox 事件。凭据只保存在 `status` 历史的 `detail.externalCompletion`，不新增任务或台账顶层回执字段；归档移动会完整保留。重复响应丢失后可安全重试同一请求，即使期间重开也不会再次完成任务。取消勾选不调用此接口，也不自动重开。

## 返回与失败处理

成功：退出码 0，`{"ok":true,"code":"ok",...}`。`id` 为操作目标，`backup` 为本次快照目录（有实际提交时），`warnings` 为提交后清理异常。无变化时返回 `changed:false`。`recoveredTransaction:true` 表示本次先完成了一次中断事务，应在当前上下文说明。

失败：退出码 1，`{"ok":false,"code":"...","message":"..."}`。代码包括 `validation_failed`、`conflict`、`not_found`、`lock_timeout`、`recovery_required`、`io_error`。

- 锁超时：其他进程仍可能工作，稍后重试；永远不要删除 `.task-store.lock`。
- 结构、旧值或身份目标错误：保留现状，读取并核对后再生成新请求。
- IO 错误或进程退出：可能已提交部分或全部结果。保留所有现场，先调用 `read` 让事务恢复并核对操作结果。不要直接重放创建、评论等非幂等请求。
- 事务文件与正式文件不符：停止写入，保留事务、快照和正式文件，人工核对；不要删除事务文件来强行绕过。

台账业务操作与 macOS 同步分别返回结果，不构成跨系统事务。业务操作已经返回 `ok: true` 而原生同步失败时，报告“台账已保存，提醒事项同步失败”，保留原生部分结果并仅重试同步。不要把原生应用错误改报成台账写入失败，也不要重放已经提交的创建或评论。

锁内的读取会先执行必要的事务恢复，因此 `read` / `validate` 不是取证意义上的完全只读命令；上线取证应先暂停写入者并复制整个数据目录。

## 备份与恢复

备份的创建、读取与清理均通过已打开的目录文件描述符定位，逐级禁止跟随符号链接，并检查目录或文件是否被替换。数据根目录、备份目录和快照必须属于当前运行用户且不可被其他用户写入；备份文件必须是同一用户拥有的普通文件且不能是硬链接。新建备份目录和快照权限为 `0700`，文件为 `0600`。旧版同属主且不可被其他用户写入的 `0755` 备份根目录会在创建快照时收紧到 `0700`；属主不符、可被其他用户写入或类型异常时停止，不自动接管。

清理仅处理匹配快照标识的目录，删除前校验该快照的全部台账文件。未知文件使该快照保留；符号链接、硬链接、异常属主或路径替换会停止清理，不递归追踪链接。若台账已经提交成功而清理失败，仍返回 `ok: true` 并在 `warnings` 中报告清理异常，避免调用方误以为未提交而重复写入。

每次提交将所有被修改文件的原始字节保存在 `backups/时间戳-唯一标识/`，完成 fsync 后才准备事务。首次新建文件没有旧内容，快照目录可以为空。保留最近 100 次提交的快照，以及所有不足 30 天的快照；清理只在成功提交之后执行，不按任务数计算。

事务包含所有参与文件的修改前/后 SHA-256 及完整待提交内容。恢复先验证全部参与文件分别匹配前态或后态，再补全尚未替换的文件；发现第三种状态则不替换任何文件。同目录临时文件回读验证成功后用 `os.replace` 替换，每次同步目录。中断期间直接读取多个文件仍可能观察到中间态，所以读者同样应走入口。

遗留 `.bak` 与正式文件均有效且解码内容相同时可清理；其他情况暂停写入，不依据时间新旧自动选择。显式恢复前，用只读工具查看两份文件并计算当前目标文件 SHA-256；目标不存在时 `expectedHash` 为 `null`。

```json
{
  "op": "restore",
  "backup": "backups/20260908T060000.000000Z-0123456789abcdef0123456789abcdef/team-tasks.json",
  "target": "team-tasks.json",
  "expectedHash": "当前目标文件的SHA-256"
}
```

目标只允许活动文件或合法月份的归档文件。`backup` 接受相对于数据目录的路径，或以规范化数据目录为前缀的绝对路径；只允许 `backups/快照标识/目标台账文件`。快照标识格式为脚本生成的 UTC 时间戳加 32 位十六进制标识，文件名必须与目标一致。拒绝 `..`、目录外来源、各级符号链接、硬链接及非普通文件；通过目录文件描述符和禁止跟随符号链接的打开方式读取，并检查读取期间的路径替换或文件变化。旧版任意路径恢复请求不再兼容，外部导入需独立核对流程，不能借用恢复入口。恢复源必须结构有效，并与其他现有台账合并通过 ID 唯一性检查。被替换文件即使损坏也按原字节备份；相关遗留 `.bak` 复制到 `legacy-evidence-唯一标识/`，提交成功后才删除旧 `.bak` 标记。若恢复也中断，保留证据并先执行事务恢复。

现有台账缺少 `version`、`updatedAt`、任务状态或合法 `comments/history` 时停止，不通过自动补空数组掩盖数据丢失。修复或迁移必须另行核对完整来源，不从本次事故中的 9 项列表推断完整台账。

## 接入与上线

1. 在实际运行机器确认台账位于本地文件系统；找出任务处理、定时提醒、归档、手工维护及恢复脚本的全部写入入口。
2. 暂停这些写入者，保存整个数据目录的取证快照；检查遗留 `.bak` 和事务，核对任务总数、评论及历史。
3. 安装完整技能包（包括脚本和内置日历），升级前备份并保留已有历史日历；相同年度不同内容不得直接覆盖。用 `task_store.py` 的 `validate` 检查现有台账，用 `calendar_manager.py validate --year YEAR` 检查所需日历。有错误先处理；不得初始化覆盖旧台账。
4. 把所有操作接入上述请求接口；查询和导出改用 `read`，提醒逐任务提交 `remind`，归档与重开使用专用操作。技能进入时读取并校验台账，业务写入成功后立即回复；普通会话不执行原生同步、自动计划或轮询。持久台账由已启用后台在现有合法时点合并同步；未启用时说明不会自动更新。仅用户明确要求手动同步、初始化或原生诊断时调用对应入口。原生同步使用自己的固定 `.macos-reminders.lock` 串行化，不在访问原生应用或等待系统授权时持有台账锁；锁文件不可手动删除。
5. 在临时目录执行 `python3 -m unittest discover -s tests -v`（测试自行创建临时台账），通过后在运行环境验证读写入口与权限、备份目录可写。
6. macOS 宿主用 `--dry-run` 核对全量任务及字段映射，用 `--plan` 查看原生差异；首次镜像按已授权的覆盖范围显式执行 `--initialize-mirror`。旧列表快照只保存可读取字段，不能承诺附件等信息无损恢复。核对重建数量、原生标记、重复同步、完成回写及重开保护；存储 `read` 仍可能恢复中断事务。需要周期运行时，按 [原生定时同步](periodic-sync.md) 完成实际后台身份的权限诊断后启用，沿用已配置入口，无需日常重复初始化。随后恢复其他自动化，检查任务集合、备份、提醒回执及错误输出；日常风险提醒仍只读日历，脚本离线。年度日历维护按 [适配器契约](reminder-adapters.md#年度日历维护契约) 独立接入。仍有程序直接覆盖文件时不能视为完成上线。

仅更新技能不能从操作系统层面阻止绕过。若必须使旧脚本或代理完全无法直接写文件，需要把存储进程与调用者权限隔离；本版未部署独立服务。

## 只读状态快照 inspect（1.6.6）

请求 `{"op":"inspect"}` 返回与 `read` 相同的 `ledgers`，但不进入事务恢复或旧备份清理。打开已有安全锁文件进行共享读取，最多等 1 秒；不创建目录、锁或任何状态文件。缺少锁返回 `inspect_unavailable`，锁忙返回 `lock_timeout`，待恢复事务/旧备份返回 `recovery_required`，损坏数据按验证错误报告。调用方应直接报告这些结果，不自动降级为原生检查。`read` 的恢复语义保持不变，业务操作仍使用原有存储入口。
