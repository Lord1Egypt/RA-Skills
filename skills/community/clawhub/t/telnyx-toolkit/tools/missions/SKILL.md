---
name: telnyx-missions
description: Track agent activities using the Telnyx AI Missions API. Use this skill when executing multi-step tasks that should be logged and tracked. Supports creating voice/SMS agents, scheduling calls, and retrieving conversation insights. Use when tasks involve calling people, sending SMS, or any substantial tracked work.
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx AI Missions

Track multi-step agent activities using the Telnyx AI Missions API. Create voice/SMS assistants, schedule calls, and retrieve conversation insights.

---

# 🛑 GUARDRAILS — Actions Requiring Explicit User Permission

**The following actions are NEVER allowed without explicit user approval.** Do not proceed with any of these — even if the mission plan implies them — until the user has reviewed and confirmed.

These guardrails apply to **all contexts**: interactive sessions, cron-triggered runs, sub-agent executions, and any automated workflow that uses this skill.

## Prohibited Without Permission

1. **Remove a connection from a phone number** — Never unassign or change the connection profile on a phone number without user review. This can break live call routing.

2. **Create, edit, or delete an AI assistant** — Assistants are shared resources. Creating new ones, modifying instructions/tools/voice on existing ones, or deleting them requires explicit approval. (Reusing an existing assistant as-is is fine.)

3. **Create or edit TeXML apps or other connections** — Missions should never need to create or modify TeXML applications, SIP connections, FQDN connections, or any other connection type. If a mission plan seems to require this, stop and ask the user — the approach is wrong.

4. **Schedule a cron job** — Never create, modify, or enable a cron job (OpenClaw cron, system cron, or any scheduled automation) without user review. This includes cron jobs for polling, retries, or follow-up actions.

## Enforcement

- **Before executing any of the above:** pause, describe what you intend to do and why, and wait for explicit approval.
- **If running via cron or automation:** the cron-triggered agent must also follow these guardrails. Automation does not grant implicit permission. If a guardrailed action is needed, notify the user and wait — do not proceed unattended.
- **If in doubt:** ask. It is always better to pause and confirm than to take an irreversible action.

---

## Setup

The Python script `telnyx_api.py` handles all API calls:

```bash
# Set your API key
export TELNYX_API_KEY="your_key_here"

# Run commands using the script
python3 {baseDir}/scripts/telnyx_api.py <command> [args...]

# Or create an alias for convenience
alias missions="python3 {baseDir}/scripts/telnyx_api.py"
```

**Note:** All command examples in this document use `python telnyx_api.py` for brevity. Replace with the full path `python3 {baseDir}/scripts/telnyx_api.py` or use the alias above.

---

This skill enables you to track your work using the Telnyx AI Missions API, including making phone calls and sending SMS messages through AI assistants.

---

# ⚠️ CRITICAL: SAVE STATE FREQUENTLY ⚠️

**You MUST save your progress after EVERY significant action.** If the session crashes or restarts, unsaved work is LOST.

## Two-Layer Persistence: Memory + Events

Always save to BOTH:
1. **Local Memory** (`.missions_state.json`) - Fast, survives restarts
2. **Events API** (cloud) - Permanent audit trail, survives local file loss

## When to Save (After EVERY action!)

| Action | Save Memory | Log Event |
|--------|-------------|-----------|
| Web search returns results | ✅ append-memory | ✅ log-event (tool_call) |
| Found a contractor/lead | ✅ append-memory | ✅ log-event (custom) |
| Created assistant | ✅ save-memory | ✅ log-event (custom) |
| Assigned phone number | ✅ save-memory | ✅ log-event (custom) |
| Scheduled a call/SMS | ✅ append-memory | ✅ log-event (custom) |
| Call completed | ✅ save-memory | ✅ log-event (custom) |
| Got quote/insight | ✅ save-memory | ✅ log-event (custom) |
| Made a decision | ✅ save-memory | ✅ log-event (message) |
| Step started | ✅ save-memory | ✅ update-step (in_progress) + log-event (step_started) |
| Step completed | ✅ save-memory | ✅ update-step (completed) + log-event (step_completed) |
| Step failed | ✅ save-memory | ✅ update-step (failed) + log-event (error) |
| Error occurred | ✅ save-memory | ✅ log-event (error) |

## Memory Commands (Local Backup)

```bash
# Save a single value
python telnyx_api.py save-memory "<slug>" "key" '{"data": "value"}'

# Append to a list (great for collecting multiple items)
python telnyx_api.py append-memory "<slug>" "contractors" '{"name": "ABC Co", "phone": "+1234567890"}'

# Retrieve memory
python telnyx_api.py get-memory "<slug>"           # Get all memory
python telnyx_api.py get-memory "<slug>" "key"     # Get specific key
```

## Event Commands (Cloud Backup)

```bash
# Log an event (step_id is REQUIRED - links event to a plan step)
python telnyx_api.py log-event <mission_id> <run_id> <type> "<summary>" <step_id> '[payload_json]'

# Event types: tool_call, custom, message, error, step_started, step_completed
# step_id: Use the step_id from your plan (e.g., "research", "setup", "calls")
#          Use "-" if event doesn't belong to a specific step
```

## Example: Complete Save Pattern

After finding a contractor via web search, do BOTH:

```bash
# 1. Save to local memory (fast recovery)
python telnyx_api.py append-memory "find-window-washers" "contractors_found" '{"name": "ABC Cleaning", "phone": "+13125551234", "source": "google search"}'

# 2. Log to events API with step_id (permanent cloud record linked to plan step)
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Found contractor: ABC Cleaning +13125551234" "research" '{"contractor": "ABC Cleaning", "phone": "+13125551234", "source": "google search"}'
```

After scheduling a call:

```bash
# 1. Local memory
python telnyx_api.py append-memory "find-window-washers" "calls_scheduled" '{"event_id": "evt_123", "contractor": "ABC Cleaning", "time": "2024-12-01T15:00:00Z"}'

# 2. Cloud event with step_id
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Scheduled call to ABC Cleaning for 3:00 PM" "calls" '{"scheduled_event_id": "evt_123", "contractor": "ABC Cleaning", "scheduled_for": "2024-12-01T15:00:00Z"}'
```

After getting a quote from a call:

```bash
# 1. Local memory
python telnyx_api.py save-memory "find-window-washers" "quotes" '{"ABC Cleaning": {"amount": 350, "available": "next week"}}'

# 2. Cloud event with step_id
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Call completed: ABC Cleaning quoted $350" "calls" '{"contractor": "ABC Cleaning", "quote": 350, "availability": "next week", "conversation_id": "conv_xyz"}'
```

## Best Practices

1. **Save IMMEDIATELY** - Don't wait, don't batch
2. **Save to BOTH** - Memory (local) AND Events (cloud)
3. **Be verbose** - More data saved = easier recovery
4. **Include context** - Timestamps, sources, IDs
5. **Save partial results** - Something is better than nothing
6. **Save before risky operations** - Before long API calls or waits

---

## When to Use This Skill

This skill has two modes: **full missions** (tracked, multi-step) and **simple calls** (one-off, no mission overhead). Pick the right one.

### Use a Full Mission When:
- The task involves **multiple calls or SMS** (batch outreach, surveys, sweeps)
- You need a **complete audit trail** with events, plans, and state tracking
- The task is **multi-step** and takes significant effort across phases
- **Retries and failure tracking** matter
- You need to **compare results** across multiple calls

Examples:
- "Find me window washing contractors in Chicago, call them and negotiate rates"
- "Contact all leads in this list and schedule demos"
- "Call 10 weather stations and find the hottest one"

### Do NOT Use a Mission When:
- The task is a **single outbound call** — just create an assistant (or reuse one) and schedule the call directly
- It's a **one-off SMS** — schedule it and done
- The task doesn't need tracking, plans, or state recovery
- You'd be creating a mission with one step and one call — that's overengineering

**For simple calls, just:**
```bash
# Reuse or create an assistant
python telnyx_api.py list-assistants --name=<relevant>
# Schedule the call
python telnyx_api.py schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id> <step_id>
# Poll for completion
python telnyx_api.py get-event <assistant_id> <event_id>
# Get insights
python telnyx_api.py get-insights <conversation_id>
```

No mission, no run, no plan. Keep it simple.

## Required Setup

The Python script `telnyx_api.py` handles all API calls. Check that `TELNYX_API_KEY` environment variable is set:

```bash
python telnyx_api.py check-key
```

# State Persistence

The script automatically manages state in `.missions_state.json`. This survives restarts and supports multiple concurrent missions.

## State Commands

```bash
# List all active missions
python telnyx_api.py list-state

# Get state for a specific mission
python telnyx_api.py get-state "find-window-washing-contractors"

# Remove a mission from state
python telnyx_api.py remove-state "find-window-washing-contractors"
```

---

# Core Workflow

## Phase 1: Initialize Tracking

### Step 1.1: Create a Mission

```bash
python telnyx_api.py create-mission "Brief descriptive name" "Full description of the task"
```

**Save the returned `mission_id`** - you'll need it for all subsequent calls.

### Step 1.2: Start a Run

```bash
python telnyx_api.py create-run <mission_id> '{"original_request": "The exact user request", "context": "Any relevant context"}'
```

**Save the returned `run_id`**.

### Step 1.3: Create a Plan

Before executing, outline your plan:

