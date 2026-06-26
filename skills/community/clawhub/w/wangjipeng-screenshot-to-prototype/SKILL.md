---
name: screenshot-to-prototype
description: >
  Use when (1) user pastes a UI screenshot and needs editable frontend code prototype. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Screenshot To Prototype

Use when (1) user pastes a UI screenshot and needs editable frontend code prototype. 

## Core Position

This skill solves the specific engineering problem of: *user pastes a UI screenshot and needs editable frontend code prototype*

This skill is NOT:
- A general-purpose capability that activates on anything
- A replacement for manual human judgment
- A tool that stores state or remembers across sessions

This skill IS activated ONLY when the trigger conditions are explicitly met.

## Modes

### `/screenshot-to-prototype`

**Default mode.** Performs the core task end-to-end.

When to use: User provides input matching the trigger conditions above.


## Execution Steps

1. **Receive screenshot** — User pastes a UI screenshot (PNG/JPG/WebP)
   - Confirm the image is a UI mockup, not a photo or diagram
   - If the image is unclear or not a UI, state: "This skill converts UI screenshots to editable frontend prototypes. Please provide a clear screenshot of a UI design."

2. **Analyze UI structure** — Identify key elements from the screenshot:
   - Detect layout structure (header, sidebar, main content, footer)
   - Identify component types: buttons, input fields, cards, tables, navigation
   - Estimate spacing, font sizes, and color scheme from visual cues

3. **Generate component map** — Map detected elements to frontend structure:
   - Container elements (div/section) based on layout regions
   - Interactive elements (button, input, select) with appropriate attributes
   - Text content areas with estimated typography (size, weight, color)

4. **Output prototype code** — Generate clean, well-structured HTML/CSS (or React/Vue):
   - Use semantic HTML tags matching the detected structure
   - Include inline CSS or basic class names for styling
   - Add placeholder content that reflects the screenshot layout
   - Structure the code so it is immediately readable and editable

5. **Deliver with guidance** — Return the code with a brief explanation:
   - State what framework/libraries the output uses
   - Note any assumptions made about sizing or positioning
   - Offer to refine specific components if the user provides more detail

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
