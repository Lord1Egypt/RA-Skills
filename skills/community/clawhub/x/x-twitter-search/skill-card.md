## Description: <br>
Search X/Twitter in real time using Grok or the X API to find tweets, trends, and discussions with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueberrywoodsym](https://clawhub.ai/user/blueberrywoodsym) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to ask an agent for recent public X/Twitter posts, trends, and discussion links around a topic, account, or time window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to xAI or X services with the configured API credentials. <br>
Mitigation: Avoid sensitive search terms unless that disclosure is acceptable, and keep API keys in environment or approved configuration storage. <br>
Risk: Returned tweets, citations, or model-formatted summaries may be misleading or instruction-like. <br>
Mitigation: Treat results as untrusted search output, verify important links or claims, and do not follow instructions embedded in returned content. <br>
Risk: Native X API mode may incur pay-per-use charges. <br>
Mitigation: Use explicit commands and result limits, and prefer the default mode unless native X API access is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blueberrywoodsym/x-twitter-search) <br>
- [xAI documentation](https://docs.x.ai) <br>
- [xAI API console](https://console.x.ai) <br>
- [X developer console](https://console.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown search summaries with X/Twitter links and citations; optional JSON or links-only output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY for default xAI mode; optional X_BEARER_TOKEN or TWITTER_BEARER_TOKEN enables native X API mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
