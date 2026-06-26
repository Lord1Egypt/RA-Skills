# Pre-Continuation Checks

Run these checks **in order** at every gate point: between Phase 2 steps, after each Phase 3 merge, after the retrospective, and before re-entering Phase 0 — whether triggered by a user reply, a timer firing, or the automatic loop.

## Channel Reconnect (run first, before the numbered checks)

If `NOTIFY_SOURCE` is not `"terminal"` (i.e. a channel like Telegram is configured), run `/reload-plugins` now. This is a **built-in Claude Code CLI command** — do NOT invoke it via the Skill tool, just execute it directly. This is a no-op when the plugin is already connected, and silently restores it when it has dropped. No user-visible output needed unless the channel was actually missing.

**Harness note:** Checks 2 and 3 require session state data. On Claude Code, this is available via the session-state hook installed by `/bad setup` (Step 3). On other harnesses this data may not be available — each check gracefully skips if its fields are absent.

Read the current session state using the Bash tool:

```bash
cat ".claude/bad-session-state.json" 2>/dev/null || echo "{}"
```

Parse the output as JSON. The relevant fields:

- `context_window.used_percentage` — 0–100, percentage of context window consumed (treat null as 0)
- `rate_limits.five_hour.used_percentage` — 0–100 (Claude Code Pro/Max only)
- `rate_limits.five_hour.resets_at` — Unix epoch seconds when the 5-hour window resets
- `rate_limits.seven_day.used_percentage` — 0–100 (Claude Code only)
- `rate_limits.seven_day.resets_at` — Unix epoch seconds when the 7-day window resets

**If the file does not exist** — print `"⚠️ Pre-Continuation: session state unavailable (.claude/bad-session-state.json missing — check that the session-state hook is installed via /bad setup Step 3). Skipping rate limit checks."` and proceed.

**If a specific field is absent** — silently skip only that check. If the file exists but `rate_limits` is entirely absent, print `"⚠️ Pre-Continuation: rate limit data not in session state — skipping usage checks."` once (not on every gate).

---

## Check 1: Context Window

If `context_window.used_percentage` **> `CONTEXT_COMPACTION_THRESHOLD`**:

1. Print: `"⚠️ Context window at {usage}% — compacting before continuing."`
2. Compact context using your platform's mechanism (e.g. `/compact` on Claude Code). Wait for it to complete.

---

## Check 2: Five-Hour Usage Limit

If `rate_limits.five_hour.used_percentage` is present and **> `API_FIVE_HOUR_THRESHOLD`**:

1. Convert reset epoch to human-readable time:
   ```bash
   # macOS
   date -r {resets_at}
   # Linux
   date -d @{resets_at}
   ```
2. Print: `"⏸ 5-hour usage limit at {usage}% — auto-pausing until reset at {reset_time}. BAD will resume automatically."`
3. **If `TIMER_SUPPORT=true`:** compute a cron expression 10 minutes after the reset epoch (to avoid a false positive if the reset lands slightly late) and schedule a resume:
   ```bash
   # macOS
   date -r $(( {resets_at} + 600 )) '+%M %H %d %m *'
   # Linux
   date -d @$(( {resets_at} + 600 )) '+%M %H %d %m *'
   ```
   Call `CronCreate`:
   - `cron`: expression from above
   - `recurring`: `false`
   - `prompt`: `"BAD_RATE_LIMIT_TIMER_FIRED (five_hour) — The 5-hour rate limit window has reset. Re-check five_hour.used_percentage; if now below API_FIVE_HOUR_THRESHOLD, continue with Pre-Continuation Check 3 (seven-day). If still too high, schedule another pause until the next reset time."`

   Save the job ID. Do not ask the user for input — resume automatically when `BAD_RATE_LIMIT_TIMER_FIRED` arrives.

4. **If `TIMER_SUPPORT=false`:** print the reset time and wait for the user to reply when they're ready to continue. Then re-check the limit before proceeding.

---

## Check 3: Seven-Day Usage Limit

If `rate_limits.seven_day.used_percentage` is present and **> `API_SEVEN_DAY_THRESHOLD`**:

1. Convert reset epoch to human-readable time:
   ```bash
   # macOS
   date -r {resets_at}
   # Linux
   date -d @{resets_at}
   ```
2. Print: `"⏸ 7-day usage limit at {usage}% — auto-pausing until reset at {reset_time}. BAD will resume automatically."`
3. **If `TIMER_SUPPORT=true`:** compute a cron expression 10 minutes after the reset epoch (to avoid a false positive if the reset lands slightly late) and schedule a resume:
   ```bash
   # macOS
   date -r $(( {resets_at} + 600 )) '+%M %H %d %m *'
   # Linux
   date -d @$(( {resets_at} + 600 )) '+%M %H %d %m *'
   ```
   Call `CronCreate`:
   - `cron`: expression from above
   - `recurring`: `false`
   - `prompt`: `"BAD_RATE_LIMIT_TIMER_FIRED (seven_day) — The 7-day rate limit window has reset. Re-check seven_day.used_percentage; if now below API_SEVEN_DAY_THRESHOLD, continue with Phase 0. If still too high, schedule another pause until the next reset time."`

   Save the job ID. Resume automatically when `BAD_RATE_LIMIT_TIMER_FIRED` arrives.

4. **If `TIMER_SUPPORT=false`:** print the reset time and wait for the user to reply when ready. Then re-check before proceeding.

---

Only after all applicable checks pass, proceed with the next step (or re-run Phase 0, if that is what triggered this gate).
