## Description:

深蓝财经新闻 helps agents retrieve real-time Chinese financial dispatches, headlines, trending content, article search results, and listed-company announcements through the public Shenlan News API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qxsclass](https://clawhub.ai/user/qxsclass)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to answer Chinese finance-news questions, monitor A-share and macroeconomic updates, search finance articles, and retrieve listed-company announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns third-party market and news content that may be incomplete, delayed, or inappropriate to treat as financial advice.

Mitigation: Present retrieved content as informational, cite Shenlan News source links and timestamps where available, and avoid making investment recommendations from the content alone.

Risk: The skill makes outbound HTTPS requests to shenlannews.com and depends on that service's availability and public API limits.

Mitigation: Install only when outbound access to shenlannews.com is acceptable, handle request failures gracefully, and respect the documented public API limits.

## Reference(s):

- [深蓝财经新闻 API 参考文档](references/api-reference.md)
- [深蓝财经 homepage](https://www.shenlannews.com)
- [ClawHub skill page](https://clawhub.ai/qxsclass/skills/shenlannews)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or text responses grounded in JSON returned by Shenlan News API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, article or dispatch links, AI summaries, sentiment fields, announcement search results, and JSON-derived citations from shenlannews.com.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
