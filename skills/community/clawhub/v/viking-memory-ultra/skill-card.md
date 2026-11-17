## Description:

Viking Memory System Ultra provides a layered memory system for agents, with hot, warm, cold, and archive tiers, review status tracking, semantic promotion, weighted recall, and reversible archive summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsangho](https://clawhub.ai/user/tsangho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to organize agent memory into lifecycle tiers, write and read memory files, track review state, promote relevant archived memories, and manage compression behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain secrets, credentials, private personal data, or sensitive business decisions.

Mitigation: Review memory content before writing it and do not store sensitive data unless explicit approval, redaction, and local-only controls are available.

Risk: Shared memory can make important entries visible across agents.

Mitigation: Limit shared writes to approved content and review entries before using shared-memory commands.

Risk: Archived memory content may be processed by external LLMs during promotion or summarization workflows.

Mitigation: Use the skill only when external processing is acceptable, or configure local-only processing and approval controls before deployment.

## Reference(s):

- [Viking Memory System Ultra on ClawHub](https://clawhub.ai/tsangho/skills/viking-memory-ultra)
- [Publisher profile](https://clawhub.ai/user/tsangho)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and memory frontmatter templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create persistent memory files, shared memory entries, review metadata, and archive summaries.]

## Skill Version(s):

1.4.0 (source: frontmatter, server release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
