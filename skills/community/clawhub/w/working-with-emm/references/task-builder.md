# Task Builder

The Task Builder is a guided builder on the Emm dashboard that helps users prepare rich, personalized task prompts for complex tasks.

## When to Suggest the Task Builder

Suggest the Task Builder when a task would benefit from gathering personal context across multiple memory categories:

- **Trip planning** — pulls from travel, food, health, personal preferences
- **Meeting prep** — pulls from work, notes, stakeholder insights
- **Purchase decisions** — pulls from shopping, preferences, past decisions
- **New projects** — pulls from work, notes, relevant past decisions

Direct the user to the **Tasks page** in the web app (the builder lives there). The deep-link URL for their actor is in the account snapshot returned by `how_to_use()` — share that link in your reply rather than composing one from parts.

## How It Works

1. **User describes the task** — One statement of what they want to accomplish
2. **Builder offers optional enhancements** — Add facts and preferences, weave in relevant memories and documents, adapt the prompt to the agent that will run it (including the user's own saved custom adaptation rules), get improvement suggestions; every change is reviewed and explicitly accepted by the user
3. **User may pick a Target agent** — An optional intended runner (Claude / ChatGPT / Cursor / a generic agent), drawn from the agent types among their connections
4. **User marks task as ready** — When satisfied with the curated prompt
5. **You retrieve and work on it** — Call `work_on_task()` to get the task; the user-curated prompt is the authoritative description of what they want

Tasks are stored in a system-managed `memory_requests` category (`system: true`, `owner_tool: "work_on_task"` in `memory_types()`). Each task item carries the user-curated task prompt (with any context the builder wove in). The generic `memory_save`/`memory_update`/`memory_delete` tools refuse writes to this category — call `work_on_task()` instead.

## Using work_on_task()

**Retrieve the next ready task:**
```
work_on_task()
```

**Retrieve a specific task by ID:**
```
work_on_task(task_id=42)
```

**List all ready and completed tasks:**
```
work_on_task(list_only=true)
```

`work_on_task(list_only=true)` is the authoritative source of ready
tasks. Items the user is **still preparing in the builder** also live in
`memory_requests` and *will* show up in `memory_search`, but they are
not yet ready and won't appear in `work_on_task` until marked ready. A
`memory_search` hit on a `memory_requests` item is not a pending task —
don't infer one from search; trust the `work_on_task` count.

**Tasks are leased when handed out.** Retrieving a task claims it for 60
minutes, so two runs of the cycle working the queue at the same time get
*different* tasks instead of both doing the same one. You don't manage
this — the server does it on every hand-out, whether or not you ask.

(It narrows the window rather than sealing it: two requests arriving at the
very same instant can still both be given the task. What it removes is the
old behaviour, where the queue handed the same task to every run that asked.)

What you will notice:

- `work_on_task()` skips tasks another run is currently holding, and
  returns "no ready tasks" if every ready task is claimed. That is not the
  queue being empty; it means someone else is on them.
- `work_on_task(list_only=true)` still lists a claimed task as `ready` —
  it *is* ready, just taken — and flags it with `claimed: true`.
  `has_ready_task` counts only unclaimed ones, so it always matches what a
  retrieve would actually hand back.
- `work_on_task(task_id=42)` overrides the lease: you asked for that task
  by name, so you get it and the claim moves to you. Use it when the user
  names a task, not to jump a queue.
- A claim lapses after 60 minutes, so a task whose run died returns to the
  pool on its own. `mark_done=true` releases it immediately.

**Intended agent (advisory).** Tasks may carry an intended target. The
list view shows it per task (`target_agent`, e.g. "— intended for
Claude"), and a retrieved task's brief declares it as
`**Intended agent:** <label>`. Compare the declared key against your own
`you_are.agent_type` from `status()` — all Claude surfaces classify to
`claude`, so any Claude connection matches a Claude-targeted task. A
mismatch never blocks you: mention that the task was intended for the
other agent in your output, and proceed if the user wants you to handle
it.

**Mark a task as completed after helping:**
```
work_on_task(task_id=42, mark_done=true)
```

## Best Practices

- When `work_on_task()` returns a task, it includes relevant memories automatically — use this context for deeply personalized responses
- After completing the task, mark it as done with `mark_done=true`
- If no ready tasks are found, suggest the user visit their dashboard to create one
- The Task Builder is especially valuable for tasks spanning multiple memory categories
