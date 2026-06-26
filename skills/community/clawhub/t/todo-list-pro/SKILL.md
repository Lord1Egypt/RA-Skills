---
name: todo_list
description: Track local todo or work-report items in a SQLite database, including planned work, progress amounts, completion status, deletion, and archiving. Use when Codex needs to add tasks, delete tasks, update progress, list current work, mark work complete, summarize progress, or archive finished or cancelled items for a user.
---

# todo_list

Use this skill to persist local work items instead of keeping them only in chat context.

## Workflow

- Run commands from `{baseDir}/scripts/todo_list.py`.
- Store data in `~/.work_report_summary/todo_list.db` by default.
- Override the database path with `TODO_LIST_DB_PATH` only for tests or when the user explicitly wants a different file.
- Prefer `--json` whenever the command output will be used in a follow-up step.
- Keep completed items visible in active lists until the user asks to archive them.
- Treat archived items as terminal history. Do not update their progress after archiving.
- Use `delete` only when the user explicitly wants permanent removal. Prefer `archive` when the user means "move to history".
- Before running `delete`, ask for one more explicit confirmation from the user. Permanent deletion should be confirmed, not inferred.

## Natural-Language Patterns

Map common user requests to the deterministic CLI instead of keeping task state only in conversation memory.

- Add planned work when the user says things like:
  `帮我记一下今天要做周报`
  `新增一个任务：整理 demo，计划 3 步`
  `记个 todo：修登录页 bug`
- Update progress when the user says things like:
  `这个任务我做了 2 步`
  `把周报进度更新到 60%`
  `这个任务今天先完成一半`
- Mark complete when the user says things like:
  `这个任务做完了`
  `把第 3 个任务标记完成`
  `周报已经完成`
- List or review current work when the user says things like:
  `看看我现在还有什么没做`
  `列出今天的 todo`
  `我有哪些已经完成但还没归档的任务`
- Summarize when the user says things like:
  `汇总一下我今天做了多少`
  `看下整体进度`
  `给我一个当前完成情况`
- Archive only when the user explicitly asks to archive or move finished work into history:
  `把这个任务归档`
  `把已完成任务都归档`
- Delete only when the user explicitly asks to permanently remove a task:
  `把这个任务删掉`
  `永久删除第 3 个任务`
  `这个 todo 不要了，直接删除`
- If the user asks to delete, confirm once more before actually deleting.

When the user does not specify an exact task id, identify the task by title or recent context first, then run the CLI with the resolved id.

## Core Commands

- Add a task:
  `python {baseDir}/scripts/todo_list.py --json add --title "Prepare weekly report" --planned-amount 3 --unit sections --details "Collect wins and blockers"`
- Record progress:
  `python {baseDir}/scripts/todo_list.py --json progress --id 1 --increment 1 --note "Finished the metrics section"`
- Mark a task complete:
  `python {baseDir}/scripts/todo_list.py --json complete --id 1`
- List active tasks:
  `python {baseDir}/scripts/todo_list.py --json list --status active`
- Archive a task:
  `python {baseDir}/scripts/todo_list.py --json archive --id 1`
- Archive by exact title:
  `python {baseDir}/scripts/todo_list.py --json archive --title "Prepare weekly report"`
- Archive all completed tasks:
  `python {baseDir}/scripts/todo_list.py --json archive --all-completed`
- Delete a task permanently:
  `python {baseDir}/scripts/todo_list.py --json delete --id 1 --confirm`
- Delete by exact title:
  `python {baseDir}/scripts/todo_list.py --json delete --title "Prepare weekly report" --confirm`
- Summarize progress:
  `python {baseDir}/scripts/todo_list.py --json summary`

## References

- Read `{baseDir}/references/commands.md` for full CLI shapes and example flows.
- Read `{baseDir}/references/chat_reference.md` for natural-language examples and intent-to-command mapping.
- Read `{baseDir}/references/storage.md` when changing the SQLite schema, default path, or environment-variable behavior.
