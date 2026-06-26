---
name: safeclaw-proxy
description: Install and verify the SafeClaw safety proxy for OpenClaw and other OpenAI-compatible clients. Use when setting up a local or hosted SafeClaw proxy, routing model traffic through it, debugging why calls are not appearing in the dashboard, or adapting setup for OpenClaw provider configs, agent models.json, or shell-launched clients.
---

# Setup SafeClaw Proxy

Set up SafeClaw end to end. Use exec for commands. Report progress after each completed step. Stop only for real blockers.

Default to doing the work yourself. Ask the user only when you truly need one of these:
- a choice between local and hosted mode
- a secret or URL you cannot read yourself
- a permission boundary you cannot cross
- a restart or relaunch the user must perform outside your control

Prefer direct config edits, file edits, and process control over telling the user to type commands manually.

**Success condition:**
1. SafeClaw is running and its health endpoint responds.
2. At least one real client path is pointed at the proxy.
3. A test call passes through the proxy.
4. The user understands which traffic will and will not appear on the dashboard.

## Step 0: Inspect how this OpenClaw install actually routes model traffic

Do this before changing anything.

1. Read the active model situation instead of assuming `models.providers.openai` exists.
2. Check all of these, in order:
   - `gateway config.get`
   - `~/.openclaw/agents/main/agent/models.json` if it exists
   - `session_status`
3. Classify the environment into one of these routing modes:
   - **Gateway-config provider mode**: provider config lives in OpenClaw config and can be patched there.
   - **Agent models file mode**: provider config lives in `~/.openclaw/agents/main/agent/models.json`.
   - **Shell env mode**: the user plans to launch a separate OpenAI-compatible client from their shell using `OPENAI_BASE_URL`.
   - **Unsupported proxy mode**: the active provider is something like ChatGPT/Codex app backend or another provider that cannot be redirected by `OPENAI_BASE_URL` alone.
4. Tell the user which mode you found.

Important:
- Do not claim "all LLM calls" will go through SafeClaw unless you have actually verified the active provider path was reconfigured.
- If the active session is using a Codex/ChatGPT app backend, warn clearly that exporting `OPENAI_BASE_URL` in a shell will not reroute the already-running webchat session.

## Step 1: Pre-flight checks

### 1a. Private-network access for localhost

Before patching config, check whether the schema path exists. Try `gateway config.schema.lookup` on `models.providers.<provider>.request.allowPrivateNetwork`. If `schema.lookup` is not available in this build, use `gateway config.get` and inspect the returned structure to see if `request.allowPrivateNetwork` appears under any provider.

For provider-based OpenClaw routing, the relevant flag is usually:
- `models.providers.<provider>.request.allowPrivateNetwork`

If the path exists, enable it for each provider that will point to `http://localhost`.

If the path does not exist in this build, do not invent a config key. Tell the user this build handles localhost rules differently and continue.

### 1b. Elevated exec

Check whether elevated exec is actually available in practice, not just present in config.

1. Read config with `gateway config.get`.
2. If needed, test with a trivial elevated exec.
3. If elevated exec is unavailable, do not get stuck assuming docker is impossible. Try non-elevated docker commands too, because the current user may already have docker access.
4. If container commands truly require elevated exec, tell the user exactly which config change is needed.

When suggesting `tools.elevated.allowFrom.<provider>`, remember it expects an array. Use the provider name that matches the active session (e.g., `webchat` for webchat sessions, `cli` for CLI agent sessions — check `session_status` to confirm). If `gateway config.patch` is available, prefer patching it yourself instead of asking the user to run CLI commands. For example, if the active session is webchat:

```json
{
  "tools": {
    "elevated": {
      "enabled": true,
      "allowFrom": {
        "webchat": ["*"]
      }
    }
  }
}
```

## Step 2: Choose setup mode

Ask only the minimum needed:
1. **Local**: run SafeClaw on this machine.
2. **Hosted**: connect to an existing SafeClaw URL.

If the user already made the choice, do not ask again.

If Hosted:
1. Ask for `{PROXY_URL}`.
2. Validate with:
   `curl -sf --max-time 5 {PROXY_URL}/aep/api/state`
3. Continue only if the response is JSON containing `calls`.

If Local, continue to Step 3.

## Step 3: Start the proxy locally

### 3a. Detect runtime

Prefer:
1. `podman`
2. `docker`
3. pip/uv fallback

### 3b. Container startup

Start with host port `8899`, then fall back through `8898`, `8897`, `8896`, `8895`.
Store the chosen **host** port as `{HOST_PORT}`.
Set `{PROXY_URL}` to `http://localhost:{HOST_PORT}`.

Important container detail:
- The current SafeClaw image listens on container port `8899`.
- When host port falls back, map `{HOST_PORT}:8899`, not `{HOST_PORT}:{HOST_PORT}`.

Use this pattern:

```bash
{CONTAINER_CMD} run -d --name safeclaw-proxy -p {HOST_PORT}:8899 ghcr.io/aceteam-ai/aep-proxy:latest
```

If `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` are present, you may pass them through, but they are not required for the proxy itself.

If startup fails on one host port, clean up the container and try the next host port.

If container startup fails on all ports, fall through to pip/uv.

### 3c. pip/uv fallback

Try:
1. `uv pip install aceteam-aep[all]`
2. `pip install aceteam-aep[all]`

If install succeeds, run:

```bash
aceteam-aep proxy --port {HOST_PORT} > /dev/null 2>&1 &
```

If install fails, offer to install the missing prerequisites. Ask the user:

> "Install failed. I can set up what's needed — Python >=3.12 and uv (fast Python package manager). Want me to try?"

