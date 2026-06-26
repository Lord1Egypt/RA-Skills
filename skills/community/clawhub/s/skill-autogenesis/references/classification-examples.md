# Classification Examples

Use these examples to avoid confusing rules with skills.

## Required internal template

Before any persistence action, fill this template:

Classification:
- knowledge_type:
- recurrence:
- stability:
- verification:
- recommended_action:

Reason:
- why this is or is not an executable reusable procedure
- why the selected persistence layer is the lightest correct one

## Create or patch a skill

### Example
A debugging session used multiple tools, found the root cause, applied a stable fix, and verified the result.

### Why this is a skill
- There is a trigger.
- There is a repeatable sequence of actions.
- There is a verification step.
- Another agent could follow the same procedure.

## Store in memory, not a skill

### Example
The user prefers short paragraphs and dislikes certain punctuation.

### Why this is not a skill
- This is a communication preference.
- It does not define a reusable executable workflow.
- It belongs in user memory.

## Store in prompt or runtime policy, not a skill

### Example
Never publish without explicit user approval.

### Why this is not a skill
- This is a governance rule.
- It constrains behavior but does not define a complete procedure.
- It belongs in prompt, policy, or runtime guardrails.

## No persistence yet

### Example
A one-off workaround succeeded once but has not been validated on a second run.

### Why this is not ready
- The pattern may be accidental.
- Verification is weak.
- Wait for stronger evidence before writing memory or skills.
