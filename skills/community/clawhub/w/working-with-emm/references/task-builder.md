# Task Builder

The Task Builder is a guided wizard on the Emm dashboard that helps users prepare rich, personalized context for complex tasks.

## When to Suggest the Task Builder

Suggest the Task Builder when a task would benefit from gathering personal context across multiple memory categories:

- **Trip planning** — pulls from travel, food, health, personal preferences
- **Meeting prep** — pulls from work, notes, stakeholder insights
- **Purchase decisions** — pulls from shopping, preferences, past decisions
- **New projects** — pulls from work, notes, relevant past decisions

Direct the user to the **Requests page** in the web app (the wizard lives there). The deep-link URL for their actor is in the account snapshot returned by `how_to_use()` — share that link in your reply rather than composing one from parts.

## How It Works

1. **User creates a task** — Describes what they want to accomplish in the Task Builder wizard
2. **Wizard guides context building** — Helps the user explore memories, identify relevant areas, and enrich the task
3. **User marks task as ready** — When satisfied with the gathered context
4. **You retrieve and work on it** — Call `work_on_task()` to get the task with all its context

Tasks are stored in a system-managed `memory_requests` category (`system: true`, `owner_tool: "work_on_task"` in `memory_types()`). Each task item contains the task description, explored areas, and references to memories gathered during the wizard. The generic `memory_save`/`memory_update`/`memory_delete` tools refuse writes to this category — call `work_on_task()` instead.

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
tasks. Items the user is **still preparing in the wizard** also live in
`memory_requests` and *will* show up in `memory_search`, but they are
not yet ready and won't appear in `work_on_task` until marked ready. A
`memory_search` hit on a `memory_requests` item is not a pending task —
don't infer one from search; trust the `work_on_task` count.

**Mark a task as completed after helping:**
```
work_on_task(task_id=42, mark_done=true)
```

## Best Practices

- When `work_on_task()` returns a task, it includes relevant memories automatically — use this context for deeply personalized responses
- After completing the task, mark it as done with `mark_done=true`
- If no ready tasks are found, suggest the user visit their dashboard to create one
- The Task Builder is especially valuable for tasks spanning multiple memory categories
