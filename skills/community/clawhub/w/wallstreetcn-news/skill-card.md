## Description:

Fetches WallstreetCN financial news, including latest articles, headlines, trending stories, and keyword search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wallstreetinsights](https://clawhub.ai/user/wallstreetinsights)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve WallstreetCN-sourced financial news and present concise article summaries with source links, author information, and dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad finance-news prompts where the user did not specifically request WallstreetCN.

Mitigation: Use it when WallstreetCN-sourced financial news is desired, and confirm the source preference for general finance-news requests.

Risk: The skill may add WallstreetCN branding or Chinese formatting when a neutral format or another language is preferred.

Mitigation: Review the generated response for source branding, language, and formatting fit before presenting it in contexts that require neutrality.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wallstreetinsights/skills/wallstreetcn-news)
- [WallstreetCN latest articles API](https://api-one-wscn.awtmt.com/apiv1/content/information-flow?channel=global&accept=article&limit=10)
- [WallstreetCN headlines API](https://api-one-wscn.awtmt.com/apiv1/content/carousel/information-flow?channel=global&limit=10)
- [WallstreetCN hot articles API](https://api-one-wscn.awtmt.com/apiv1/content/articles/hot?period=all)
- [WallstreetCN article search API](https://api-one-wscn.awtmt.com/apiv1/search/article?query=关键词&limit=10)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown news summaries with article links and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise WallstreetCN-branded summaries with titles, approximately 50-character summaries, authors, dates, and source links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
