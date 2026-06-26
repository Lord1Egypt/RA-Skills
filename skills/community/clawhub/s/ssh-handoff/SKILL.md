---
name: ssh-handoff
description: Create and reuse a secure shared terminal handoff when a human must authenticate first and the agent must resume work in the same shell session afterward. Use for SSH handoff, sudo handoff, browser-opened temporary terminal access, or LAN-restricted terminal sharing backed by tmux when direct agent authentication is blocked or undesirable.
---

# SSH Handoff

Use this skill when a human must complete a sensitive authentication step first, and the agent should continue in the exact same shell session afterward.

The core pattern is:

1. keep terminal state in a named `tmux` session
2. let the human attach and authenticate inside that session
3. capture the pane state
4. let the agent continue from the same shell

Prefer this skill when the user should not paste credentials into chat and when direct agent authentication is blocked, undesirable, or less safe than a shared-session handoff.

## Choose the simplest mode

Prefer Mode A unless browser access is actually needed.

### Mode A — plain tmux handoff

Use when the human already has terminal access to the host.

Typical flow:

1. create or reuse a named `tmux` session
2. ask the human to attach
3. let the human authenticate
4. capture the pane
5. continue through `tmux`

Example:

```bash
tmux has-session -t handoff-session 2>/dev/null || tmux new-session -d -s handoff-session
tmux attach -t handoff-session
```

### Mode B — local browser terminal

Use when the human wants a browser-based terminal on the same machine that hosts the service.

This mode uses `ttyd` directly and fits:

- localhost-only access
- quick temporary sessions
- cases where basic auth is acceptable

Bundled launcher:

```bash
./scripts/start-local-web-terminal.sh handoff-session
```

### Mode C — LAN-restricted browser terminal with one-shot token

Use when the human opens the terminal from another trusted machine on the same local network and you want less friction than repeated username/password entry.

This mode works like this:

1. a named `tmux` session holds the real shell state
2. `ttyd` runs on localhost as the terminal backend
3. a small local proxy exposes a LAN URL with a one-shot `?token=`
4. the first valid request becomes a browser session through a cookie
5. the agent continues using the same `tmux` session

Bundled launcher:

```bash
./scripts/start-url-token-web-terminal.sh handoff-session
```

## Requirements

Check these first:

```bash
command -v tmux
command -v ttyd
command -v node
command -v python3
```

Install on Debian / Ubuntu:

```bash
sudo apt update && sudo apt install -y tmux ttyd
```

`node` must also exist for Mode C because the proxy launcher uses the bundled Node script.

## Quick usage

### Create or reuse the session

```bash
tmux has-session -t handoff-session 2>/dev/null || tmux new-session -d -s handoff-session
```

### Launch Mode C with placeholders

Use placeholders that match the environment instead of copying real addresses blindly. The `192.0.2.x` addresses below are documentation-only example addresses.

```bash
HOST=<server-ip> CLIENT_IP=<trusted-client-ip> PORT=48080 UPSTREAM_PORT=48081 FORBID_REUSE_IF_AUTHENTICATED=1 ./scripts/start-url-token-web-terminal.sh handoff-session
```

The launcher prints:

- one-shot URL
- expiry time
- proxy and backend PIDs
- cleanup command
- optional UFW helper commands

Example with documentation-only IPs:

```bash
HOST=192.0.2.10 CLIENT_IP=192.0.2.20 PORT=48080 UPSTREAM_PORT=48081 FORBID_REUSE_IF_AUTHENTICATED=1 ./scripts/start-url-token-web-terminal.sh handoff-session
```

### Resume after authentication

Always inspect the pane before assuming the handoff worked:

```bash
tmux capture-pane -t handoff-session -p | tail -80
```

Look for:

- remote hostname or expected prompt
- expected working directory
- absence of a password prompt
- absence of a terminal program that would swallow commands unexpectedly

If uncertain, ask one short confirmation question before continuing.

## Launcher variables

### `start-local-web-terminal.sh`

Supported variables:

- `HOST` — bind address, default `127.0.0.1`
- `PORT` — optional explicit port, otherwise a random free port
- `TTL_MINUTES` — default `30`
- `BIND_SCOPE` — metadata only, usually `local` or `lan`
- `CLIENT_IP` — optional, used only to print UFW helper commands in LAN mode