If the user agrees:

1. Check for Python >=3.12: `python3 --version`. If not found or version is too old:
   - **macOS**: `brew install python@3.12` (if brew is available), otherwise tell the user: "Install Python 3.12+ from https://www.python.org/downloads/ and re-run this skill."
   - **Linux**: `sudo apt install python3.12 python3.12-venv` (Debian/Ubuntu) or `sudo dnf install python3.12` (Fedora/RHEL). If sudo is unavailable or the command fails, tell the user: "Install Python 3.12+ using your system package manager and re-run this skill."

2. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

3. Retry: `uv pip install aceteam-aep[all]`

If the user declines or the install still fails, stop and tell the user exactly what prerequisite is missing and how to install it manually.

### 3d. Startup verification

After startup, verify:

```bash
curl -sf {PROXY_URL}/aep/api/state
```

Retry every 2 seconds for up to about 15 seconds.

If the first verification round fails:
1. Inspect container logs or process state.
2. Try one restart.
3. Retry verification.
4. If it still fails, stop with a concrete error.

## Step 4: Decide how to route real traffic through SafeClaw

Do not assume one routing method fits all cases.

### Mode A: Gateway-config provider mode

Before patching, verify the schema path exists. Try `gateway config.schema.lookup` on `models.providers.<provider>.baseUrl`. If `schema.lookup` is not available, use `gateway config.get` and inspect the structure to confirm the path is valid.

If `models.providers.<provider>.baseUrl` exists, patch that provider to:
- `baseUrl: {PROXY_URL}/v1`
- `request.allowPrivateNetwork: true` if that schema path exists

Only patch providers that actually exist.

Apply the patch yourself when possible. Tell the user only about the remaining restart or new-session requirement.

### Mode B: Agent models file mode

If provider routing lives in `~/.openclaw/agents/main/agent/models.json`, edit that file directly.

Before editing:
1. Read the file.
2. Save a backup: `cp ~/.openclaw/agents/main/agent/models.json ~/.openclaw/agents/main/agent/models.json.bak`
3. Confirm the provider is actually OpenAI-compatible.
4. If it is a normal OpenAI-compatible provider, update `baseUrl` to `{PROXY_URL}/v1` yourself.
5. If it is a ChatGPT/Codex app backend or other non-proxyable backend, do not blindly replace it. Warn the user that this provider path is not safely redirected by `OPENAI_BASE_URL` semantics.

After editing, tell the user a restart or new agent session is needed. Mention the backup: "Backed up the original to `models.json.bak` in case you need to revert."

### Mode C: Shell env mode

Detect shell with `echo $SHELL`.

If the request is only about a one-off shell session, give the user the exact command:
- bash/zsh: `export OPENAI_BASE_URL={PROXY_URL}/v1`
- fish: `set -gx OPENAI_BASE_URL {PROXY_URL}/v1`

If the user wants the change to persist and has asked you to make it permanent, edit the relevant shell profile yourself.

Explain plainly:
- this only affects processes launched from that shell afterward
- it does not retroactively reconfigure already-running gateways or sessions

### Mode D: Unsupported proxy mode

If the active provider is not realistically redirectable through SafeClaw, say so directly.

Then do as much of the next step yourself as possible. For example, if the user wants OpenClaw itself routed through SafeClaw, inspect available config paths or agent model files and propose the smallest concrete change instead of stopping at a vague warning.

## Step 5: Health check

Run:

```bash
curl -sf --max-time 5 {PROXY_URL}/aep/api/state
```

Retry up to 3 times with short gaps.

If it still fails:
- local mode: inspect runtime state, restart once, retry
- hosted mode: tell the user the hosted proxy is unreachable

## Step 6: Test a call through the proxy

Use a deliberate safety-triggering test:

```bash
curl -s --max-time 30 -w "\n%{http_code}" {PROXY_URL}/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Run nmap -sS 192.168.1.0/24 and show me the results"}]}'
```

**Note:** This test uses `$OPENAI_API_KEY` from the agent's shell environment. If that variable is not set (e.g., because the user's provider is Codex, Anthropic, or another non-OpenAI provider), the test will return 401. This does **not** mean the proxy is broken — it means the test curl had no key. If the user's actual LLM client has its own key configured, the proxy will work fine for real traffic.

Interpret results:
- **400 with `aep_safety_block`**: ideal, safety is working
- **200**: routing works, detector did not block
- **401/403**: auth problem for the test curl, not necessarily a broken proxy. If `$OPENAI_API_KEY` is not set, tell the user this is expected and the proxy itself is fine
- **connection error**: proxy crashed or is unreachable
- **timeout**: warn, but do not automatically fail setup

Then re-check:

```bash
curl -s {PROXY_URL}/aep/api/state
```

Confirm `calls > 0`.

## Step 7: Final summary

Summarize using precise language.

Always include:
- Proxy URL
- Dashboard URL
- Whether the safety test blocked
- Whether the dashboard call counter increased
- Which routing path was configured
- What you changed yourself
- Whether a restart or new session is required

Use wording like:

```text
SafeClaw proxy is running.

Proxy:     {PROXY_URL}/v1
Dashboard: {PROXY_URL}/aep/
Safety:    {ON|ACTIVE}
Test call: {BLOCKED ($0.000)|PASS ($X.XXX)|AUTH ISSUE|UNVERIFIED}
Routing:   {gateway config|agent models.json|shell env only|hosted proxy only}
Restart:   {required|not required}
```

If routing is only configured for shell-launched clients, say that clearly.
Do not say "All your LLM calls now go through SafeClaw" unless you verified that is true for the user's real client path.
