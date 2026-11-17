## Description:

Skill Sentinel helps agents diagnose, fix, and prevent skill trigger failures by auditing descriptions, YAML frontmatter, token budgets, discovery, conflicts, and remediation paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to troubleshoot skills that fail to activate, trigger incorrectly, or are ignored after installation. It guides audits of skill descriptions, YAML frontmatter, token budgets, discovery paths, conflicts, and remediation choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic remediation can rewrite skill files and may affect paths beyond the intended scope.

Mitigation: Run audit mode without --fix first, pass a specific trusted --skills-dir, inspect proposed changes, and avoid elevated privileges.

Risk: Incorrect remediation guidance can make skill routing less accurate or introduce misleading trigger descriptions.

Mitigation: Review generated suggestions against real trigger failures and verify behavior with natural language tests after changes.

## Reference(s):

- [Failure Pattern Reference](references/failure-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file edits when automatic remediation is requested; audit output should be reviewed before applying changes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
