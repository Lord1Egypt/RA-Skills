## Description:

Sentiment Radar helps agents collect and analyze public social-media opinions about products, brands, and topics across XHS, Twitter, Reddit, and Douyin, then produce structured sentiment reports with product mentions, pricing complaints, comparisons, and actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielwangyy](https://clawhub.ai/user/danielwangyy)

### License/Terms of Use:


## Use Case:

Developers, analysts, and market-intelligence teams use this skill to monitor launch reception, competitor sentiment, product pain points, pricing complaints, and comparison signals from public social-media data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser scraping and MCP collection can use authenticated sessions or OAuth tokens for social-media access.

Mitigation: Run only in a sandboxed environment with an ephemeral browser profile, and avoid exposing personal browser sessions or OAuth tokens unnecessarily.

Risk: Security evidence flags under-scoped browser scraping and an unsafe external config rewrite that could run injected code.

Mitigation: Pin and inspect MediaCrawler before running it, avoid untrusted keyword input, and review generated crawler configuration before execution.

Risk: Collected social-media content may contain sensitive or personal data.

Mitigation: Define retention and redaction rules for collected social-media data before storing, analyzing, or sharing results.

## Reference(s):

- [Sentiment Radar ClawHub Release](https://clawhub.ai/danielwangyy/skills/sentiment-radar)
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- [Sentiment Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON analysis output, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis covers sentiment split, product mentions, pricing complaints, comparison comments, user pain points, and engagement metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
