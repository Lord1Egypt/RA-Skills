# Session Lifecycle

> Load this reference when you need the full rules for `browser_start_session` / `browser_attach_session` / `browser_end_session`, when handling **composite tasks**, or when **analyzing already-open tabs**.

## Why Sessions Are Mandatory

AI agents MUST wrap every **new browser task** with `browser_start_session` / `browser_end_session` — or, when taking over tabs that are **already open**, with `browser_attach_session` / `browser_end_session`. The extension creates a dedicated **Chrome Tab Group** as the AI workspace, isolating the task from the user's other tabs and letting the user review the AI's work after the task ends (the tab group is preserved on `end_session`).

> **Do NOT use `browser_start_session` when the user only wants to analyze already-open tabs.** `browser_start_session` always creates a new tab inside a new Chrome Tab Group — the command does not operate on the tabs the user already has open. For already-open tabs, use `browser_get_tab_content` (content-only) or `browser_attach_session` (deep analysis) instead — see [Analyzing Existing Tabs](#analyzing-existing-tabs).

## Hard Rules

- **Always start with `browser_start_session`** (or `browser_attach_session` when the task must operate on already-open tabs — see [Attaching Existing Tabs](#attaching-existing-tabs-browser_attach_session)), before any other `browser_*` command. Calling other commands without an active session is **forbidden** — it will mix AI-driven tabs with the user's personal browsing.
- **Isolation mode is fixed to `enforce`** and is no longer configurable from the client side — `browser_start_session` does not accept an `--isolation` flag. Every AI task automatically runs in the enforced Tab Group isolation mode.
- **Always call `browser_end_session`** when the task finishes (success, failure, or early exit), so the in-memory mapping is released cleanly.
- **One `sessionId` per task.** Generate a unique, stable ID per task and do **not** reuse it across unrelated tasks. Recommended format: `task-<purpose>-<counter>` (e.g. `task-form-001`, `task-extract-002`). UUIDs or other stable unique strings also work.

## Command Syntax

```bash
browser_start_session --sessionId <id> [--title "<title>"] [--color <color>] [--initialUrl <url>]
browser_attach_session --tabIds "[<tabId1>,<tabId2>]" [--primaryTabId <id>] [--sessionId <id>] [--focus]   # tabIds come from browser_tab_list — see below
browser_end_session --sessionId <id>
```

Optional flags for `browser_start_session`:

| Flag | Default | Notes |
|------|---------|-------|
| `--title` | `"AI: <first 8 chars of sessionId>"` | Shown as the tab group title |
| `--color` | `blue` | One of: `blue`, `red`, `green`, `yellow`, `grey`, `pink`, `purple`, `cyan`, `orange` |
| `--initialUrl` | `about:blank` | Page to open in the first tab |

Example:

```bash
qqbrowser-skill browser_start_session --sessionId task-demo-001 \
    --title "AI: research" --color blue \
    --initialUrl https://www.baidu.com
```

## Attaching Existing Tabs (browser_attach_session)

For tasks that need to interact with tabs that are **already open** (not create new ones), use `browser_attach_session`. It complements `browser_start_session`, which always creates a new tab.

```bash
browser_attach_session --tabIds "[<tabId1>,<tabId2>]" [--primaryTabId <id>] [--sessionId <id>] [--focus]
```

- **Only for interaction** (click / input / scroll / keys). For reading page text, use `browser_get_tab_content` — no session, no activation, no tab switch needed.
- **Prerequisite**: tab IDs cannot be guessed or constructed — you MUST first call `browser_tab_list` to get the `tabId` of the open tabs, then pass those IDs as exact `tabIds` (no fuzzy URL matching).
- `tabIds` (array) takes precedence over `tabId` (single); `primaryTabId` must be within `tabIds`.
- If `sessionId` is omitted, the server generates one (`attach_<timestamp>_<random>`) and returns it in the ack — **carry it in subsequent commands**.
- `focus` defaults to `false` (does not steal user focus). Do **not** pass `--focus` unless the user explicitly asks to switch to the target tab — keeping focus off avoids switching the user away from their current active tab.
- The returned `sessionId` is registered in the daemon exactly like `start_session`, so subsequent business commands automatically carry it.

Typical flow:

```bash
# Step 1: MANDATORY — get the tabIds of already-open tabs (they cannot be guessed)
qqbrowser-skill browser_tab_list

# Step 2: attach the target tabs as the session's interactive target
qqbrowser-skill browser_attach_session --tabIds "[1412805661, 1412805662]" \
    --primaryTabId 1412805661 --sessionId task-attach-001

# Step 3: interact (click / input / scroll / keys) as usual ...
qqbrowser-skill browser_snapshot

# Step 4: end the session like any other task
qqbrowser-skill browser_end_session --sessionId task-attach-001
```

## Idempotency & Recovery

- `browser_start_session` is **idempotent** — calling it twice with the same `sessionId` reuses the existing tab group.
- `browser_end_session` only releases the in-memory mapping; the tab group and its tabs stay open for the user to review.
- If the WebSocket disconnects, the extension auto-ends the session after a ~30-minute grace period, so leaking sessions on crashes is bounded — but AI agents must still explicitly call `browser_end_session`; do not rely on the grace period as the normal exit path.

## Human-in-the-Loop Verification Points

If the site requires CAPTCHA, SMS code, email code, MFA/2FA, QR login, device confirmation, or any other human verification step:

- Pause automation at that point.
- Keep the current session alive.
- Ask the user to complete the verification manually.
- Resume only after the verification step is finished.

Do **not** blindly retry replay or switch branches just because a human verification wall appears.

---

## Handling Composite Tasks

A **composite task** is any user request that contains multiple discrete browser sub-tasks, especially when data must be transformed, summarized, rewritten, or routed between steps.

It may span multiple domains, multiple sites within one workflow, or multiple phases inside the same site/app. Detect it before starting the session and handle it explicitly — do **not** feed the whole request to a single `playbook_list` call.

### Pipeline

1. **Decompose** the request into atomic sub-tasks (one target site, one app phase, or one discrete action each).
2. **Start exactly ONE session for the whole composite task** before the first sub-task. Do **not** start/end a separate session for each sub-task.
3. **For each sub-task independently**, run the sub-task flow: call `playbook_list`, then pick **Branch A** (replay) if a playbook matches, otherwise fall back to **Branch B** (only if the user asked to record) or **Branch C** (one-off manual) — the branch choice is made **per sub-task**, not for the composite as a whole.
4. **Between sub-tasks**, perform AI mediation (summarize, rewrite, transform format). No browser commands are needed in the mediation stage; consume the previous sub-task's output and produce the next sub-task's input variables.
5. **Each Branch A replay runs on its own `browser_replay` invocation** — never chain multiple playbooks inside a single call, and never wrap them in one shared `task_begin` / `task_end` (recording, if any, is also per sub-task).
6. **Report progress after each sub-task completes**, since a composite pipeline can run for many minutes.
7. **End the session once**, after all sub-tasks and mediation are complete.

### `sessionId` Rule for Composites

**One `sessionId` for the whole composite task.** A composite request is a single task — reuse the **same** `sessionId` for every sub-task inside the pipeline, so they share the same Tab Group and the user can review the full workflow in one place. Do **not** open a new session per sub-task.

### Example

```bash
# One session for the whole composite task
qqbrowser-skill browser_start_session --sessionId task-composite-001

# Sub-task A: playbook exists → Branch A (replay)
qqbrowser-skill playbook_list
qqbrowser-skill browser_replay --script ~/.qqbrowser-skill/playbooks/zhihu-article-extractor.json \
  --variables '{"topic": "人工智能", "count": "3"}'

# AI mediation: transform extracted content to target platform style
# (no browser commands here — pure AI processing of Sub-task A's output)

# Sub-task B: playbook exists → Branch A (replay)
qqbrowser-skill playbook_list
qqbrowser-skill browser_replay --script ~/.qqbrowser-skill/playbooks/xiaohongshu-publish.json \
  --variables '{"notes_title": "AI生成标题", "notes_content": "转换后内容"}'

# If Sub-task B had NO playbook, fall back to Branch B / C for that sub-task only
# (still inside the same session).

qqbrowser-skill browser_end_session --sessionId task-composite-001
```
