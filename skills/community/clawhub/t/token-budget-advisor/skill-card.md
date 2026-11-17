## Description:

Helps agents ask users to choose response depth and manage token usage before answering prompts about budget, length, or detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make agent responses fit a preferred level of detail, from brief answers to exhaustive responses. It is useful when token cost, response length, or answer depth should be chosen before the agent replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic token estimates can be approximate.

Mitigation: Treat token counts as guidance and allow the user to change the selected response depth.

Risk: The skill may interrupt answers when users use common length words such as brief or detailed.

Mitigation: Apply the documented trigger limits: skip trivial one-line answers and avoid asking again once depth is set for the session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djc00p/skills/token-budget-advisor)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with response-depth options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses heuristic token estimates; no real tokenizer.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
