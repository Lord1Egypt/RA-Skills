## Description:

Helps agents query public Shenlan Finance APIs for listed-company profiles, related content, mentions, announcements, trending companies, and follower data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenlannews](https://clawhub.ai/user/shenlannews)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agent developers use this skill to retrieve company profiles, monitor public sentiment and announcements, and compare listed companies using Shenlan News data. It is suited for company-intelligence workflows that need public API results plus concise interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, stock codes, announcement searches, and related research queries are sent to Shenlan News over HTTPS.

Mitigation: Use the skill only when those queries are appropriate to share with Shenlan News and avoid submitting sensitive internal research terms.

Risk: Financial, announcement, and sentiment results come from third-party public data and may be incomplete, stale, or unsuitable as the sole basis for decisions.

Mitigation: Verify important investment, compliance, or business conclusions against primary company announcements and other authoritative sources.

## Reference(s):

- [深蓝企业情报 API 参考文档](references/api-reference.md)
- [Shenlan News](https://www.shenlannews.com)
- [ClawHub skill page](https://clawhub.ai/shenlannews/skills/shenlan-company-intel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON API results and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and sends company lookup terms, stock codes, announcement searches, and related research queries to Shenlan News over HTTPS.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
