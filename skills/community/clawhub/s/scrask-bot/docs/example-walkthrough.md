# Example walkthrough — a real conversation, end to end

A vague WhatsApp screenshot is the most useful example because every
interesting part of the pipeline fires: Gemini parses, Claude is invoked
as fallback, `shape_intent` emits per-field clarifications, the bot asks
them, the user replies, and the patched item is dispatched to a calendar
skill.

Three participants in the transcript:

- **USER** — the person who sent the screenshot.
- **BOT** — the OpenClaw agent running on Telegram / iMessage / Slack.
  Lives in a separate codebase. Drives the conversation.
- **PARSER** — `scripts/scrask_bot.py` in this repo. Stateless, runs once
  per screenshot, prints JSON to stdout, exits. Never talks to the user
  directly.

## The transcript

```
USER  → [sends screenshot of "lets meet fri" message]
BOT   → "📸 Got it — analyzing your screenshot..."

[bot spawns parser process]
PARSER → Gemini parse → low confidence on time → Claude rerun →
         shape_intent → clarifications: [date, time] →
         prints JSON to stdout → exits

[bot reads stdout]
BOT   → "🤔 Need a quick check on **Meet on Friday**
         📅 Event so far:
           Title: Meet on Friday
           Date:  2026-05-29
           Time:  ?

         I need to confirm:
           • What date is Meet on Friday?
           • What time is Meet on Friday?

         Reply with the details, or **skip** to drop this one."

USER  → "May 30, 7pm"

BOT   → [parses reply, patches item.date = "2026-05-30", item.time = "19:00"]
BOT   → [invokes calctl with patched item]
BOT   → "📅 Added to Calendar via calctl: **Meet on Friday** — 2026-05-30 at 19:00"
```

## What is happening at each step

**Acknowledgement** — the bot replies immediately so the user knows the
screenshot landed and is being processed. Per `SKILL.md` Step 1.

**Provider routing** — Scrask runs in `auto` mode (the default). Gemini
2.0 Flash parses first because it is fast and cheap. The model returns
a `time` confidence of `0.0` (no time visible in "lets meet fri"). That
trips `FALLBACK_THRESHOLD = 0.60`, so Claude Opus reruns the parse.
Claude's average confidence beats Gemini's by more than
`FALLBACK_IMPROVEMENT_MIN = 0.05`, so Claude's result is kept.

**Normalisation** — `shape_intent` takes Claude's raw item and walks
the mandatory fields for `type: event` (title + date + time). It finds
`date` confidence below `FIELD_THRESHOLD = 0.70` and `time` value
missing entirely. Two clarifications are appended to
`clarifications[]`, and `needs_confirmation` is set to `true`.

**Preview** — `format_summary` renders the chat-ready preview text.
That preview is the literal block the bot sends to the user. The
clarification questions ("What date is…", "What time is…") come from
the `CLARIFICATION_QUESTIONS` lookup table with the item title
interpolated in.

**Patch and dispatch** — when the user replies, the bot parses the
free-text answer ("May 30, 7pm" → ISO date and time), writes the
values onto the item dict in memory, and invokes the destination
skill. `shape_intent` does not run again. The parser process is long
gone by this point — it exited the moment it printed the JSON.

**Confirmation** — the bot sends one line back acknowledging the
write. Same pattern for every save, regardless of whether
clarifications were involved.

## Other paths

For the clean-meeting-invite happy path (zero clarifications, silent
dispatch) and the actionable-gate path (the parser is unsure whether
the screenshot is about an event at all), see the narrated sections
at the bottom of [`decision-flow.md`](decision-flow.md) — or open
[`decision-flow.html`](decision-flow.html) for the same content with
interactive flowcharts.
