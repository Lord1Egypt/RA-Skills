## Description:

Self-reflection + self-criticism + self-learning + self-organizing memory for agents that evaluate their own work, catch mistakes, and improve over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyu-157](https://clawhub.ai/user/xiaoyu-157)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an agent record explicit corrections, reflect on completed work, and maintain local memory files that can guide future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist corrections and preferences in local memory files that influence future agent behavior.

Mitigation: Require explicit approval before creating memory files, promoting rules to always-loaded memory, or using stored preferences in a session.

Risk: The skill can modify workspace steering files such as AGENTS.md, SOUL.md, and HEARTBEAT.md during setup.

Mitigation: Review proposed file changes before applying them and scan the skill before deployment.

Risk: The security evidence notes that setup and boundary documents referenced by the skill were missing from the artifact.

Mitigation: Verify any missing setup and boundary documents come from a trusted source before installation or use.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/xiaoyu-157/test-import-skill-3)
- [ClawHub skill page](https://clawhub.ai/xiaoyu-157/skills/test-import-skill-3)
- [Skill homepage](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with file paths, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory and workspace steering files when installed and approved.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.2.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
