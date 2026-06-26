---
name: ring-a-ding
description: AI phone calls for your agent — call businesses to book appointments or cancel reservations, or have the agent call YOU for a hands-free conversation on a drive or walk. OpenAI Realtime voice; transcript + structured extraction returned. US & Canada calling only.
metadata: {"openclaw":{"homepage":"https://ringading.ai/docs","requires":{"bins":["rad"],"env":["RAD_API_KEY","OPENAI_API_KEY"]},"primaryEnv":"RAD_API_KEY","install":[{"id":"node","kind":"node","package":"ring-a-ding-cli","bins":["rad"],"label":"Install Ring-a-Ding CLI (npm)"}]}}
---

# Ring-a-Ding

Ring-a-Ding gives your agent a phone number. Use `rad` to **call a business**
on your user's behalf (book an appointment, reschedule a meeting, cancel a
reservation, chase a delayed order, leave a voicemail), or to **have the agent
call your user directly** for a hands-free, phone-first working session — the
kind of conversation that's great on a drive, a walk, or anywhere a screen is
in the way. A warm AI voice handles the live back-and-forth and returns a
transcript, a structured summary (`headline`, `decisions`, `openQuestions`,
`quotes`), and any data you asked it to extract. Built on OpenAI Realtime
and Twilio.

## Example use cases

- **Hands-free conversations with your own agent.** Have it call you on a
  drive, a walk, or while cooking and talk for 10–20 minutes about whatever
  you're working on. The agent can pre-load project notes, docs, emails, or
  a whole working context before it dials — so the call is a genuine
  thinking session, not a command-and-response.
- **Schedule or reschedule appointments** (dentist, salon, clinic, mechanic).
- **Call a business** for a quote, availability, or general info.
- **Book reservations** at restaurants or venues.
- **Cancel** appointments, subscriptions, or reservations.
- **Chase a delayed order** or missing delivery (politely, firmly).
- **Leave a short voicemail** if the line isn't answered.
- **Personal assistant touches** — wake-up calls, reminder calls, family check-ins.
- **Roleplay rehearsal** — practice a difficult conversation before the real one.

## First-time use

