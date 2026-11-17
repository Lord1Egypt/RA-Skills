## Description:

Xiaopi Self Improving helps agents record command failures, user corrections, best practices, and knowledge gaps as persistent local memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to preserve recurring failures, user corrections, and preferred practices so future agent sessions can check relevant memory before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may capture commands, errors, corrections, or project context that contain secrets or sensitive information.

Mitigation: Avoid logging tokens, passwords, private URLs, customer data, or project secrets; review memory entries before retaining or sharing them.

Risk: Automatic persistence to project instruction or memory files can carry incorrect guidance into later sessions.

Mitigation: Require review before writing to AGENTS.md, MEMORY.md, project learnings, or Git-backed backups.

Risk: Stored recommendations may include privileged command guidance such as sudo usage.

Mitigation: Require explicit approval before reusing privileged commands or applying stored fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a-din/skills/xiaopi-self-improving)
- [Publisher profile](https://clawhub.ai/user/a-din)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSONL memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local memory files when its helper scripts are executed.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
