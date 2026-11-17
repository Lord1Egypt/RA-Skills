## Description:

Mines WeChat search results, related index results, popular articles, and suggested queries to propose evidence-based content topics for a keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and marketing teams use this skill to assess a WeChat topic, find narrower article angles, and support their choices with search results and related queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls can incur unexpected charges or collect more pages than intended.

Mitigation: Check the live cost estimate, obtain approval for paid calls, and cap collection with --pages.

Risk: Search parameters are sent to a third-party API, and result files are saved locally.

Mitigation: Avoid sensitive queries, choose a suitable local output location, and review retained files.

Risk: Exposing the API key in chat or shared files could allow unauthorized use.

Mitigation: Keep the key in local configuration or WM_API_KEY; do not paste it into chat or reports.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dunkong/skills/wechat-search-topic-mining)
- [We-Media API product documentation](https://api.we-media.cn/client/products)
- [We-Media AI integration guide](https://api.we-media.cn/client/ai-guide)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files]

**Output Format:** [Markdown summary with optional JSON or Excel result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports actual API spending and identifies partial results; retains a full local JSON copy of exported results.]

## Skill Version(s):

1.4.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
