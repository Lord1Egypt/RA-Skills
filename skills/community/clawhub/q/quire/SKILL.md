---
name: quire
description: Read and modify Quire tasks, projects, comments, statuses, and tags via the quire CLI — list, search, get, create, update, complete/uncomplete, set dates, comment.
version: 0.3.1
metadata:
  openclaw:
    requires:
      bins:
        - quire
    emoji: "📋"
    homepage: https://quire.io
---

# Quire

Access to a user's Quire workspace via the `quire` CLI. Reads cover tasks
(list, get, search, subtasks, tree), task comments, projects, project
statuses and tags, and URL resolution. Writes cover creating tasks,
updating task fields, setting/clearing task dates, marking
complete/uncomplete, and posting comments. Use this skill when the user
asks about their Quire tasks, projects, or comments, wants to act on a
Quire URL they've pasted, or wants to mutate a task or post a comment.

Authentication is handled by the CLI's own token store (`quire login` runs an
OAuth loopback flow once per machine). No environment variables or API keys are
needed from the user.

All commands emit raw API JSON when invoked with `--json`. Shape is stable
across CLI versions — safe to depend on.

## When to use this skill

Invoke when the user asks anything along the lines of:

- "What's on my plate today?" / "What am I assigned to?"
- "What tasks are open in project X?"
- "Find tasks tagged Y in org Z that are blocked."
- "Show me the subtree of task #408."
- "Summarize this Quire URL: …"
- "Who's on the Marketing project?"
- "Create a task / update task / set due date / mark complete or re-open /
  post a comment" — the six supported writes are `create_task`,
  `update_task`, `set_task_dates`, `complete_task`, `uncomplete_task`,
  and `add_comment`.

## When NOT to use this skill

- Questions about Notion, Asana, Linear, Jira, Todoist, or any tracker other
  than Quire — even if the phrasing is similar. Pick the skill that matches
  the user's tool, not this one.
- Heavier writes that aren't in this skill's surface yet — deleting tasks
  or comments, attaching files, moving or transferring tasks across
  projects, editing comments, managing tags/statuses/sublists, and
  approval workflows. If asked for one of these, decline politely and
  tell the user it isn't in this skill's surface yet.
- General productivity advice, planning, or coaching with no concrete need
  to read live Quire data.

---

## Tool: whoami

**Use for:** identity grounding — who am I logged in as, and which orgs do I
belong to? Cheap to call; useful at the start of a session to know which org's
projects are reachable.

**Command:**
```bash
quire whoami --json
```

**Output:** a single user object plus an `organizations` array.

```json
{
  "oid": "0e…",
  "id": 12345,
  "name": "Jane Doe",
  "nameText": "Jane Doe",
  "email": "jane@example.com",
  "organizations": [
    { "oid": "0e…", "id": "acme", "name": "Acme Inc.", "nameText": "Acme Inc." }
  ]
}
```

---

## Tool: list_my_tasks

**Use for:** "what's on my plate" — tasks assigned to the signed-in user.
**Exactly one** scope flag is required.

**Command:**
```bash
quire mine [--project <id> | --inbox | --org <id> | --all-orgs] [--skip-inbox] [--limit <n>] --json
```

**Scope flags (pick one):**
- `--project <id>` — one project (slug or OID).
- `--inbox` — the user's private Inbox.
- `--org <id>` — one organization.
- `--all-orgs` — every org the user belongs to. Includes Inbox by default;
  add `--skip-inbox` to exclude it.

**Other flags:**
- `--limit <n>` — positive integer or `no` for unlimited. Default is paged.

**Output:** array of task objects (`oid`, `id`, `name`, `status`, `priority`,
`due`, `assignees`, `tags`, `project`, …).

**Examples:**
```bash
quire mine --all-orgs --json                       # Everything assigned to me
quire mine --project marketing-launch --json       # Just my tasks in one project
quire mine --org acme --limit 50 --json            # First 50 in Acme org
```

---

## Tool: list_project_tasks

**Use for:** all tasks in a specific project (regardless of assignee). Use
this when the user names a project; use `list_my_tasks --project` when they
want only their own tasks in that project.

**Command:**
```bash
quire task list <project-id> [--limit <n>] [--cursor <token>] --json
```

**Args:**
- `<project-id>` — project slug, numeric ID, or OID.

**Flags:**
- `--limit <n>` — positive integer or `no` for unlimited.
- `--cursor <token>` — pass the cursor from a previous page to continue.

