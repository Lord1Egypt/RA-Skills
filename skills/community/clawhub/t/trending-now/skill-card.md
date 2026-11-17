## Description:

Monitor internet and social media trends with heartbeat topic watchlists, freshness scoring, and concise alerts on what changed and why it matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and teams use this skill to monitor selected topics across public internet and social sources, score emerging signals, and receive concise alerts only when there is decision-relevant movement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topic keywords are sent to public trend and social sources during live monitoring.

Mitigation: Set explicit topics, source boundaries, geographies, languages, active hours, and avoid sensitive or confidential query terms.

Risk: Local Markdown memory under ~/trending-now may be used to store monitoring preferences and run history.

Mitigation: Do not store credentials or secrets in the memory files, and keep local file permissions restricted.

Risk: Trend alerts can be misleading when based on stale stories, repost loops, or a single source family.

Mitigation: Require timestamped evidence, cross-source confirmation, freshness scoring, and explicit uncertainty before alerting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/trending-now)
- [Skill Homepage](https://clawic.com/skills/trending-now)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)
- [X](https://x.com)
- [Reddit](https://www.reddit.com)
- [Google News](https://news.google.com)
- [Google Trends](https://trends.google.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown alerts, setup guidance, local file templates, and occasional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return HEARTBEAT_OK exactly when no actionable change is detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
