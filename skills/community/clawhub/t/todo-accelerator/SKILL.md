---
name: todo-accelerator
description: Use when a user needs to add a new task or record a pending to-do item; when prompting an Agent to execute a pending task; during Agent heartbeat events to pick up and work on tasks; when a user expresses interest in a topic for later research, saves a bookmark for processing, or asks for help preparing deliverables. Not for reminders (eating, sleeping, meetings).
---

# To-Do Accelerator

Collaborative task management between users and AI Agents. Agents pick up tasks, work on them, deliver results, and update progress — functioning as teammates with the user. The Obsidian Kanban board serves as the shared communication channel.

## Setup

**Check:** If `todo-accelerator-config.yaml` exists in the agent's workspace → ready to use. If not → follow `initialization.md` in this directory (one-time process).

## Working Scenarios

| Scenario | Agent Action |
|----------|-------------|
| User describes a new task or bookmarks a topic | Ask for missing details (targets, requirements, priority) → `add-todo` |
| Agent heartbeat event | Call `work-on-todo` → process the returned prompt → `commit` when done or blocked |
| User asks to handle a specific task | Call `list-pending` → confirm with user → `work-on-todo --name "..."` → `commit` |

## Commands

**Base command** (referred to as `<CMD>` below):

```
python3 <skill-dir>/scripts/todo.py --config <workspace>/todo-accelerator-config.yaml
```

Replace `<skill-dir>` with the absolute path to this skill's directory, and `<workspace>` with the agent's workspace directory.

### add-todo

Create a new to-do with a companion note, added under "Ideas".

```bash
<CMD> add-todo --name "title" [--targets "outcome1" "outcome2"] [--requirements "req1" "req2"] [--priority N] [--allow-subagent | --no-allow-subagent] [--assigned-agent "agent-id"]
```

**Example:**

```bash
<CMD> add-todo --name "Research AutoResearch" --targets "Summary of features and setup guide" --requirements "Read the README" "Try running the demo" "Write up findings" --priority 1
```

**Do not guess parameters.** If the user hasn't specified targets or requirements, ask them:
- "What outcome do you expect from this?"
- "Are there specific sub-tasks or questions to address?"
- "Should this be prioritized? (0 = normal, higher = more urgent)"

### work-on-todo

Pick up the highest-priority to-do from Ideas and prepare it for processing.

```bash
<CMD> work-on-todo
<CMD> work-on-todo --name "specific todo"
```

**Example:**

```bash
<CMD> work-on-todo --name "Research AutoResearch"
```

**Behavior:**
- Without `--name`: auto-selects by priority (highest first, random among ties)
- With `--name`: works on that specific to-do (confirm exact name with user first)
- If the selected to-do has no unchecked requirements → moves it to 审阅中 and skips (no action needed)
- Otherwise → moves card from Ideas to 推进中, increments iteration count, and returns a structured prompt

After `work-on-todo` returns, follow the instructions in `references/processing-work-on-todo.md`.

### commit

Check off completed requirements and finalize the current round of work.

```bash
<CMD> commit --name "todo name" --completed "requirement 1" "requirement 2"
```

**Example:**

```bash
<CMD> commit --name "Research AutoResearch" --completed "Read the README" "Try running the demo"
```

Each `--completed` string must **exactly match** an unchecked requirement in the note's "What's More" section. If any string doesn't match, the script returns an error with the remaining unchecked requirements — re-examine and pass the exact strings.

The script moves the card to 审阅中 after committing.

### list-pending

List all to-dos under "Ideas" with their priority levels.

```bash
<CMD> list-pending
```

**Example:**

```bash
<CMD> list-pending
```

## Note Structure

Each to-do has a companion `.md` note. For YAML frontmatter properties, see `references/note-yaml-properties.md`.

| Section | Purpose | How to update |
|---------|---------|---------------|
| **What's More** | Requirements checklist (`- [ ]` / `- [x]`) | Managed via `commit` command |
| **Target** | Final results and deliverables | Write directly in the note |
| **Investigation and Problems** | Ongoing findings, progress notes, obstacles | Write directly in the note |

## Case Studies

See `references/case-study.md` for detailed usage examples covering the full lifecycle.