**Output:** array of task objects.

**Example:**
```bash
quire task list marketing-launch --json
```

---

## Tool: get_task

**Use for:** full detail on one task — description, custom fields, recurrence,
dates, assignees. Always use this before suggesting a write that the user has
to confirm (e.g. "should I close #408?") so the suggestion is grounded.

**Command:**
```bash
quire task get <id> --json
```

**Args:**
- `<id>` — accepts `#408` (short id, within current project context), a full
  OID, or a full Quire task URL. If the user pasted a URL, `quire resolve` is
  often cleaner — it returns a typed `{kind, resource}` envelope.

**Output:** single task object (raw API shape).

---

## Tool: create_task

**Use for:** creating a new task inside a project (or as a subtask of an
existing task). The user must have named a destination — don't guess a
project. If they only said "add a task to remind me…", ask which project
or offer to put it in their Inbox.

**This is a write.** Restate the task you're about to create — name,
project (or parent task), assignee, due date, priority — and wait for
the user's explicit confirmation before invoking.

**Command:**
```bash
quire task create <project> --name <name> [--description <text>] [--priority <p>] [--due <date>] [--start <date>] [--assignee <user>] [--tag <tag>] [--parent <id>] [--sibling <id>] [--position <before|after>] [--recurrence-freq <freq>] [--recurrence-interval <n>] [--recurrence-byweekday <days>] [--recurrence-until <date>] --json
```

