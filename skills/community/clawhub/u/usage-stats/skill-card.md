## Description:

Usage Stats analyzes local OpenClaw session records and generates a usage report covering token consumption, estimated cost, model distribution, tool usage, errors, and activity trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqq664590975-del](https://clawhub.ai/user/qqq664590975-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to summarize their local main-agent session history into usage, cost, model, tool, error, and trend reports. It is most useful for local usage auditing and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads all local OpenClaw main-agent session history, which may contain sensitive conversations, command output, file paths, or credentials.

Mitigation: Run it only when an all-history report is intended; restrict or delete the generated report and history files after use.

Risk: The skill saves ongoing usage summaries without date filters, explicit confirmation, or a no-persist mode.

Mitigation: Review the generated files before sharing them and prefer a filtered or non-persistent variant for sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qqq664590975-del/skills/usage-stats)
- [Changelog](references/changelog.md)
- [Output Format](references/output-format.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown report with a JSON history snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes usage_stats_latest.md and retains up to 90 usage_stats_history.json snapshots.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog, released 2026-04-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
