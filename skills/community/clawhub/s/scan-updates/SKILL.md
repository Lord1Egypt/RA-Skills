---
name: scan_updates
description: Scan registered Gitea or Obsidian Git material sources manually or on a schedule, detect added modified or deleted files, create incremental compilation jobs, and update source fingerprints.
---

# Skill: scan_updates - 资料源增量扫描

## 用途

检查已接入的 Gitea/Obsidian Git 资料源是否有新增、修改、删除文件，并创建增量编译任务。

第一版不做 webhook，支持：

- 每日定时扫描：由 `daily_scan_worker.py` 触发
- 用户手动扫描：私聊机器人要求检查更新

## 触发条件

Activate when:

- 用户说“检查资料源有没有更新”
- 用户说“扫描 repoA / 更新我的 Obsidian 笔记库”
- 定时任务触发每日扫描

Do NOT activate when:

- 资料源尚未完成第一次批量编译
- 用户要新接入资料源，交给 `batch_compile`

## 权限

- 个人资料源：本人可扫描。
- 团队资料源：团队成员可扫描。
- 普通成员不能修改资料源配置。

## 手动扫描流程

OpenClaw 字段映射：

- `SenderId`：触发扫描的人 open_id
- `ChatType`：`direct` 或 `group`
- `GroupSubject`：群聊 chat_id
- `MessageSid`：消息 id，用于审计

群聊手动扫描规则：

- 必须先用 `GroupSubject -> chat_bindings.json -> team_id` 找到当前群绑定团队。
- 群聊未绑定团队：拒绝扫描。
- 群聊只能扫描属于当前绑定团队的资料源。
- 发送者 `SenderId` 必须是该团队成员。

1. 扫描变化：

```bash
python3 scripts/scan_updates.py --source_id <source_id> \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid> \
  --save_to /tmp/paperkb/updates.json
```

2. 把扫描结果保存成 JSON 后创建增量任务：

```bash
python3 scripts/run_incremental.py --source_id <source_id> \
  --updates_file /tmp/paperkb/updates.json \
  --created_by <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid>
```

规则：

- 无变化：回复无更新。
- 变化数 `<= 100`：自动创建 `incremental_compile` job。
- 变化数 `> 100`：创建确认任务，先给用户预览；如果脚本返回 `interactive_card`，优先用飞书互动卡片让用户点击确认或取消。

3. 如果需要确认，用户确认后调用：

```bash
python3 scripts/confirm_incremental.py --task_id <task_id> \
  --confirmed_by <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid>
```

如果用户点击取消，调用：

```bash
python3 scripts/cancel_incremental.py --task_id <task_id> \
  --sender_id <SenderId>
```

收到 scan_updates 卡片按钮回调时，也可以先调用 `resolve_card_action.py --action_value <CardActionValue>`，再按返回的 `command` 和 `args` 执行。

4. 展开增量 job：

```bash
python3 scripts/execute_incremental_job.py --job_id <job_id>
```

该脚本会：

- 标记已删除源文件对应的知识库页面，设置 `source_deleted=true`
- 把新增/修改文档放入 `document_files`
- 把代码/README/依赖变化放入 `code_files`
- 若只有删除/跳过文件，直接完成 job 并写回 fingerprints
- 若仍需语义编译，交给 `batch_compile` 的分批流程继续处理

## 每日扫描

第一版不在代码里自建定时器。需要在 OpenClaw 控制台配置一个定时任务，按固定频率调用：

```bash
python3 scripts/daily_scan_worker.py --threshold 100 --created_by system
```

它会遍历 `sources.json` 中 `enabled=true` 且 `auto_update=true` 的资料源。
如果 `created_by` 不是 `system`，脚本会按用户权限校验是否能扫描该资料源。

代码负责扫描、创建增量 job、记录结果；OpenClaw 控制台负责“几点运行、多久运行一次”。建议第一版配置每日一次，例如每天凌晨或低峰时间运行。

批量编译和增量编译的完成通知不放在 `scan_updates` 里发。另设一个 OpenClaw 控制定时任务调用 `batch_compile/scripts/notify_jobs.py`，发现 `notify_status=pending` 的终态 job 后再发飞书消息并标记 `--mark_sent`。

## 增量处理规则

- 新增文档：生成新 summary。
- 修改文档：按 `source_id + source_path` 覆盖旧 summary。
- 删除源文件：不删除知识库页面，只标记 `source_deleted=true`。
- 代码/README/依赖变化：重新生成整个 codebase 总览。

删除标记也可以单独调用：

```bash
python3 scripts/mark_source_deleted.py --owner <owner> --repo <repo> \
  --source_id <source_id> --source_path "<path>"
```

## 通知

- 个人资料源：通知资料源 owner。
- 团队手动扫描：通知触发者。
- 团队定时扫描：通知团队管理员。

## 脚本清单

- `scan_updates.py`：扫描单个资料源变化
- `chat_context.py`：解析 OpenClaw 群聊上下文和群绑定
- `run_incremental.py`：根据变化数创建确认任务或增量 job
- `resolve_card_action.py`：解析增量扫描卡片按钮
- `confirm_incremental.py`：确认大批量增量更新
- `cancel_incremental.py`：取消待确认的大批量增量更新
- `execute_incremental_job.py`：展开增量 job，处理删除标记和待编译队列
- `daily_scan_worker.py`：每日扫描 worker
- `mark_source_deleted.py`：单独标记某个源文件已删除
- `permissions.py`：校验个人资料源 owner、团队成员和团队管理员权限
- `cards.py`：生成飞书互动卡片 payload
