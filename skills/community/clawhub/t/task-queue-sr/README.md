# TaskQueue — Async Task Queue for AI Agents

When you need your agent to handle multiple tasks in sequence — with retry logic, priority levels, and graceful failure handling.

## The Problem

You say: "Check email, summarize top 3, draft replies, update the board."

What happens: it tries everything at once, loses context halfway through, and the board never gets updated.

## The Solution

TaskQueue manages sequential and parallel task execution:

```javascript
const { TaskQueue } = require('./src/task-queue');

const queue = new TaskQueue({
  maxRetries: 3,
  retryDelay: 5000,
  concurrency: 1  // sequential
});

queue.add({ task: 'Check email', priority: 1 });
queue.add({ task: 'Summarize top 3 emails', priority: 2 });
queue.add({ task: 'Draft replies', priority: 3 });
queue.add({ task: 'Update project board', priority: 4 });

const results = await queue.run();
```

## Features

- **Priority levels** — critical tasks run first
- **Retry logic** — configurable retries with exponential backoff
- **Failure isolation** — one failed task doesn't kill the queue
- **Dependency chains** — "only run Y after X succeeds"
- **Logging** — full execution log with timestamps and durations
- **Pause/Resume** — stop mid-execution, resume later

## Task Status

| Status | Meaning |
|--------|---------|
| `queued` | Waiting to execute |
| `running` | Currently executing |
| `success` | Completed successfully |
| `failed` | Failed after all retries |
| `skipped` | Skipped (dependency failed) |

## Use Cases

- **Morning routine**: email → calendar → weather → briefing
- **Research pipeline**: search → read → summarize → compile
- **Content creation**: outline → draft → edit → format → publish
- **System maintenance**: backup → cleanup → verify → report
---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at . If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
