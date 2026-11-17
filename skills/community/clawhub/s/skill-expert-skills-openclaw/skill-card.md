## Description:

Creates, optimizes, validates, and packages AI Agent Skills in SKILL.md format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinkcarlos](https://clawhub.ai/user/tinkcarlos)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent builders use this skill to create, optimize, validate, and package reusable SKILL.md agent skills with structured phases, quality gates, and supporting reference material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaging script can accidentally include files outside the chosen skill folder, especially when packaging untrusted or shared directories.

Mitigation: Avoid packaging skill folders that contain symlinks, inspect the file list before distributing archives, and run the packager only on directories you intentionally provide.

Risk: The skill uses write and bash permissions for skill creation, validation, and packaging workflows.

Mitigation: Use the skill in a controlled workspace, review generated changes before deployment, and prefer a virtual environment with pinned dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tinkcarlos/skills/skill-expert-skills-openclaw)
- [AgentSkills.io](https://agentskills.io/)
- [Anthropic Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Official Best Practices](references/official-best-practices.md)
- [Skill Templates](references/skill-templates.md)
- [Tools Guide](references/tools-guide.md)
- [Skills Knowledge Base](references/skills-knowledge-base.md)
- [Knowledge Validation Checklist](references/knowledge-validation-checklist.md)
- [User Confirmation Protocol](references/user-confirmation-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and generated or modified skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces updated SKILL.md content, change summaries, validation results, and optional references, scripts, or assets.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; skill metadata version: 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