**Args:**
- `<project>` — project OID, slug, or URL. Required even when creating
  a subtask via `--parent` (the parent's project must match).

**Required flag:**
- `--name <name>` — the task name. The only mandatory field.

**Common flags:**
- `--description <text>` — task body.
- `--priority <low|medium|high|urgent>`.
- `--due <date>`, `--start <date>` — `YYYY-MM-DD` or ISO 8601.
- `--assignee <user>` — OID, numeric id, or email. Repeat for multiple.
- `--tag <tag>` — tag name. Repeat for multiple.

**Positioning flags:**
- `--parent <id>` — create as a subtask of this parent task.
- `--sibling <id>` plus `--position before|after` — place the new task
  adjacent to an existing sibling. Use one positioning approach, not both.

**Recurrence flags:** same as `update_task` (`--recurrence-freq`,
`--recurrence-interval`, `--recurrence-byweekday`, `--recurrence-until`).

**Output:** the new task object (same shape as `get_task`).

**Examples:**
```bash
quire task create marketing-launch --name "Draft Q3 announcement" --due 2026-06-01 --assignee jane@acme.com --json
quire task create marketing-launch --name "Write social copy" --parent marketing/#408 --json
quire task create marketing-launch --name "Daily standup notes" --recurrence-freq daily --recurrence-interval 1 --json
```

---

## Tool: update_task

**Use for:** modifying fields on an existing task — renaming, editing
description, changing status or priority, setting/clearing dates, adding or
removing tags, reassigning, managing successors, setting custom-field
values, or configuring recurrence. Pass **only** the flags the user asked
to change; omitted flags leave existing values alone.

**This is a write.** Before invoking, restate the change in plain language
("Change priority of `#408 Launch site` from high to urgent — confirm?")
and wait for the user's explicit go-ahead. If you fetched the task with
`get_task` first to ground the diff, mention what's changing from/to.
Do not chain multiple updates in a single turn without re-confirming.

**Command:**
```bash
quire task update <id> [--name <name>] [--description <text>] [--status <0-100>] [--priority <p>] [--due <date>] [--start <date>] [--add-tag <tag>] [--remove-tag <tag>] [--add-assignee <user>] [--remove-assignee <user>] [--add-successor <id>] [--remove-successor <id>] [--custom-field key=value] [--recurrence-freq <freq>] [--recurrence-interval <n>] [--recurrence-byweekday <days>] [--recurrence-until <date>] --json
```

**Args:**
- `<id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Field flags (pass only what you're changing):**
- `--name <name>` — new task name. Replaces outright.
- `--description <text>` — new description body. Replaces outright.
- `--status <0-100>` — numeric workflow status. `0` = active, `100` =
  complete; projects can define custom statuses in between. If the user
  names a status ("blocked", "in review"), call `list_statuses` first to
  resolve the numeric value. To mark a task complete, prefer
  `complete_task` over `--status 100` — same effect, clearer intent.
  Same for "add a tag" — call `list_tags` first if the user names a
  tag you haven't seen, so you spell it the way the project does.
- `--priority <low|medium|high|urgent>`.
- `--due <date>`, `--start <date>` — ISO 8601 / `YYYY-MM-DD`. Pass the
  literal string `null` to clear a date.
- `--add-tag <tag>` / `--remove-tag <tag>` — repeat for multiple. Tags are
  matched by name within the task's project.
- `--add-assignee <user>` / `--remove-assignee <user>` — accepts OID,
  numeric id, or email. Repeat for multiple users.
- `--add-successor <id>` / `--remove-successor <id>` — manage cross-task
  dependencies (this task blocks `<id>`).
- `--custom-field key=value` — repeat for multiple. `key` matches the
  custom field's name in the task's project.

**Recurrence flags (set together when adding/changing recurrence):**
- `--recurrence-freq <daily|weekly|monthly|yearly>`
- `--recurrence-interval <n>` — positive integer, every N freq-units.
- `--recurrence-byweekday <days>` — comma-separated day numbers `0`–`6`
  (`0` = Sunday). Only meaningful with `--recurrence-freq weekly`.
- `--recurrence-until <date>` — end date for the recurrence.

**Output:** the updated task object (same shape as `get_task`).

**Examples:**
```bash
quire task update marketing/#408 --priority urgent --add-assignee jane@acme.com --json
quire task update marketing/#408 --due null --remove-tag backlog --json
quire task update 0e0123abc --status 30 --due 2026-06-01 --json
```

> If the user is **only** changing dates, `set_task_dates` (below) is a
> smaller-surface alternative — same effect for dates, narrower diff.
> To mark a task done, use `complete_task` (below) rather than
> `--status 100`.

---

## Tool: set_task_dates

**Use for:** setting or clearing **only** a task's `start` or `due` date.
Prefer this over `update_task` when dates are the only change — the diff
is smaller, the safety conversation is shorter, and there's no risk of
accidentally touching other fields.

**This is a write.** Restate the change ("Set due of `#408 Launch site`
to 2026-06-01 — confirm?") and wait for explicit confirmation. Clearing
a date is also a real change worth confirming.

**Command:**
```bash
quire task dates <id> [--start <date>] [--due <date>] --json
```

**Args:**
- `<id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Flags (pass at least one):**
- `--start <date>` — ISO 8601 / `YYYY-MM-DD`, or the literal string
  `null` to clear the start date.
- `--due <date>` — same shape; pass `null` to clear.

**Output:** the updated task object (same shape as `get_task`).

**Examples:**
```bash
quire task dates marketing/#408 --due 2026-06-01 --json
quire task dates marketing/#408 --start null --due null --json
```

---

## Tool: complete_task

**Use for:** marking a task complete. Prefer this over
`update_task --status 100` — same effect, clearer intent.

**This is a write.** Restate the task ("Mark `#408 Launch site` complete
— confirm?") and wait for explicit confirmation. If the user says
something ambiguous like "wrap that up," confirm before assuming they
mean "complete."

**Command:**
```bash
quire task complete <id> --json
```

**Args:**
- `<id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Output:** the updated task object (status now reflects the project's
"complete" state).

**Example:**
```bash
quire task complete marketing/#408 --json
```

> To re-open a completed task, use `uncomplete_task` (below) — the natural
> pair with `complete_task`.

---

## Tool: uncomplete_task

**Use for:** re-opening a task that was previously completed. Resets the
task's status to `0` (active). Natural pair with `complete_task`.

**This is a write.** Restate the task ("Re-open `#408 Launch site` —
confirm?") and wait for explicit confirmation. Re-opening is a real
state change others can see on the task; don't do it silently.

**Command:**
```bash
quire task uncomplete <id> --json
```

**Args:**
- `<id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Output:** the updated task object (status now `0`).

**Example:**
```bash
quire task uncomplete marketing/#408 --json
```

---

## Tool: add_comment

**Use for:** posting a comment on a task. Comments are visible to
everyone with access to the task — treat them as you would a public Slack
message.

**This is a write.** Restate the task and the exact comment text — quote
it verbatim — and wait for explicit confirmation. Don't paraphrase: the
user is on the hook for the wording. If they gave you a summary ("tell
the team the deploy slipped"), draft the comment, show it back, and ask
them to approve or edit before sending.

**Command:**
```bash
quire comment add <task-id> --text <text> --json
```

**Args:**
- `<task-id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Flag:**
- `--text <text>` — the comment body. Plain string works for short
  content. For long content, `--text @/path/to/file.md` reads from disk
  and `--text -` reads from stdin. Newlines and Markdown are preserved.

**Output:** the new comment object (`oid`, `text`, `author`, `created`,
`task`, …).

**Example:**
```bash
quire comment add marketing/#408 --text "Pushing the launch to Monday — Jane is OOO Friday." --json
```

> Comment **editing** (`quire comment update <oid> --text …`) and
> **deletion** (`quire comment delete <oid>`) are not exposed by this
> skill. If asked, decline and point the user at the CLI directly.

---

## Tool: list_task_comments

**Use for:** "what's been said about this task?" Pulls every comment on
a task in chronological order. Use this before drafting a reply with
`add_comment` so the comment lands in context.

**Command:**
```bash
quire comment list <task-id> --json
```

**Args:**
- `<task-id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Output:** array of comment objects (`oid`, `text`, `author`,
`created`, `pinned`, `task`, …). Author is a full user object — refer
to people by `nameText`, not by OID.

**Example:**
```bash
quire comment list marketing/#408 --json
```

---

## Tool: search_tasks

**Use for:** filtered queries — "blocked tasks tagged backend in Acme org",
"high-priority items due this week in project X". Must scope with **one of**
`--project`, `--org`, or `--folder`.

**Command:**
```bash
quire task search <query> ( --project <id> | --org <id> | --folder <id> ) \
  [--mine] [--assignee <user>] [--tag <tag>] [--status <s>] \
  [--priority <p>] [--limit <n>] --json
```

**Args:**
- `<query>` — free-text search string. Pass `""` (empty) if you only want to
  filter, not text-search.

**Scope flags (pick one — required):**
- `--project <id>`
- `--org <id>`
- `--folder <id>` — a folder OID.

**Filter flags:**
- `--mine` — restrict to tasks assigned to the signed-in user.
- `--assignee <user>` — OID, numeric id, or email.
- `--tag <tag>` — tag name.
- `--status <s>` — `active`, `completed`, or numeric `0`–`100`.
- `--priority <p>` — `low`, `medium`, `high`, `urgent`, or `-1`/`0`/`1`/`2`.
- `--limit <n>` — page size.

**Output:** array of task objects.

**Example:**
```bash
quire task search "deploy" --org acme --priority high --status active --json
```

> There is **no `--due` filter.** If the user asks for "tasks due this week",
> fetch with the available filters and then filter by `due` field in your
> own logic (or just summarize what came back).

---

## Tool: get_task_tree

**Use for:** the full subtree under one task — useful when summarizing an
epic or when the user asks about subtasks of subtasks.

**Command:**
```bash
quire task tree <id> [--depth <n>] --json
```

**Flags:**
- `--depth <n>` — positive integer (default `3`) or `full` for unbounded.
  Prefer a small depth (1–3) for chat responses; only ask for `full` if the
  user explicitly wants everything.

**Output:** array of nested tree nodes. Each node has `oid`, `id`, `name`, a
`tasks` array of children, and an optional `cropped: true` flag when the
depth cut off further children.

> For just one level of children (no grandchildren), `list_subtasks` is
> cheaper and easier to summarize.

---

## Tool: list_subtasks

**Use for:** **direct** children of a task only — one level deep, no
grandchildren. Use this when the user asks "what's under #408?" and
doesn't need the recursive tree. Cheaper and easier to summarize than
`get_task_tree` for narrow questions.

**Command:**
```bash
quire task subtasks <id> [--limit <n>] [--cursor <token>] --json
```

**Args:**
- `<id>` — task OID, `project-slug/#408`, or full Quire task URL.

**Flags:**
- `--limit <n>` — page size.
- `--cursor <token>` — pass the cursor from a previous page to continue.

**Output:** array of task objects (same shape as `list_project_tasks`).

**Example:**
```bash
quire task subtasks marketing/#408 --json
```

---

## Tool: list_projects

**Use for:** discovery — "what projects do I have access to?" Filter to one
org when the user has named one.

**Command:**
```bash
quire project list [--org <id>] --json
```

**Output:** array of project objects (`oid`, `id`, `name`, `nameText`,
`organization`, `archived`, …).

---

## Tool: get_project

**Use for:** project-level metadata — owner, description, dates, archived
status, custom-field schema.

**Command:**
```bash
quire project get <id> --json
```

**Output:** single project object.

---

## Tool: list_statuses

**Use for:** resolving a status the user named ("blocked", "in review")
to the numeric value that `update_task --status` accepts. Each project
defines its own workflow statuses between `0` (active) and `100`
(complete) — the numbers aren't standardized across projects, so always
look them up for the specific project before passing a number.

**Command:**
```bash
quire status list <project> --json
```

**Args:**
- `<project>` — project OID, slug, or URL.

**Output:** array of status objects (`oid`, `name`, `value`, `color`, …).
Match by case-insensitive `name`; pass the `value` to `update_task`.

**Example:**
```bash
quire status list marketing-launch --json
```

---

## Tool: list_tags

**Use for:** discovering the tag vocabulary on a project before passing
`--add-tag` / `--remove-tag` (in `update_task`) or `--tag` (in
`create_task`). Tags are matched by exact name, so the user's casual
spelling ("backend") may not match the project's actual tag ("Backend"
or "back-end"). Look up first, spell it the way the project does.

