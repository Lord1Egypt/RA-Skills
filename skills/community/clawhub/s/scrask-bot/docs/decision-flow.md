# Scrask decision flow

What happens between "user sends a screenshot" and "item saved in Calendar / Task list."

There are two sides to this flow. The **parser side** (`scripts/scrask_bot.py`) is stateless — it ingests a screenshot, decides what to extract, and emits a JSON intent with clarification questions baked in. The **bot side** (the OpenClaw agent running on Telegram / iMessage / Slack) is the conversation loop — it renders the parser's output, asks the clarification questions, and dispatches each item to the user's installed destination skill.

## Thresholds at a glance

| Threshold                       | Default | Where it gates                                                                 |
|---------------------------------|---------|--------------------------------------------------------------------------------|
| `FALLBACK_THRESHOLD`            | 0.60    | Worst per-field score below this → Claude reruns the parse.                    |
| `FALLBACK_IMPROVEMENT_MIN`      | 0.05    | Claude's result is only kept if its avg confidence beats Gemini by this much.  |
| `ACTIONABLE_THRESHOLD`          | 0.70    | Top-level `actionable_confidence` below this → "Is this actually an event/task?" |
| `TYPE_THRESHOLD`                | 0.70    | Per-item `type_confidence` below this → "Calendar or task list?"               |
| `FIELD_THRESHOLD`               | 0.70    | Per mandatory field: null or below this → targeted field clarification.        |
| `DEFAULT_CONFIDENCE_THRESHOLD`  | 0.75    | Legacy per-item gate. Only kicks in for items with no `confidences{}` block.   |

## 1. Parser side — what `scrask_bot.py` does

```mermaid
flowchart TD
    A[User sends screenshot] --> B[OpenClaw agent activates scrask-bot]
    B --> C[scrask_bot.py runs]

    C --> D{Provider mode}
    D -->|openclaw| OC[OpenClaw configured vision LLM]
    D -->|claude| E[Claude Opus parses]
    D -->|gemini| F[Gemini 2.0 Flash parses]
    D -->|auto| AR{Which keys are set?}

    AR -->|GEMINI_API_KEY| G[Gemini 2.0 Flash parses]
    AR -->|ANTHROPIC_API_KEY only| E
    AR -->|Neither| OC

    G --> H{Worst per-field<br/>score &lt; 0.60?}
    H -->|No| K[Use Gemini result]
    H -->|Yes + ANTHROPIC_API_KEY| I[Claude Opus reruns]
    H -->|Yes, no Claude key| K
    I --> J{Claude avg &gt; Gemini avg + 0.05?}
    J -->|Yes| L[Use Claude result]
    J -->|No| K

    E --> M[Raw parse_data]
    F --> M
    K --> M
    L --> M
    OC --> M

    M --> N{no_actionable_content == true<br/>OR items empty?}
    N -->|Yes| O[Return: 'couldn't find anything']
    N -->|No| P[For each raw item:<br/>shape_intent]

    P --> Q[Build clarifications]
    Q --> R{type_confidence &lt; 0.70?}
    R -->|Yes| S["Prepend type clarification:<br/>'Calendar or task list?'"]
    R -->|No| T[Skip type clarification]
    S --> U[Walk mandatory fields]
    T --> U

    U --> V[For each mandatory field:<br/>event/reminder = title, date, time<br/>task = title only]
    V --> W{Value is null/empty?}
    W -->|Yes| X[Append clarification<br/>reason: missing]
    W -->|No| Y{Per-field conf &lt; 0.70?}
    Y -->|Yes| Z[Append clarification<br/>reason: low_confidence]
    Y -->|No| AA[Field OK]
    X --> AB{More fields?}
    Z --> AB
    AA --> AB
    AB -->|Yes| V
    AB -->|No| AC[needs_confirmation = len of clarifications &gt; 0]

    AC --> AD{actionable_confidence &lt; 0.70?}
    AD -->|Yes| AE[needs_actionable_confirmation = true]
    AD -->|No| AF[Render summary_text]
    AE --> AF
    AF --> AG[Return JSON to bot]
```

## 2. Bot side — what the OpenClaw agent does with the parser output

