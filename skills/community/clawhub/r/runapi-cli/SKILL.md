---
name: runapi-cli
description: Install and use the RunAPI CLI as the universal execution layer for RunAPI models. Use when the user asks to run any RunAPI model from an agent, inspect auth, install RunAPI on a local machine/server/CI, pass JSON request bodies, wait for tasks, or automate RunAPI workflows from the terminal.
documentation: https://runapi.ai/models.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models
    primaryEnv: RUNAPI_API_KEY
    requires:
      bins:
      - runapi
    install:
    - kind: brew
      formula: runapi-ai/tap/runapi
      bins:
      - runapi
    envVars:
    - name: RUNAPI_API_KEY
      required: false
      description: Optional RunAPI API key; runapi login or saved CLI config can also authenticate the runapi binary.
---

# RunAPI CLI

The `runapi` CLI is the universal execution layer for every RunAPI model that
ships a CLI service. Use it whenever an agent needs to run a one-off model task,
pass a JSON request body, wait for an async task, or script RunAPI from a
terminal, server, or CI job.

## Install

| Target | Command |
|---|---|
| macOS / Linux (interactive) | `brew install runapi-ai/tap/runapi` |
| Server / CI (headless) | `curl -fsSL https://runapi.ai/cli/install.sh \| sh` |
| Pin a specific version | `curl -fsSL https://runapi.ai/cli/install.sh \| sh -s -- --version v0.1.0` |

The installer detects OS and architecture (Linux and macOS, amd64 and arm64), verifies a SHA-256 checksum from `https://runapi.ai/cli/latest.json`, and refuses to write the binary if verification fails.

## Authentication

| Source | How |
|---|---|
| Browser login (interactive) | `runapi login` |
| Environment | `export RUNAPI_API_KEY=<key>` |
| Saved config (recommended for servers) | `printf '%s' "$KEY" \| runapi auth import-token --token -` (writes `~/.config/runapi/config.json` with mode 0600) |

`RUNAPI_BASE_URL` overrides the default base URL. Check the current state with `runapi auth status`.

Avoid `runapi auth import-token --token "$KEY"` directly — the value would be visible in `ps -ef` on shared hosts. Use stdin (`--token -`) or `RUNAPI_API_KEY` in the environment.

## Discover services, actions, and fields

The CLI is JSON-first: every service exposes typed actions, and each action
documents its request fields through `--help`. Always inspect before composing a
request instead of guessing flags.

```shell
runapi --help
runapi suno --help
runapi suno text-to-music --help
```

## Run a model

Pass the request body as JSON through `--input-file` (or `--input` for inline
JSON, or `-` for stdin). The default flow is synchronous and polls until the
task completes.

```shell
# Synchronous: submit and poll until done
runapi suno text-to-music --input-file request.json

# Asynchronous: submit and return immediately, then poll separately
runapi suno text-to-music --async --input-file request.json
runapi wait <task-id> --service suno --action text-to-music

# Inspect a task without waiting
runapi get <task-id> --service suno --action text-to-music
```

JSON responses go to stdout; progress lines go to stderr. Pipe to `jq` for downstream parsing.

## Account

```shell
runapi account info
runapi account balance
```

## Install the skill into another agent runtime

```shell
runapi agent install-skill --target claude    # ~/.claude/skills/runapi-cli/
runapi agent install-skill --target codex     # ~/.codex/skills/runapi-cli/
runapi agent install-skill --target gemini    # ~/.gemini/skills/runapi-cli/
runapi agent install-skill --target openclaw  # ~/.openclaw/skills/runapi-cli/
runapi agent list-targets                     # JSON list with resolved paths
runapi agent install-skill --target-dir <path>  # custom location
```

## Safety notes for agents

- Never paste API keys into example commands. Reference `RUNAPI_API_KEY` or `runapi auth import-token` instead.
- The CLI exits non-zero on validation failures, network errors, and timeouts. Check the exit code before assuming success.
- For long-running tasks, prefer `--async` plus a `wait` loop so the agent can release the shell promptly.

## References

- Browse every RunAPI model and its CLI service: https://runapi.ai/models.md
