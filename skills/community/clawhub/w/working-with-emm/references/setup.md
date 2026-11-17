# Setup Guide

Only needed on first use or after losing credentials. Skip if memory tools are already working.

## Requirements

- **OpenClaw users**: mcporter must be installed (`npm install -g mcporter`)

## Option A — Platform-managed MCP (Claude.ai, ChatGPT, etc.)

Configure the MCP server directly in your AI platform's settings:

- **MCP endpoint:** `https://ai.actingweb.io/mcp`
- **Auth:** OAuth 2.0 (Google sign-in)

Follow your platform's guide for adding an MCP server, then sign in when prompted.

## Option B — mcporter (CLI agents, OpenClaw, custom setups)

**1. Install mcporter**

```bash
npm install -g mcporter
```

**2. Register the Emm AI server**

```bash
mcporter config add emm https://ai.actingweb.io/mcp --auth oauth
```

**3. Authenticate**

```bash
mcporter auth emm --log-level debug
```

This opens a browser for Google OAuth. If it succeeds, skip to step 4.

**If authentication fails** (common in headless or GUI-less environments — the session closes before the browser callback completes):

The debug output prints a line like:
> `If the browser did not open, visit https://...`

Copy that URL. Then run the helper script from the skill's `scripts/` directory — it handles the full PKCE flow, starts a local callback server, and writes the token to mcporter's vault automatically:

```bash
bash scripts/manual-oauth.sh
```

Requirements for the script: `curl`, `python3`, `node`, `openssl`, `mcporter`.

**4. Verify**

```bash
mcporter list emm --schema
```

Should list the available memory tools. You're done.

Note: `manual-oauth.sh` above assumes a CLI agent with local filesystem access
(it writes the token to mcporter's vault). It doesn't apply to platform-managed
clients (Claude.ai, ChatGPT) — use Option A there.

## Emm unreachable, or a tool call fails with an auth error

Work through in order:

1. **Is the server connected at all?** Call `status()`. If it errors or the
   tool isn't in your loaded tool list, the connector isn't configured or
   isn't enabled for this conversation — see Option A or B above.
2. **Is the auth still valid?** An expired or revoked OAuth session fails
   tool calls with an auth error even though the connector still shows as
   configured. Re-run the platform's connect/authenticate step (Option A) or
   `mcporter auth emm --log-level debug` (Option B).
3. **Test the connector independently of your current task.** `mcporter list
   emm --schema` (Option B) or a bare `status()` call (either option) isolates
   whether the problem is the connection itself or something about the
   specific call you were making.
4. **Tool names are case-sensitive.** `Memory_Search` or `memorySearch` will
   not resolve — use the exact name from your loaded tool list
   (`memory_search`, lowercase with underscores).

If all four check out and the call still fails, see
[error handling during a run](mission-control.md#error-handling-during-a-run)
for the structured-envelope codes.