```mermaid
flowchart TD
    A[Bot receives parser JSON] --> B{no_actionable_content?}
    B -->|Yes| C["Reply: 'couldn't find any event or task'<br/>End"]
    B -->|No| D{needs_actionable_confirmation?}

    D -->|Yes| E["Send: 'Is this actually an event or task?'"]
    E --> F{User reply}
    F -->|no / skip| G["Reply: 'Got it, skipped ✓'<br/>End"]
    F -->|yes| H[Process each item]
    D -->|No| H

    H --> I{Item needs_confirmation?}
    I -->|No| J[Route silently to destination skill]
    J --> K{destination}
    K -->|calendar| L["calctl / accli / apple-calendar /<br/>brainz-calendar / gcal-pro"]
    K -->|task| M["apple-reminders / things-mac /<br/>notion"]
    L --> N["Reply: 'Added to Calendar: ...'"]
    M --> O["Reply: 'Added to Tasks: ...'"]

    I -->|Yes| P[Walk clarifications in order]
    P --> Q{clarification.field}
    Q -->|type| R["Ask: 'Calendar or task list?'"]
    R --> S[Update item.destination]
    Q -->|date / time /<br/>location / title / etc.| T["Ask: 'What time is X?'<br/>(question from clarifications[])"]
    T --> U[Patch item field with reply]
    S --> V{More clarifications?}
    U --> V
    V -->|Yes| P
    V -->|No| W{Any reply was 'skip'?}
    W -->|Yes| X["Reply: 'Got it, skipped ✓'"]
    W -->|No| J

    H --> Y{More items?}
    Y -->|Yes| I
    Y -->|No| Z[Done]
    N --> Y
    O --> Y
    X --> Y
```

## 3. End-to-end happy path, narrated

Cleanest case — a meeting invite email screenshot with everything visible:

1. User sends screenshot. Bot acks: "Got it, analyzing…"
2. `scrask_bot.py` runs in auto mode. Gemini parses. Worst per-field score is 0.92. No Claude fallback.
3. `actionable_confidence` = 0.96. Above threshold, so no actionable gate.
4. `shape_intent` walks mandatory fields for `type: event` — title, date, time all present, all above 0.85. No clarifications. `needs_confirmation: false`.
5. Bot reads `needs_confirmation: false`, routes to `calctl` (first available calendar skill). Skill creates the event.
6. Bot replies: "📅 Added to Calendar: **Team Standup** — 2026-03-01 at 09:00"

## 4. End-to-end ambiguous path, narrated

Vague WhatsApp — "lets meet fri":

1. User sends screenshot. Bot acks.
2. Gemini parses. Time confidence is 0.0 (no time visible), date confidence is 0.60. Worst per-field score is 0.0, below 0.60 threshold → Claude reruns.
3. Claude's avg is 0.65, Gemini's was 0.55. Improvement 0.10 ≥ 0.05 → Claude result kept.
4. `actionable_confidence` = 0.85. No actionable gate.
5. `shape_intent` walks mandatory fields for `type: event`:
   - `title` OK (above threshold)
   - `date` below threshold → clarification `reason: low_confidence`
   - `time` is null → clarification `reason: missing`
   - `needs_confirmation: true`
6. Bot reads `clarifications[]` and asks: "I need to confirm: What date is meet on Friday? What time is meet on Friday?"
7. User replies. Bot patches the fields, routes to `calctl`, confirms "📅 Added to Calendar: …"

## 5. End-to-end actionable-gate path, narrated

A flyer that might just be content, not an invite:

1. User sends screenshot. Bot acks.
2. Parser runs. `actionable_confidence` = 0.55. Below 0.70 → `needs_actionable_confirmation: true`.
3. Bot leads with: "🤔 Is this actually an event or task? (55% sure) Reply **yes** to continue, or **no** to skip."
4. User: "no" → "Got it, skipped ✓". Done.
5. User: "yes" → continue into the per-item loop (steps 5 onward from the ambiguous narrative above).

## See also

- [`scripts/scrask_bot.py`](../scripts/scrask_bot.py) — the implementation. `shape_intent` is the most concept-dense function.
- [`SKILL.md`](../SKILL.md) — the bot-side instructions referenced by the OpenClaw agent.
- [`journal/entries/2026-05-25-2023-per-field-confidence-clarifications.md`](../journal/entries/2026-05-25-2023-per-field-confidence-clarifications.md) — why the confidence model is shaped this way.
