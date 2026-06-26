# Natural-Language Reference

Use this file when the user expresses todo actions in conversational Chinese or mixed Chinese-English phrasing.

## Intent Mapping

### Add Task

User phrasing:

- `帮我记一个 todo：写周报`
- `新增任务，明天做发版检查`
- `记录一下我要做登录页联调`

Map to:

- `add --title ...`
- Add `--planned-amount` and `--unit` when the user gives an amount such as `3 步`, `2 个模块`, `4 小时`
- Add `--details` when the user gives extra context

### Update Progress

User phrasing:

- `这个任务做了 2 步`
- `周报现在完成 1/3`
- `把 demo 任务进度改成 80%`
- `我今天又推进了一点`

Map to:

- Prefer `progress --increment ...` when the user describes newly completed work
- Prefer `progress --done-amount ...` when the user gives the new total completed amount
- Add `--note` when the user includes a short status note

If the user only says `推进了一点` without a measurable amount, ask for the missing amount unless there is already a clear unit convention in context.

### Complete Task

User phrasing:

- `做完了`
- `这个已经完成`
- `把任务 2 标记完成`

Map to:

- `complete --id ...`

### List Current Work

User phrasing:

- `看看还有什么没做`
- `列出当前任务`
- `我现在有哪些 active todo`

Map to:

- `list --status active`

### Show Completed Or Archived Work

User phrasing:

- `看下已经完成的任务`
- `把归档过的列出来`
- `我历史任务有哪些`

Map to:

- `list --status completed`
- `list --status archived`
- `list --status all`

### Summary

User phrasing:

- `汇总一下现在做了多少`
- `看整体进度`
- `给我一个完成情况统计`

Map to:

- `summary`
- `summary --include-archived` only when the user explicitly wants historical totals

### Archive

User phrasing:

- `把这个归档`
- `归档第 4 个任务`
- `把做完的移到历史`
- `把“周报”这个任务归档`
- `把已完成任务都归档`

Map to:

- `archive --id ...`
- `archive --title ...`
- `archive --all-completed`

Archive is explicit. Do not auto-archive immediately after completion unless the user asks.

### Delete

User phrasing:

- `把这个任务删掉`
- `删除第 3 个任务`
- `这个 todo 不要了，永久删除`

Map to:

- `delete --id ... --confirm`
- `delete --title ... --confirm`

Delete is permanent. Prefer `archive` when the user says `归档`, `移到历史`, or otherwise implies retention.
Before deleting, ask for one more explicit confirmation.

## Resolution Rules

- Prefer exact task ids when the user provides them.
- Otherwise resolve by exact title match first.
- If multiple active tasks match the same phrase, ask a narrow follow-up instead of guessing.
- Keep completed tasks in active views until archive is explicitly requested.
