# Scrask architecture overview

A guide to how this skill is built. The first half is written for anyone,
technical or not. The second half goes into code-level detail.

---

## Part 1: For everyone

### What Scrask does

You take a screenshot on your phone. A WhatsApp message planning dinner.
An email invite. A flyer for an event. You send the screenshot to your AI
assistant. A few seconds later, the dinner is on your calendar, or the
reminder is in your task list. You did not type the title, the date, the
time, or the location. The AI read the screenshot, figured out what was
actionable, and saved it.

That is Scrask.

Specifically, Scrask is a parser. It does not save anything itself. It
looks at the screenshot, decides what is there, and tells your AI
assistant in a structured way: "this looks like a dinner event on Friday
at 7pm at Bombay Canteen, with Priya." Your assistant then routes that
information to whichever calendar or task app you have installed.

### Who does what

Three actors are involved when you send a screenshot:

**You.** You send a screenshot. Sometimes you answer a follow-up
question if the AI is unsure about something.

**The bot.** This is the AI assistant running on Telegram, iMessage,
Slack, or wherever you chat with it. The bot's job is to talk to you. It
receives your screenshot, asks Scrask to parse it, asks you any
follow-up questions, and saves the result to your calendar or task list.

**Scrask (the parser).** This is the code in this repo. It does one
thing: take a screenshot, return a structured description of what is in
it. It does not talk to you, save anything, or remember anything between
screenshots. It runs once, returns its answer, and exits.

The clean separation matters. The bot deals with conversations, network
calls, your accounts, your installed apps. Scrask deals only with
screenshots and language. Both stay simpler that way.

### The pipeline, in steps

When you send a screenshot, this is what happens:

1. The bot acknowledges: "Got it, analyzing..."
2. The bot runs Scrask with the screenshot as input.
3. Scrask sends the image to a vision AI (Gemini by default; Claude as
   backup if Gemini seems unsure).
4. The vision AI returns a structured guess: a list of events,
   reminders, or tasks it detected, with confidence scores attached.
5. Scrask normalizes that guess into a clean, routable plan, including a
   list of follow-up questions to ask you if anything is missing or
   shaky.
6. Scrask prints the plan to standard output, then exits.
7. The bot reads the plan. If everything is clear, it saves the item
   silently and confirms. If there are follow-up questions, it asks
   them.
8. You answer (or say "skip"). The bot patches the answers into the
   plan.
9. The bot saves the item to your calendar or task app and confirms.

Most of the interesting design decisions are in step 5.

### Two passes: why the AI does not do the whole job

The vision AI is great at perception and bad at decisions. Code is great
at decisions and incapable of perception. Scrask is split along that
line.

**First pass: perception.** The vision AI reads the screenshot and
produces a "what I saw" report: titles, dates, times, locations, with
confidence numbers attached. This is a probabilistic job. Same
screenshot, slightly different output each time.

**Second pass: decisions.** A Python function called `shape_intent`
takes the AI's report and produces a "what to do about it" plan: which
destination skill to invoke, whether the bot needs to ask follow-up
questions, which exact questions to ask. This is a mechanical job. Same
input, same output, every time.

