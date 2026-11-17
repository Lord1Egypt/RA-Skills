## Description:

Create, edit, improve, or audit AgentSkills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, edit, validate, package, and audit AgentSkills and SKILL.md files with guidance on structure, progressive disclosure, and bundled resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaging untrusted or shared skill directories could include unintended content or be affected by local file replacement during archive creation.

Mitigation: Run packaging only on skill directories you control, avoid shared or attacker-writable folders, and review generated .skill archives before publishing.

Risk: Skill-authoring guidance can produce incomplete or inappropriate skill content for a specific release.

Mitigation: Review SKILL.md and bundled resources, then run validation before publishing or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/utromaya-code/skills/skill-creator-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and generated files or shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill files and may run validation or packaging scripts when the user requests implementation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
