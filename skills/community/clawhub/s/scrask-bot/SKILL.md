---
name: scrask-bot
version: 4.3.0
description: >
  When the user sends a screenshot via any chat surface (Telegram, iMessage, Slack, etc.),
  parse it for events and tasks using OpenClaw's configured vision LLM by default, with
  optional Gemini fast-path and Claude fallback for users who bring their own keys. Then
  delegate creation to the user's installed calendar / task skills. Scrask does not write
  to any store itself; it emits structured intent and the agent routes it.
author: sandip
metadata:
  openclaw:
    emoji: "🦞"
    # Invocation: implicit by default (agent reads the Trigger Conditions section
    # of this manifest and routes), with explicit override via the aliases below.
    # If any alias appears at the start of a user message (with or without `@`
    # or `/` prefix), the platform must dispatch to scrask regardless of the
    # implicit trigger conditions.
    invocation:
      mode: hybrid              # 'implicit' | 'explicit' | 'hybrid'
      aliases:
        - scrask
        - "scrask this"
        - screenshot
        - "screenshot to calendar"
    # No mandatory env vars. Default 'auto' provider routing uses OpenClaw's
    # configured vision LLM when no skill-level keys are set, so the skill works
    # out of the box.
    requires:
      env: []
      bins:
        - python3
    optional_env:
      # GEMINI_API_KEY: enables the cheap+fast Gemini-first routing in 'auto' mode,
      #   and is required if you pin --provider gemini.
      # ANTHROPIC_API_KEY: enables Claude fallback in 'auto' mode (when Gemini
      #   confidence is shaky), and is required if you pin --provider claude.
      - GEMINI_API_KEY
      - ANTHROPIC_API_KEY
    suggests:
      # Calendar destination skills (any one is enough)
      - calctl
      - accli
      - apple-calendar
      - brainz-calendar
      - gcal-pro
      # Task destination skills (any one is enough)
      - apple-reminders
      - things-mac
      - notion
    config:
      vision_provider:
        type: string
        description: >
          'auto' (default) routes by what you have: GEMINI_API_KEY → Gemini-first
          with Claude fallback; else ANTHROPIC_API_KEY → Claude only; else falls
          back to OpenClaw's configured vision LLM. 'openclaw' always uses the
          platform LLM. 'gemini' / 'claude' pin a specific provider (and require
          the matching key).
        default: auto
      fallback_threshold:
        type: number
        description: "Worst per-field confidence floor for auto mode. If any per-field score drops below this, Claude reruns the parse."
        default: 0.60
      timezone:
        type: string
        description: "User's IANA timezone. Used when none is detected in the screenshot."
        default: "UTC"
      confidence_threshold:
        type: number
        description: "Legacy 0.0–1.0 per-item gate. Kept for backward-compatible callers; the new thresholds below drive clarification behaviour."
        default: 0.75
      actionable_threshold:
        type: number
        description: "Top-level 'is this actually an event/task?' gate. Below this, the parser flags needs_actionable_confirmation."
        default: 0.70
      type_threshold:
        type: number
        description: "Per-item 'calendar or task list?' gate. Below this type_confidence, the parser emits a type clarification."
        default: 0.70
      field_threshold:
        type: number
        description: "Per mandatory field. Below this confidence (or null value) the parser emits a targeted clarification question for that field."
        default: 0.70
---

# Scrask Bot

## Overview

Scrask is a **screenshot-to-intent parser**. The user sends a screenshot via whatever chat surface
they have wired into OpenClaw (Telegram, iMessage, Slack, etc.). Scrask:

1. Decides whether the screenshot contains any actionable content (event, reminder, task). If not, ignores it.
2. Extracts every actionable item — a single screenshot may yield both an event and a task.
3. Emits structured intent JSON.
4. The OpenClaw agent then delegates each item to the user's installed destination skill:
   - `destination: "calendar"` → `calctl` / `accli` / `apple-calendar` / `brainz-calendar` / `gcal-pro` / etc.
   - `destination: "task"` → `apple-reminders` / `things-mac` / `notion` / etc.

Scrask never writes to a store directly. No service account JSON, no OAuth, no API keys for the
calendar/task layer — that's the destination skill's job.

## Invocation

Scrask is invoked in two ways. The platform tries explicit invocation first; if no alias matches, it falls back to the implicit trigger conditions.

### Explicit override (checked first)

If the user message begins with any of these aliases (case-insensitive, with or without a `@` or `/` prefix), the platform dispatches to Scrask regardless of the implicit conditions below:

- `scrask`
- `scrask this`
- `screenshot`
- `screenshot to calendar`

Examples that force-route to Scrask:

