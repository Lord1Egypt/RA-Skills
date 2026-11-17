## Description:

Tech Radar Daily discovers and scores daily technical intelligence from GitHub Trending, Product Hunt, Hacker News, and Awesome Lists, then sends selected items to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dereklu515](https://clawhub.ai/user/dereklu515)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and technology analysts use this skill to collect, score, de-duplicate, archive, and optionally push a daily digest of noteworthy developer tools, technical trends, and monetizable projects to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can post generated reports to a configured Feishu webhook.

Mitigation: Use test mode first, configure only the intended FEISHU_WEBHOOK_URL, and review report content before enabling scheduled delivery.

Risk: The artifact includes a Feishu tenant chat-discovery script that uses app credentials.

Mitigation: Do not run scripts/test-feishu-chat.js or provide FEISHU_APP_ID and FEISHU_APP_SECRET unless tenant chat discovery is intentional.

Risk: Proxy and PAC dependencies may affect network routing in sensitive environments.

Mitigation: Review proxy-agent behavior and update or remove the proxy dependency chain before using the skill on restricted networks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dereklu515/skills/tech-radar-daily)
- [Awesome Lists Reference](references/awesome-lists.md)
- [Search Queries Reference](references/search-queries.md)
- [Report Template](assets/report_template.md)
- [Product Hunt](https://www.producthunt.com)
- [Hacker News API](https://hacker-news.firebaseio.com/v0/topstories.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Shell commands]

**Output Format:** [Markdown daily report, JSON stats/cache files, and optional Feishu webhook message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and FEISHU_WEBHOOK_URL for webhook delivery; GITHUB_TOKEN and proxy environment variables are optional.]

## Skill Version(s):

1.0.9 (source: SKILL.md frontmatter and server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