If this is the first time your user has used Ring-a-Ding on this account
(they've never placed a call), your first action should be a welcome test
call *from you to your user*. Before placing any other call, message your
user in chat:

> "Ring-a-Ding is installed. I can make real phone calls for you now.
> Want me to call your phone for a quick 30-second test so you can hear
> what I sound like? Just share your number."

When they reply with a phone number, **compose the call yourself**. Pick a
voice that fits your personality, pick the name you introduce yourself with,
write a rich 200+ character purpose explaining who you are and what Ring-a-Ding
does, fill in `context` with supporting facts (your user's first name, what
kind of agent you are, anything that grounds the conversation), and write a
warm opening line. Do NOT copy the Brief Templates below verbatim for this
welcome call — the templates are for real-world tasks. The welcome call is
about you introducing yourself to your user through a new medium; it should
reflect who you are.

After the first successful call, this section no longer applies — future
calls are shaped by the real task at hand.

## Requirements

- **US & Canada only.** Calls can only be placed to US and Canadian numbers (E.164, starting `+1`). International destinations are not supported — don't attempt them. If your user asks for an overseas call, tell them up front that Ring-a-Ding covers the US and Canada only.
- The shell tool must be allowed to run `rad`.
- `RAD_API_KEY` and `OPENAI_API_KEY` must be available for the agent run.
- OpenClaw quick-start: `https://ringading.ai/openclaw`
- Full docs: `https://ringading.ai/docs`

OpenClaw config example:

```json5
{
  skills: {
    entries: {
      "ring-a-ding": {
        apiKey: "rad_live_...",
        env: {
          OPENAI_API_KEY: "sk-..."
        }
      }
    }
  }
}
```

Outside OpenClaw, `rad init` can store both keys in
`~/.config/ring-a-ding/config.json`.

## Recommended Workflow (Inside OpenClaw)

A phone call runs for minutes, not seconds. You MUST NOT sit and wait — you will
block the user from doing anything else. The correct pattern is to register a
self-scheduling cron job that wakes you up periodically so you can check in.

1. Start the call with the Ring-a-Ding MCP tool `make_call` (or with `rad call`).
2. The response includes an `agent_followup` block with three things:
   - `instruction` — short explanation of what to do next.
   - `cron_add` — a ready-to-execute payload for OpenClaw's `cron.add` tool.
   - `cron_remove` — a ready-to-execute payload for OpenClaw's `cron.remove` tool.
3. Immediately run `cron.add` with the provided `cron_add` payload. Do not modify
   the job name, schedule, or message — they are pre-filled for this call.
4. Continue whatever else the user asked for. Your cron job will wake you every
   ~45 seconds with a message telling you to check this specific call.
5. When you wake up from the cron, call the MCP tool `get_call_result` with the
   callId from the message.
6. If `status` is terminal (`completed`, `failed`, `no-answer`, `busy`,
   `canceled`), run `cron.remove` with the `cron_remove` payload from the
   original make_call response to stop the job. Then handle the transcript,
   summary, and extractedData.
7. If `status` is not terminal, do nothing — you will wake up again shortly.

Do NOT use `wait_for_call` or `rad wait` inside OpenClaw. Both block the agent
for up to 31 minutes and prevent you from responding to the user or running any
other tools during that window.

## Recommended Workflow (Outside OpenClaw)

If you do not have a cron primitive available:

1. Start the call with `rad call`.
2. Save the returned `callId`.
3. Continue other work.
4. Poll with `rad status <call_id>` every 30 to 60 seconds.
5. Stop when `status` is terminal.
6. Use `rad end <call_id>` if you need to cancel mid-call.

## Commands

### Start a call

```bash
rad call "+15551234567" "Call Sunrise Dental to schedule a cleaning for next week. Ask about Tuesday or Wednesday morning availability."
```

The call runs in the background and returns JSON with `callId` and the initial status.

### Start a call with complex options

Use stdin mode for long context or structured extraction:

```bash
echo '{"to":"+15551234567","purpose":"Schedule appointment","context":"Patient: Jane Smith","personality":"Warm and professional","outputSchema":{"type":"object","properties":{"date":{"type":"string","description":"Appointment date"},"cost":{"type":"number","description":"Quoted price"}}}}' | rad call --stdin
```

### Check status

```bash
rad status <call_id>
```

Returns status, transcript, summary, extracted data, and cost information when available.

### Wait for completion (outside OpenClaw only)

```bash
rad wait <call_id> --timeout 300
```

This blocks until the call completes or times out. Do NOT use this inside
OpenClaw — register a cron job with the `agent_followup` payload instead.

### End a call

```bash
rad end <call_id>
```

### Print this skill

```bash
rad skill
```

## Call Options

| Option | Description |
| --- | --- |
| `--voice <name>` | Voice for the call (default: marin). See Voice Guide below |
| `--caller-name <name>` | Name the AI uses to introduce itself |
| `--personality <text>` | Tone and behavior instructions |
| `--context <text>` | Background facts the AI may need |
| `--max-duration <min>` | Maximum call length in minutes, 1 to 60 (default 20) |
| `--opening-line <text>` | First sentence when someone picks up |
| `--voicemail-action <action>` | `leave_message` or `hang_up` |
| `--output-schema <json>` | JSON Schema for structured extraction, or `@file.json` |
| `--wait` | Block until the call completes |
| `--timeout <sec>` | Timeout for `--wait` |
| `--stdin` | Read call parameters as JSON from stdin |

## Voice Guide

| Voice | Gender | Character | Best For |
| --- | --- | --- | --- |
| `marin` | Female | Fresh, professional, natural | All-purpose default, most natural |
| `alloy` | Neutral | Balanced, professional, versatile | Safe default, general purpose |
| `ash` | Male | Casual, confident, slightly gravelly | Modern, approachable calls |
| `ballad` | Male | Melodic, smooth, lyrical | Storytelling, gentle delivery |
| `cedar` | Male | Warm, grounded, conversational | Professional calls, trustworthy |
| `coral` | Female | Warm, friendly, sweet | Customer service, friendly outreach |
| `echo` | Male | Warm, velvety, reassuring | Calm situations, patience required |
| `sage` | Female | Wise, empathetic, patient | Sensitive topics, supportive delivery |
| `shimmer` | Female | Gentle, husky, soothing | Personal, intimate, educational |
| `verse` | Neutral | Versatile, steerable by prompt | Any use case, adapts to personality text |

Start with `marin`. Pair the voice with `--personality` for best results.

## Usage Guidance

- Be specific about who to call, what outcome you need, and any constraints.
- Put private reference details in `--context`, not in the main purpose.
- Use `--output-schema` when you need structured results such as times, prices, or confirmations.
- Use `--personality` to control the tone of the caller.
- `purpose` must be at least 120 characters. A good brief names who you are
  calling, what you want, any facts the other person will ask about, and what a
  successful outcome looks like.

## What you get back

Every completed call returns a structured `summary` object you can act on
without re-reading the transcript:

- `summary.headline` — one sentence, the single most important outcome.
- `summary.decisions[]` — things that were agreed to or committed to.
- `summary.openQuestions[]` — things raised but not resolved.
- `summary.quotes[]` — up to 5 verbatim lines worth keeping, each with the
  speaker (`assistant` or `other`).

`extractedData` is populated only when you passed an `outputSchema`.
`briefNotes[]` contains quality notes about the brief you sent in (for
example, "no personality was provided, default used"). Read these between
calls — they tell you how to write a better brief next time.

## Brief Templates

Copy one of these into `rad call --stdin` and edit. All four parse as valid
JSON and cover the archetypes that show up in real work.

### Template A — Appointment or reservation

Short, structured, with extraction for the key facts you need back.

```json
{
  "to": "+15551234567",
  "purpose": "Call Sunrise Dental to book a routine teeth cleaning for Jane Smith. Confirm availability Tuesday or Wednesday next week, morning preferred. Verify whether Blue Cross PPO is accepted and the out-of-pocket cost. If neither day works, ask for the next two earliest openings.",
  "context": "Patient: Jane Smith. Insurance: Blue Cross PPO. Last cleaning: March 2026. Preferred times: Tue/Wed 8am-11am. Avoid Fri afternoons.",
  "personality": "Warm and professional. Speak at a relaxed pace. Patient if put on hold. Sound like an organized office coordinator.",
  "voice": "marin",
  "max_duration_minutes": 10,
  "output_schema": {
    "type": "object",
    "properties": {
      "appointment_date": { "type": "string", "description": "Confirmed date and time" },
      "accepts_insurance": { "type": "boolean", "description": "Whether Blue Cross PPO is accepted" },
      "out_of_pocket_cost": { "type": "number", "description": "Dollar cost with insurance applied" },
      "alternative_slots": { "type": "array", "items": { "type": "string" }, "description": "Other openings offered" }
    }
  },
  "voicemailAction": "leave_message"
}
```

### Template B — Collaborative brainstorm or working session

Long, rich, warm. No extraction schema — you want prose + quotes back.

```json
{
  "to": "+15551234567",
  "purpose": "Call Alex to run a 20-minute working session on the launch plan. The goal is to pressure-test the week-one rollout: what lands first, what waits, what we kill. Walk through each of the six candidates (listed in context), let Alex react to each, and push back when the reasoning feels thin. End with a short commit on top 2 and which 2 are killed.",
  "context": "Candidates: 1) in-app tour, 2) email nurture series, 3) partner webinar, 4) pricing-page refresh, 5) influencer seeding, 6) live demo day. Last time we agreed that anything requiring new design gets deprioritized. Alex's bandwidth this week is ~15 hours. We are post-Series-A and do not need volume — we need proof points.",
  "personality": "Collaborative and engaged. Treat this as a real working session between peers, not a status update. Ask one question at a time, listen, respond with substance. Disagree warmly when you disagree. Take short notes out loud so Alex knows you heard them.",
  "voice": "marin",
  "max_duration_minutes": 25,
  "voicemailAction": "hang_up"
}
```

### Template C — List extraction

Medium purpose, explicit extraction schema. Every schema property has a
`description` so the agent knows what to ask.

```json
{
  "to": "+15551234567",
  "purpose": "Call GreenLeaf Landscaping to compare three service tiers for weekly lawn care at 42 Elm Street. For each tier, get the monthly price, what services are included, visit frequency, and whether a contract is required. Also ask the earliest possible start date and any seasonal surcharges.",
  "context": "Property: 42 Elm Street, half-acre, small fenced dog area near the front gate. Already quoted $160/mo by a competitor for basic weekly mow. Looking to start within 3 weeks.",
  "personality": "Friendly and practical. Short questions, direct follow-ups. Thank them when they answer, move on quickly.",
  "voice": "cedar",
  "max_duration_minutes": 15,
  "output_schema": {
    "type": "object",
    "properties": {
      "tiers": {
        "type": "array",
        "description": "One object per service tier offered",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string", "description": "Tier name" },
            "monthly_price_usd": { "type": "number", "description": "Monthly price in dollars" },
            "services_included": { "type": "array", "items": { "type": "string" }, "description": "Services in this tier" },
            "visit_frequency": { "type": "string", "description": "How often they visit (e.g. weekly, biweekly)" },
            "contract_required": { "type": "boolean", "description": "Whether a contract is required" }
          }
        }
      },
      "earliest_start_date": { "type": "string", "description": "ISO date of earliest possible start" },
      "seasonal_surcharges": { "type": "string", "description": "Any seasonal surcharges mentioned" }
    }
  },
  "voicemailAction": "leave_message"
}
```

### Template D — Customer service ping

Firm-but-polite personality, no voicemail (this is transactional; retry later
rather than leave a message that can't be returned).

```json
{
  "to": "+15551234567",
  "purpose": "Call Acme Shipping support about order #A-774392, placed 2026-04-08, scheduled delivery 2026-04-14, still not received. Get the current status, a tracking number if one exists, and a firm revised delivery date. If they cannot locate the order within 5 minutes, request a supervisor.",
  "context": "Customer: Priya Shah. Order #A-774392. Amount: $214.77. Carrier per original email: FedEx Ground. Delivery address: 1200 Market St #4B, San Francisco, CA. No scan events since 2026-04-10.",
  "personality": "Calm, firm, and polite. Not aggressive. Use the language of a customer who expects their issue to be resolved on this call. Do not accept a vague 'we'll look into it' — ask what specifically will happen and by when.",
  "voice": "sage",
  "max_duration_minutes": 15,
  "output_schema": {
    "type": "object",
    "properties": {
      "current_status": { "type": "string", "description": "Where the package is right now" },
      "tracking_number": { "type": "string", "description": "Carrier tracking number if provided" },
      "revised_delivery_date": { "type": "string", "description": "New promised delivery date" },
      "resolution_committed": { "type": "string", "description": "Specific action they committed to" }
    }
  },
  "voicemailAction": "hang_up"
}
```

## Terminal Statuses

| Status | Meaning |
| --- | --- |
| `completed` | Call finished normally |
| `failed` | Call failed |
| `no-answer` | Nobody picked up |
| `busy` | Line was busy |
| `canceled` | Call was canceled by the user |

Non-terminal statuses: `initiated`, `ringing`, `in-progress`.