- `scrask this` (with an attached image)
- `@scrask` (with an attached image)
- `/scrask` (with an attached image)
- `screenshot to calendar` (with an attached image)

When invoked explicitly with no image attached, Scrask responds with a brief prompt asking the user to attach a screenshot, then stops. Do not run the parser without an image.

### Implicit (default, used when no alias matches)

The OpenClaw agent reads the incoming message and activates Scrask when:

1. The user sends a message in any connected chat surface that contains an **image attachment**.
2. The image appears to be a **screenshot** — not a photo of a person, place, or physical object.
3. No other skill has already claimed the image.

Do not activate (implicitly) for:

- Photos of people, places, food, scenery.
- Screenshots of code, errors, or UI bugs (leave for other skills).
- Images the user explicitly asks to edit, describe, or analyze for another purpose.

The implicit path is the one users will hit by default. The explicit aliases exist for two cases:

1. **Debugging / power-user override** — force Scrask to run on an ambiguous image the agent would otherwise route elsewhere (or skip).
2. **Recovery** — if the agent misses an obvious screenshot, the user can recover with `scrask this` instead of resending.

## Step-by-Step Instructions

### Step 1: Acknowledge Immediately

Reply on the user's current chat surface so they know the skill is working:

> "📸 Got it — analyzing your screenshot..."

### Step 2: Run the Parser

```bash
python3 {baseDir}/scripts/scrask_bot.py \
  --image-path "<path-to-temp-image>" \
  --provider "$CONFIG_VISION_PROVIDER" \
  --timezone "$CONFIG_TIMEZONE" \
  --confidence-threshold "$CONFIG_CONFIDENCE_THRESHOLD" \
  --actionable-threshold "$CONFIG_ACTIONABLE_THRESHOLD" \
  --type-threshold "$CONFIG_TYPE_THRESHOLD" \
  --field-threshold "$CONFIG_FIELD_THRESHOLD"
```

The script reads credentials from the environment — never pass them on the command line.
In default `auto` mode it routes by what is available:

- `GEMINI_API_KEY` set → Gemini-first with Claude fallback (cheap + fast path).
- `ANTHROPIC_API_KEY` set (no Gemini key) → Claude only.
- Neither set → OpenClaw's configured vision LLM, read from the platform-injected env vars
  `OPENCLAW_VISION_PROVIDER`, `OPENCLAW_VISION_KEY`, and optional `OPENCLAW_VISION_MODEL`.

So the skill works out of the box for any OpenClaw user with a vision-capable LLM
configured at the platform level. Bringing your own Gemini key only adds the cost-and-speed
optimisation on top.

The script returns JSON with:

- `success` — whether parsing worked
- `no_actionable_content` — true if nothing actionable was found
- `actionable_confidence` — 0.0–1.0, how sure the parser is the screenshot is actionable
- `needs_actionable_confirmation` — true if `actionable_confidence` is in the maybe band;
  the bot should confirm "is this actually an event or task?" before dispatching
- `items[]` — one entry per detected item with:
  - `type`, `destination`, `confidence` (legacy aggregate), `type_confidence`
  - `confidences{}` — per-field 0.0–1.0 scores (`title`, `date`, `time`, `location`,
    `participants`, `description`, `priority`, …)
  - `needs_confirmation` — true when there is at least one outstanding clarification
  - `clarifications[]` — targeted questions to ask the user, e.g.
    `{ "field": "time", "question": "What time is dinner with Priya?", "reason": "low_confidence" }`
  - all the extracted fields (`title`, `date`, `time`, `location`, `participants`, etc.)
- `summary_text` — chat-ready preview of what was found; send this verbatim, do not rephrase
- `screenshot_summary`, `parse_notes` — context

### Step 3: Handle the Output

**If `no_actionable_content` is true:**
Silently ignore the screenshot — or, if the user clearly meant for scrask to act on it,
reply with the `summary_text` field (which is a polite "couldn't find anything" message).

**If `success` is true:**
Send the `summary_text` value back to the user on the same chat surface. Then process each item.

### Step 4: Route Each Item to a Destination Skill

For every item in `items[]`:

**If `needs_actionable_confirmation: true` (top level):**
Send `summary_text` (which already opens with "Is this actually an event or task?") and wait for
the user. On "yes", proceed item-by-item below. On "no", reply "Got it, skipped ✓" and stop.

**For each item — if `needs_confirmation: false` (no outstanding clarifications):**
Invoke the appropriate destination skill **without** asking the user first.

- `destination: "calendar"` → invoke the user's installed calendar skill. Preference order:
  `calctl` → `accli` → `apple-calendar` → `brainz-calendar` → `gcal-pro` → first available.
