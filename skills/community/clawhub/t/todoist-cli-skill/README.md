# todoist-cli-skill — OpenClaw Skill

![version](https://img.shields.io/badge/version-1.0.4-blue) [![clawhub](https://img.shields.io/badge/🦞_clawhub-1.0.4-blue)](https://clawhub.ai/leaofelipe/todoist-cli-skill)

An [OpenClaw](https://openclaw.ai) agent skill that gives your AI full control over **Todoist** using the [Doist CLI](https://github.com/Doist/todoist-cli) (`@doist/todoist-cli`).

This skill uses the [Official Todoist CLI tool](https://github.com/Doist/todoist-cli) (`td`) — no MCP server or extra infrastructure needed.

## Requirements

- Node.js + npm
- A [Todoist API token](https://todoist.com/app/settings/integrations/developer)

## Installation

**1. Install the CLI:**

```bash
npm install -g @doist/todoist-cli
```

**2. Authenticate:**

```bash
td auth token "your-token-here"
# or export it as an environment variable:
export TODOIST_API_TOKEN="your-token-here"
```

**3. Install this skill** into your OpenClaw agent:

```bash
clawhub install todoist-cli-skill
```

## What Your Agent Can Do

Once this skill is active, your agent understands natural language requests and translates them into `td` commands:

| What you say | What the agent does |
|---|---|
| "What's on my plate today?" | `td today` |
| "Add 'Review PR' to Work, priority 1" | `td task add "Review PR" --project "Work" --priority p1` |
| "Mark the grocery task as done" | finds it, then `td task complete <ref>` |
| "What did I finish this week?" | `td completed --since <date>` |
| "Remind me to call the dentist tomorrow" | `td task add ... + td reminder add ...` |

### Full Feature Coverage

- **Tasks** — view today/upcoming/inbox, add, complete, update, delete, reschedule, move between projects
- **Projects** — list, create, rename, archive, delete
- **Sections** — organize tasks within projects
- **Labels** — create and apply labels for filtering
- **Reminders** — add time-based reminders to any task
- **Comments** — add notes to tasks or projects
- **Activity & Stats** — view recent activity log, karma score, and productivity stats

## Quick Reference

```bash
td today                                         # Due today + overdue
td upcoming 7                                    # Next 7 days
td task add "Buy milk" --due "tomorrow" --priority p2
td task list --filter "p1 & overdue"            # Overdue high-priority tasks
td task complete <ref>                           # Complete a task
td task reschedule <ref> "next monday"           # Reschedule (preserves recurrence)
td stats                                         # Karma + productivity overview
```

## How It Works

The `SKILL.md` file in this package contains the full command reference and behavioral instructions that the OpenClaw agent loads at runtime. When you install this skill, the agent knows which commands to run, how to parse their output, and how to handle edge cases (like recurring tasks, fuzzy name matching, etc.).

## License

MIT-0
