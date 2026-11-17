## Description:

曙光记忆系统 provides local five-layer persistent memory, hybrid recall, WAL-style write logging, and self-improvement records for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add local cross-session memory for preferences, facts, decisions, entities, reflections, errors, and lessons. It is intended for agents that need persistent recall and periodic memory maintenance without an external database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store user preferences, decisions, errors, lessons, and other broad user content as local plaintext memory.

Mitigation: Use it only for non-sensitive content and avoid secrets, credentials, regulated data, or confidential multi-user/project information.

Risk: Memory scope defaults and security guidance indicate weak isolation controls.

Mitigation: Use separate workspace or memory directories per user and project, and review recalled content before relying on it.

Risk: The security summary notes misleading durability and scope claims, including weak WAL accuracy and retention/deletion controls.

Mitigation: Treat persistence, archival, and WAL behavior as best-effort until recovery, retention, deletion, and permissions are tested in the target environment.

## Reference(s):

- [ClawHub Skill Page: shuguang-memory](https://clawhub.ai/chen6896qqwee/skills/shuguang-memory)
- [Publisher Profile: chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code examples, local file paths, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When helper code is run, it can create and update local plaintext memory files under the OpenClaw workspace.]

## Skill Version(s):

4.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
