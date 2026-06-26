# Agent operating model

This file explains how to behave like a careful **Resend CLI operator** instead of a generic shell
scripter.

## 1) Classify the task first

Put every request into one of these buckets before you touch the terminal:

| Task shape | Typical examples | First move |
| --- | --- | --- |
| Environment diagnosis | “Why is Resend not working in CI?” | `resend --json -q doctor` |
| Bounded live mutation | send email, create domain, create webhook | choose command, prepare files, run with `--json -q` |
| Long-running dev loop | local webhook or inbound listener | choose a `listen` command and treat output as a stream |
| Architecture / modelling | subscription model, domains, template strategy | choose primitive before command |
| Coverage-gap handling | hosted template send, receiving toggle on existing domain | surface the gap early and fall back deliberately |

## 2) Prefer CLI-first, but do not become CLI-dogmatic

Use the official CLI when:

- the user wants a real account operation from an agent, shell, or CI environment
- structured subprocess output is useful
- you want the CLI to set Resend-specific client behaviour for you

Use MCP/API/SDK only when:

- the CLI is unavailable and cannot be installed
- the CLI does not expose the feature cleanly enough
- the user needs idiomatic application code, not an operational command

## 3) Use the right command class

### Bounded commands

These return and exit:

- `doctor`
- `emails send`, `emails list`, `emails get`, `emails batch`, `emails update`, `emails cancel`
- `domains create`, `domains get`, `domains list`, `domains update`, `domains verify`
- `webhooks create`, `webhooks get`, `webhooks list`, `webhooks update`
- `contacts *`, `topics *`, `segments *`, `broadcasts *`, `templates *`, `api-keys *`

For these, use:

```bash
resend --json -q <command> ...
```

### Streaming commands

These stay alive until interrupted:

- `resend webhooks listen`
- `resend emails receiving listen`

For these:

- do **not** pretend they are normal request/response calls
- expect line-oriented event output in JSON/piped mode
- manage them like supervised background processes with explicit stop conditions
- keep stderr for status and operational context

## 4) Default mutation workflow

For live mutations:

1. choose the correct primitive
2. choose the exact CLI command
3. build any file input first (`--html-file`, batch JSON)
4. run with deterministic flags
5. verify with a read/list/get command
6. save the returned IDs

## 5) Default safety rules

- Prefer **environment variables or stored profiles** over putting secrets in command arguments.
- Add an idempotency key for `emails send` and `emails batch` when retries are possible.
- Prefer `--html-file` over inlining large HTML strings into shell commands.
- Prefer explicit **ISO 8601** timestamps for agent-generated transactional schedules.
- For any webhook plan, include signature verification, dedupe, and out-of-order handling.
- For inbound plans, treat the webhook as a trigger and then fetch the full message/attachments.

## 6) How to answer well

A good Resend CLI answer usually contains:

1. the primitive,
2. the command sequence,
3. any file content the user needs,
4. the caveats that actually matter,
5. the verification step,
6. the fallback path if the CLI surface is incomplete.
