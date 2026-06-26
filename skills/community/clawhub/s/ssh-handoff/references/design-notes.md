# Secure web-terminal design notes

## Goal

Allow a human to authenticate in a browser-opened terminal while keeping the terminal temporary, local or LAN-scoped, and tied to a `tmux` session that preserves shell state for the agent.

## Security envelope

Default requirements:

- bind to `127.0.0.1` by default when remote browser access is not needed
- use short-lived access material such as a temporary token or password
- keep `tmux` as the real terminal state holder
- shut down the temporary web terminal after the task or at TTL expiry
- avoid public tunnels, public reverse proxies, and internet exposure unless the human explicitly asks for that risk tradeoff

For LAN use, tighten exposure with:

- a trusted server bind address only
- a single trusted client IP when possible
- strict `Host` and websocket `Origin` checks when a proxy is used
- cleanup of temporary processes and metadata

## Recommended runtime shape

A launcher should:

1. ensure the `tmux` session exists
2. generate short-lived secrets
3. choose or validate ports
4. launch the backend terminal service
5. launch the access-control layer if needed
6. print the connection details and cleanup information
7. stop automatically at expiry

Pseudo-flow:

```text
ensure tmux session
create short-lived access token
start terminal backend bound to localhost
optionally start LAN-facing proxy with access checks
return connection details
install TTL cleanup
```

## UX notes

Prefer a short operator-facing output:

- one connection method
- one expiry time
- one cleanup command
- one short safety note

The success criterion should be simple: the human authenticates, then the agent confirms the expected prompt or shell state before continuing.

## Failure modes

### Required binaries missing

Explain what is missing and offer either:

- fallback to plain `tmux` handoff, or
- installation with approval

### Browser path unreachable

Do not automatically create a public route. Prefer:

- localhost access on the host machine
- trusted LAN access
- a different handoff mode

### Session state unclear

Capture the pane, inspect the prompt, and avoid sending blind commands. If needed, send one interrupt and capture again before continuing.

### Session appears already authenticated

Prefer refusing to relaunch when reuse would be risky. A configurable guard such as `FORBID_REUSE_IF_AUTHENTICATED=1` is a safer default for repeated use.

## Candidate tools

### ttyd

Pros:

- lightweight
- common on Linux
- easy to wrap around `tmux attach`

Questions to confirm during implementation:

- installed version behavior
- auth capabilities on the target host
- compatibility with local proxying or token gating

### Wetty

Pros:

- browser terminal purpose-built
- Node-friendly ecosystem

Questions to confirm during implementation:

- auth support model
- attach pattern to `tmux`
- install footprint and operational complexity

## Suggested implementation split

- `SKILL.md`: workflow and guardrails
- `scripts/`: deterministic launchers and cleanup helpers
- `references/design-notes.md`: rationale and security envelope

## Non-goals

- embedding the terminal directly into a separate product UI
- public exposure by default
- long-lived shared terminal services with no expiry