The benefit: thresholds (the cutoffs that decide "is 0.7 confidence high
enough?") live in code, not in the AI's prompt. Change the threshold,
and every item gets re-evaluated consistently. The AI never has to know
what your thresholds are.

This pattern shows up everywhere AI meets engineering. Whisper
transcribes audio (perception); a separate program converts the
transcript into commands (decisions). A recommender model scores 1000
candidates (perception); business rules pick the final 10 (decisions).
Same split.

### Raw item vs shaped intent

The transformation that happens in step 5 is worth understanding by
example.

The vision AI returns a raw item. For a vague "lets meet fri" WhatsApp
message, the raw item might look like:

```json
{
  "type": "event",
  "title": "Meet on Friday",
  "date": "2026-05-29",
  "time": null,
  "location": null,
  "confidences": {
    "title": 0.70,
    "date": 0.60,
    "time": 0.0
  }
}
```

The AI is telling you what it saw, with its confidence in each piece. It
is NOT telling you what to do about the missing time.

After `shape_intent` runs, that raw item becomes a shaped intent. A plan
for action:

```json
{
  "type": "event",
  "destination": "calendar",
  "title": "Meet on Friday",
  "date": "2026-05-29",
  "time": null,
  "needs_confirmation": true,
  "clarifications": [
    {
      "field": "date",
      "question": "What date is Meet on Friday?",
      "reason": "low_confidence"
    },
    {
      "field": "time",
      "question": "What time is Meet on Friday?",
      "reason": "missing"
    }
  ]
}
```

Note what changed. A `destination` ("where does this go?"). A
`needs_confirmation` flag ("does the bot need to ask anything?"). A
`clarifications` list ("here are the exact questions to ask"). The AI's
data is preserved unchanged. The new fields are derived.

Most importantly, the clarification questions are now strings. The
model's confidence scores have been translated into actionable
human-readable questions. Whoever consumes this (the bot) no longer
needs to know anything about thresholds or per-field confidences. It
just sees: "this item needs confirmation, here are two questions to
ask."

### Confidence as a first-class concept

A subtle but important design choice: every field carries its own
confidence, not just the item as a whole.

The old way (and how most parsers work) was a single `confidence: 0.6`
number per item. That can only tell you "the model is somewhat unsure."
It cannot tell you whether the model is unsure about the title, the
date, the time, or all three.

The new way is three layers of confidence:

- `actionable_confidence`: is this screenshot actually about an event or
  task at all?
- `type_confidence`: is this a calendar event, or does it belong on the
  task list?
- `confidences.{field}`: how sure are we about each individual field?

Each layer can fail independently. The screenshot might be clearly
actionable (high `actionable_confidence`), clearly an event (high
`type_confidence`), but missing a time (low `confidences.time`). With
per-field confidence, the bot can ask only what it actually needs ("What
time?") instead of a generic "Is this right?"

The user experience improves. Fewer questions, more specific questions,
less re-typing of stuff that was already clearly visible.

### Why the parser does not loop

When you answer a clarification, the bot patches your answer directly
into the item and dispatches. The parser does NOT run again.

This is deliberate. Once you have spoken, the data is no longer a guess.
There is no confidence threshold to re-check, no clarification to
maybe-emit. The fields are ground truth.

Re-running the parser would also mean re-calling the vision AI on the
same screenshot. Wasteful, slow, and probably worse than the original
parse. The AI does not know anything new. Your answer is more
authoritative than any re-perception could be.

So `shape_intent` is idempotent in a one-shot sense. It runs once,
produces a plan, and the plan is then executed by the bot. The plan
includes the patches the bot can apply when you answer. No recursion, no
re-running, no state held inside the parser.

---

## Part 2: For technical readers

### File and code map

The whole skill is small. The interesting parts:

```
scrask-bot/
├── SKILL.md                         # Operator instructions for the OpenClaw agent
├── README.md                        # Quickstart and overview
├── scripts/
│   └── scrask_bot.py                # Everything: providers, shape_intent, summary
└── docs/
    ├── ARCHITECTURE_OVERVIEW.md     # This file
    ├── decision-flow.md             # Mermaid diagrams + threshold table
    ├── decision-flow.html           # Same, interactive (clickable nodes)
    └── example-walkthrough.md       # A concrete USER/BOT/PARSER transcript
```

`scripts/scrask_bot.py` is one file because the surface area is small
enough that splitting it into modules would obscure more than it would
clarify. Organised top-down:

| Lines | Section | What lives there |
|---|---|---|
| 47-95 | Constants | Thresholds, model names, mandatory-field tables, clarification question templates |
| 97-249 | Prompt | `SYSTEM_PROMPT` and `USER_PROMPT_TEMPLATE`, the JSON schema and rules the vision AI follows |
| 254-316 | Providers | `parse_with_claude`, `parse_with_gemini`, prompt formatting |
| 318-433 | Routing | `parse_screenshot`, `_parse_with_auto_fallback`, confidence aggregation helpers |
| 436-535 | Normalization | `shape_intent`, turns raw items into shaped intents |
| 543-619 | Output | `format_summary`, chat-ready preview text |
| 622+ | CLI | argparse, `main()`, error handling |

The single seam between AI and code is `shape_intent`. Everything before
is provider-specific glue. Everything after is bot-side concern that
does not live in this repo.

### `shape_intent` in detail

The function ([`scripts/scrask_bot.py:436-535`](../scripts/scrask_bot.py)) does
six things, in order:

1. **Decide where the item routes.** `destination = "calendar" if
   item_type == "event" else "task"`. Three types collapse into two
   routing destinations.
2. **Synthesize the legacy `confidence` number.** Honour what the model
   gave; otherwise compute `min(confidences.values())`. Worst-field-wins
   when deriving.
3. **Backfill defaults for missing decision scores.** `type_confidence`
   falls back to the per-item confidence if absent; `title` falls back
   to `"this item"` for question templating.
4. **Build `clarifications[]`.** Type-level clarification first if
   `type_confidence < TYPE_THRESHOLD`. Then loop the mandatory-field
   list for this item type, appending clarifications for fields that
   are missing or low-confidence. Question text comes from the
   `CLARIFICATION_QUESTIONS` lookup table at
   [`scrask_bot.py:74-85`](../scripts/scrask_bot.py), with `{title}`
   interpolated.
5. **Derive `needs_confirmation`.** `bool(clarifications)` plus a
   legacy fallback for items with no `confidences{}` block.
6. **Return the shaped dict.** Every original field passed through,
   with three optional defaults filled (`recurrence` → `"none"`,
   `priority` → `"medium"`, `already_in_calendar_hint` → `False`).

The two lookup tables it depends on, also in
[`scrask_bot.py:65-85`](../scripts/scrask_bot.py):

```python
MANDATORY_FIELDS_BY_TYPE = {
    "event":    ["title", "date", "time"],
    "reminder": ["title", "date", "time"],
    "task":     ["title"],
}

CLARIFICATION_QUESTIONS = {
    "title":        "What should I call this?",
    "date":         "What date is {title}?",
    "time":         "What time is {title}?",
    "end_time":     "When does {title} end?",
    "location":     "Where is {title}?",
    "participants": "Who is going to {title}?",
    "description":  "Any details I should add for {title}?",
    "priority":     "How urgent is {title}?",
    "type":         "Should {title} go on your calendar or task list?",
}
```

To add a new clarification surface you edit two of these three pieces
(the table or the templates plus `shape_intent`'s loop). To change
which fields are mandatory for an item type, you edit one.

### Provider routing and fallback

In `auto` mode (the default), Gemini 2.0 Flash parses first because it
is fast and cheap. If the **worst per-field confidence** across the
result is below `FALLBACK_THRESHOLD` (0.60), Claude Opus reruns the
parse. Claude's result is kept only if its average confidence beats
Gemini's by at least `FALLBACK_IMPROVEMENT_MIN` (0.05). Otherwise the
Gemini result is retained even though the fallback was attempted.

The aggregation across all per-field scores happens in `_min_confidence`
and `_avg_confidence`. Both walk every value in every item's
`confidences{}` plus `type_confidence` plus the legacy `confidence`,
producing one min and one average across the whole result.

This is finer-grained than the v3 behaviour, which looked at a single
per-item confidence number. The new approach catches cases where the
model is broadly confident but missed a single critical field.

### Configuration knobs

Six thresholds in total. Three new ones drive the clarification
mechanism; two govern provider fallback; one is kept for backward
compatibility.

| Threshold | Default | What it gates |
|---|---|---|
| `FALLBACK_THRESHOLD` | 0.60 | Worst per-field score below this triggers Claude rerun. |
| `FALLBACK_IMPROVEMENT_MIN` | 0.05 | Claude's avg must beat Gemini's by this to be kept. |
| `ACTIONABLE_THRESHOLD` | 0.70 | Top-level "is this actually an event/task?" gate. |
| `TYPE_THRESHOLD` | 0.70 | "Calendar or task list?" gate per item. |
| `FIELD_THRESHOLD` | 0.70 | Per mandatory field: null or below triggers field clarification. |
| `DEFAULT_CONFIDENCE_THRESHOLD` | 0.75 | Legacy per-item gate. Kept for callers without per-field info. |

All six are exposed as CLI flags on `scripts/scrask_bot.py` and as
`config` entries the OpenClaw agent passes from `SKILL.md`. Tuning is
done by editing the constant or passing the flag, then restarting. No
model re-prompting required.

### The bot side, restated

The bot lives in a separate repo (the OpenClaw agent) and does not
share code with Scrask. It interacts with Scrask through one contract:
the stdout JSON. After reading that JSON it makes three branching
decisions:

1. `no_actionable_content` → reply "couldn't find anything," stop.
2. `needs_actionable_confirmation` → ask "is this actually an event or
   task?" first, then proceed only if the user says yes.
3. Per item, `needs_confirmation` → either dispatch silently to the
   destination skill, or walk `clarifications[]` asking each question
   in order, patching `item[field]` (or `item["destination"]` for
   `field == "type"`) with the user's reply, then dispatch.

Destination skill preference order is defined in `SKILL.md`. Calendar:
calctl → accli → apple-calendar → brainz-calendar → gcal-pro. Task:
apple-reminders → things-mac → notion. The bot picks the first
installed one.

### Backward compatibility

The new schema is additive. Old v3 items (with a single per-item
`confidence` and no `confidences{}` block) still flow through
`shape_intent` correctly: the function detects the absence of the
per-field block, falls back on the legacy `DEFAULT_CONFIDENCE_THRESHOLD`
gate, and produces the same `needs_confirmation` decision the v3 code
would have made.

This means downstream callers that branch on `item["confidence"]` keep
working. The synthesized value is `min(confidences.values())`, which
preserves the worst-case semantic the legacy code expected.

---

## Design principles, recap

1. **Separation of perception and decision.** The vision AI guesses;
   code routes.
2. **Per-field confidence over per-item confidence.** Lets the bot ask
   only what it needs.
3. **Stateless parser.** One call, one plan, exit. No loops, no memory.
4. **Targeted clarifications.** The parser pre-formats questions so the
   bot does not have to.
5. **Defaults belong downstream.** The parser reports what it saw, not
   what to assume. Destination skills apply their own defaults.
6. **Backward compatibility.** Old fixtures with legacy `confidence`
   numbers still route correctly.

## See also

- [`docs/decision-flow.md`](decision-flow.md): flowcharts of the parser
  and bot decision flow.
- [`docs/decision-flow.html`](decision-flow.html): interactive version
  of the same, with clickable nodes.
- [`docs/example-walkthrough.md`](example-walkthrough.md): a concrete
  end-to-end transcript.
- [`scripts/scrask_bot.py`](../scripts/scrask_bot.py): the
  implementation.
- [`SKILL.md`](../SKILL.md): what the OpenClaw agent is told about how
  to use this skill.