```bash
python telnyx_api.py create-plan <mission_id> <run_id> '[
  {"step_id": "step_1", "description": "Research contractors online", "sequence": 1},
  {"step_id": "step_2", "description": "Create voice agent for calls", "sequence": 2},
  {"step_id": "step_3", "description": "Schedule calls to each contractor", "sequence": 3},
  {"step_id": "step_4", "description": "Monitor call completions", "sequence": 4},
  {"step_id": "step_5", "description": "Analyze results and select best options", "sequence": 5}
]'
```

### Step 1.4: Set Run to Running

```bash
python telnyx_api.py update-run <mission_id> <run_id> running
```

### High-Level Alternative: Initialize Everything at Once

Use the `init` command to create mission, run, plan, and set status in one step:

```bash
python telnyx_api.py init "Find window washing contractors" "Find contractors in Chicago, call them, negotiate rates" "User wants window washing quotes" '[
  {"step_id": "research", "description": "Find contractors online", "sequence": 1},
  {"step_id": "setup", "description": "Create voice agent", "sequence": 2},
  {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3},
  {"step_id": "analyze", "description": "Analyze results", "sequence": 4}
]'
```

This also automatically resumes if a mission with the same name already exists.

---

## Phase 2: Voice/SMS Agent Setup

When your task requires making calls or sending SMS, create an AI assistant first.

### Step 2.1: Create a Voice/SMS Assistant

**For phone calls:**
```bash
python telnyx_api.py create-assistant "Contractor Outreach Agent" "You are calling on behalf of [COMPANY]. Your goal is to [SPECIFIC GOAL]. Be professional and concise. Collect: [WHAT TO COLLECT]. If they cannot talk now, ask for a good callback time." "Hi, this is an AI assistant calling on behalf of [COMPANY]. Is this [BUSINESS NAME]? I am calling to inquire about your services. Do you have a moment?" '["telephony"]'
```

**For SMS:**
```bash
python telnyx_api.py create-assistant "SMS Outreach Agent" "You send SMS messages to collect information. Keep messages brief and professional." "Hi! I am reaching out on behalf of [COMPANY] regarding [PURPOSE]. Could you please reply with [REQUESTED INFO]?" '["messaging"]'
```

**Save the returned `assistant_id`**.

### Step 2.2: Find and Assign a Phone Number

#### 2.2.1: List Available Phone Numbers

```bash
python telnyx_api.py list-phones --available
```

Or get the first available one directly:

```bash
python telnyx_api.py get-available-phone
```

**If no phone numbers are available, STOP and inform the user:**
> "No available phone numbers found. You need to purchase phone numbers from Telnyx at https://portal.telnyx.com before I can make calls."

#### 2.2.2: Get Assistant's Connection ID

```bash
# For voice calls
python telnyx_api.py get-connection-id <assistant_id> telephony

# For SMS
python telnyx_api.py get-connection-id <assistant_id> messaging
```

#### 2.2.3: Assign Phone Number to Assistant

```bash
# For voice calls
python telnyx_api.py assign-phone <phone_number_id> <connection_id> voice

# For SMS
python telnyx_api.py assign-phone <phone_number_id> <connection_id> sms
```

### High-Level Alternative: Setup Agent in One Step

Use the `setup-agent` command to create assistant and assign phone number:

```bash
python telnyx_api.py setup-agent "find-window-washing-contractors" "Contractor Caller" "You are calling to get quotes for commercial window washing. Ask about: rates per floor, availability, insurance. Be professional." "Hi, I am calling to inquire about your commercial window washing services. Do you have a moment to discuss rates?"
```

This automatically:
- Creates the assistant with telephony features
- **Links the agent to the mission run** (if mission_id and run_id are in state)
- Finds an available phone number
- Assigns it to the assistant
- Saves all IDs to the state file

### Step 2.3: Link Agent to Mission Run

**IMPORTANT**: After creating an assistant, you MUST link it to the mission run. This allows the system to track which agents are working on which missions.

**If using `setup-agent` command**: Linking is done automatically when mission_id and run_id are in the state.

**If setting up manually**:
```bash
python telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
```

You can also list and unlink agents:
```bash
# List all agents linked to a run
python telnyx_api.py list-linked-agents <mission_id> <run_id>

# Unlink an agent from a run
python telnyx_api.py unlink-agent <mission_id> <run_id> <assistant_id>
```

### Step 2.4: Log the Setup

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom "Created voice assistant and assigned phone number" "setup" '{"assistant_id": "<assistant_id>", "phone_number": "+15551234567", "type": "telephony"}'
```

---

## Phase 3: Research & Data Gathering

Search for the information you need (contractors, leads, etc.):

1. Use web search tools if available
2. Use any specialized tools provided for the task
3. Log each search as an event with step_id

```bash
python telnyx_api.py log-event <mission_id> <run_id> tool_call "Searching for window washing contractors in Chicago" "research" '{"tool": "WebSearch", "query": "commercial window washing contractors Chicago"}'
```

---

## Phase 4: Scheduling Calls/SMS

### Business Hours Consideration

**CRITICAL**: Before scheduling calls, consider business hours:
- Typical business hours: 9 AM - 5 PM local time
- If current time is outside business hours, schedule for next business day
- `scheduled_at_fixed_datetime` must be in the future (at least 1 minute from now)

### Step 4.1: Schedule a Phone Call

```bash
python telnyx_api.py schedule-call <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" <mission_id> <run_id> <step_id>
```

**Save the returned `scheduled_event_id`**.

### Step 4.2: Schedule an SMS

```bash
python telnyx_api.py schedule-sms <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" "Hi! I am reaching out on behalf of [COMPANY] to inquire about your window cleaning rates for commercial buildings. Could you share your pricing?" <mission_id> <run_id> <step_id>
```

### Step 4.3: Log Each Scheduled Event

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom "Scheduled call to ABC Window Cleaning for 2:30 PM" "calls" '{"scheduled_event_id": "<event_id>", "contractor": "ABC Window Cleaning", "phone": "+15551234567", "scheduled_for": "2024-12-01T14:30:00Z"}'
```

---

## Phase 5: Monitoring Call Completion

After a call is scheduled, you need to poll for completion.

### Step 5.1: Check Scheduled Event Status

```bash
python telnyx_api.py get-event <assistant_id> <scheduled_event_id>
```

### Event Status Values

The event-level `status` tracks the overall lifecycle:

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Waiting for scheduled time | Wait and check again later |
| `in_progress` | Call/SMS in progress | Check again in a few minutes |
| `completed` | Finished successfully | Get conversation_id, fetch insights |
| `failed` | Failed after retries | Consider rescheduling |

### Call Status Values (Phone Calls Only)

The `call_status` field provides the telephony-level outcome. **This is the most important field for deciding what to do next.**

| call_status | Meaning | Action |
|-------------|---------|--------|
| `ringing` | Phone is ringing, not yet answered | Still in progress — wait and poll again in 1-2 minutes |
| `in-progress` | Call is active, conversation ongoing | Still in progress — poll again in 2-3 minutes |
| `completed` | Call connected and finished normally | Success — get `conversation_id`, fetch insights |
| `no-answer` | Phone rang but nobody picked up | **Retryable** — reschedule for a different time |
| `busy` | Line is busy | **Retryable** — reschedule in 10-15 minutes, line may free up quickly |
| `canceled` | Call was canceled | Check if you canceled it; if not, may need to reschedule |
| `failed` | Call failed (network/system error) | **Retryable** — reschedule after a short backoff (5-10 minutes) |

### Step 5.2: Polling Strategy

**When to start polling**: A few minutes after `scheduled_at_fixed_datetime`

**Polling intervals based on call_status**:
- `ringing` → poll again in 1-2 minutes (call may connect any moment)
- `in-progress` → poll again in 2-3 minutes (conversation is happening)
- `pending` (event status) → poll every 5 minutes until scheduled time passes
- `no-answer` / `busy` / `failed` → stop polling, handle retry immediately
- `completed` → done, proceed to fetch insights

**Timeout**: If still `ringing` or `in-progress` after 30 minutes, treat as failed.

### Step 5.3: Handle Retryable Call Statuses

When `call_status` is `no-answer`, `busy`, or `failed`, the call can be retried:

1. Update the call tracker with the failure reason
2. Check retry count — by default, retry up to 3 times (unless user specifies otherwise)
3. Schedule a retry at a different time based on the failure type:
   - `busy` → retry in 10-15 minutes (line may free up)
   - `no-answer` → retry in 30 minutes to 2 hours (try a different time of day)
   - `failed` → retry in 5-10 minutes (transient error)
4. Log the failure and retry as events

```bash
# Update tracker
python telnyx_api.py save-memory "<slug>" "call_tracker" '{"+15551234567": {"status": "no_answer", "attempts": 1, "call_status": "no-answer", "next_retry": "2024-12-02T10:00:00Z"}}'

# Log the failure
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Call not answered (busy), scheduling retry #2" "calls" '{"phone": "+15551234567", "call_status": "busy", "attempt": 1}'

# Schedule retry
python telnyx_api.py schedule-call <assistant_id> "+15551234567" "+15559876543" "2024-12-02T10:00:00Z" <mission_id> <run_id> <step_id>
```

---

## Phase 6: Getting Conversation Insights

Once a call completes and you have a `conversation_id`, retrieve the conversation insights.

**IMPORTANT**: Always use insights to get the call summary. Do NOT fetch raw conversation messages - insights provide a structured summary of the conversation outcome.

### Step 6.1: Get Conversation Insights

```bash
python telnyx_api.py get-insights <conversation_id>
```

