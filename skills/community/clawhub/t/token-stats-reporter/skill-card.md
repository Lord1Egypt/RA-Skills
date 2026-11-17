## Description:

Generates token usage and reference cost reports from local OpenClaw session logs, with selectable Opus 4.7, GPT-5.5, or custom reference rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinoslug](https://clawhub.ai/user/sinoslug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize recent and monthly token usage and estimate reference costs for agent conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session logs, which may contain conversation metadata or usage history.

Mitigation: Install and invoke it only when local session-log scanning is acceptable, and review the generated token summary before sharing it.

Risk: Broad trigger phrases may cause the agent to scan local history when a user asks about token usage or costs.

Mitigation: Ask for confirmation before running the reporting script in contexts where local history access may be sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinoslug/skills/token-stats-reporter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and single-line token/cost report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw session logs and reports token totals, message counts, model name, and reference costs in CNY.]

## Skill Version(s):

1.5.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
