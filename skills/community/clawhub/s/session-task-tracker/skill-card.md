## Description:

Task-based cross-session context management for OpenClaw agents that maintains persistent task files so context survives session resets, compaction, and channel switches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanzhang1128](https://clawhub.ai/user/dylanzhang1128)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to keep structured per-task memory across sessions, including task status, progress, decisions, todos, and related files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create durable workspace task records that may capture sensitive user context.

Mitigation: Avoid storing secrets, credentials, private account details, or sensitive personal information in tracked task files, and review or delete task records regularly.

## Reference(s):

- [Task Tracker Reference](references/DESIGN.md)
- [ClawHub skill page](https://clawhub.ai/dylanzhang1128/skills/session-task-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown task files and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workspace task records under tasks/ when the agent follows the skill workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
