# ssh-handoff

Secure shared terminal handoff for cases where a human must authenticate first and the agent must resume work in the same shell session afterward.

## What it does

This skill is built around a simple pattern:

1. keep terminal state inside a named `tmux` session
2. let the human complete the sensitive login step
3. let the agent continue in that exact same shell session

It supports three practical modes:

- plain `tmux` handoff
- local browser terminal via `ttyd`
- LAN-restricted browser terminal with one-shot URL token

## Quick start

1. prefer plain `tmux` handoff when browser access is not needed
2. use the local browser mode for temporary same-machine access
3. use the LAN token mode only for trusted local-network access
4. verify the shell state with `tmux capture-pane` before continuing
5. if a session already exists, ask whether to replace it before using `REPLACE_EXISTING=1`
6. if the requested port is already busy, either get approval to replace the conflicting session or relaunch on another port and update firewall rules if needed
7. clean up the temporary web terminal when the handoff is done

## Included files

- `SKILL.md` — operational instructions for the agent
- `scripts/` — launchers and proxy code
- `references/` — design notes and usage examples

## Runtime requirements

Required binaries:

- `tmux`
- `ttyd`
- `node`
- `python3`

No external downloads are required at runtime. The skill expects these binaries to already be installed from trusted packages.

## Runtime behavior

At runtime, this skill may:

- create temporary files under `/tmp`
- create a temporary state file
- start background processes (`ttyd`, Node proxy, cleanup watcher)
- bind local or LAN ports for temporary browser-terminal access

These behaviors are expected and are part of the documented handoff workflow.

## Notes on examples

Documentation examples may use `192.0.2.x` addresses. These are placeholder documentation-only IPs from the TEST-NET range and must be replaced with real local addresses.

## Security posture

This skill is best suited for:

- localhost-only use
- trusted LAN use with firewall restrictions
- short-lived human-auth-first terminal handoff

Risk guidance:

- localhost: low to moderate risk
- trusted filtered LAN: moderate risk
- loosely controlled shared LAN: moderate to high risk
- public internet exposure: high risk and not recommended

## Recommended hardening

- keep `ttyd` on localhost whenever possible
- expose the frontend only to a trusted client IP when LAN access is required
- keep TTLs short
- treat one-shot URLs as sensitive until expiry
- ask before replacing an existing live session
- prefer `FORBID_REUSE_IF_AUTHENTICATED=1` for normal use
- do not use public tunnels or public reverse proxies for this workflow
- prefer HTTPS/TLS if this is ever used beyond strictly trusted local conditions

## External-channel caution

Do not casually use browser-terminal modes from external messaging channels such as Telegram, Discord, Slack, or similar remote chat surfaces.

In those contexts, prefer:

- plain `tmux` handoff
- or no browser terminal at all

Only use browser-terminal modes when the human explicitly confirms that the setup is local or on a trusted LAN and understands the risk.

## Registry / review note

This skill should be treated as security-sensitive, not malicious. It opens temporary local or LAN terminal endpoints by design for a documented human-auth-first workflow, but it does not download remote code, does not require unrelated cloud credentials, and is not intended for public internet exposure.

## Safety notes

- keep it local-only by default
- if exposed on LAN, restrict access to one trusted client IP
- do not expose through a public tunnel or reverse proxy
- use short TTLs and clean up after use
- do not replace an existing live session without the human's approval

## Repository scope

This repository contains only the `ssh-handoff` skill and its bundled resources.