**Command:**
```bash
quire tag list <project> --json
```

**Args:**
- `<project>` — project OID, slug, or URL.

**Output:** array of tag objects (`oid`, `name`, `color`, …).

**Example:**
```bash
quire tag list marketing-launch --json
```

---

## Tool: resolve_url

**Use for:** turning a Quire URL the user pasted into a typed resource
without having to guess what kind of thing it points to. Handles project,
task, chat, document, organization, and user URLs uniformly.

**Command:**
```bash
quire resolve <url> --json
```

**Output:** `{ "kind": "task" | "project" | "chat" | "document" | "organization" | "user", "resource": { … } }`.

After resolving, you typically already have the full object — no follow-up
`get` call needed.

---

## Common pitfalls

1. **Singular subcommands.** The CLI uses `quire task …` and `quire project …`
   (singular), not `tasks`/`projects`. The `mine`, `whoami`, and `resolve`
   commands sit at the top level, not under `task`.
2. **`task list` requires a project argument.** It is not a global "list every
   task I can see" command. For "my tasks across everything", use
   `quire mine --all-orgs --json`.
3. **`task search` requires a scope flag** (`--project` / `--org` / `--folder`).
   Searching with no scope is rejected with a validation error.
4. **No `--due` filter on search.** Fetch then filter the `due` field yourself.
5. **IDs come in three shapes.** Project IDs accept slug, numeric id, or OID.
   Task IDs accept short id (`#408` or `408`), full OID, or full Quire URL.
   When a Quire URL is in hand, prefer `quire resolve` over guessing.
