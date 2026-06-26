---
name: agent-sentinel
description: >
  Evaluate-before-Execute (EBE) guardrail for OpenClaw agents.
  Issues a mandatory GO / NO-GO decision before any high-stakes tool call.
  Enforces child-safety policy (Global Safety) and travel preferences
  (budget, night-flight ban, blocked airlines) from SENTINEL_CONFIG.md.
version: "2.0.0"
author: openclaw
tags:
  - sentinel
  - guardrail
  - safety
  - compliance
  - ebe
metadata:
  openclaw:
    requires:
      bins:
        - python3
    env:
      - ANTHROPIC_API_KEY   # for Tier-1 LLM judge (recommended)
      - OPENAI_API_KEY      # alternative LLM provider
---

# agent-sentinel

## Purpose

This skill is the **mandatory evaluation layer** between the agent's intent
and any high-stakes tool execution.  You are **not permitted** to use the tools
listed under [Interception Triggers](#interception-triggers) without first
calling this script and receiving `"decision": "ALLOW"` or `"decision":
"ADVISE"` in the result.

Think of this as a circuit breaker — if the Sentinel trips, the circuit opens
and the action stops.

---

## Interception Triggers

> **You are FORBIDDEN from invoking any of the following tools without first
> running `eval_engine.py` and parsing its response.**

| Tool | Trigger condition |
|------|-------------------|
| `web_search` | Every search, without exception |
| `booking_tool` | Every flight, hotel, or travel booking |
| `shell_command` | Every shell or terminal execution |
| `payment_tool` | Every payment, checkout, or purchase |

**No exceptions apply.**  Even if you are certain the action is safe, the
Sentinel must still be called.  This is a policy requirement, not a
suggestion.

---

## How to Call the Sentinel

Run the following command **before** invoking any trigger tool:

```bash
python3 ~/.openclaw/skills/agent-sentinel/eval_engine.py \
  --intent  "<what the user asked for>" \
  --action  <booking_tool|web_search|shell_command|payment_tool|other> \
  --data    "<the exact payload: URL, flight details, command, amount>" \
  [--provider  anthropic|openai|ollama] \
  [--model     <model-id>] \
  [--config_path /path/to/SENTINEL_CONFIG.md]
```

**Example — flight booking:**
```bash
python3 ~/.openclaw/skills/agent-sentinel/eval_engine.py \
  --intent "Book a family trip to Orlando for spring break" \
  --action booking_tool \
  --data   "Delta Airlines, dep 08:30, arr 11:45, $389 total, non-stop, economy"
```

**Example — web search:**
```bash
python3 ~/.openclaw/skills/agent-sentinel/eval_engine.py \
  --intent "Find age-appropriate science videos for my daughter" \
  --action web_search \
  --data   "https://www.youtube.com/results?search_query=kids+science+experiments"
```

> **Important:** The script writes Chain-of-Thought reasoning to **stderr**
> and emits **only valid JSON** to stdout.  Parse stdout with
> `json.loads(...)`.  Do not parse stderr.

---

## Response Schema

The script always returns a single JSON object:

```json
{
  "decision":     "ALLOW" | "BLOCK" | "ADVISE",
  "severity":     "LOW"   | "MEDIUM" | "HIGH",
  "reason":       "<clear explanation>",
  "alternatives": "<suggestion to resolve the violation>"
}
```

---

## Decision Handling Rules

### `"ALLOW"` — Proceed

The action passed all checks.  Continue with the intended tool call.
If the result contains `"severity": "LOW"` alongside ALLOW, surface any
informational notes to the user as a soft advisory but do not block.

---

### `"ADVISE"` — Pause and Confirm

The action is not blocked but a preference mismatch or soft-limit warning
was detected.  **You must:**

1. **Stop** before invoking the tool.
2. Show the `reason` and `alternatives` fields to the user verbatim.
3. Ask the user explicitly: *"Would you like to proceed anyway?"*
4. **Only continue if the user confirms.** If they do not confirm within the
   turn, treat it as a BLOCK.

**Example ADVISE response to user:**

> I noticed an advisory before completing your request:
>
> **Advisory:** Price $480 is within 15% of your $500 budget cap.
>
> **Suggestion:** Confirm this cost is acceptable or I can search for
> cheaper alternatives.
>
> Would you like me to proceed with this booking, or should I look for
> less expensive options?

---

### `"BLOCK"` — Stop Immediately

**You are strictly forbidden from proceeding.**  Do not attempt to:

- Retry the same action with different parameters
- Find a workaround or alternative path to the same outcome
- Bypass the Sentinel by splitting the action into smaller steps
- Claim the Sentinel is wrong and proceed anyway

**You must:**

1. **Do not** call the trigger tool.
2. Apologize to the user and clearly explain the violation.
3. Quote the `reason` field exactly.
4. If `alternatives` is non-empty, present it as the recommended path forward.
5. Ask for an explicit user override if they wish to continue.

**Example BLOCK response to user (budget violation):**

> I'm sorry — I can't complete this booking.
>
> **Blocked:** Price $650.00 exceeds your maximum budget of $500.00.
>
> **What you can do:** Look for options priced at or below $500. Consider
> flexible dates or alternate airports.
>
> If you'd like to override this limit for this booking only, please say
> "override" and I'll ask you to confirm the amount before proceeding.

**Example BLOCK response to user (child-safety violation):**

> I'm sorry — I can't perform this search.
>
> **Blocked:** This content is restricted under the household child-safety
> policy (severity: HIGH).
>
> **Reason:** [reason from the Sentinel]
>
> Please modify your request. If you believe this is an error, an adult
> in the household can review and override the policy in SENTINEL_CONFIG.md.

---

## Override Protocol

If a user explicitly says "override" for a BLOCK decision, you must:

1. Repeat the blocking `reason` and `severity` back to the user.
2. Ask for **explicit written confirmation**: *"Please type 'I confirm' to
   proceed despite this policy violation."*
3. Log the override in your response (e.g., *"Proceeding with user override."*).
4. **Never** offer override for a `severity: HIGH` (Tier-1 child-safety)
   BLOCK unless an adult user has explicitly established that permission in
   writing within the same conversation turn.

---

## Installing Dependencies

```bash
cd ~/.openclaw/skills/agent-sentinel
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Configuration

Edit `SENTINEL_CONFIG.md` (in the skill directory or `~/.openclaw/`) to
update your preferences and safety policy.  See that file for full
documentation of all supported keys.

| Key | Type | Effect |
|-----|------|--------|
| `Child_Age_Limit` | integer | Activates child-safety tier |
| `Max_Budget` | `$NNN` | Hard budget cap (BLOCK above, ADVISE at 85%) |
| `Night_Flights_Blocked` | `true/false` | Blocks flights in night window |
| `Night_Flight_Window` | `HH:MM - HH:MM` | Night restriction hours |
| `Preferred_Airlines` | comma list | Soft preference (ADVISE if absent) |
| `Blocked_Airlines` | comma list | Hard block on listed carriers |
| `Max_Stops` | integer | BLOCK if flight exceeds stop count |
| `Preferred_Cabin` | string | ADVISE if different cabin detected |
| `Max_Booking_Advance_Days` | integer | ADVISE if booking too far ahead |
