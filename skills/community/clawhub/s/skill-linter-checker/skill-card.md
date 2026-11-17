## Description:

Analyze and validate SKILL.md files for best practices, common issues, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbin92](https://clawhub.ai/user/mengbin92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to review SKILL.md files, identify frontmatter and content-quality issues, and receive structured improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file-editing authority while reviewing SKILL.md files.

Mitigation: Use read-only permissions for routine linting and enable edits only through an explicit user-confirmed remediation workflow.

Risk: The skill may inspect untrusted skill content.

Mitigation: Treat inspected skill content as untrusted data and review proposed changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengbin92/skills/skill-linter-checker)
- [ClawHub publisher profile](https://clawhub.ai/user/mengbin92)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report with severity-labeled findings and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an optional rewritten SKILL.md when significant improvements are needed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