- `destination: "task"` → invoke the user's installed task skill. Preference order:
  `apple-reminders` → `things-mac` → `notion` → first available.

Pass the item fields (`title`, `date`, `time`, `end_time`, `end_date`, `location`, `participants`,
`description`, `recurrence`, `online_link`, etc.) to whatever creation command that skill exposes.
If `end_date` is present and different from `date`, treat the item as a multi-day event.

**For each item — if `needs_confirmation: true`:**
The `clarifications[]` array lists the specific things to ask. Each entry has:
- `field` — which field needs clarification (e.g. `"time"`, `"date"`, `"type"`)
- `question` — the user-facing question (already pre-formatted with the item title)
- `reason` — `"missing"` (value is null) or `"low_confidence"` (extracted but uncertain) or
  `"low_type_confidence"` (unsure whether this is a calendar event or a task)

The `summary_text` already renders these as a bullet list. Ask the user the questions in order
and patch the corresponding fields with their replies. Once every clarification is resolved,
route the item to the destination skill as above. If the user says **skip** at any point, drop
the item and confirm "Got it, skipped ✓".

For the special case of `field: "type"`, the user's reply determines whether the item routes to
`calendar` or `task` — update `destination` accordingly before dispatch.

### Step 5: Confirm Saves

After each destination skill returns, relay a one-line confirmation to the user. Examples:

- `📅 Added to Calendar via calctl: **Team Standup** — 2026-03-01 at 09:00`
- `🔔 Added to Reminders: **Pay electricity bill** (due 2026-02-28)`
- `✅ Added to Things: **Send Sandip my resume**`

If the destination skill errors, surface the error and ask whether to retry with a different destination.

## Edge Cases

| Scenario | Behavior |
|---|---|
| Single screenshot has both an event and a task | Process each independently; route to its own destination. |
| Event implies a prep step (e.g. dinner at a restaurant → book table) | The parser emits BOTH an event and a prep reminder. Inferred fields on the prep reminder land in the 0.65–0.80 band, so most prep reminders hit `needs_confirmation: true` with targeted clarifications (typically `time` and `date`). |
| Multi-day event (trip, conference) | `end_date` is set and differs from `date`. Pass both to the calendar skill (e.g. `calctl add --date --end-date --all-day`). |
| Rescheduled / cancelled event | Parser extracts the NEW date; `parse_notes` flags it as a reschedule. Confirm with user before overwriting any existing entry. |
| Screenshot is in Hindi, Tamil, or another language | Title and description are already in English; `language` holds the ISO code. Save as-is. |
| Recurring event ("every Monday") | Pass `recurrence` and `recurrence_day` to the calendar skill. |
| Date has already passed | Flag in the reply: "⚠️ This date has already passed. Save anyway?" |
| Screenshot of someone's calendar | `already_in_calendar_hint: true` — reply: "Looks like this is already in your calendar 🗓️" and skip. |
| No calendar / task skill installed | Reply with the missing-skill hint and stop. |
| Zoom/Meet link found | Pass `online_link` to the calendar skill; it should set both location and description. |
| Meme / non-actionable screenshot | `no_actionable_content: true` — ignore silently unless user clearly asked for action. |

## Configuration

```json
{
  "skills": {
    "entries": {
      "scrask-bot": {
        "enabled": true,
        "env": {
          // Both keys are OPTIONAL in v4.2+. Without either, Scrask uses
          // OpenClaw's configured vision LLM via the platform-injected
          // OPENCLAW_VISION_* env vars. Setting GEMINI_API_KEY opts into
          // the cheap+fast Gemini routing. Setting ANTHROPIC_API_KEY adds
          // Claude as a fallback (or as the primary if no Gemini key).
          "GEMINI_API_KEY": "AIza-your-gemini-key",
          "ANTHROPIC_API_KEY": "sk-ant-your-key-here"
        },
        "config": {
          "vision_provider": "auto",
          "fallback_threshold": 0.60,
          "timezone": "Asia/Kolkata",
          "confidence_threshold": 0.75,
          "actionable_threshold": 0.70,
          "type_threshold": 0.70,
          "field_threshold": 0.70
        }
      }
    }
  }
}
```

`ANTHROPIC_API_KEY` is optional. Without it, auto mode runs Gemini only.

## Permissions Required

- `image:read` — to access the screenshot from the chat surface.
- `network:outbound` — to call the vision model API (Gemini and optionally Claude).
- `chat:reply` — to send confirmation messages back via the user's chat surface.
- Whatever permissions the downstream calendar / task skill needs (handled by that skill).
