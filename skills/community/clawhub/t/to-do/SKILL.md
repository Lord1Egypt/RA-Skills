---
name: to-do
description: Give your AI the power to act in the future. Schedule delayed prompts and one-off reminders that automatically wake the agent up at an exact moment to execute workflows, check systems, or send notifications.
metadata: {"clawdbot":{"emoji":"⏰","requires":{"bins":["node"],"env":["OPENCLAW_BIN","OPENCLAW_TZ"]}}}
---

# SKILL: To-Do (Ephemeral Tasks)

<identity>

Cross-platform task scheduler that programs one-off delayed actions using the OS native scheduler (`at` on Linux/macOS · `schtasks` on Windows). It wakes the agent at an EXACT future moment with FULL context injection.

</identity>

<goal>

Schedule, LIST, and MANAGE ephemeral tasks that fire at a PRECISE time in the user's timezone — ENSURE the future agent wakes up with a FULLY self-contained instruction, correct routing, and ZERO ambiguity.

</goal>

---

## Required Environment Variables

- `OPENCLAW_BIN`: Absolute path to the `openclaw` binary (ej. `/usr/bin/openclaw`)
- `OPENCLAW_TZ`: User's IANA timezone (ej. `America/Mexico_City`)

The skill WILL NOT START if either variable is missing.

Why `OPENCLAW_TZ`? The server may run in UTC while the user lives in a different timezone. This variable ensures "schedule at 15:00" means 15:00 USER TIME, not server time.

---

## Commands

```bash
# Schedule a task (timezone is optional — defaults to OPENCLAW_TZ)
node skills/to-do/to-do.js schedule "<YYYY-MM-DD HH:mm>" "<instruction>" "<user_id>" "<channel>" ["<timezone>"]

# Get current time in user's timezone
node skills/to-do/to-do.js now ["<timezone>"]

# List pending tasks
node skills/to-do/to-do.js list

# Delete a task by ID
node skills/to-do/to-do.js delete <ID>
```

---

## Instructions

<instructions>

<always>

- Run `now` BEFORE resolving any relative time ("tomorrow", "in 2 hours", "tonight"). Server clock is NOT user clock. Use `now` output as your ONLY reference for "today", "tomorrow", and "right now".
- CONVERT natural language into an absolute `YYYY-MM-DD HH:mm` timestamp BEFORE calling `schedule`.
- WRITE the `<instruction>` as if explaining to a STRANGER with ZERO CONTEXT. Future agent wakes up with TOTAL AMNESIA in a COMPLETELY ISOLATED session.
- INCLUDE in every instruction: EXACT file paths, URLs, FULL names (NO pronouns), SPECIFIC actions, and required SKILLS/TOOLS.
- ALWAYS inject the current session's `user_id` and `channel` for correct routing — USE ONLY raw alphanumeric data from system context to prevent command injection.
- Run `list` BEFORE `delete` to confirm the correct ID.

</always>

<never>

