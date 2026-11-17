## Description:

Tracks keyword positions, SERP feature ownership, and AI visibility over time from provided exports or connected tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

SEO and marketing teams use this skill to set up keyword rank tracking, compare current rankings against baselines, and produce ranking delta reports with source labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ledger command examples include user-supplied placeholders that could be unsafe if copied into a shell with untrusted values.

Mitigation: Validate domains and keyword data first, pass structured arguments, and review shell commands before execution.

Risk: Estimated ranking, traffic, or AI visibility values could be mistaken for measured data.

Mitigation: Label every metric as measured, user-provided, estimated, or N/A, and avoid inventing missing metrics.

Risk: Ranking changes can be confounded by algorithm updates, competitors, location, device, or tool differences.

Mitigation: Compare against baselines and controls, document hypotheses as unconfirmed, and spot-check data quality before acting.

## Reference(s):

- [Ranking Analysis Output Templates](references/ranking-analysis-templates.md)
- [Rank Tracking Setup Guide](references/tracking-setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/rank-tracker)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise summaries, optionally including shell commands for ledger-based snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Metrics are labeled as measured, user-provided, estimated, or N/A.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
