---
name: workday-mcp
description: Read your Workday HR data — tasks, pay, benefits, compensation — via MCP through your own signed-in session. Triggers on phrases like "check my workday", "what's in my workday", "read my workday compensation", "my workday benefits", "pull this workday page", or any request involving your Workday tasks, pay, or benefits. Read-only. Requires workday-mcp installed and the fetchproxy extension active (see Setup below).
---

# workday-mcp

Read-only MCP server for Workday. Fetches your Workday tasks and data cards
(pay, benefits, compensation) and returns them as structured JSON. Every request
routes through your own signed-in `*.myworkday.com` tab via the fetchproxy
browser extension, reusing your existing SSO-authenticated session.

- **npm:** [npmjs.com/package/workday-mcp](https://www.npmjs.com/package/workday-mcp)
- **Source:** [github.com/chrischall/workday-mcp](https://github.com/chrischall/workday-mcp)

> ⚠️ Workday does not give employees a personal API. This server reads the same
> internal `*.htmld` endpoints the Workday web app calls, dispatched through your
> own signed-in browser tab via the fetchproxy extension. It is **read-only** and
> touches only your own data. Check your employer's acceptable-use policy. Use at
> your own discretion.

## Setup

### 1. Install workday-mcp

`.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "workday": {
      "command": "npx",
      "args": ["-y", "workday-mcp"],
      "env": {
        "WORKDAY_TENANT": "your-tenant-slug",
        "WORKDAY_HOST": "wd5.myworkday.com"
      }
    }
  }
}
```

- `WORKDAY_TENANT` (**required**) — the path segment after the host, e.g. for
  `https://wd5.myworkday.com/acme` it is `acme`.
- `WORKDAY_HOST` (optional) — your data-center host; defaults to `wd5.myworkday.com`.
- `WORKDAY_WS_PORT` (optional) — override the fetchproxy port (default 37149).

### 2. Install the fetchproxy extension (one-time, shared across fetchproxy MCPs)

```bash
git clone https://github.com/chrischall/fetchproxy
cd fetchproxy
npm ci
npm --workspace=@fetchproxy/extension-chrome run build
```

Load `fetchproxy/packages/extension-chrome/dist` as an unpacked extension in
`chrome://extensions`. On the first request you'll be asked to approve a pairing
code in the extension popup (one-time, per server identity).

### 3. Sign into Workday

Open `https://<host>/<tenant>` in your browser and complete SSO. workday-mcp
reuses that live session — there is no separate login.

## Tools

- **`workday_get_apps`** — list your Workday apps (Personal Information, Benefits
  and Pay, Directory, Total Rewards, …), each with a launchable task id. The
  discovery entry point.
- **`workday_get_task`** — read a Workday task or data card. Returns title,
  current user, each section's `label`/`value` fields, navigable `references`
  (instance ids + drill-in uris), related tasks, and export links. Accepts a
  **bare task id** (e.g. `2998$43525`, from `workday_get_apps`), a prior result's
  `references[].uri`, or the pasted URL of a Workday page you have open (a
  `/{tenant}/d/...` SPA URL is normalized to its data endpoint automatically).
- **`workday_healthcheck`** — verify the bridge + session end-to-end and get a
  plain-English hint distinguishing "bridge down" from "extension not connected"
  from "Workday session expired (re-sign-in)".

## How navigation works

Start with `workday_get_apps`, pass an app's `taskId` to `workday_get_task`, then
follow the `references[].uri` it returns into deeper data. Some apps share a
generic launcher id and open to a near-empty page — for those (and for any rich
data card), open the page in your browser and paste its URL into
`workday_get_task`, since Workday data-card paths carry opaque, page-context-bound
tokens that can't be constructed.

## Status

v1 is **read-only**. Typed pay/benefits/compensation tools, inbox/search (Workday
serves these via GraphQL), and (later) `confirm`-gated writes are planned — see
`docs/WORKDAY-API.md`.