6. **Do not surface opaque OIDs (the `0e…` strings) in user-facing replies.**
   They are internal handles. Refer to tasks by name + short id (`#408`) and
   to projects by name. Use OIDs only when piping back into another CLI call.
7. **One scope at a time on `mine`.** `--project`, `--inbox`, `--org`, and
   `--all-orgs` are mutually exclusive; pick one.
8. **Rate limits exist.** Avoid fan-out loops that call `get_task` over
   hundreds of tasks in a single turn. Prefer `task tree` or `task list` to
   pull many tasks in one request.
9. **Free Quire plans restrict org-wide scope.** `quire mine --all-orgs`,
   `quire mine --org`, `quire task search --org`, and `quire task search --folder`
   return error **469** ("Quire quota exceeded … isn't supported on the free
   plan") when the signed-in user is on a free plan. **Recovery — fan out
   per project, which IS allowed on free:**
   1. Call `list_projects` (no scope) to enumerate every project the user
      can see. This works on free.
   2. If the project count is ≤ 10, call `list_my_tasks --project <id>` for
      each project and concatenate the results. Mention to the user that
      you fanned out because cross-org scope isn't available on their plan.
   3. If the project count is > 10, do **not** fan out blindly — ask the
      user which subset of projects (or which org) to check. Blanket
      fan-out across many projects risks API rate limits.

   Same pattern applies to `task search`: if `--org` / `--folder` is blocked,
   loop the search over `--project <id>` for the projects you care about.

## Authentication failures

If a command exits with an authentication error, tell the user to run
`quire login` once in their terminal — the skill cannot drive that flow
itself (it opens a browser for OAuth). After that completes, retry.

## Reference

- CLI source and docs: <https://github.com/quire-io/quire-cli>
- AI usage recipes: see `AI_GUIDE.md` in the CLI repo for end-to-end pipe
  patterns (weekly digests, triage queues, bulk task creation from notes).
- Quire API docs: <https://quire.io/dev/api/>
