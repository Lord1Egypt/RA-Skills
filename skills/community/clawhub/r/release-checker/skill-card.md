## Description:

All-in-one release compatibility checking tool that analyzes Git diffs, identifies release-related Java, Gateway, Push Center, configuration, and SQL changes, generates TODO lists and Markdown reports, and can convert MySQL SQL into PostgreSQL and Oracle variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qfann](https://clawhub.ai/user/qfann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect release diffs, identify database and service-configuration compatibility work, convert SQL for multiple databases, and produce reviewable release reports before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an unsafe branch argument path that can execute unintended shell commands.

Mitigation: Install only from a trusted maintainer, review or patch the script before use, and never pass branch names sourced from untrusted text.

Risk: Generated SQL conversion output and release reports may be incorrect or written to unintended paths.

Mitigation: Use a disposable workspace, check report and SQL output paths before running conversion or batch mode, pin sqlglot, and manually validate generated SQL in a test environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qfann/skills/release-checker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal summaries, TODO lists, and converted SQL files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown reports and PostgreSQL/Oracle SQL conversion files to user-selected output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
