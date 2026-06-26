## Description: <br>
Searches and analyzes Reddit content using semantic AI search through the reddapi.dev HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dowands](https://clawhub.ai/user/dowands) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and product researchers use this skill to query Reddit discussions for market research, pain-point discovery, sentiment tracking, product validation, and content inspiration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and API credentials are sent to the third-party reddapi.dev service, and paid API usage can consume account quota. <br>
Mitigation: Use a dedicated REDDAPI_API_KEY, avoid exposing the key in prompts or logs, and monitor plan limits and account usage. <br>
Risk: Search queries may contain secrets, personal data, or highly confidential business details. <br>
Mitigation: Keep queries Reddit-focused and omit secrets, personal data, and highly confidential information before invoking the skill. <br>


## Reference(s): <br>
- [reddapi.dev](https://reddapi.dev) <br>
- [reddapi.dev account and API key](https://reddapi.dev/account) <br>
- [Semantic search endpoint](https://reddapi.dev/api/v1/search/semantic) <br>
- [Vector search endpoint](https://reddapi.dev/api/v1/search/vector) <br>
- [Subreddit listing endpoint](https://reddapi.dev/api/v1/subreddits) <br>
- [Trends endpoint](https://reddapi.dev/api/v1/trends) <br>
- [reddapi.dev MCP endpoint](https://reddapi.dev/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples, JSON request and response examples, and environment variable setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDDAPI_API_KEY; calls reddapi.dev and can consume paid API quota.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
