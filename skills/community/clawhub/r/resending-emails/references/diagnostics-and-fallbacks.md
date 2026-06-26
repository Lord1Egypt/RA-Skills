# Diagnostics and fallbacks

This file covers the fastest debug order and the deliberate fallback rules.

## Start with `doctor`

When the environment is unclear:

```bash
resend --json -q doctor
```

Read it in this order:

1. did the CLI run at all?
2. is a key resolved?
3. is the key coming from the expected source?
4. are there verified domains?
5. is this obviously an agent environment?

## Common failure order

### 1. CLI missing

Check install first. Do not assume `resend` exists on the machine.

### 2. Auth resolution failure

If you see `auth_error`:

- check `RESEND_API_KEY`
- check `--profile`
- check whether the expected profile actually exists
- run `doctor`

### 3. Domain mismatch / sending prerequisites

If sending fails:

- check the exact `from` domain/subdomain
- check whether the domain is verified
- check whether the account has verified domains at all
- remember that `resend.dev` is not for real customer sending

### 4. Batch shape failure

If `emails batch` fails:

- ensure the input is valid JSON
- ensure it is an array
- ensure it has 100 items or fewer
- ensure no item includes `attachments`
- ensure no item includes `scheduled_at`

### 5. Webhook/inbound design mistakes

If webhook handling is flaky:

- verify raw body, not parsed JSON
- dedupe on `svix-id`
- assume retries
- assume out-of-order delivery

## CLI-specific quirks to remember

### Output channel discrepancy

Use tolerant parsing because JSON errors may be written to stderr.

### Update notices

Set `RESEND_NO_UPDATE_NOTIFIER=1` for deterministic output in wrappers.

### Long-running commands

Do not run `listen` commands as if they were bounded commands. Supervise them explicitly.

## When to fall back to MCP/API

Fallback is appropriate when:

- the CLI is not installed and cannot be installed
- the installed CLI version does not expose the required surface
- the flow is currently better represented through MCP/API

Current likely fallback cases:

- sending via hosted `template_id` from the CLI
- enabling receiving on an already-created domain if local `domains update --help` still lacks the toggle
- any future feature that exists in docs/API but is not exposed in the installed CLI

## How to phrase a fallback well

Good fallback phrasing:

1. explain exactly what the CLI covers,
2. identify the missing or ambiguous piece,
3. name the fallback surface,
4. preserve the user's goal.

Example:

> The CLI clearly covers template creation/publish, but the current `emails send` flags do not show
> a direct hosted-template send path. If you want true hosted-template sends today, the safest next
> step is MCP/API for that final send operation.
