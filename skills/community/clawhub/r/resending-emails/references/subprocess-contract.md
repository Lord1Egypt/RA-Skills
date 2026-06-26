# Subprocess contract for AI agents

This file describes how an agent should invoke the official `resend` CLI so output stays
deterministic and machine-friendly.

## Default bounded invocation

For most commands, use:

```bash
resend --json -q <command> ...
```

Why:

- `--json` forces structured output
- `-q` suppresses spinners/status noise and implies JSON mode
- global flags go **before** the command/subcommand

## Default environment

Set this unless you have a reason not to:

```bash
RESEND_NO_UPDATE_NOTIFIER=1
```

That prevents update notices from appearing and keeps output stable.

## Auth for agents

Prefer one of these:

1. `RESEND_API_KEY` in the environment
2. `--profile <name>` with a pre-seeded profile

Avoid interactive prompts and avoid raw `--api-key` unless you intentionally want to override the
resolved key for one invocation.

## Output parsing order

Use this parser strategy:

1. try full JSON from stdout
2. try NDJSON from stdout
3. try full JSON from stderr
4. try NDJSON from stderr
5. fall back to raw text only if structured parse fails everywhere

### Why parse stderr too?

The README documents JSON-to-stdout for machine mode, but the current `output.ts` implementation
uses `console.error` for JSON error output. Agents should therefore parse both channels.

## Streaming commands

Treat these specially:

- `resend webhooks listen`
- `resend emails receiving listen`

Guidance:

- do not wait forever unless the user explicitly wants a long-running stream
- if you need only a short observation window, run with a supervisor/timeout
- in JSON/piped mode, expect one JSON object per line
- keep stderr because it carries useful operational status in interactive mode

## File inputs

Use files, not shell-escaped blobs, when content is non-trivial.

Prefer:

- `--html-file ./message.html`
- `--file ./batch-emails.json`

over very long inline strings.

## Secret handling

Good:

- environment variables injected by CI
- stored profiles
- secret managers that export `RESEND_API_KEY`

Riskier:

- `--api-key` inside recorded shell history
- logging fully expanded commands with secrets included

## Suggested bounded wrapper behaviour

A robust wrapper should:

- prepend `--json -q`
- set `RESEND_NO_UPDATE_NOTIFIER=1`
- capture stdout and stderr
- parse both channels
- preserve the return code
- include the raw text in its structured result for debugging

The bundled `scripts/resend_cli.py run` command does exactly this.
