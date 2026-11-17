---
name: voice-notes-to-reminders
description: Turn NxVET voice notes / button recordings into LOCAL reminders, calendar events (.ics), and a daily triage note — entirely on the user's own machine, no send paths. Use when someone wants to poll NxVET (labels or NxHub conversations) for spoken notes and turn "follow up with X about Y next Tuesday" into a calendar file + triage line.
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - NXVET_API_KEY
    primaryEnv: NXVET_API_KEY
    emoji: "🎙️"
    homepage: https://api.nx.vet/skills.html#voice-notes
---

# Voice notes → reminders & calendar (local-only)

> **A NxVET recipe for AI coding agents.** Point Claude Code, Codex, Cursor, or any
> LLM-based agent at this file and say *"Read SKILL.md and implement it — start with Phase 0."*
> The recipe is agent-neutral: it's plain Markdown plus two dependency-free Python scripts.
> See `INSTALL.md` for how to load it into a specific agent.

Build a small, **local-only** tool that polls the NxVET API for voice notes (button
recordings), interprets each transcript, and produces:

- a **daily triage note** (`output/Reminders_YYYY-MM-DD.md`) — sections for *Scheduled*,
  *Follow-ups*, *Ideas*, *Unclear*, each line quoting the original transcript, and
- **calendar events as `.ics` files** (`output/events/…`) the user double-clicks to add to
  Outlook or Google Calendar — no OAuth, works for both.

The whole point is the **privacy architecture**: NxVET's servers only ever see the raw voice
note. The calendar, the triage note, and everything the tool *does* with a note live entirely
on the user's machine. There is **no send path** — the tool only creates drafts and files for
the user to accept.

This recipe is generic: it works for any NxVET organization with an API key. Adapt the person
names, device name, schedule, and timezone to whoever is running it.

### Prerequisites (tell the user if they're missing any)

This skill needs three things. If the user doesn't have them, point them to these links before
building — the tool can't work without them:

1. **A NxVET account** — sign up at https://app.nx.vet/ if the clinic isn't set up yet.
2. **A NxVET API key** — https://app.nx.vet/integrations → API Keys tab (starts `nxvet_sk_`).
3. **An NxHUB device** — the recorder that captures the voice notes this skill processes. If
   they don't have one, it's at https://nx.vet/products/nxhub. (If they already record on an
   NxHUB, skip this.)

---

## Ground rules (non-negotiable)

1. **Local-only.** The only network calls are authenticated `GET`s to the NxVET API
   (`https://app.nx.vet`). No telemetry, no third-party services, no email, no posting anywhere.
2. **No send paths.** Produce *files* (markdown notes, `.ics`). Never send an email, text, or
   meeting invite on anyone's behalf. Adding a real "send" step is a separate, explicitly
   approved feature — not part of this tool.
3. **Secrets hygiene.** The API key lives in `.env` as `NXVET_API_KEY=nxvet_sk_...`. Add `.env`
   to `.gitignore` if a repo is initialized. Never print the full key; never commit it; never
   paste it anywhere that leaves the machine. See `reference/security.md`.
4. **Idempotency.** Never process the same note twice. Keep `state/processed_ids.json` of
   handled label/conversation IDs and always skip them. See `reference/caching-and-state.md`.
5. **Non-technical operator.** Explain what you're doing in plain language, ask before
   installing runtimes/packages, and keep everything inside the one project folder.

---

## How to build it — phases

Work through these in order. Confirm each phase works before moving on. The reference files
carry the API quirks, security rules, and state/caching design — read them; don't re-derive.

### Phase 0 — Connect and verify

1. Ask the operator for the API key. Write `.env` with `NXVET_API_KEY=...`. Confirm `.env` is
   git-ignored.