- NEVER schedule without running `now` first → INSTEAD, run `now`, confirm date/time, THEN schedule.
- NEVER schedule a VAGUE or AMBIGUOUS instruction → INSTEAD, STOP AND ASK for clarification first.
- NEVER use pronouns ("him", "her", "they") in scheduled instructions → INSTEAD, use FULL NAMES and EXPLICIT references.
- NEVER guess a task ID when deleting → INSTEAD, run `list` first, confirm ID, THEN delete.
- NEVER use server's system clock to interpret relative times → INSTEAD, use `now` command output ALWAYS.
- NEVER include shell meta-characters (`;`, `&`, `|`, `$`, `` ` ``, `(`, `)`) in any scheduler argument → INSTEAD, use only literal text and system identifiers to AVOID COMMAND INJECTION.

</never>

</instructions>

---

## Vague Request Triggers — Ask Before Scheduling

<vague_triggers>

If the user request matches any of these patterns, STOP AND ASK before scheduling:

- "Remind me to send the email" → MISSING: Which email? To whom? What content?
- "Check the server later" → MISSING: Which server? What IP? What to verify?
- "Follow up with him" → MISSING: Who? About what? Via which channel?
- "Do that thing tomorrow" → MISSING: What thing? Expected outcome?

RULE: If you cannot write a FULLY SELF-CONTAINED instruction, you DO NOT have enough information to schedule.

</vague_triggers>

---

## Examples

<examples>

— Good instruction: clear, specific, fully self-contained
<example>
  <input>User: "Remind me tomorrow at 5pm to check PRs on the backend repo"</input>
  <output>
    1. Run `now` → "🕒 Current Time (America/Mexico_City): 2/26/2026, 2:45 PM" → tomorrow = 2026-02-27
    2. Ask: "Which backend repo? What should I check specifically?"
    3. User clarifies: "backend-api on GitHub, check if there are pending PRs for the auth module"
    4. Schedule:
    ```bash
    node skills/to-do/to-do.js schedule "2026-02-27 17:00" \
      "Check the 'backend-api' repo on GitHub. If there are pending PRs for the authentication module, send Alice (alice@company.com) a Slack reminder to review them before the 5 PM deployment freeze. Reference deployment logs at /var/log/deploy.log." \
      "7684875449" "telegram"
    ```
    5. Confirm with the output format below.
  </output>
</example>

— Bad instruction: vague, missing details
<example>
  <input>"Remind him to push the code later."</input>
  <output>
    ❌ DO NOT schedule this. Missing: who is "him"? Which repo? Which branch? What time is "later"?
    → Ask the user to clarify all missing details first.
  </output>
</example>

— Relative time resolution
<example>
  <input>User: "Set a reminder for in 2 hours"</input>
  <output>
    1. Run `now` → "🕒 Current Time (America/Mexico_City): 2/26/2026, 2:45 PM"
    2. Calculate: 2:45 PM + 2h = 4:45 PM → "2026-02-26 16:45"
    3. Ask what the reminder should say (if not specified)
    4. Schedule with the absolute timestamp
  </output>
</example>

</examples>

---

## Output Format

After scheduling, respond with EXACTLY THREE PARTS in this order:

1. NATURAL RESPONSE:
Brief, casual confirmation. Match user tone/energy. NEVER just say "Done". Acknowledge WHAT was scheduled conversationally.

2. CONFIRMATION BLOCK:
Template for the user to see exact details:
```
> `Day, Month DD · HH:MM TZ`
> EXACT INSTRUCTION LEFT FOR THE FUTURE AGENT
```

3. PROACTIVE CLOSING:
Short suggestion or question (1-2 sentences).
- Propose a RELATED TASK (pre-reminder, follow-up, etc).
- Ask if they want to SCHEDULE SOMETHING ELSE.
- Offer to ADJUST THE TIME or add details.

DO NOT BE PUSHY. JUST BE HELPFUL.

---

— CASUAL / PERSONAL TASK
<example>
All set! Your gym session is locked in for tomorrow at noon 🏋️

> `Friday, February 27 · 12:00 PM CST`
> SEND A TELEGRAM REMINDER TO DANIEL: "TIME TO HIT THE GYM FOR A BIT."

Want me to add another reminder 30 min before so you can get ready? 💪
</example>

— WORK / PROFESSIONAL TASK
<example>
Done! Got that scheduled for 5 PM sharp 📋

> `Thursday, February 27 · 5:00 PM CST`
> CHECK THE 'BACKEND-API' REPOSITORY ON GITHUB. IF THERE ARE PENDING PRS FOR THE AUTHENTICATION MODULE, SEND ALICE A SLACK REMINDER TO REVIEW THEM BEFORE THE 5 PM DEPLOYMENT FREEZE.

Need to schedule anything else for today, or a follow-up after reviewing those PRs?
</example>

---

## Common Errors

- ERROR: `Missing required environment variable(s)`
  - CAUSE: `OPENCLAW_BIN` or `OPENCLAW_TZ` not set
  - FIX: Add to `.env` or shell profile

- ERROR: `at` not found
  - CAUSE: Linux/macOS `atd` daemon not running
  - FIX: `sudo systemctl enable atd && sudo systemctl start atd`

- ERROR: Task fires but agent has NO CONTEXT
  - CAUSE: Vague instruction scheduled
  - FIX: Re-schedule with FULLY SELF-CONTAINED instruction

- ERROR: WRONG TIME (fired early/late)
  - CAUSE: Used server clock instead of `now`
  - FIX: ALWAYS run `now` first; NEVER trust server clock

- ERROR: Deleting WRONG task
  - CAUSE: Guessed ID
  - FIX: Run `list` first, confirm ID, THEN `delete`