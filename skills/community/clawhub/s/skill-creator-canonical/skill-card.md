## Description:

Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch, restructuring an existing skill, auditing skill quality, or making a skill easier for weaker AI models and agent runtimes to follow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent-skill maintainers use this skill to create new AgentSkills, restructure existing skills, audit skill quality, improve weak-model reliability, validate packages, and prepare releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaging or publishing can expose local files from a skill folder when ignore rules are incomplete.

Mitigation: Keep sensitive files out of skill directories, maintain a complete .clawhubignore, inspect generated .skill archives before publishing, and follow the packaging checklist.

Risk: Deep review depends on the optional dual-thinking skill being installed and trustworthy.

Mitigation: Verify or pin dual-thinking before relying on the full review path, and stop when the skill reports that dual-thinking is unavailable.

## Reference(s):

- [Authoring Guide](references/authoring-guide.md)
- [Progressive Disclosure](references/progressive-disclosure.md)
- [Workflow Patterns](references/workflows.md)
- [Output Patterns](references/output-patterns.md)
- [Weak-Model Fallbacks](references/weak-model-fallbacks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file edits, generated skill files, validation results, package artifacts, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify SKILL.md, references, scripts, assets, .clawhubignore, and .skill archives depending on the selected workflow path.]

## Skill Version(s):

6.1.2 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
