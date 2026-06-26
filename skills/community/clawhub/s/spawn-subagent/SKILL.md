---
name: spawn-subagent
description: "Spawn isolated subagents to handle long-running, complex, or blocking tasks without stalling the main session. Use when: a task will take more than 30 seconds, involves multiple sequential steps, requires heavy file processing, could block the main session, or when parallelism would speed things up. Prevents the main agent from getting stuck on slow operations."
---

# Spawn Subagent Skill

## Minimum Model
Any model. Task delegation doesn't require complex reasoning.

---

## When to Spawn vs. Stay in Main Session

**Spawn a subagent when:**
- Task takes >30 seconds.
- Task has many sequential steps (research → draft → send → log).
- Task could fail and block the main session.
- Multiple independent tasks can run in parallel.
- Owner wants results "when ready," not now.

**Stay in main session when:**
- Task takes <10 seconds.
- Task needs back-and-forth with the owner.
- Task needs the current conversation context.

---

## How to Spawn

### Basic Spawn

```python
sessions_spawn(
    task="[Detailed task description here]",
    mode="run",             # "run" = one-shot task
    runtime="subagent",
    runTimeoutSeconds=300   # Kill after 5 min if still running
)
```

### With Custom Model (for expensive reasoning tasks)

```python
sessions_spawn(
    task="[Complex analysis task]",
    mode="run",
    runtime="subagent",
    runTimeoutSeconds=300,
    # Use a capable model only when the task needs it
    model="your-provider/your-capable-model"
    # Examples: "anthropic/claude-opus-4-6", "openai/gpt-4o", "google/gemini-1.5-pro"
)
```

---

## Writing Good Task Descriptions

A good task description has 4 parts:

1. **What to do** — specific actions
2. **Where inputs are** — file paths, env vars, API endpoints
3. **What to output** — exact format and save location
4. **What "done" looks like** — clear completion signal

### Good Example

```
Read all .md files in /tmp/reports/
Summarize each in 2–3 sentences
Save all summaries to /tmp/reports/summary.md — one section per file
Print "DONE: X files summarized" when finished
Do not modify the original files
```

### Bad Example

```
Summarize the reports
```
*Too vague — subagent won't know where files are or what to do with results.*

---

## Common Patterns

### Batch Processing

```python
# Spawn one subagent to process all items — not one per item
sessions_spawn(
    task="""
    Process each item in /tmp/items.json:
    1. Read the file
    2. For each item: [describe action]
    3. Save results to /tmp/results/ as one file per item (item_ID.json)
    4. Print "DONE: X items processed"
    """,
    mode="run",
    runtime="subagent",
    runTimeoutSeconds=300
)
```

### Research + Draft

```python
sessions_spawn(
    task="""
    1. Search the web for: [topic]
    2. Summarize the top 5 results in bullet points
    3. Draft a 3-paragraph briefing in plain language
    4. Save the draft to /tmp/briefing.md
    5. Print "DONE" when finished
    """,
    mode="run",
    runtime="subagent",
    runTimeoutSeconds=180
)
```

### Parallel Independent Tasks

```python
# Both spawn at the same time — runs faster than sequential
sessions_spawn(
    task="Fetch latest emails. Save to /tmp/emails.json. Print DONE.",
    mode="run", runtime="subagent", runTimeoutSeconds=60
)
sessions_spawn(
    task="Get today's calendar events. Save to /tmp/calendar.json. Print DONE.",
    mode="run", runtime="subagent", runTimeoutSeconds=60
)
# Wait for both completion events, then read both files
```

### PA Daily Briefing (Non-Blocking)

```python
sessions_spawn(
    task="""
    Generate the daily morning briefing:
    1. Get calendar: GOG_ACCOUNT=owner@company.com gog calendar events primary --from TODAY --to TOMORROW
    2. Get emails: GOG_ACCOUNT=owner@company.com gog gmail search 'is:unread newer_than:1d' --max 5
    3. Format as plain text (use CAPS for section titles, no markdown headers)
    4. Save to /tmp/morning-briefing.txt
    5. Print DONE
    """,
    mode="run",
    runtime="subagent",
    runTimeoutSeconds=120
)
# Main session stays free. Read /tmp/morning-briefing.txt when done, then send it.
```

---

## Handling Completion

**Do not poll.** Wait for the push-based completion event.

When the completion event arrives:
1. Read the output file the subagent created.
2. Use the results in the main session.
3. Reply with `NO_REPLY` if the owner doesn't need a response.

---

## Failure Handling

If a subagent times out or fails:
1. Log the failure: append to `.learnings/ERRORS.md`.
2. Notify owner if the task was time-sensitive.
3. Retry with a simpler, more explicit task description.
4. If still failing → run in the main session as a fallback.

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---|---|
| Poll with sessions_list in a loop | Wait for push-based completion events |
| Spawn for a 5-second task | Run quick tasks in main session |
| Use vague task descriptions | Be explicit about inputs, outputs, file paths |
| Spawn without a timeout | Always set `runTimeoutSeconds` |
| Ignore subagent failures | Check for error events and handle them |
| Spawn a subagent from inside a subagent | Keep delegation to one level |

---

## Cost Tips

- **Cheaper:** Use small models for batch/shell operations — spawn with `model="provider/small-model"`.
- **Larger models only for:** Complex reasoning, code generation, analysis.
- **Avoid:** Do not spawn many subagents simultaneously — they compete for resources.
- **Batch:** One subagent processing 100 items is cheaper than 100 subagents with 1 item each.
