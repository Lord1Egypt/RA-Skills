# Output Contracts

Use this file when defining what a skill should produce once triggered.

## Goal

Do not let the skill stop at abstract guidance.
The instructions should make it obvious what the agent must deliver.

## Strong Contract Elements

A strong output contract usually defines:

- the task mode
- the summary of current state or target
- the main findings or design goals
- the concrete changes or artifacts to create
- validation expectations
- readiness or completion status

## Weak Contract Smells

- "Help the user think through the problem"
- "Offer suggestions"
- "Give guidance"

These may be useful, but they are not enough on their own for a production-quality skill.

## Practical Rule

If another agent read the skill and still would not know what to output, the contract is too weak.

