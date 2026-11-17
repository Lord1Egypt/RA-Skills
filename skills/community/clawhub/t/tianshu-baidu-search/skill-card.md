## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live Baidu web searches for current information, documentation, and research topics through the Baidu AI Search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu's Qianfan AI Search API.

Mitigation: Avoid sensitive queries unless that data sharing is acceptable under the user's Baidu account and data-handling expectations.

Risk: The skill requires a BAIDU_API_KEY in the environment.

Mitigation: Provide the key only in the intended runtime environment and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangshengli0421/skills/tianshu-baidu-search)
- [Baidu AI Search API Key Console](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
- [Baidu AI Search Web Search Endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; accepts query, optional count from 1 to 50, and optional freshness filters.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