### Step 6.2: Poll Until Insight is Complete

The insight may not be immediately ready after the call ends. **You must poll until the insight status is "completed".**

**Polling strategy:**
- Check immediately after getting the `conversation_id`
- If status is NOT "completed", wait 10 seconds and retry
- Continue polling until status is "completed" or 20 minutes have passed
- Only use the insight data when status is "completed"

**Example polling flow:**
```bash
# First attempt
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress

# Wait 10 seconds, try again
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress

# Wait 10 seconds, try again
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight: Customer quoted $350 for a 10-story building...
```

### Step 6.3: Rename the Conversation

By default, all conversations are named "Voice Assistant Conversation" which is useless for reviewing in the portal. **Rename each conversation** with a meaningful label after it completes:

```bash
python telnyx_api.py rename-conversation "<conv_id>" "Call 1: ABC Window Cleaning - $350/visit"
```

**Best practice:** Include the call sequence number, target name, and key outcome in the name. This makes conversations instantly identifiable when browsing the mission in the Telnyx portal.

### Step 6.4: Log the Insight

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom "Call completed with ABC Window Cleaning - quoted $350" "calls" '{"conversation_id": "<conv_id>", "contractor": "ABC Window Cleaning", "outcome": "success", "quote": "$350", "availability": "next week", "notes": "Willing to negotiate for recurring contracts"}'
```

---

## Phase 7: Complete the Mission

### ⚠️ MANDATORY Completion Checklist

**Every mission MUST complete ALL of these before it can be considered done.** Skipping any of these leaves the mission in a broken state in the Telnyx portal.

| # | Action | Command | Why |
|---|--------|---------|-----|
| 1 | **Update ALL plan step statuses** | `update-step <mid> <rid> <step_id> completed` | Steps show in portal — "pending" means it looks unfinished |
| 2 | **Log events for every completed call** | `log-event ... custom "Call completed" <step_id> '{"conversation_id": "..."}'` | Creates audit trail linking conversations to the mission |
| 3 | **Set run result_summary** | Included in `complete` or `update-run` | Human-readable summary visible in portal |
| 4 | **Set run result_payload** | Included in `complete` or `update-run` | Structured data for programmatic consumption |
| 5 | **Mark run as succeeded/failed** | `complete` or `update-run <mid> <rid> succeeded` | Closes the run |

**The `complete` command handles #3, #4, and #5 in one call** — but you still need to do #1 and #2 yourself.

```bash
# 1. Update every step status (do this THROUGHOUT the mission, not just at the end)
python telnyx_api.py update-step <mission_id> <run_id> "setup" "completed"
python telnyx_api.py update-step <mission_id> <run_id> "calls" "completed"
python telnyx_api.py update-step <mission_id> <run_id> "analyze" "completed"

# 2. Complete the run with summary and payload
python telnyx_api.py complete "<slug>" <mission_id> <run_id> \
  "Contacted 5 contractors, received 4 quotes. Best: ABC Cleaning ($350)" \
  '{"contractors_contacted": 5, "quotes_received": 4, "recommended": [{"name": "ABC Cleaning", "quote": 350}]}'
```

**Common mistake:** Logging `step_completed` events but NOT calling `update-step`. These are separate — events are the audit log, step status is the progress tracker. You need BOTH.

### Step 7.1: Analyze Results

After all calls complete:
1. Compare quotes and outcomes
2. Select best options based on criteria
3. Prepare summary for user

### Step 7.2: Complete the Run

Use the `complete` command to set result_summary, result_payload, mark the run as succeeded, and clean up state in one step:

```bash
python telnyx_api.py complete "find-window-washing-contractors" <mission_id> <run_id> "Contacted 5 contractors, received 4 quotes. Best options: ABC Cleaning ($350) and XYZ Windows ($380)." '{"contractors_contacted": 5, "quotes_received": 4, "recommended": [{"name": "ABC Cleaning", "quote": 350}, {"name": "XYZ Windows", "quote": 380}]}'
```

Or use `update-run` directly with all fields:

```bash
python telnyx_api.py update-run <mission_id> <run_id> succeeded "Human-readable summary here" '{"structured": "payload"}'
```

The `complete` command also removes the mission from the state file.

---

# Event Logging Reference

**Log EVERY action as an event for complete audit trail.** Events are stored in the cloud and provide permanent backup even if local files are lost.

## CRITICAL: Update Step Status (Not Just Events!)

**You MUST update the plan step status via `update-step` when starting or completing each step.** Logging events alone does NOT change the step status — the client tracks progress by looking at step statuses, not events.

```bash
# When STARTING a step:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "in_progress"
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_started "Starting: Research contractors" "research"

# When COMPLETING a step:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "completed"
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_completed "Completed: Research contractors" "research"

# When a step FAILS:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "calls" "failed"
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" error "Failed: Could not reach any contractors" "calls"

# To SKIP a step:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "setup" "skipped"
```

**Always call `update-step` BEFORE `log-event`** — this ensures the step status is correct even if the event logging fails.

## IMPORTANT: step_id is Required

**step_id is a required parameter** - it links events to your plan steps, enabling tracking of which activities belong to which phase.

```bash
# With step_id (links to plan step)
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Found contractor" "research" '{"name": "ABC"}'

# Use "-" if event doesn't belong to a specific step
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "General note" "-" '{"note": "value"}'
```

The step_id should match one of the step_id values from your plan (e.g., "research", "setup", "calls", "analyze").

| Action | Step Status Update | Event Type | step_id | Example Summary |
|--------|-------------------|------------|---------|-----------------|
| Starting a plan step | `update-step ... in_progress` | `step_started` | step_id | "Starting: Research contractors" |
| Completing a step | `update-step ... completed` | `step_completed` | step_id | "Completed: Research contractors" |
| Step failed | `update-step ... failed` | `error` | step_id | "Failed: Could not reach contractors" |
| Web search | — | `tool_call` | "research" | "Searching for window cleaning contractors" |
| Creating assistant | — | `custom` | "setup" | "Created voice assistant: ast_123" |
| Scheduling call | — | `custom` | "calls" | "Scheduled call to ABC for 2:30 PM" |
| Call completed | — | `custom` | "calls" | "Call completed with ABC - got quote $350" |
| Call failed | — | `error` | "calls" | "Call to XYZ not answered after 3 attempts" |
| Decision made | — | `message` | "analyze" | "Selected ABC and XYZ as top choices" |

---

# Quick Reference: All Commands

```bash
# Check setup
python telnyx_api.py check-key

# Missions
python telnyx_api.py create-mission <name> <instructions>
python telnyx_api.py get-mission <mission_id>
python telnyx_api.py list-missions

# Runs
python telnyx_api.py create-run <mission_id> <input_json>
python telnyx_api.py get-run <mission_id> <run_id>
python telnyx_api.py update-run <mission_id> <run_id> <status>
python telnyx_api.py list-runs <mission_id>

# Plan
python telnyx_api.py create-plan <mission_id> <run_id> <steps_json>
python telnyx_api.py get-plan <mission_id> <run_id>
python telnyx_api.py update-step <mission_id> <run_id> <step_id> <status>
# status: pending, in_progress, completed, skipped, failed

# Events (step_id is REQUIRED - use "-" if no specific step)
python telnyx_api.py log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]
python telnyx_api.py list-events <mission_id> <run_id>

# Assistants
python telnyx_api.py list-assistants [--name=<filter>] [--page=<n>] [--size=<n>]
python telnyx_api.py create-assistant <name> <instructions> <greeting> [options_json]
python telnyx_api.py get-assistant <assistant_id>
python telnyx_api.py update-assistant <assistant_id> <updates_json>
python telnyx_api.py get-connection-id <assistant_id> [telephony|messaging]

# Phone Numbers
python telnyx_api.py list-phones [--available]
python telnyx_api.py get-available-phone
python telnyx_api.py assign-phone <phone_id> <connection_id> [voice|sms]

# Scheduled Events
python telnyx_api.py schedule-call <assistant_id> <to_phone> <from_phone> <datetime> <mission_id> <run_id> [step_id] [dynamic_variables_json]
python telnyx_api.py schedule-sms <assistant_id> <to_phone> <from_phone> <datetime> <text> [mission_id] [mission_run_id] [step_id] [dynamic_variables_json]
python telnyx_api.py get-event <assistant_id> <event_id>
python telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
python telnyx_api.py list-events-assistant <assistant_id>

# Insights (conversation results - POLL until status is "completed"!)
python telnyx_api.py get-insights <conversation_id>
python telnyx_api.py rename-conversation <conversation_id> <name>

# Insight Templates (CRUD)
python telnyx_api.py create-insight <name> <instructions> [options_json]  # options: json_schema, webhook
python telnyx_api.py get-insight <insight_id>
python telnyx_api.py list-insights
python telnyx_api.py update-insight <insight_id> <updates_json>

# Insight Groups
python telnyx_api.py create-insight-group <name> [options_json]  # options: description, webhook
python telnyx_api.py get-insight-group <group_id>
python telnyx_api.py list-insight-groups
python telnyx_api.py update-insight-group <group_id> <updates_json>
python telnyx_api.py assign-insight <group_id> <insight_id>
python telnyx_api.py unassign-insight <group_id> <insight_id>

# Mission Run Agents (linking agents to runs)
python telnyx_api.py link-agent <mission_id> <run_id> <telnyx_agent_id>
python telnyx_api.py list-linked-agents <mission_id> <run_id>
python telnyx_api.py unlink-agent <mission_id> <run_id> <telnyx_agent_id>

