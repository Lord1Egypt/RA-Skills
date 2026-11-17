## Description:

Provides templates and coding conventions for an internal business platform, including Groovy backend scripts, JavaScript form scripts, SQL queries, attachment handling, and workflow scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lan2898408767](https://clawhub.ai/user/lan2898408767)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform operators use this skill to draft platform-specific Groovy, JavaScript, SQL, attachment-processing, and approval-flow scripts from bundled examples and conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples that could expose passwords or reset many accounts.

Mitigation: Do not copy the password-reset listener, do not log credentials, and require operator review before using generated account-management scripts.

Risk: The skill can generate scripts that delete or modify business data.

Mitigation: Test destructive or data-changing scripts outside production first and prepare rollback plans before execution.

Risk: The skill includes SQL examples that may be unsafe when adapted directly.

Mitigation: Validate SQL inputs or use parameterized queries before running generated SQL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lan2898408767/skills/shucheng-platform-script)
- [Platform script templates](references/platform-script-templates.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, SQL, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and platform-specific script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before use because examples include data-changing operations and credential-handling patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