2. Prefer the **hosted MCP server** over raw REST when your agent supports MCP (it exposes ~22
   NxVET tools directly):
   ```bash
   claude mcp add nxvet --transport http https://mcp.nx.vet/mcp \
     --header "Authorization: Bearer nxvet_sk_YOUR_API_KEY"
   ```
   (Codex/Cursor/other clients: add the same `https://mcp.nx.vet/mcp` server per their config —
   see https://api.nx.vet/mcp.html.) For headless scripts, a small REST client is fine — see
   `reference/nxvet-api.md`.
3. Call the identity tool (`get_identity`) or `GET /api/auth/me`. Confirm HTTP 200 and capture
   the `organizationId`. Save it to `config.json`.
4. `GET /api/devices?organizationId=...`; show the operator the device list and save the
   chosen `deviceId` to `config.json`.

### Phase 1 — Find where the voice notes land (discovery)

Button recordings appear as **labels** (records) OR as **NxHub conversations** depending on the
device. Determine this empirically — do not assume:

1. Ask the operator to press the device button and record a test note, e.g.
   *"Test reminder — follow up with Alex tomorrow at 10am."*
2. Wait ~2 minutes, then list recent **labels** and recent **NxHub conversations** for the
   org/device, newest first.
3. Whichever collection the test note appears in is the source of truth. Fetch its detail and
   confirm you can read the transcript text (list responses have `null` transcripts — always
   fetch the detail).
4. Record the finding in `config.json` (`"source": "labels"` or `"source": "nxhub"`) and write
   a short `NOTES.md` with what you learned.

### Phase 2 — The poller

A helper is provided: `{baseDir}/scripts/nxvet_poll.py` (stdlib-only Python 3; no pip installs).
Run it with `python3 {baseDir}/scripts/nxvet_poll.py`. It reads
`.env` + `config.json`, fetches new recordings for the configured source, skips already-processed
and still-empty transcripts, and emits new transcripts as JSON for the classifier. Run it or
adapt it. It must:

1. Load `config.json` + `state/processed_ids.json`.
2. Fetch recordings since the last run — **overlap the window** (re-check the last 24h against
   processed IDs) so late-arriving notes from flaky Wi-Fi are not missed.
3. Skip already-processed IDs; skip items whose transcript is still empty (`"{}"` / null) —
   leave those for the next run, do **not** mark them processed.
4. Hand each new transcript to the classifier (Phase 3).
5. Append results to the outputs (Phase 4), then mark the ID processed.
6. Log a one-line summary per run to `state/run.log`.

### Phase 3 — Classify each voice note

The agent does the interpretation. For each transcript pick one bucket:

| Bucket | Signal | Output |
|---|---|---|
| **Timed commitment** | Explicit date/time ("10am tomorrow", "next Tuesday") | `.ics` event + triage line under *Scheduled* |
| **Follow-up reminder** | "Follow up with X about Y", no firm time | triage line under *Follow-ups* (suggested date: +2 business days) |
| **Idea / note** | No action, just a thought | *Ideas* section of the triage note |
| **Ambient recording** | Long multi-speaker conversation (devices capture ambient audio alongside button notes — can be 20k+ chars) | One-line summary under *Ambient* in the triage note; do NOT extract every incidental "need to" from chatter as a reminder |

Devices record ambient conversations in the same label type as button voice notes — expect
both. Short single-speaker notes are usually deliberate voice notes; long multi-speaker
transcripts are usually ambient. A buried explicit commitment in an ambient recording
("let's meet Tuesday at 3") may still be surfaced, but flag it `[FROM AMBIENT]` so the
operator knows the context.

Extract **who** / **what** / **when**. Resolve relative dates against the **recording's
timestamp**, not the processing time (a note recorded Friday saying "tomorrow" means Saturday).
Use the operator's timezone (ask; default `America/New_York`). When genuinely ambiguous, put it
under *Unclear* flagged `[UNCLEAR]` rather than guessing a calendar slot.

### Phase 4 — Outputs (MVP)

Use `python3 {baseDir}/scripts/make_ics.py --help` to inspect the bundled calendar-file generator,
then use it to generate calendar files.

1. **Daily triage note** `output/Reminders_YYYY-MM-DD.md` — sections *Scheduled*, *Follow-ups*,
   *Ideas*, *Unclear*; every line quotes the original transcript sentence so the operator can
   verify.
2. **Calendar events** `output/events/2026-07-15_follow-up-sally.ics` — standard iCalendar
   `VEVENT` (summary, description containing the original transcript, start/end, and a `VALARM`
   reminder). Double-clicking adds it to Outlook *or* Google Calendar — no OAuth, no creds. Ask
   the operator to double-click one as a test.
3. Optionally open the day's triage note at the end of each run.

Do **not** integrate directly with Outlook/Google APIs in the MVP.

### Phase 5 — Run on a schedule

- Ask how often. Sensible default: **every 30 min during working hours + a 4am full sweep** so
  the prior day is triaged before the operator starts.
- Use the OS-native scheduler (detect the OS first): `launchd` on macOS, Task Scheduler on
  Windows, `cron` on Linux. A missed run must just catch up on the next one — the processed-IDs
  state makes that safe.
- Log clearly when the API is unreachable (Wi-Fi is often flaky; the device queues recordings
  and they arrive late). The overlapping since-last-run window (Phase 2) tolerates this.

### Stretch (only after MVP works end-to-end)

- **Power Automate / webhook bridge** for users who want events pushed into Outlook: POST each
  timed commitment to a user-built "When an HTTP request is received" flow. Keeps their creds
  inside their own automation. Document as a demo, don't build the send path into this tool.
- **Duplicate for a second person**: second instance, own `.env` + own state folder, same code.
- **Done-detection**: cross-check follow-ups so the tool stops nagging completed items
  (design-only).

---

## Acceptance checklist (the demo)

- [ ] Press device button, speak a reminder with a date/time → within one poll an `.ics`
      appears; double-click adds it to the calendar.
- [ ] Speak an untimed follow-up → it appears in today's triage note.
- [ ] Re-running the poller duplicates nothing.
- [ ] Drop Wi-Fi mid-recording → reconnect → note still arrives and is processed on a later poll.
- [ ] Show `.env` + state files to demonstrate no credentials or clinic data ever leave the machine.

## Reference files

- `reference/nxvet-api.md` — endpoints, auth, MCP setup, and the data-format gotchas.
- `reference/security.md` — secrets, local-only guarantee, no-send rule, what to send if stuck.
- `reference/caching-and-state.md` — idempotency, the overlapping poll window, HTTP caching,
  rate-limit backoff.
- `reference/good-practices.md` — code layout, error handling, timezone handling, testing.
