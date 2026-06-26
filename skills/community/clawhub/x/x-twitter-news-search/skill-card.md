## Description: <br>
Searches Twitter/X for recent tweets matching keyword, language, time-window, and engagement filters, then returns raw tweet JSON with author details, metrics, and URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berthelol](https://clawhub.ai/user/berthelol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch recent Twitter/X posts for news monitoring, topic discovery, and scheduled data collection while leaving scoring, summarization, and presentation to the caller. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Twitter/X bearer token that can spend API quota or money when used repeatedly or autonomously. <br>
Mitigation: Store the token securely, set provider budget or rate limits where available, and enable scheduled or autonomous use only when repeated API spending is intended. <br>
Risk: The skill returns raw tweets and engagement metrics without scoring, summarization, or verification. <br>
Mitigation: Have the calling agent or user validate source reliability, context, and relevance before using the results for decisions or publication. <br>


## Reference(s): <br>
- [Twitter API v2 Reference](references/twitter-api.md) <br>
- [X Developer Portal](https://developer.x.com) <br>
- [Twitter/X Recent Search API Endpoint](https://api.x.com/2/tweets/search/recent) <br>
- [ClawHub Skill Page](https://clawhub.ai/berthelol/x-twitter-news-search) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration, JSON] <br>
**Output Format:** [JSON returned through shell commands and jq filters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw filtered tweet objects; the calling agent handles scoring, summarization, ranking, and formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
