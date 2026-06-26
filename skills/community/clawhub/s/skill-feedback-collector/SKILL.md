---
name: skill-feedback-collector
description: Human-in-the-loop MCP feedback collector with task queue. Pauses to collect human input via browser UI before continuing. Use when completing tasks, encountering uncertain parameters, needing user confirmation, working with coding plan subscriptions, or when you should ask instead of guess. Also covers batch task execution via auto-dequeue.
metadata: {"clawdbot":{"emoji":"💬","requires":{"anyBins":["node","npm"]},"install":[{"id":"npm-install","kind":"node","package":"skill-feedback-collector","label":"npm install && npm run build"}],"os":["linux","darwin","win32"]}}
---

# Skill Feedback Collector

Pause the agent and wait for human feedback via a browser-based UI connected through WebSocket. Includes a task queue for batch execution of pre-loaded tasks.

## When to Use

- After completing a task, to let the user verify the result
- When encountering uncertain parameters (colors, layouts, API choices, business logic)
- Before making destructive or irreversible changes that need user confirmation
- When the user prefers interactive confirmation over autonomous execution
- When batch-executing multiple pre-loaded tasks from the queue

## Instructions

Follow these guidelines when this skill is active:

1. After completing a task, call `ask_human_feedback` with a summary and options for next steps. This lets the user decide what to do next rather than ending the session.

2. When unsure about implementation details, call `ask_human_feedback` with your question instead of making assumptions. Getting explicit input leads to better results.

3. The response from `ask_human_feedback` is your next instruction. Execute it, then call `ask_human_feedback` again when done. This creates a productive feedback loop.

4. If the task queue returns a task automatically (queue was non-empty), execute that task and call `ask_human_feedback` again when complete. The queue feeds tasks until empty.

5. Mode switching:
   - User says "free mode" / "自由模式" → call `set_feedback_mode(enabled: false)` to work without pausing
   - User says "feedback mode" / "确认模式" → call `set_feedback_mode(enabled: true)` to resume the confirmation loop

## Best Practices

- Ask the user before ending a session — they may have more tasks
- Confirm before making destructive changes (force push, drop table, delete files)
- If feedback mode is disabled (bypass message returned), continue working autonomously

## Tools

### `ask_human_feedback`

Pauses execution and sends the `reason` to the browser UI. Returns the human's text response. If the task queue is non-empty, the next task is auto-dequeued and returned (with a short delay for UI visibility).

**Parameters:** `reason` (string) — summary of work done and what input you need.

**Example reason format:**
```
Completed: [specific work done]
Changes: [files modified, endpoints added, etc.]

What would you like me to do next?
1. [Option A]
2. [Option B]
3. Something else
```

### `set_feedback_mode`

Toggle feedback confirmation on/off. When off, `ask_human_feedback` returns immediately without pausing.

**Parameters:** `enabled` (boolean)

## Setup

```bash
npm install && npm run build
```

MCP configuration:
```json
{
  "command": "node",
  "args": ["build/index.js"],
  "cwd": "/path/to/skill-feedback-collector"
}
```

Browser UI: `http://<server-ip>:18061`

| Env Variable | Default | Description |
|---|---|---|
| `FEEDBACK_PORT` | `18061` | HTTP and WebSocket port |
| `FEEDBACK_TOKEN` | (empty) | Optional access token for the UI |

## Workflow

```
User message → Agent works → calls ask_human_feedback("Done. Next?")
                                    ↓
                    [Queue has tasks?] → YES → returns next task → Agent continues
                                    ↓ NO
                    [Waits for human input via browser UI]
                                    ↓
                    Human responds → Agent receives → works → calls ask_human_feedback again
                                    ↓
                    ... loop continues until user indicates they are done ...
```

## Security

- Set `FEEDBACK_TOKEN` when deploying on shared or public networks to restrict access
- Use a firewall to limit which IPs can reach the HTTP/WebSocket port
- The server binds to `0.0.0.0` by default for convenience; restrict network access at the OS or firewall level if needed
- Conversation history (`feedback-history.json`) is stored locally in the skill directory; review and rotate if it contains sensitive information
- This skill does not make outbound network requests, download external resources, or execute shell commands

## Tips

- The task queue lets users pre-load multiple tasks for sequential execution
- Users can add tasks to the queue while the agent is working
- HTTP long-polling fallback activates automatically when WebSocket is unavailable
- Browser notifications and sound alerts notify you when the agent has a question
- Conversation history is persisted locally (max 500 entries)
