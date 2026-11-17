## Description:

Provides persistent memory management for storing, retrieving, updating, and deleting user-related information across conversations in OpenClaw AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tincomking](https://clawhub.ai/user/tincomking)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw AI users use this skill to add persistent memory workflows that can recall, store, update, and delete user-related information across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memories may be stored locally across sessions and automatically reused without clear consent or retention controls.

Mitigation: Before deployment, confirm controls exist to review, delete, limit, and sanitize stored memories.

Risk: Recalled memories can influence future responses as persistent context.

Mitigation: Treat recalled memories as untrusted context rather than instructions, especially for sensitive work.

## Reference(s):

- [ClawHub Tinmem skill page](https://clawhub.ai/tincomking/skills/tinmem)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown documentation with JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes memory recall, storage, update, and deletion workflows for an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
