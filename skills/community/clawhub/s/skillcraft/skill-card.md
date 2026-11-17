## Description:

Design and build OpenClaw skills. Use when asked to "make/build/craft a skill", extract ad-hoc functionality into a skill, or package scripts/instructions for reuse. Covers OpenClaw-specific integration (tool calling, memory, message routing, cron, canvas, nodes) and ClawHub publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmz1](https://clawhub.ai/user/jmz1)

### License/Terms of Use:


## Use Case:

Developers and agent builders use Skillcraft to design, extract, and package reusable OpenClaw skills, including API wrappers, CLI wrappers, monitoring skills, and ClawHub-ready metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API or CLI wrapper skills may include under-scoped secret-storage guidance.

Mitigation: Require generated skills to keep secrets in environment variables, a keychain, or a secret manager; do not store tokens in publishable skill directories.

Risk: Generated skills may store runtime automation state inside publishable skill directories.

Mitigation: Keep runtime state outside publishable directories unless it is non-sensitive and explicitly excluded from packaging.

## Reference(s):

- [Skillcraft on ClawHub](https://clawhub.ai/jmz1/skills/skillcraft)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Creating Skills Documentation](https://docs.openclaw.ai/tools/creating-skills)
- [AgentSkills Specification](https://agentskills.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce skill directory plans, SKILL.md content, scripts, wrapper patterns, and ClawHub publishing guidance after user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
