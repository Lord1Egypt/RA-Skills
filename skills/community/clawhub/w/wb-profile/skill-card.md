## Description:

采集微博用户主页中的公开微博，提供正文、互动数据、发布时间和链接，并支持 CSV 导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use the CLI to collect public posts from a Weibo profile, review post text and engagement counts, and export the results as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags comment-collection features beyond the stated Weibo profile-post purpose, and the review is incomplete.

Mitigation: Before installation, ask the maintainer to explain the additional features and clarify the required tool access.

Risk: The security review identifies token-transport and TLS-verification risks.

Mitigation: Use only after the maintainer addresses these risks; use protected token transport and validated TLS, and leave insecure TLS disabled.

## Reference(s):

- [ClawHub wb-profile release](https://clawhub.ai/mystery77777777/skills/wb-profile)

## Skill Output:

**Output Type(s):** [JSON, CSV files, Markdown tables, Guidance]

**Output Format:** [JSON task results, CSV exports, and Markdown summaries or tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include post text, timestamps, engagement counts, links, and repost relationships. Collection supports up to 10 pages per task.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