### `start-url-token-web-terminal.sh`

Supported variables:

- `HOST` — proxy bind address, default `127.0.0.1`
- `PORT` — proxy frontend port, default `48080`
- `UPSTREAM_PORT` — localhost `ttyd` backend port, default `48081`
- `CLIENT_IP` — optional trusted client IP for UFW helper commands and proxy-side IP filtering
- `TTL_MINUTES` — default `30`
- `BIND_SCOPE` — metadata only, usually `local` or `lan`
- `COOKIE_SECURE` — set to `1` when serving through local HTTPS so the session cookie gets the `Secure` flag
- `EXPECTED_HOST` — strict allowed `Host` header, default `<HOST>:<PORT>`
- `EXPECTED_ORIGIN` — strict allowed websocket `Origin`, default derived from host and cookie mode
- `FORBID_REUSE_IF_AUTHENTICATED` — set to `1` to refuse startup if the tmux pane already looks authenticated
- `REPLACE_EXISTING` — set to `1` only after the human explicitly approves replacing the current web handoff for the same `SESSION_NAME`; otherwise the launcher prints the existing URL/PIDs/cleanup command and exits without touching the running session
- `AUTH_GUARD_REGEX` — optional override for the pane-authentication detection regex

If the default ports are already occupied, override them explicitly.

When a handoff already exists for the same `SESSION_NAME`, the launcher does not silently start a second one: it reports the existing session details and exits with `READY=0`. Ask the human whether to replace it. Use `REPLACE_EXISTING=1` only after explicit approval.

If the requested proxy or upstream port is already occupied, the launcher also exits with `READY=0` and reports a port conflict instead of killing anything automatically. In that case, either get approval to replace the conflicting session or relaunch on another port and update firewall rules if LAN access is involved.

## Use Mode C correctly

1. ensure the `tmux` session exists
2. launch the token-based terminal
3. if needed, allow access only from the trusted client IP
4. send the printed one-shot URL to the human through an appropriate channel
5. let the human authenticate inside the terminal
6. capture the pane and verify state
7. continue through `tmux`
8. if the launcher reports an existing session or a port conflict, ask whether to replace it or use a different port
9. stop the temporary web terminal when done

## Cleanup

For Mode B, use:

```bash
./scripts/stop-local-web-terminal.sh <pid> <session-name>
```

For Mode C, prefer the printed cleanup command because it removes both temporary processes and the temporary runtime directory:

```bash
TTYD_PID=<ttyd-pid> PROXY_PID=<proxy-pid> RUNTIME_DIR=<runtime-dir> <cleanup-script>
```

If that command is unavailable, killing the printed proxy and backend PIDs is still acceptable.

The launcher also installs automatic TTL cleanup for the proxy, `ttyd`, and temporary files. Leave the `tmux` session alive if it may be reused.

## Guardrails

- Keep exposure local-only by default.
- If LAN exposure is needed, restrict it to one trusted client IP only.
- Do not expose the terminal through a public tunnel or reverse proxy.
- Do not ask the human to paste passwords, OTP codes, or private keys into chat if the handoff can avoid it.
- Use short-lived access material for browser modes.
- Prefer one `tmux` session per target or task.
- Capture pane state before sending more commands.
- Ask before destructive actions.
- Enable `FORBID_REUSE_IF_AUTHENTICATED=1` by default for normal use; disable it only when reopening an already-authenticated session is intentional.
- Treat the printed one-shot URL as sensitive until expiry.
- Expect the proxy to reject mismatched `Host`, websocket `Origin`, or client IP when those checks are configured.
- Do not suggest or launch browser-terminal modes casually from external messaging channels such as Telegram, Discord, Slack, or similar remote chat surfaces.
- Prefer plain `tmux` handoff instead when the interaction happens over an external channel, unless the human explicitly confirms a trusted local-network setup and accepts the risk.

## References

Read these when needed:

- `references/examples.md` — generic usage examples
- `references/design-notes.md` — security and design envelope
- `references/lan-restricted.md` — LAN-only restricted-IP pattern

Bundled scripts:

- `scripts/start-local-web-terminal.sh`
- `scripts/start-url-token-web-terminal.sh`
- `scripts/stop-local-web-terminal.sh`
- `scripts/url-token-proxy.js`
