# Debug / Iteration History

This file summarizes the release hardening work behind the public version of TransPrompt.

## What was fixed before release

### 1. Post-generation topic stickiness
The skill originally treated the generated prompt as the next default topic. This was fixed so prompt conversion stays scoped to the current turn.

### 2. Bypass wording
Bypass replies originally sounded too much like internal debugging language. This was changed to direct, user-facing wording.

### 3. Ending restraint
The skill originally tended to append extra next-step menus. This was removed so the output ends cleanly by default.

### 4. Summary style
The old explanation style was too long. It was replaced with a short `Prompt 关键处理` summary that says what the prompt did.

### 5. Trigger boundary hardening
The trigger was updated to support forms like `@prt帮我...` while still avoiding false matches like `@promptify...`.

### 6. Clarification restraint
The skill now asks only the minimum missing question needed to continue.

### 7. Execution-boundary blocker
A critical blocker was identified and fixed: a message starting with `@prt` must still be treated as a prompt-transformation request first, even if the content describes a real-world execution task.

## Release confidence

This version was refined through multiple rounds of:
- real conversation testing
- dirty-input regression
- release smoke testing
- blocker-driven iteration

It is designed to be:
- practical
- lightweight
- clear to end users
- safe in conversation
- easy to call when needed

## Update note

This skill will continue to be updated with real-world usage and feedback.

If you find it useful, please give it a star on ClawHub.