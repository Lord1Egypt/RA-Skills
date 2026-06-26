---
name: meeting-transcript-to-summary
description: >
  Use when (1) user pastes meeting transcript and needs structured summary with action items and decision owners. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Meeting Transcript To Summary

Use when (1) user pastes meeting transcript and needs structured summary with action items and decision owners. 

## Core Position

This skill solves the specific engineering problem of: *user pastes meeting transcript and needs structured summary with action items and decision owners*

This skill is NOT:
- A general-purpose capability that activates on anything
- A replacement for manual human judgment
- A tool that stores state or remembers across sessions

This skill IS activated ONLY when the trigger conditions are explicitly met.

## Modes

### `/meeting-transcript-to-summary`

**Default mode.** Performs the core task end-to-end.

When to use: User provides input matching the trigger conditions above.


## Execution Steps

1. **Receive transcript** — User pastes meeting transcript text (from Whisper, Otter, Fireflies, or manual notes)
   - If the input looks like a different format (code, logs, article), state: "This skill extracts structured summaries from meeting transcripts. Please provide a conversation transcript."

2. **Identify speakers and segments** — Parse the transcript structure:
   - Detect speaker labels or turn-taking patterns
   - Identify distinct topics or discussion sections
   - Note timestamps if present

3. **Extract key content** — Identify the substantive parts:
   - Key decisions made (explicit statements of what was decided)
   - Action items with assignees (who will do what by when)
   - Open questions or unresolved issues
   - Important context or constraints referenced

4. **Format structured summary** — Organize into the standard format:
   - **Summary**: 2-3 sentence overview of the meeting topic and outcome
   - **Decisions**: numbered list of decisions made with rationale
   - **Action Items**: who → does what → by when (if stated)
   - **Open Items**: questions left unresolved or follow-ups needed

5. **Deliver and validate** — Return the formatted summary:
   - If any section is empty, note "No [decisions/action items] identified"
   - If speakers aren't labeled, note "Speaker names not detected; labeled as Speaker 1, 2..."
   - Ask if the user wants to adjust granularity or add missing items

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
