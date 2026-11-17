## Description:

Use when accessing memory, recording information, searching prior context, or managing subjects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxpetretta](https://clawhub.ai/user/maxpetretta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Reclaw to search remembered context, record user-specific facts, decisions, tasks, and questions, manage subject histories, and retrieve prior session context in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically persists and indexes user-specific conversation context, which can include sensitive personal, business, or client information.

Mitigation: Install only where persistent memory is desired; review Reclaw storage, deletion, and access controls before using it with sensitive information.

Risk: Append-only memory and generated subject projections can retain older entries alongside later corrections.

Mitigation: State corrections clearly, mark tasks done explicitly, and refresh or remove Reclaw memory data when retained context is no longer appropriate.

## Reference(s):

- [Reclaw repository](https://github.com/maxpetretta/reclaw)
- [ClawHub skill page](https://clawhub.ai/maxpetretta/skills/reclaw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw binary and a Reclaw plugin registered in the current OpenClaw environment for live memory tools.]

## Skill Version(s):

2026.3.11-3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
