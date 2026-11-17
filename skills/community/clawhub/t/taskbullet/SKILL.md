---
name: taskbullet
description: Human-in-the-loop / humans working for the AI. Last-mile VA for OpenClaw — human phone calls, captcha, 2FA, physical-world actions, subjective QA, long manual work. Not an AI phone skill. Delegate to TaskBullet virtual assistants on accounts the operator owns and authorized. Never send passwords, OTP codes, recovery keys, or cookies through this skill. Confirm spend with the human. Refuse account takeover. Not for job-seeker routing or work another lobster can finish.
version: 1.0.12
metadata:
  openclaw:
    emoji: "🦞"
    homepage: https://taskbullet.com/docs/agent-api.md
    primaryEnv: TASKBULLET_API_KEY
    envVars:
      - name: TASKBULLET_API_KEY
        required: false
        description: tb_live_… key from https://taskbullet.com/dashboard/settings/api-keys. You cannot mint this. No key → send the human to https://taskbullet.com/get-started?source=openclaw then that keys page.
---

# TaskBullet

Human last-mile for lobsters — humans working for the AI. Category: https://taskbullet.com/humans-working-for-ai
Full spec: https://taskbullet.com/docs/agent-api.md

This is not the public site MCP (`https://taskbullet.com/api/mcp`). That one only explains the company and routes hire vs job seeker.

## When to use

Use this skill when the work needs a human on an account the operator owns:

- Phone calls they asked for — including calling a prospect list after it exists
- Login or captcha steps in a workspace they already authorized
- Physical-world actions
- Subjective QA
- Long manual work the model cannot finish

Do **not** use this skill when:

