# Good practices

Guidance for building this so it stays reliable and a non-technical operator can trust it.

## Keep it in one folder, minimal dependencies

- Everything lives under the one project folder. No global installs the operator can't see.
- Prefer the **standard library** (the provided scripts are stdlib-only Python 3 — no `pip`).
  Ask before installing any runtime or package, and explain why in plain language.
- Suggested layout:
  ```
  project/
    .env                # NXVET_API_KEY (git-ignored)
    config.json         # orgId, deviceId, source, timezone
    scripts/            # poller, ics generator
    state/              # processed_ids.json, run.log (git-ignored)
    output/
      Reminders_2026-07-23.md
      events/*.ics       (git-ignored)
    NOTES.md            # what Phase 1 discovery found
  ```

## Timezones & relative dates

- Resolve "tomorrow" / "next Tuesday" against the **recording's timestamp**, not the moment the
  poller runs. A Friday note saying "tomorrow" means Saturday even if processed Monday.
- Use one clinic timezone everywhere (ask; default `America/New_York`). Store it in `config.json`.
- `.ics` files: emit `DTSTART`/`DTEND` in UTC (`...Z`) or with a `TZID`, and always include a
  `VALARM` so the operator gets a reminder. `make_ics.py` handles this.

## Classification quality

- When a note is genuinely ambiguous, put it under **Unclear `[UNCLEAR]`** in the triage note —
  never invent a calendar time. A wrong calendar event is worse than an unclear line.
- Always quote the **original transcript sentence** in the output so the operator can verify
  what the tool understood.
- Default follow-up date for untimed items: **+2 business days**.

## Error handling

- Any single note that fails to classify/emit must not crash the whole run — log it, skip it,
  leave its ID unprocessed so it retries. One bad note ≠ lost batch.
- Network errors → treat the run as a no-op, log, exit 0 (see `caching-and-state.md`).
- Mask the API key in every log line.

## Testing before the demo

- Feed the classifier a few canned transcripts (timed / untimed / idea / ambiguous) and confirm
  each lands in the right bucket and the `.ics` opens in the operator's calendar app.
- Run the poller twice in a row and confirm the second run produces **no duplicates**.
- Simulate a flaky-Wi-Fi late arrival: add an old ID to the fetch window and confirm the
  overlapping window + processed-IDs set handle it correctly.
- Verify `.env`, `state/`, `output/` are git-ignored before any commit.

## Plain-language operator UX

- Print a short human summary at the end of each run ("Added 1 calendar event, 2 follow-ups.
  Open output/Reminders_2026-07-23.md to review.").
- Optionally auto-open the day's triage note.
- Keep messages jargon-free; the operator is non-technical.
