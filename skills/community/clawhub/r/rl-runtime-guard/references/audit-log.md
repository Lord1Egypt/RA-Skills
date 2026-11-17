# Audit Log (opt-in)

**As of v1.0.5, audit logging is OFF by default.** This is a privacy-by-default change — no user content is captured unless you explicitly opt in.

## Why this changed

The original handler captured the first 80 characters of every user message that triggered a guard. This is useful for debugging but creates a privacy concern: prompts may contain secrets, customer data, proprietary code, or personal information. If you do not need audit telemetry, **do not enable it**.

## How to enable (opt-in)

Set `auditLogPath` in your config to a path of your choice:

```json
{
  "auditLogPath": "~/.openclaw/logs/audit/rl-guard-decisions.jsonl"
}
```

The path supports `~` expansion. The skill creates the parent directory if it does not exist.

## Schema (when enabled)

```typescript
type AuditEntry = {
  timestamp: string;         // ISO 8601 UTC
  sessionKey: string;        // session identifier (anonymized by caller)
  decisions: string[];       // list of guards that fired
  guardPromptLength: number; // bytes of injected prompt
  userContentLength: number; // length of user message in chars
  error?: string;            // only present if the guard failed
};
```

**Important**: when audit logging is enabled, the schema records `userContentLength` (a number) and never stores the actual user message text.

## Example entries

```json
{"timestamp":"2026-08-30T18:30:00Z","sessionKey":"agent-main-abc123","decisions":["retry_loop"],"guardPromptLength":215,"userContentLength":48}
{"timestamp":"2026-08-30T18:30:01Z","sessionKey":"agent-main-abc123","decisions":["complex_task","platform_path_hint"],"guardPromptLength":512,"userContentLength":720}
```

## Common queries

Count guard fires per session:

```bash
jq -s 'group_by(.sessionKey) | map({session: .[0].sessionKey, count: length})' \
  ~/.openclaw/logs/audit/rl-guard-decisions.jsonl
```

Show recent decisions:

```bash
tail -f ~/.openclaw/logs/audit/rl-guard-decisions.jsonl | jq .
```

## Disabling after enabling

Set `auditLogPath` back to empty string or `null`:

```json
{ "auditLogPath": "" }
```

## Purging old logs

```bash
rm ~/.openclaw/logs/audit/rl-guard-decisions.jsonl
```

This is a permanent deletion. Make sure no compliance or debug process depends on the log first.

## Permission recommendation

If you do enable audit logging, restrict file permissions:

```bash
chmod 600 ~/.openclaw/logs/audit/rl-guard-decisions.jsonl
```

The skill does not set restrictive permissions automatically — that is the operator's responsibility.

## Retired field: `userContentPreview`

Earlier versions (1.0.0 - 1.0.4) captured a preview of the user message. That field has been **removed** in 1.0.5+. If you upgrade from an older version, the old field will simply not appear in new entries; existing log entries are not retroactively modified.