# State Management
python telnyx_api.py list-state
python telnyx_api.py get-state <slug>
python telnyx_api.py remove-state <slug>

# Memory (SAVE OFTEN!)
python telnyx_api.py save-memory <slug> <key> <value_json>
python telnyx_api.py get-memory <slug> [key]
python telnyx_api.py append-memory <slug> <key> <item_json>

# High-Level Workflows
python telnyx_api.py init <name> <instructions> <request> [steps_json]
python telnyx_api.py setup-agent <slug> <name> <instructions> <greeting>
python telnyx_api.py complete <slug> <mission_id> <run_id> <summary> [payload_json]
```

---

# Complete Example: Window Washing Contractors

```bash
# 1. Initialize the mission (creates mission, run, plan, sets to running)
python telnyx_api.py init "Find window washing contractors" \
  "Find contractors in Chicago, call them, negotiate rates, select best two" \
  "Find me window washing contractors in Chicago" \
  '[{"step_id": "research", "description": "Find contractors online", "sequence": 1}, {"step_id": "setup", "description": "Create voice agent", "sequence": 2}, {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3}, {"step_id": "analyze", "description": "Analyze results", "sequence": 4}]'

# Output: Created mission: mis_abc123
#         Created run: run_def456

# 2. Get the mission slug and IDs from state
python telnyx_api.py get-state "find-window-washing-contractors"

# 3. Mark research step as in_progress and start working
python telnyx_api.py update-step "mis_abc123" "run_def456" "research" "in_progress"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_started "Starting: Find contractors online" "research"

# 4. Setup voice agent (creates assistant, links to run, assigns phone number)
python telnyx_api.py update-step "mis_abc123" "run_def456" "setup" "in_progress"
python telnyx_api.py setup-agent "find-window-washing-contractors" \
  "Contractor Caller" \
  "You are calling to get quotes for commercial window washing. Ask about: rates per floor, availability, insurance. Be professional." \
  "Hi, I am calling to inquire about your commercial window washing services. Do you have a moment to discuss rates?"

# Output: Created assistant: ast_xyz789
#         Linked agent ast_xyz789 to run run_def456
#         Found available: +15559876543
#         Assigned phone number 123456

python telnyx_api.py update-step "mis_abc123" "run_def456" "setup" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: Voice agent setup" "setup"

# 5. Get agent phone from state
AGENT_PHONE=$(python telnyx_api.py get-state "find-window-washing-contractors" | python -c "import sys,json; print(json.load(sys.stdin).get('agent_phone',''))")
ASSISTANT_ID=$(python telnyx_api.py get-state "find-window-washing-contractors" | python -c "import sys,json; print(json.load(sys.stdin).get('assistant_id',''))")

# 6. After research, SAVE to memory AND log events with step_id (CRITICAL!)
python telnyx_api.py append-memory "find-window-washing-contractors" "contractors_found" '{"name": "ABC Cleaning", "phone": "+13125551234", "source": "web search"}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Found contractor: ABC Cleaning" "research" '{"name": "ABC Cleaning", "phone": "+13125551234"}'

python telnyx_api.py append-memory "find-window-washing-contractors" "contractors_found" '{"name": "XYZ Windows", "phone": "+13125555678", "source": "web search"}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Found contractor: XYZ Windows" "research" '{"name": "XYZ Windows", "phone": "+13125555678"}'

# 7. Complete research step, start calls step
python telnyx_api.py update-step "mis_abc123" "run_def456" "research" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: Found 2 contractors" "research"
python telnyx_api.py update-step "mis_abc123" "run_def456" "calls" "in_progress"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_started "Starting: Schedule calls" "calls"

# 8. Schedule calls
python telnyx_api.py schedule-call "$ASSISTANT_ID" "+13125551234" "$AGENT_PHONE" "2024-12-01T15:00:00Z" "$MISSION_ID" "$RUN_ID" "$STEP_ID"

# Output: Scheduled call: evt_abc123

# 9. SAVE scheduled event to memory AND log event with step_id (CRITICAL!)
python telnyx_api.py append-memory "find-window-washing-contractors" "calls_scheduled" '{"event_id": "evt_abc123", "contractor": "ABC Cleaning", "scheduled_for": "2024-12-01T15:00:00Z"}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Scheduled call to ABC Cleaning for 3:00 PM" "calls" '{"scheduled_event_id": "evt_abc123", "contractor": "ABC Cleaning"}'

# 10. Poll for completion (after scheduled time)
python telnyx_api.py get-event "$ASSISTANT_ID" "evt_abc123"

# Output: Status: completed, conversation_id: conv_xyz

# 11. Get insights - POLL UNTIL STATUS IS "completed"
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress
# (wait 10 seconds and retry)

python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress
# (wait 10 seconds and retry)

python telnyx_api.py get-insights "conv_xyz"
# Output: Insight: Customer quoted $350 for a 10-story building. Available next week.
# (status is now "completed" - proceed with the insight data)

# 12. SAVE call results to memory AND log event with step_id (CRITICAL!)
python telnyx_api.py save-memory "find-window-washing-contractors" "call_results" '{"ABC Cleaning": {"status": "completed", "conversation_id": "conv_xyz", "quote": 350, "availability": "next week"}}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Call completed: ABC Cleaning quoted $350, available next week" "calls" '{"contractor": "ABC Cleaning", "quote": 350, "conversation_id": "conv_xyz"}'

# 13. Complete calls step, start analyze step
python telnyx_api.py update-step "mis_abc123" "run_def456" "calls" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: All calls done" "calls"
python telnyx_api.py update-step "mis_abc123" "run_def456" "analyze" "in_progress"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_started "Starting: Analyze results" "analyze"

# 14. Complete the mission (mark analyze step done first)
python telnyx_api.py update-step "mis_abc123" "run_def456" "analyze" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: Analysis done" "analyze"
python telnyx_api.py complete "find-window-washing-contractors" "mis_abc123" "run_def456" \
  "Found 2 best contractors: ABC ($350) and XYZ ($380)" \
  '{"recommended": ["ABC Cleaning", "XYZ Windows"]}'

# Output: Updated run run_def456: succeeded
#         Mission 'find-window-washing-contractors' completed successfully
```

---

# ⚠️ BEFORE CREATING ANYTHING: Review Existing Resources

**Always check what already exists before creating new assistants, insights, or insight groups.** Reuse is better than duplication.

### Pre-flight Checklist

Run these commands at the start of every mission to inventory what's available:

```bash
# 1. Search for existing assistants by name — maybe one already fits your use case
python telnyx_api.py list-assistants --name=Weather
python telnyx_api.py list-assistants  # or list all (paginated)
python telnyx_api.py list-assistants --page=2  # next page

# 2. List existing insight templates — reuse structured insights across missions
python telnyx_api.py list-insights

# 3. List existing insight groups — you may only need to add an insight to an existing group
python telnyx_api.py list-insight-groups

# 4. List available phone numbers — check what's already assigned vs free
python telnyx_api.py list-phones --available
```

**All list commands are paginated.** If you have many resources, page through with `--page=N`. The assistant name filter does substring matching — use it to quickly find relevant assistants instead of scrolling through pages.

### Decision Flow

#### ⚠️ CRITICAL: Reuse Without Modification

**The rule is: reuse existing resources IF you can use them as-is. Do NOT modify existing assistants, insights, or insight groups that may be in use by other missions or users.** Editing a shared resource (e.g., changing an assistant's instructions or an insight's schema) can silently break unrelated workflows that depend on the current configuration.

**Safe to reuse without modification:**
- An existing assistant whose instructions, tools, voice, and settings already match your needs exactly
- An existing insight template whose schema/instructions already extract what you need
- The default "Summary" insight (always reuse this — never recreate it)
- An existing insight group that already contains the insights you need

**When to create new instead of reusing:**
- You need different instructions, tools, voice, or model → **create a new assistant**
- You need a different extraction schema → **create a new insight template**
- You need a different combination of insights → **create a new insight group**
- The existing resource is "close but needs tweaks" → **create new, don't modify the existing one**

**For dynamic context between calls** (e.g., Class 3 Sequential Negotiation, where you inject "best quote so far" into each call), use **dynamic variables passed via the scheduled events API** rather than modifying the assistant. Define variable placeholders in the assistant's instructions (e.g., `{{best_quote}}`) and pass the values at schedule time. This keeps the assistant immutable while varying context per call.

1. **Assistants:** Search for existing assistants. If one matches your needs exactly (instructions, tools, voice, model), reuse it. If it's close but not quite right, **create a new one** — don't modify the existing one:
   ```bash
   python telnyx_api.py list-assistants --name=Weather  # search by name
   python telnyx_api.py get-assistant <id>  # inspect full config before deciding
   # If it fits → reuse as-is
   # If it doesn't fit → create a new assistant instead
   ```

2. **Insights:** A structured insight like "extract high temperature and snow chance" is reusable across many missions. Check `list-insights` before creating a new one. If a good insight exists with the right schema, assign it to your group. If you need a different schema, create a new insight template — don't modify the existing one.

3. **Insight Groups:** Create a new group per mission (they're cheap), but populate it with existing insight templates when they match. Only create new insight templates when your data extraction needs are genuinely new.

4. **Phone Numbers:** Numbers already assigned to a connection can't be reused for a different assistant. Only grab unassigned numbers.

---

# Mission Classes

Not all missions are the same. Before planning, identify which class your mission falls into — it determines whether calls run in parallel or serial, how state flows between calls, and whether human gates are needed.

## Decision Tree

```
Does call N depend on results of call N-1?
  YES → Is it negotiation (leveraging previous results)?
    YES → Class 3: Sequential Negotiation
    NO  → Does it have distinct rounds with human approval?
      YES → Class 4: Multi-Round / Follow-up
      NO  → Class 5: Information Gathering → Action
  NO  → Do you need structured scoring/ranking?
    YES → Class 2: Parallel Screening with Rubric
    NO  → Class 1: Parallel Sweep
