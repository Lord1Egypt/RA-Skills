## Description:

Triphasic Execution guides agents through an Execute, Review, Advance loop with semantic task parsing, planning, progress tracking, retry limits, idle cutoff rules, and issue/risk/lesson logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to impose a structured execution discipline on complex, multi-step tasks. It is intended to reduce skipped review, repeated failed attempts, and lost task state by requiring semantic parsing, planning, progress updates, and completion records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workflow control can broadly steer agent behavior across tasks.

Mitigation: Use on-demand mode unless global automatic behavior is explicitly required, and review configuration before enabling daemon or wrapper features.

Risk: Shell-command interception and plaintext local command-output logs can expose sensitive command context.

Mitigation: Avoid exec wrapper registration unless this logging is acceptable, and keep the data directory away from sensitive projects.

Risk: Progress verification and cleanup behavior can read, hash, or delete local workspace artifacts.

Mitigation: Run the settings UI only when needed, close it afterward, and review cleanup or uninstall targets before invoking them.

## Reference(s):

- [Skill overview and quick start](SKILL.md)
- [Mandatory execution rules](references/mandatory.md)
- [Command reference, data layout, and installation](references/reference.md)
- [FAQ](references/faq.md)
- [Antipatterns](references/antipatterns.md)
- [Examples](references/examples.md)
- [Permission summary](references/permissions.md)
- [Machine-readable permission report](references/permission_report.json)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local progress, issue, risk, lesson, log, state, and configuration files when its helper scripts are used.]

## Skill Version(s):

5.19.1 (source: frontmatter, _meta.json, release evidence, changelog released 2026-06-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
