# HEARTBEAT

This workspace uses `say-hi-to-me` for companionship-style proactive greetings.

## Runbook

1. Run `python3 scripts/heartbeat_bridge.py --json --mark-sent`.
2. Read the returned JSON.
3. If `response_text` is `HEARTBEAT_OK`, reply with exactly `HEARTBEAT_OK`.
4. Otherwise, send exactly the `response_text` value and nothing else.

## Guardrails

1. This heartbeat is for a lightweight social check-in only.
2. Do not resume stale work tasks or infer old unfinished jobs.
3. Do not explain internal policy checks, timers, or cooldown state to the user.
4. Keep the final greeting concise and natural.

## Note

`--mark-sent` is a best-effort shortcut for a simple setup. In a production host integration, you can move the `last_sent_at` update to a post-delivery acknowledgment step if you want stricter delivery accounting.
