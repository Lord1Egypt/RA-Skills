# YumFu v1.7.9

This patch fixes a real daily-evolution delivery bug discovered in production Telegram play.

## Fix: daily evolution turn IDs are now day-scoped

Previously, daily evolution delivery could reuse the same `turn_id` across multiple days for the same player + universe pair.
That caused YumFu's delivery-state guard to think image/TTS had already been sent for the new day's update.

### Symptom
- daily evolution text still arrived
- image was skipped with `image_already_sent`
- TTS was skipped with `tts_already_sent`
- this made cron-driven "前情 / 今日推进" updates degrade into text-only delivery

### Root cause
- `prepare_daily_evolution_delivery.py` derived a stable but overly-reused `turn_id`
- delivery-state is keyed by `turn_id`
- once a previous day marked `image_sent=true` and `tts_sent=true`, later days could inherit that sent-state incorrectly

### What changed
- daily evolution `turn_id` derivation now includes a per-day stamp
- stamp is derived from payload time fields when available, otherwise file mtime / current day fallback
- this preserves duplicate-send protection within a day while preventing cross-day state collisions

### Result
- daily evolution image delivery works again
- daily evolution TTS voice-bubble delivery works again
- Telegram re-entry updates no longer silently downgrade to text-only after prior successful runs

## Scope
- targeted patch only
- no storybook flow changes
- no save format changes
- no unrelated cron logic included in this release