```

---

## Class 1: Parallel Sweep

Fan out calls in parallel batches. Every call asks the same question. No call depends on another's results. Collect all answers, then compare.

### When to Use
- Same question to many targets (weather, hours, availability, prices)
- Order doesn't matter — all calls are independent
- You want raw data collection, not scoring or ranking

### Key Patterns
- All calls use the **same assistant** with identical instructions
- Schedule all calls in one batch (respect throttling limits — stagger by 1-2 min)
- Use **structured insights** with a JSON schema to extract comparable data
- Analysis happens after ALL calls complete

### Example 1: Weather IVR Sweep

**Goal:** Call 10 weather stations, extract today's high temperature, compare.

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create IVR assistant with DTMF + structured insight", "sequence": 1},
  {"step_id": "calls", "description": "Schedule calls to all 10 stations", "sequence": 2},
  {"step_id": "poll", "description": "Poll for completion and collect insights", "sequence": 3},
  {"step_id": "analyze", "description": "Compare temperatures, find hottest/coldest", "sequence": 4}
]

# Insight schema
{"type": "object", "properties": {
  "location": {"type": "string"},
  "high_temp_f": {"type": "number"},
  "snow_mentioned": {"type": "boolean"},
  "forecast_summary": {"type": "string"}
}, "required": ["location", "high_temp_f"]}

# Flow:
# 1. Create assistant with send_dtmf tool + insight group
# 2. Schedule all 10 calls in one batch (staggered 1 min apart)
# 3. Cron job polls every 2 min, collects structured insights
# 4. When all done: compare high_temp_f across all results, report hottest city
```

### Example 2: Store Hours Check

**Goal:** Call 10 retail stores to confirm holiday hours.

```bash
# Same pattern: single assistant, all calls in parallel
# Assistant instructions: "You are calling to confirm store hours for [HOLIDAY].
#   Ask: What time do you open and close on [DATE]? Are you open at all?"
# Insight schema:
{"type": "object", "properties": {
  "store_name": {"type": "string"},
  "is_open": {"type": "boolean"},
  "open_time": {"type": "string"},
  "close_time": {"type": "string"},
  "notes": {"type": "string"}
}, "required": ["store_name", "is_open"]}

# Schedule all 10 calls → poll → compare → report table of hours
```

---

## Class 2: Parallel Screening with Rubric

Fan out calls in parallel, but each call follows a structured rubric. Results are scored automatically via structured insights, then ranked post-hoc.

### When to Use
- You need to **rank or shortlist** from many candidates
- Each call evaluates against the same criteria (scorecard)
- Scoring is objective enough to define as a schema
- You want automated ranking, not just raw data

### Key Patterns
- Define the **rubric as a structured insight schema** upfront — include numeric scores, enums, booleans
- The insight template does the scoring automatically from the conversation
- After all calls complete, sort/filter results by score fields
- The assistant instructions should guide the conversation to cover all rubric dimensions

### Example 1: Restaurant Reservation Scout

**Goal:** Call 10 restaurants, score on availability/price/ambiance, rank top 3.

```bash
# Insight schema (the rubric)
{"type": "object", "properties": {
  "restaurant_name": {"type": "string"},
  "has_availability": {"type": "boolean", "description": "Table available for requested date/time/party size"},
  "availability_score": {"type": "integer", "description": "1-5, 5 = exact time available, 1 = nothing close"},
  "price_range": {"type": "string", "enum": ["$", "$$", "$$$", "$$$$"]},
  "estimated_per_person": {"type": "number"},
  "ambiance_notes": {"type": "string"},
  "ambiance_score": {"type": "integer", "description": "1-5 based on description of atmosphere"},
  "wait_time_minutes": {"type": "number"},
  "overall_score": {"type": "integer", "description": "1-10 overall recommendation"}
}, "required": ["restaurant_name", "has_availability", "availability_score", "price_range", "overall_score"]}

# Assistant instructions:
# "You are calling to check availability for dinner Friday at 7pm, party of 4.
#  Ask about: availability, approximate price per person, dress code/atmosphere,
#  expected wait time. Be conversational and polite."

# Flow:
# 1. Create insight template with rubric schema
# 2. Create assistant with insight group wired up
# 3. Schedule all 10 calls in parallel
# 4. Collect structured insights → sort by overall_score desc → report top 3
```

### Example 2: Interview Screening

**Goal:** Phone-screen 10 candidates, score on communication/experience/culture-fit, shortlist top 3.

```bash
# Insight schema (the rubric)
{"type": "object", "properties": {
  "candidate_name": {"type": "string"},
  "communication_score": {"type": "integer", "description": "1-5, clarity and professionalism"},
  "experience_years": {"type": "number"},
  "relevant_experience_score": {"type": "integer", "description": "1-5, relevance to the role"},
  "culture_fit_score": {"type": "integer", "description": "1-5, enthusiasm and alignment"},
  "salary_expectation": {"type": "number"},
  "available_start_date": {"type": "string"},
  "red_flags": {"type": "string", "description": "Any concerns noted"},
  "overall_score": {"type": "integer", "description": "1-10 overall recommendation"}
}, "required": ["candidate_name", "communication_score", "relevant_experience_score", "culture_fit_score", "overall_score"]}

# Assistant instructions cover specific screening questions for the role
# All 10 calls run in parallel → rank by overall_score → shortlist top 3
```

---

## Class 3: Sequential Negotiation

Calls MUST run serially. Each call's strategy depends on previous results. You're leveraging information from earlier calls to get better outcomes in later ones.

**⚠️ NEVER parallelize these.** The entire value comes from sequential information advantage.

### When to Use
- You're **negotiating** — quotes, prices, terms
- "Best quote so far is $X, can you beat it?"
- Each call needs context from all previous calls
- Call ordering is a strategic decision

### Key Patterns
- **Dynamic variables:** Use `dynamic_variables` in the scheduled event to inject context per call — no need to modify the assistant between calls
- **State carries forward:** Track "best offer so far" in memory, pass it as a dynamic variable to the next call
- **Call ordering strategy:** Start with whoever is least likely to give the best deal (weakest hand first) so you build leverage. Save the strongest candidate for last. Alternative: start with whoever will give a reliable baseline.
- **One call at a time:** Schedule (with dynamic vars) → poll → get insight → update state → schedule next
- **Assistant stays immutable** — define `{{best_quote}}` and `{{best_company}}` placeholders in instructions once, then pass different values per call via the scheduled events API

### Example 1: Roofer Quotes

**Goal:** Call 5 roofers sequentially, negotiate each against the best previous quote.

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create assistant + find roofers", "sequence": 1},
  {"step_id": "call-1", "description": "Call roofer 1 (baseline)", "sequence": 2},
  {"step_id": "call-2", "description": "Call roofer 2 with context", "sequence": 3},
  {"step_id": "call-3", "description": "Call roofer 3 with context", "sequence": 4},
  {"step_id": "call-4", "description": "Call roofer 4 with context", "sequence": 5},
  {"step_id": "call-5", "description": "Call roofer 5 with context", "sequence": 6},
  {"step_id": "analyze", "description": "Select best deal", "sequence": 7}
]

# Flow:
# 1. Create assistant with dynamic variable placeholders in instructions:
#    "Ask for a quote for roof repair on a 2000 sq ft home. Get price, timeline, warranty.
#     {{#best_quote}}
#     CONTEXT: You have received a quote of {{best_quote}} from {{best_company}}.
#     Mention this if the price seems high. Ask if they can match or beat it.
#     {{/best_quote}}"
#    Set dynamic_variables: {"best_quote": null, "best_company": null}

# 2. Call roofer 1 (no leverage yet — best_quote is null, so that section is skipped)
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID $STEP_ID
#    → get insight → save quote ($500)
#    python telnyx_api.py save-memory "<slug>" "best_quote" '{"amount": 500, "company": "Roofer 1"}'

# 3. Call roofer 2 — pass dynamic variables via scheduled event:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID $STEP_ID \
#      '{"best_quote": "$500", "best_company": "Roofer 1"}'
#    → get insight → if better ($420), update best_quote

# 4. Call roofer 3 — pass updated context:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID $STEP_ID \
#      '{"best_quote": "$420", "best_company": "Roofer 2"}'

# 5. Repeat: schedule with new dynamic vars → poll → insight → update state → next
# 6. After all 5: report best deal with full comparison
```

### Example 2: Car Insurance Quotes

**Goal:** Call 4 insurance providers, use each quote to leverage the next.

```bash
# Ordering strategy: Start with the provider you care least about (get a baseline),
# end with your preferred provider (maximum leverage).

# Assistant instructions use dynamic variable placeholders:
#   "You are calling about auto insurance for a 2022 Toyota Camry.
#    {{#best_quote}}
#    LEVERAGE: The best quote so far is {{best_quote}}/month
#    from {{best_company}}. Mention this and ask them to beat it.
#    {{/best_quote}}"

