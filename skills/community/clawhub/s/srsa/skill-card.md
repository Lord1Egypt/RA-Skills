## Description:

Use when running Spaced Repetition Systems for AI Agents (SRSA) daily review sessions, grading cards with again/hard/good/easy, and proposing explicit memory add/delete/update actions after each review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheanus](https://clawhub.ai/user/cheanus)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to run daily spaced-repetition reviews, maintain local review cards, grade recall, and propose explicit memory corrections after review outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead the agent to add, update, or delete persistent memory based on review outcomes without clear user consent.

Mitigation: Require explicit user confirmation before any memory add, delete, or update action.

Risk: Card override or removal can change the local review database and may affect personal, sensitive, or ambiguous information.

Mitigation: Require explicit confirmation before overriding or removing cards, and review sensitive or ambiguous card content before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheanus/skills/srsa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with inline shell command snippets and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill also maintains local SQLite review state and card schedules through its CLI.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
