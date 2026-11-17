## Description:

通过API与本地Obsidian知识库交互，实现笔记创建、语义搜索及笔记管理功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[admirobot](https://clawhub.ai/user/admirobot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to create, search, list, retrieve, and index Markdown notes in a shared Obsidian knowledge base. It is suited to work logs, project lessons, team knowledge sharing, and structured experience capture when the target knowledge-base service is intentionally trusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive broad shared knowledge-base read, write, list, and index access over unauthenticated plaintext HTTP.

Mitigation: Install only in environments that intentionally trust the 192.168.18.15 service and protect it with authentication, TLS, access controls, and retention rules before storing sensitive material.

Risk: Test and example scripts can create or modify live knowledge-base notes.

Mitigation: Run tests against a staging endpoint or add a dry-run mode before executing them in a production or shared knowledge base.

Risk: Shared notes may expose private prompts, regulated data, credentials, or sensitive project information to other agents with service access.

Mitigation: Keep secrets and sensitive content out of the knowledge base unless access controls and data handling policies are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/admirobot/skills/tvdr-obsidian-kb)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [SKILL_VERIFICATION.md](artifact/SKILL_VERIFICATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples plus JSON API responses from the knowledge-base service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and searches Markdown notes through a configured Obsidian knowledge-base HTTP API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