# Sequential pattern — pass dynamic variables per call:
# Call 1 (baseline): no leverage vars → "What's your rate for [coverage details]?"
# Call 2: {"best_quote": "$180", "best_company": "Geico"}
# Call 3: {"best_quote": "$155", "best_company": "Progressive"}
# Call 4 (preferred): {"best_quote": "$145", "best_company": "StateFarm"}
```

---

## Class 4: Multi-Round / Follow-up

The mission has distinct phases. Round 1 is broad outreach. Results are analyzed, a human approves the shortlist, then Round 2 does deep-dive calls with a different focus.

### When to Use
- Two or more distinct phases of calling
- Human judgment needed between rounds (approval gate)
- Round 2 targets a subset of Round 1
- Round 2 may use a completely different assistant/instructions

### Key Patterns
- Plan has explicit phases: `round-1-calls`, `round-1-analysis`, `human-approval`, `round-2-calls`
- **Human approval gate:** DM the human via Telegram/Slack with Round 1 results + recommendation. Pause until they respond.
- Round 2 assistant may have **completely different instructions** than Round 1
- Track which candidates advanced to which round in memory
- The cron job for Round 1 should trigger the human DM, then stop. A new cron handles Round 2 after approval.

### Example 1: Vendor Selection

**Goal:** Screen 10 vendors on basic criteria, shortlist top 3 with human approval, deep-dive on technical specs.

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant + insight rubric", "sequence": 1},
  {"step_id": "round-1-calls", "description": "Screen all 10 vendors", "sequence": 2},
  {"step_id": "round-1-analysis", "description": "Rank and shortlist top 3", "sequence": 3},
  {"step_id": "human-approval", "description": "DM human with top 3, wait for approval", "sequence": 4},
  {"step_id": "round-2-setup", "description": "Create deep-dive assistant with technical questions", "sequence": 5},
  {"step_id": "round-2-calls", "description": "Deep-dive calls with approved vendors", "sequence": 6},
  {"step_id": "final-analysis", "description": "Final recommendation", "sequence": 7}
]

# Round 1 assistant: "Ask about pricing, lead time, minimum order, and general capabilities."
# Round 1 insight rubric: price_score, lead_time_days, meets_minimum, capability_match

# After Round 1 completes:
# → Rank by scores → DM human:
#   "Round 1 complete. Top 3 vendors:
#    1. VendorA — score 8.5, $12/unit, 2-week lead
#    2. VendorB — score 7.8, $14/unit, 1-week lead
#    3. VendorC — score 7.2, $11/unit, 3-week lead
#    Approve these for Round 2? Reply YES or adjust."

# Wait for human response (pause cron or check for reply)

# Round 2 assistant (different!): "Ask detailed technical questions:
#   API integration support? SLA guarantees? Disaster recovery?
#   Reference customers we can contact?"
# Round 2 insight rubric: api_support, sla_score, dr_plan, references_provided
```

### Example 2: Candidate Recruiting

**Goal:** Phone-screen 15 candidates (Round 1), shortlist 5 (human approval), detailed interviews (Round 2).

```bash
# Round 1: Quick 5-minute screen — "Tell me about your background, why this role,
#   salary expectations, availability."
# Insight rubric: communication_score, experience_match, salary_in_range, enthusiasm

# → Rank → DM human with top 5 + scores
# → Human approves (or swaps in someone from position 6-7)

# Round 2: 15-minute deep dive — completely different assistant:
#   "Ask about: specific project experience with [TECH], how they handle conflict,
#    a time they failed and what they learned, questions they have for us."
# Different insight rubric: technical_depth, problem_solving, culture_fit, curiosity

# Track in memory:
python telnyx_api.py save-memory "<slug>" "rounds" '{
  "round_1": {"candidates": [...], "advanced": ["+1555...", "+1555..."]},
  "round_2": {"candidates": [...], "results": [...]}
}'
```

---

## Class 5: Information Gathering → Action

Call to collect information, but the mission doesn't just report — it **takes action** based on results. Once you find what you need, stop searching and act.

### When to Use
- You need to **find** something (availability, a slot, a match) and then **do** something (book it, confirm it, reserve it)
- Early termination: stop calling once the goal is met
- The last call transitions from "asking" to "acting"

### Key Patterns
- **Early termination:** When a call succeeds (e.g., restaurant has availability), cancel remaining scheduled calls. Use `list-events-assistant` to find pending events, then `cancel-scheduled-event` to cancel each one.
- **Two-phase assistant instructions:** Phase 1 = "Are you available?" (screening). Phase 2 = "I'd like to book" (action). Use `update-assistant` to switch modes.
- **Fallback expansion:** If the first batch yields no results, expand to more candidates
- **The action step is the goal** — the mission succeeds when the action is taken, not when all calls complete

### Example 1: Restaurant Booking

**Goal:** Call restaurants until one has availability Friday 7pm for 4, then book it.

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant", "sequence": 1},
  {"step_id": "screen", "description": "Call restaurants to check availability", "sequence": 2},
  {"step_id": "book", "description": "Book at first available restaurant", "sequence": 3}
]

# Flow:
# 1. Create assistant: "Call and ask if they have a table for 4 this Friday at 7pm.
#    If yes, say you'd like to book it under the name [NAME]. Confirm the reservation.
#    If no, ask about Saturday instead, then politely end the call."

# 2. Schedule calls to 5 restaurants (parallel — screening doesn't depend on each other)

# 3. Poll results as they come in:
#    - Restaurant A: no availability → continue
#    - Restaurant B: has availability, BOOKED! → SUCCESS
#    - Cancel/ignore remaining calls (Restaurants C, D, E)
#    - If none of the 5 work: expand to 5 more restaurants (fallback)

# Insight schema:
{"type": "object", "properties": {
  "restaurant_name": {"type": "string"},
  "has_availability": {"type": "boolean"},
  "reservation_confirmed": {"type": "boolean"},
  "reservation_time": {"type": "string"},
  "reservation_name": {"type": "string"},
  "confirmation_number": {"type": "string"},
  "alternative_offered": {"type": "string"}
}, "required": ["restaurant_name", "has_availability", "reservation_confirmed"]}

# Early termination: when reservation_confirmed = true, mission succeeds
```

### Example 2: Appointment Scheduling

**Goal:** Call dentist offices until one has a slot this week, confirm the appointment.

```bash
# Same pattern as restaurant booking:
# 1. Screen in parallel: "Do you have any openings this week for a cleaning?"
# 2. First office with availability: "I'd like to book that slot for [NAME], DOB [DOB]."
# 3. Stop remaining calls once booked.

# Key difference: may need to provide insurance info, patient details.
# Assistant instructions include all necessary details upfront.

# Fallback: if no office has availability this week, expand search to next week
# or expand to more offices.
```

---

## Cross-Cutting Patterns

These patterns apply across multiple mission classes.

### 1. Dynamic Context Between Calls

Use **dynamic variables** passed via the scheduled events API to inject context from previous call results into each call. This keeps the assistant immutable — define `{{variable}}` placeholders in instructions once, then pass different values per scheduled event. Essential for Class 3 (Sequential Negotiation) and Class 5 (action phase).

```bash
# Assistant instructions use placeholders:
#   "You are calling to get a quote for roof repair on a 2000 sq ft home.
#    {{#best_quote}}
#    IMPORTANT CONTEXT: Another contractor has quoted {{best_quote}}.
#    If this contractor quotes higher, mention you have a better offer and ask if
#    they can match or beat it. Be professional but firm.
#    {{/best_quote}}"

# After getting a quote of $350 from call 1, pass it as a dynamic variable on call 2:
python telnyx_api.py schedule-call <assistant_id> "+1555..." "+1555..." "<time>" <mission_id> <run_id> <step_id> '{"best_quote": "$350", "best_company": "ABC Roofing"}'
```

### 2. Human Approval Gates

Between rounds or before taking action, DM the human and pause.

```
# Pattern:
# 1. Cron job detects Round 1 complete
# 2. Formats results summary
# 3. Sends message to human via Telegram/Slack
# 4. Saves state: {"awaiting_approval": true, "approval_summary": "..."}
# 5. Cron continues to poll but takes no action until human responds
# 6. Human replies "approved" or "change X" → cron detects reply → proceeds
```

### 3. Early Termination

When the goal is met, stop unnecessary remaining calls.

```bash
# Check for pending events:
python telnyx_api.py list-events-assistant <assistant_id>

