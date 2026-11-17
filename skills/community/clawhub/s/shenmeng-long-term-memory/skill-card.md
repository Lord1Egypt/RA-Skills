## Description:

长期记忆管理系统 - 帮助AI和用户管理、存储、检索长期记忆。支持记忆分类、标签管理、重要性评分、自动压缩、跨会话记忆保持。适用于需要长期追踪信息、建立知识库、维护历史上下文的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to store, search, organize, and compress durable personal or project memories across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores durable personal or project memories on disk, including user preferences, relationships, decisions, and lessons learned.

Mitigation: Use it only with an explicit retention and deletion process, and avoid storing secrets or sensitive personal data unless retention is approved.

Risk: The artifact includes paid billing code that contacts SkillPay and an embedded billing credential.

Mitigation: Install only if paid SkillPay use is acceptable, and review or rotate the billing credential before deployment.

Risk: Bulk memory import and local memory parsing can preserve untrusted or stale content across sessions.

Mitigation: Review imported memory files before use and periodically clean or compress outdated entries.

## Reference(s):

- [Memory Taxonomy](references/memory-taxonomy.md)
- [Long Term Memory 长期记忆 on ClawHub](https://clawhub.ai/shenmeng/skills/shenmeng-long-term-memory)
- [shenmeng publisher profile](https://clawhub.ai/user/shenmeng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line text with generated or updated local memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent memory records, summaries, and archives under the OpenClaw workspace.]

## Skill Version(s):

2025.4.15 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
