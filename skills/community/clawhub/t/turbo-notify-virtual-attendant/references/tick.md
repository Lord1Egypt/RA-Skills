# One cycle

Run this to catch up with the number. In a session it runs every minute or so; unattended it runs by itself (see the file for your harness). Each step is one command; read its JSON before the next.

## 1. Fetch the new events

1. `tn_assist cursor` gives `params` (for example `{"limit": "100", "ending_before": "evt_…"}`).
2. Call `list_events` with `event_types` = `message.received`, `message.replied`, `message.sent`, `number_id` = the bound `num_…`, and those params (`limit`, `ending_before`, `starting_after`). Save the raw result to `page1.json`.
3. `tn_assist fetch-plan --page page1.json`. If `done` is false, call `list_events` again with the returned `params`, save `page2.json`, and run `fetch-plan` with every page so far (`--page page1.json --page page2.json`). Repeat until `done` is true. A full page means there is more: never stop at one.
4. `tn_assist ingest --file page1.json --file page2.json`. Everything is stored now, before any thinking. Carry out the `deliveries` it returns (a notice about a gap in service, or about an event from another number).

## 2. Work through the queue

Repeat `tn_assist next --kinds contact,admin,attendant,compaction` until `item` is null. For each item:

1. **Hydrate.** Events carry only a short preview. For each event in `item.hydrate`, with the message id at the same position of `item.message_ids` (null when unknown: use `--unreadable`), call `get_message` with that `message_id` and `number_alias` = the `num_…`, write the full text to a file, and run `tn_assist set-text --item <id> --event <event id> --file <file>`. If the message cannot be read any more, run it with `--unreadable` instead.
2. By `item.kind`:
   - `contact`: [contact-turn.md](contact-turn.md).
   - `admin` or `attendant`: run `tn_assist run-console --item <id>`. Commands are carried out by the helper without a model. If `needs_model` is true, there is free text: see [admin-console.md](admin-console.md).
   - `compaction`: [memory.md](memory.md).
3. Carry out every delivery that `apply` or `run-console` returned, in order:
   - `send`: `send_text` with `number` = `+` and `to`, `text`, `idempotency_key`, `number_alias` = the `num_…`, and `quoted_message_id` = `quote` when the delivery has one. Do not quote anything else: `reply_to_message` is not used, because it would quote the message that was just answered.
   Do not edit text, do not skip, do not add anyone.
4. If a delivery is refused for pacing (`send_rate_spacing`, `rate_limit_exceeded`, `messages_per_minute_limit_exceeded`) or because the number is reconnecting (`number_not_connected`), wait the "Retry after" seconds (a few for pacing; try again next cycle for a reconnect) and send the same delivery again with the same `idempotency_key`. If it is refused for a quota or plan reason (`payment_required`, `contact_quota_exceeded`, `messages_quota_exceeded`, `feature_not_available`, `insufficient_scope`), do not retry: run `tn_assist report-failure --cause <the error code> --cycle <billing cycle, for example the month>` and deliver the notice it returns. It speaks once per cause and cycle. For the daily limits (`warmup_limit_exceeded`, `recipients_per_day_limit_exceeded`, `duplicate_burst_blocked`, `reply_ratio_too_low`) do not retry in this cycle: send the same delivery again with the same `idempotency_key` after about an hour, and drop it after six hours. If the key is refused (401 or 403 other than `insufficient_scope`), keep the delivery and run `tn_assist report-failure` once.

## 3. Housekeeping

- `tn_assist reminders` and `tn_assist version-check --announce`: carry out their deliveries.
- Once a day: `tn_assist purge` (old transcript lines past the retention) and `tn_assist migrate` after an update.
- If the last cycle was more than 30 minutes ago, `ingest` already warned the administrators; do not warn again.

## Timing

Run a cycle every 20 to 60 seconds. Never leave more than 10 minutes between cycles: the platform deletes message content after the plan's retention (1 hour by default).

## What you must not do here

- Do not call `get_message` for anything but the ids the item lists.
- Do not read other conversations to "get context". The pack has everything the turn is allowed to see.
- Do not answer an item whose `kind` you do not know. Leave it leased; it comes back.