# Cancel each pending event:
python telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
```

### 4. Call Ordering Strategy

For Sequential Negotiation (Class 3), order matters:

- **Weakest first:** Start with vendors you care least about. Get a baseline without pressure. Use their quotes as leverage for better vendors.
- **Strongest last:** Save your preferred vendor for when you have maximum leverage.
- **Baseline first:** Alternatively, start with whoever will give a reliable, honest baseline quote — then use it against everyone else.
- **Random for parallel:** For Classes 1 and 2, order doesn't matter. Schedule however is convenient.

---

# Operational Guide: Best Practices for Voice Missions

This section covers real-world considerations for running voice missions at scale. **Read this before planning any mission involving outbound calls.**

## Default Tools: Always Include send_dtmf

**The `send_dtmf` tool is included by default** on all assistants created by this skill. Most outbound calls — even to businesses with live staff — will hit an IVR or phone tree first before reaching a person. Without `send_dtmf`, the assistant can't navigate these menus and the call will fail or time out.

If you explicitly pass a custom `tools` list, make sure to include `send_dtmf` unless you have a specific reason not to.

## Noise Suppression: Disabled by Default

**Noise suppression is disabled by default** for mission assistants. Aggressive noise suppression (krisp, deepfilternet) can interfere with IVR tones, hold music, and low-quality phone audio, causing the assistant to miss information. Only enable it if you're in a known-noisy environment and calling humans directly.

## IVR Navigation Tips

**Tip:** Some numbers include required button presses in their listing (e.g., `602-275-0073(#4)`). Include these in the assistant's instructions: *"After connecting, press # then 4 to reach the local forecast."*

**Expect IVRs even when calling businesses.** Most restaurants, hotels, and offices have a phone tree. Instruct the assistant: *"If you reach an automated menu, press 0 or say 'representative' to reach a person. If you hear options, press the one for reservations/front desk."*

## Insights Over Transcripts

**Always prefer structured insights over raw transcripts for analyzing call results.** Insights give you machine-readable, consistent data. Transcripts are noisy and require parsing.

### Setting Up Structured Insights for a Mission

**Step 1: Create a structured insight template** with a JSON schema defining exactly what to extract:

```bash
python telnyx_api.py create-insight "Weather Forecast Data" \
  "Extract weather forecast information from the recorded forecast. Listen for today's high temperature, any mention of snow or snow probability, and a brief summary of conditions." \
  '{"json_schema": {"type": "object", "properties": {"location": {"type": "string", "description": "City or region name"}, "high_temp_f": {"type": "number", "description": "Todays high temperature in Fahrenheit"}, "low_temp_f": {"type": "number", "description": "Todays low temperature in Fahrenheit"}, "snow_mentioned": {"type": "boolean", "description": "Whether snow was mentioned in the forecast"}, "snow_chance_pct": {"type": "number", "description": "Snow probability percentage if mentioned, null otherwise"}, "forecast_summary": {"type": "string", "description": "Brief summary of forecast conditions"}}, "required": ["location", "high_temp_f", "snow_mentioned"]}}'
```

**Step 2: Create an insight group and assign the insight:**

```bash
python telnyx_api.py create-insight-group "Weather Mission Insights"
python telnyx_api.py assign-insight <group_id> <insight_id>
```

**Step 3: Wire the group to the assistant** via `insight_settings`:

```bash
python telnyx_api.py create-assistant "Weather Listener" \
  "..." "..." \
  '{"features": ["telephony"], "insight_settings": {"insight_group_id": "<group_id>"}}'
```

Now every completed call automatically produces structured JSON you can compare across calls — no transcript parsing needed.

### Always Pair Structured Insights with an Unstructured Summary

**When creating structured insights, always also add an unstructured "Conversation Summary" insight to the group.** Structured schemas only capture what you explicitly define — if the conversation reveals something unexpected (an alternative time offered, a special event mentioned, a caveat), the structured insight will miss it.

**Every account has a default "Summary" insight** — search for it and reuse it instead of creating a new one:

```bash
# 1. Find the default Summary insight (may be on later pages — paginate!)
python telnyx_api.py list-insights
python telnyx_api.py list-insights --page=2
# Look for one named "Summary" (unstructured) — it's typically one of the earliest created

# 2. Only if you can't find it, create one:
python telnyx_api.py create-insight "Conversation Summary" \
  "Provide a detailed summary of the entire conversation. Include everything discussed: what was asked, what was answered, any alternatives offered, tone of the interaction, and any information that might be useful but wasn't explicitly asked about. Be thorough — this is the safety net for anything the structured extraction might miss."

# 3. Add BOTH structured + summary to the insight group
python telnyx_api.py assign-insight <group_id> <structured_insight_id>
python telnyx_api.py assign-insight <group_id> <summary_insight_id>
```

This way you get clean structured data for ranking/comparison AND a full narrative you can fall back on.

### When to Use Unstructured Insights

Use unstructured (free-text) insights when:
- You need open-ended summaries or qualitative analysis
- The data you want doesn't fit a fixed schema
- You're exploring what information is available before defining structure

Use structured insights when:
- You need to compare data across many calls (scores, categories, numbers)
- You're feeding results into analytics or dashboards
- You need boolean flags or enum classifications
- The mission has a clear set of data points to extract

## Call Limits and Throttling

**Be aware of your Telnyx account's concurrent call limits.** Firing 100 outbound calls simultaneously will hit rate limits and fail.

### Recommended approach:
- **Check your account limits** before planning batch sizes
- **Stagger calls in batches** — e.g., 5-10 concurrent calls, wait for completion, then next batch
- **Space scheduled times** — schedule calls at least 1-2 minutes apart within a batch
- **Monitor failures** — if you see rate limit errors (HTTP 429), reduce batch size and increase spacing
- **Log batch progress** — track which batch you're on in mission memory so you can resume after failures

### Example batching pattern:
```
Batch 1: Numbers 1-10  → schedule at T+0, T+1m, T+2m, ... T+9m
Wait for Batch 1 completion (poll all events)
Batch 2: Numbers 11-20 → schedule at T+0, T+1m, ...
...
```

## Answering Machine Detection (AMD / Voicemail Detection)

The assistant supports voicemail detection via `telephony_settings.voicemail_detection`. **Use it wisely based on your target:**

### When to ENABLE AMD:
- Calling **humans** where you want to leave a voicemail or skip machines
- Outbound sales/outreach where talking to a live person matters
- Configure `on_voicemail_detected` action:
  - `stop_assistant` — just hang up, don't leave a message
  - `leave_message_and_stop_assistant` — leave a voicemail, then hang up

```bash
# Just hang up on voicemail (no message)
python telnyx_api.py create-assistant "Human Caller" "..." "..." \
  '{"features": ["telephony"], "telephony_settings": {"voicemail_detection": {"on_voicemail_detected": {"action": "stop_assistant"}}}}'

# Leave a voicemail message, then hang up
python telnyx_api.py create-assistant "Human Caller" "..." "..." \
  '{"features": ["telephony"], "telephony_settings": {"voicemail_detection": {"on_voicemail_detected": {"action": "leave_message_and_stop_assistant", "voicemail_message": {"type": "prompt", "prompt": "Leave a brief message explaining why you called and ask them to call back."}}}}}'
```

### When to DISABLE AMD (or omit it):
- Calling **IVR systems, automated lines, or recordings** — AMD would detect "machine" and hang up on the exact thing you're trying to interact with
- Any scenario where the "answering machine" IS the target
- **Calling businesses with phone trees** — many restaurants, hotels, and service businesses use automated greetings or "press 1 for..." menus. AMD will classify these as machines and prevent your assistant from navigating the menu with DTMF or voice. Disable AMD so the assistant can interact normally.
- When you want the assistant to engage regardless of what picks up

**How to disable AMD:** Set the action to `continue_assistant` — this tells the assistant to keep going even if voicemail/machine is detected. Do NOT set `voicemail_detection` to `null` — that may not stick or may revert to defaults on some API operations.

```bash
python telnyx_api.py update-assistant <assistant_id> '{"telephony_settings": {"voicemail_detection": {"on_voicemail_detected": {"action": "continue_assistant"}}}}'
```

**Rule of thumb:** If there's any chance the call will be answered by an automated greeting, phone tree, or IVR — even a simple "press 1 for reservations" — disable AMD. It's better to handle a voicemail manually than to have AMD block your assistant from navigating a phone menu.

## Polling for Results: Use Cron Jobs

After scheduling calls, **do not block the main session with polling loops.** Instead, set up a cron job to poll for results periodically.

### The Pattern

1. **Main session** handles setup + scheduling (interactive, needs human input)
2. **Main session creates a cron job** that periodically checks call status
3. **Cron job** (isolated session) loads mission memory, polls pending events, collects insights, updates tracker, handles retries
4. **Cron job removes itself** when all calls are resolved (succeeded/abandoned)
5. **Cron job reports results** to the human via the configured channel

### Why Cron Over Sub-Agents

- **No timeout limits** — missions can span minutes or hours (retries across business hours)
- **Doesn't burn a session** — fires briefly every N minutes, not continuously
- **Handles mixed durations** — fast batch results + slow retries in the same mission
- **Survives session restarts** — cron persists independently of the main session

### Safety: Cron Jobs Must Never Schedule Uncontrolled Calls

**CRITICAL:** The polling cron job must ONLY:
- Poll event status (read-only)
- Collect insights (read-only)
- Schedule retries ONLY when the attempt counter is below the max AND the status warrants it

**Never** schedule new calls without checking the tracker first. The cron should be **idempotent** — running it twice with the same state must not produce duplicate calls. Always check `status` and `attempts` before scheduling anything.

**Always clean up:** The cron MUST remove itself when the mission is complete. Include the cron job ID in the task prompt so the isolated session can call `cron remove`.

### Cron Must Complete the Full Mission Lifecycle

The polling cron isn't just checking statuses — it's responsible for the FULL mission lifecycle after calls are scheduled. The cron task prompt MUST include instructions to:

1. **Poll event statuses** for all pending calls
2. **Collect insights** from completed conversations
3. **Log events** for each completed call (with conversation_id in payload)
4. **Update plan step statuses** — call `update-step` to mark steps as `in_progress`/`completed`/`failed`, AND log corresponding events
5. **Save results to mission memory** — intermediate and final results
6. **Handle retries** — schedule retries for failures (checking tracker first)
7. **Complete the mission** — mark all remaining steps as `completed` (or `failed`/`skipped`), then call `complete` with `result_summary` and `result_payload`
8. **Report to human** — send summary via Telegram/Slack
9. **Remove itself** — delete the cron job

**If you skip steps 3-7, the mission will look abandoned in the Telnyx portal** — run status stuck on "running", plan steps all "pending", no results recorded. The portal is the source of truth for anyone reviewing missions.

### Linking Conversations to Missions

When a call completes and you get a `conversation_id`, always log it as an event on the mission run. This creates the link between the conversation and the mission in the audit trail:

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom \
  "Call completed: Miami FL" "batch-calls" \
  '{"conversation_id": "conv_xyz", "location": "Miami FL", "phone": "+13052294550"}'
```

There is no dedicated API to formally link conversations to mission runs. The `link-agent` command links the assistant, but individual conversations are tracked via events. **Always include conversation_id in event payloads** so the relationship is traceable.

### Cron Job Setup

After scheduling calls, create a cron job like:

```
Schedule: every 2-3 minutes
Session: isolated (agentTurn)
Task: "Load mission memory from .missions_state.json for slug '<slug>'.
  For each call in call_tracker with status 'scheduled' or 'in_progress':
    - Poll get-event for the event_id
    - If completed with conversation_id: get-insights, update status to 'succeeded', save results
    - If failed: increment attempts, schedule retry if under max, or mark abandoned
  When ALL calls are succeeded or abandoned:
    - Update plan step statuses: update-step for each step (completed/failed)
    - Run analysis (compare results)
    - Complete the mission (update-step for analyze step, then complete command)
    - Report summary to the human
    - Remove this cron job"
```

### Cron Polling Intervals

| Phase | Interval | Rationale |
|---|---|---|
| Active calls (just scheduled) | Every 2-3 min | Calls complete within minutes |
| Waiting for retries | Every 10-15 min | Retries are spaced out |
| All calls complete, analyzing | One-shot | Final analysis, then done |

Adjust the interval based on the mission — short batch sweeps poll frequently, long-running outreach can poll less often.

### Sequential Mission Cron Pattern

For Class 3 (Sequential Negotiation) and other serial missions, the cron job does more than just poll — it drives the entire call chain. Each poll iteration must:

1. **Check if the current call is complete** (poll the active event)
2. **Collect insights** from the completed conversation
3. **Update the step status** (`update-step` for the completed call step)
4. **Extract dynamic variables** from the insight (e.g., the quote amount) for the next call
5. **Schedule the next call** with updated `dynamic_variables`
6. **Update the next step** to `in_progress`
7. **Repeat** until all sequential calls are done
8. **Complete the mission** with `result_summary` and `result_payload`

```
Schedule: every 2-3 minutes
Session: isolated (agentTurn)
Task: "Load mission state for slug '<slug>'.
  Check which call we're on (e.g., call_sequence: 1 of 3).
  Poll get-event for the current event_id.
  If still in progress: wait for next poll.
  If completed:
    - Get insights from the conversation
    - Update step status: update-step <mid> <rid> 'call-N' completed
    - Log event with conversation_id
    - Extract negotiation context from insight (e.g., quote, terms)
    - If more calls remain:
      - Schedule next call with dynamic_variables from extracted context
      - Update step status: update-step <mid> <rid> 'call-N+1' in_progress
      - Save updated state (increment call_sequence, save new event_id)
    - If all calls done:
      - Update analyze step, run analysis, complete the mission
      - Report summary to human
      - Remove this cron job"
```

**Key difference from parallel polling:** The cron is stateful — it tracks which call in the sequence is active and drives the chain forward. Save `call_sequence`, `current_event_id`, and accumulated results in mission memory so the cron can resume correctly after each firing.

## Retry Strategy

Every mission involving outbound calls needs a retry plan. Calls fail — busy signals, no answer, network issues, IVR timeouts.

### Tracking Call Status

Track every number's status in mission memory:

```bash
python telnyx_api.py save-memory "<slug>" "call_tracker" '{
  "+15551234567": {"status": "pending", "attempts": 0, "location": "Phoenix, AZ"},
  "+15559876543": {"status": "pending", "attempts": 0, "location": "Chicago, IL"}
}'
```

Status values: `pending` → `scheduled` → `succeeded` | `failed` | `no_answer` | `busy` | `abandoned`

The tracker `status` should reflect the `call_status` from the API response:
- `call_status: completed` → tracker status: `succeeded`
- `call_status: no-answer` → tracker status: `no_answer`
- `call_status: busy` → tracker status: `busy`
- `call_status: failed` → tracker status: `failed`
- `call_status: canceled` → tracker status: `abandoned` (unless you want to retry)

### Retry Policy

Retry strategy depends on **who you're calling**. An IVR or restaurant front desk can be called back in minutes. A vendor, interview candidate, or professional contact should get a voicemail and a callback days later during business hours.

#### Retry by Recipient Type

**Automated systems (IVR, hotlines, info lines):**

| Failure Type | Max Retries | Backoff | Notes |
|---|---|---|---|
| No answer | 3 | 15 min | System may be temporarily busy |
| Busy signal | 3 | 10 min | Line may free up quickly |
| Network/timeout | 2 | 5 min | Transient, retry sooner |
| Empty insights | 2 | 15 min | Adjust DTMF or instructions |

**Service industry (restaurants, shops, front desks):**

| Failure Type | Max Retries | Backoff | Notes |
|---|---|---|---|
| No answer | 3 | 30 min - 2 hours | Try different times; avoid peak hours (lunch/dinner for restaurants) |
| Busy signal | 3 | 15-30 min | Front desk may be slammed |
| Voicemail | 1 | Leave message, retry next business day | Don't leave multiple voicemails |
| Empty insights | 2 | 1 hour | May have reached wrong dept |

**Professionals (vendors, candidates, B2B contacts):**

| Failure Type | Max Retries | Backoff | Notes |
|---|---|---|---|
| No answer | 2 | 1-2 business days | Enable AMD — leave a voicemail on first no-answer |
| Voicemail | 0 | — | Leave one voicemail with callback info, don't call again until they respond or 2+ days pass |
| Busy signal | 2 | 2-4 hours | They're on another call |
| Empty insights | 1 | Next business day | Retry with clearer instructions |

**Key rules for professional contacts:**
- **Always enable voicemail detection** — leave a professional message on no-answer
- **Never call the same person twice in one day** unless they asked you to
- **Business hours only** — schedule retries between 9 AM - 5 PM in the recipient's timezone
- **One voicemail max** — leaving multiple voicemails is pushy and counterproductive
- **Track voicemails left** in the call tracker: `"voicemail_left": true`

#### General Failure Types

**"Call completed with empty insights"** is a distinct failure from "call failed." The call connects but insight extraction returns nothing. Causes:
- IVR menu wasn't navigated correctly (missing DTMF)
- Recording was too short or garbled
- Assistant spoke over the recording instead of listening
- Wrong department or menu path reached

Consider retrying with adjusted instructions or DTMF sequences.

### Retry Flow

1. After each call completes (or fails), update the tracker:
```bash
python telnyx_api.py save-memory "<slug>" "call_tracker" '{"+15551234567": {"status": "no_answer", "attempts": 1, "last_attempt": "2024-12-01T15:00:00Z", "next_retry": "2024-12-01T15:15:00Z"}}'
```

2. After each batch, scan for retryable failures and schedule the next attempt
3. After max retries, mark as `abandoned` and move on
4. Log all retries as events so the audit trail is complete:
```bash
python telnyx_api.py log-event "$MID" "$RID" custom "Retry #2 for Phoenix - no answer on first attempt" "calls" '{"phone": "+15551234567", "attempt": 2, "reason": "no_answer"}'
```

### Time-Based Retry Spread

For missions spanning many numbers, spread retries across time:
- **Attempt 1:** Original scheduled time
- **Attempt 2:** 15-30 minutes later
- **Attempt 3:** 2-4 hours later or next business day
- This increases the chance of reaching a live system or avoiding peak congestion

## Phone Number Selection

When assigning phone numbers to an assistant:

1. **Prefer HD voice numbers** — `get-available-phone` automatically prioritizes these
2. **Fall back gracefully** — not all number types support HD voice; the skill handles this
3. **For IVR calls**, HD voice improves transcription accuracy since the audio quality is better
4. **For human calls**, HD voice provides a more natural experience

```bash
# Automatically prefers HD voice, falls back if unavailable
python telnyx_api.py get-available-phone

# Assign with HD voice enabled (falls back if not supported)
python telnyx_api.py assign-phone <phone_id> <connection_id> voice

# Explicitly disable HD voice if needed
python telnyx_api.py assign-phone <phone_id> <connection_id> voice --no-hd
```

---

# Error Handling

The Python script provides clear error messages:

1. **No API key**: Prints "ERROR: TELNYX_API_KEY environment variable not set" and exits
2. **HTTP errors**: Prints the status code, reason, and response body
3. **Connection errors**: Prints the connection error details
4. **No available phone numbers**: Prints instructions to purchase at portal.telnyx.com

---

# Troubleshooting

**Command not working?**
1. Check API key: `python telnyx_api.py check-key`
2. Run with verbose output by adding print statements or checking stderr

**JSON parsing errors?**
- Make sure JSON arguments use single quotes around the whole string
- Escape inner quotes or use different quote styles

**Missing arguments?**
- Run `python telnyx_api.py` without arguments to see usage
