## Description:

Analyze and validate SKILL.md files for best practices, common issues, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbin92](https://clawhub.ai/user/mengbin92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review, audit, and improve SKILL.md files against documented skill authoring practices. It produces structured findings, severity labels, scores, and suggested fixes for frontmatter and body content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can advise edits to SKILL.md files, and an agent using its declared tools may edit or write skill files.

Mitigation: Review suggested changes before accepting them; the bundled CLI itself only reads the provided file path and prints a report.

## Reference(s):

- [ClawHub Skill Linter Release](https://clawhub.ai/mengbin92/skills/skill-linter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with tables, severity sections, recommendations, and optional rewritten SKILL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI reads a SKILL.md path and prints a local analysis report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
