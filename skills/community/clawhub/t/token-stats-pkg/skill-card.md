## Description:

Token Stats Pkg helps users inspect local token-usage statistics for Hermes, Claude Code, CodeX, and OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhaoyong](https://clawhub.ai/user/zhouhaoyong)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI assistant users use this skill to install and run a local CLI that reports token usage by model, session, and time period for supported local assistants. It is useful for monitoring consumption, comparing periods, watching usage live, and exporting summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI reads local AI assistant usage and history stores to compute token statistics.

Mitigation: Install and run it only in accounts where access to those local stores is acceptable, and review the documented data-source paths before use.

Risk: Exported JSON or CSV reports can reveal work patterns, model usage, and session metadata.

Mitigation: Store exports in private locations, avoid sharing them broadly, and delete exports when they are no longer needed.

Risk: Setup and installation commands modify the user's local command environment.

Mitigation: Avoid elevated privileges for npm or setup commands and use trusted package registries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouhaoyong/skills/token-stats-pkg)
- [Publisher Profile](https://clawhub.ai/user/zhouhaoyong)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; CLI output is terminal text with optional JSON or CSV exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local assistant usage stores only; exported reports may contain work-pattern and session metadata.]

## Skill Version(s):

2.0.9 (source: frontmatter, script constant, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
