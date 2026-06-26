---
name: log-to-incident-report
description: >
  Use when (1) user provides error logs and needs structured incident report with root cause. (2) impact. (3) and fix steps. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Log To Incident Report

Use when (1) user provides error logs and needs structured incident report with root cause. (2) impact. (3) and fix steps. 

## Core Position

This skill solves the specific engineering problem of: *user provides error logs and needs structured incident report with root cause, impact, and fix steps*

This skill is NOT:
- A general-purpose capability that activates on anything
- A replacement for manual human judgment
- A tool that stores state or remembers across sessions

This skill IS activated ONLY when the trigger conditions are explicitly met.

## Modes

### `/log-to-incident-report`

**Default mode.** Performs the core task end-to-end.

When to use: User provides input matching the trigger conditions above.


## Execution Steps

1. **Receive logs** — User pastes error logs, stack traces, or system output
   - Identify the log format (JSON, plain text, structured key=value)
   - Note the time range covered by the logs
   - If the input is not error logs, state: "This skill converts error logs into structured incident reports. Please provide error log content."

2. **Parse and categorize errors** — Extract structured information:
   - Identify unique error types and their frequency
   - Extract error messages, codes, and stack traces
   - Note timestamps to establish an incident timeline
   - Determine affected services, endpoints, or components

3. **Analyze root cause** — Determine what triggered the incident:
   - Cross-reference error patterns with timestamps
   - Identify the first error in the chain (root cause)
   - Note any preceding events that may have contributed
   - Distinguish between symptoms and root causes

4. **Assess impact** — Quantify the scope of the incident:
   - How many users/requests were affected (if derivable from logs)
   - Which services or systems were impacted
   - Duration of the incident (first error to recovery)

5. **Generate incident report** — Produce the structured document:
   - **Incident Summary**: one-paragraph overview
   - **Timeline**: chronological sequence of events
   - **Root Cause**: what caused the incident
   - **Impact**: scope and severity of the incident
   - **Mitigation Steps**: what was done to resolve it
   - **Action Items**: follow-up tasks to prevent recurrence

6. **Deliver with confidence level** — State any assumptions or uncertainties:
   - If root cause is unclear, state "Root cause analysis based on available logs; further investigation may be needed"
   - If impact cannot be determined from logs, state what is unknown

## Mandatory Rules

### Do not

- Do not make up facts or claim actions were taken that were not
- Do not hardcode API keys — use `os.getenv("API_KEY")` instead
- Do not store sensitive user data beyond the current session
- Do not exceed token budget without warning the user first
- Do not activate for off-topic requests — return a brief decline message

### Do

- Validate all inputs before acting
- Handle errors gracefully with actionable error messages
- Log actions taken for auditability
- State explicitly when you are uncertain or data is insufficient

## Quality Bar

**A good output:**
- Solves exactly the problem described in the trigger conditions
- Provides actionable result in the expected format within 3 turns
- Handles error cases with specific guidance, not generic "try again"
- States assumptions explicitly when input is ambiguous

**A bad output:**
- Solves a different problem than the one triggered
- Provides a generic "I can't help with that" without explaining why
- Crashes, hangs, or returns malformed output on valid input
- Activates for off-topic requests (false positive)

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| Trigger matched | "I can help with that." + no action | Correct transformation delivered in structured format |
| Invalid input | Crash or wrong result | "Missing required field: [X]. Please provide [Y]." |
| Ambiguous input | Guesses and might be wrong | States assumption and asks for confirmation |
| Off-topic request | Attempts to help anyway | "This skill activates when [trigger]. Please restate your request." |

## References

- `references/` — Detailed templates, schemas, and edge-case rules for this skill
