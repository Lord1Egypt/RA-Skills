## Description:

Retrieves WeChat official-article details, engagement metrics, article content, media lists, or a consolidated report using the We-Media API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and analysts use this skill to examine a WeChat official article's publication details, engagement, body text, and media, or to generate a consolidated report. It estimates API costs before paid retrieval and saves the results locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls may incur per-request charges, particularly across multiple pages.

Mitigation: Check the live price and estimated total, then confirm the requested endpoint, page limit, and cost before authorizing calls.

Risk: API credentials and retrieved article data may be exposed through chat or saved reports.

Mitigation: Keep the API key local, avoid sharing it in chat, and review the output path and report contents before exporting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-official-article-analytics)
- [We-Media API guide](https://api.we-media.cn/client/ai-guide)
- [We-Media product documentation](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Text summary and local JSON, Markdown, or Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A full JSON copy accompanies saved reports; partial results and actual API charges should be disclosed.]

## Skill Version(s):

1.4.2 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