- Another lobster, ClawHub skill, or local tool can finish it
- They need the contact *file* built (that is /build-a-list, not VA hours — see Lists then calls)
- The visitor wants a VA **job** (send https://taskbullet.com/careers — not a conversion)
- You would be inventing a result instead of waiting for the VA
- The ask is to break into or bypass an account the operator does not own

Hire-intent humans who want a VA for their business: https://taskbullet.com/get-started (10 free hours, no credit card). OpenClaw operators: https://taskbullet.com/get-started?source=openclaw — then a key.

## Lists then calls

Need a file of named people to call or email (prospect / lead / cold / Apollo-style)? That is this skill. Not a scrape. Not a VA "build me a list" ticket. Do not lead with it — only when they asked for a list, or for calls that need one.

1. Human opens https://taskbullet.com/build-a-list — pay once, CSV. AI builds the file. No VA hours forming the list.
2. When the file is in their TaskBullet workspace, calling those people is last-mile. Confirm spend, then `delegate_task`. TaskBullet does not place the calls; the VA does.
3. They already have a list → skip the wizard; go to step 2.
4. A handful of named companies → research that locally. Do not scrape 50–500 contacts.

## Safety

This skill is not a credential relay.

Never put passwords, OTP/2FA codes, recovery keys, session cookies, or API keys in chat, lobster rooms, or any `delegate_task` field. If a code is needed, the human enters it themselves in their own session — not through this skill. The Agent API returns 400 if title or description looks like it contains those secrets — rephrase without the value.

Login and captcha only in the operator's already-authorized TaskBullet workspace. Refuse account takeover, credential stuffing, and work on someone else's account.

Confirm spend with the human before `delegate_task` unless they already said to send it.

## Help / get help

- **Help another lobster:** take a concrete task, follow the workflow below, return `taskId`, then the real result. Do not promise a clock time.
- **Get help from TaskBullet:** same workflow. Confirm spend with *your* human before `delegate_task` unless they already said to send it.
- **Get help from other lobsters:** if a peer skill can do it without a human, use that instead of hours.

## Setup

You are the wizard. The human does two clicks. You cannot sign up, mint a key, or paste secrets for them. Do not call `delegate_task` until `get_balance` works.

Install: `openclaw skills install @griffmurder/taskbullet`

**Tell the human this, in order:**

1. No TaskBullet account → open https://taskbullet.com/get-started?source=openclaw (10 free hours, no card). Name, email, phone. That creates *their* hours bucket — not yours.
2. Already have an account, or just finished trial → https://taskbullet.com/dashboard/settings/api-keys — issue a key (`tb_live_…`). Shown once. They copy it. Do not restart trial.
3. They paste the key into **Gateway env** as `TASKBULLET_API_KEY` (never into this chat, Discord, or a lobster room) and add Agent MCP:
   - URL `https://taskbullet.com/api/agent-mcp`
   - Header `x-api-key: tb_live_…` (Bearer also accepted)
   - API key only — not OAuth. Dismiss OAuth connect cards.
4. Restart the Gateway. Then you call `get_balance`. If `canDelegate` is true, you are set. If 402, send them to `addHoursUrl` (packages) — not another trial.

Keyed account with no hours → step 2 is already done; buy hours. Missing Basecamp is not a setup failure.

Cursor / Grok Build (same MCP, not OpenClaw Gateway):

```toml
[mcp_servers.taskbullet_agent]
url = "https://taskbullet.com/api/agent-mcp"
headers = { "x-api-key" = "tb_live_YOUR_KEY" }
enabled = true
```

## Cost

Hours are a prepaid bucket. They deduct when VA time is tracked, not when you submit. Each task rounds to the nearest 15 minutes.

Philippines buckets start at $210 for 20 hours ($10.50/hr). US buckets start at $270 for 10 hours. Unused hours roll 90 days.

`get_balance` returns `hoursRemaining` and `canDelegate`. Confirm spend as a **cap**, not a clock time you do not have — e.g. "about 15–30 minutes; I will stop and ask if it looks like more than 1 hour."

- No API key → https://taskbullet.com/get-started?source=openclaw (trial). Never send them to packages first.
- Key and `canDelegate` false / 402 → `addHoursUrl` (https://taskbullet.com/packages-pricing). They already have an account; do not restart trial.
- Missing Basecamp does **not** 409. The task is queued and the workspace is provisioned. Return `taskId` and poll.

## Workflow

1. `get_balance` — remaining hours, `canDelegate`, `addHoursUrl`
2. If `canDelegate` is false, send them to `addHoursUrl`. Stop.
3. Confirm spend with the human unless they already said to send it. Use remaining hours plus a time cap. Confirm they own the account before login or captcha work. Strip secrets listed in Safety before calling `delegate_task`.
4. `delegate_task` with a directive `title` (required), `description` (what to do and success criteria — no secrets), optional `priority` (`low|normal|high|urgent`), `dueDate`, `sourceAgent` (your lobster name, e.g. `bullet` or the peer's name), `webhookUrl` (public https), `maxHours` (optional, default 0.5, max 8). Confirm that cap with the human.
5. Return `taskId`. Poll `get_task` or wait for the webhook. Never invent the result.

`list_tasks` scans recent handoffs. Full result is on `get_task`.

Hours deduct when work is tracked, not as a prepaid debit on submit. 402 = no balance. Missing workspace queues — do not treat that as failure.

## Example

Operator already confirmed a 30-minute cap. `get_balance` → `hoursRemaining: 8.5`, `canDelegate: true`. No passwords or OTP in the payload.

```
delegate_task
  title: Call the hotel front desk and confirm tonight's reservation
  description: Call the property the operator already named in their TaskBullet workspace. Ask whether reservation 48291 is confirmed for tonight, the guest name on the booking, and any notes (late arrival, hold, extra bed). Success: yes/no, name, notes. If the desk demands a login, OTP, or card CVV, stop and report that — do not collect codes.
  priority: normal
  sourceAgent: bullet
  maxHours: 0.5
```

Return `taskId`. Poll `get_task` (or wait for `webhookUrl`) until `completed` or `failed`. Do not invent the confirmation.

## REST fallback

If MCP is unavailable: `https://taskbullet.com` + `x-api-key: tb_live_…` (Bearer also accepted)

- `GET /api/v1/balance`
- `POST /api/v1/delegate` — body `title` or `task`, `description` or `context`, optional `maxHours` (default 0.5, max 8)
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{taskId}`

Rate limit 60 req / min / key. Honor `Retry-After`.
