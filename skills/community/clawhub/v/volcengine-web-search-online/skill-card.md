## Description: <br>
Calls the Volcengine web search endpoint to return web, summarized web, or image search results for a query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs to run Volcengine-backed web, web summary, or image search and present the returned summaries, result links, usage data, and status information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the AZT_API_KEY are sent to the stated third-party Volcengine web search endpoint. <br>
Mitigation: Install only when that service is intended, keep the key scoped to this service, and avoid placing the key in a broad global environment when agents should not use it automatically. <br>
Risk: Missing, expired, or depleted credentials stop the search workflow. <br>
Mitigation: Provide AZT_API_KEY only through the documented parameter or environment variable and rotate or refresh it through the service documentation when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyriswu/volcengine-web-search-online) <br>
- [Volcengine Web Search Endpoint](https://coze-js-api.devtool.uk/volcengine/web-search) <br>
- [Devtool Plugin Documentation](https://devtool.uk/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown-formatted search status and results, or raw JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summary_text, web_results, image_results, result_count, usage, search_context, request status, and remaining-credit or failure information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
