## Description:

Generates a segmented daily report from Weibo hot-list topics, grouping items into finance and technology, social livelihood, culture and entertainment, and internet trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renyuzhuo](https://clawhub.ai/user/renyuzhuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current Weibo hot-list topics and produce a concise categorized daily briefing. It is useful for trend monitoring and quick topical summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a disclosed third-party Weibo hot-list source to generate live reports.

Mitigation: Deploy only where outbound access to that source is acceptable, and review the generated report before sharing it.

Risk: Hot-topic titles may include sensitive or unwanted content despite the README's filtering claim.

Mitigation: Apply downstream content review or filtering for the audience and publication context.

Risk: The helper script depends on curl and network availability, so report generation can fail when the source is unreachable.

Mitigation: Handle empty or failed fetches gracefully and rerun when network access is restored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renyuzhuo/skills/weibo-hot-daily-skill)
- [Weibo hot-list source](https://weibo.g.renyuzhuo.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown daily report with categorized topic lists; helper script prints text to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and curl. The helper script fetches up to 50 items and lists up to five topics per category.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact README also states v1.1.1 released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
