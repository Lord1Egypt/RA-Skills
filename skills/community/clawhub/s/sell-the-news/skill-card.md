## Description: <br>
Use Sell The News to retrieve real-time market news, WallStreetBets analysis, stock news, options data, news search results, and Trump Truth Social market-impact posts through the hosted Sell The News endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitansde](https://clawhub.ai/user/nitansde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Sell The News for live financial-news retrieval, market-impact analysis, ticker news, options data, and news search from an agent or shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends JSON arguments to the Sell The News remote endpoint, so sensitive private information could be exposed if included in requests. <br>
Mitigation: Do not pass secrets or sensitive private information as JSON arguments. <br>
Risk: The endpoint can be overridden with SELL_THE_NEWS_MCP_ENDPOINT, which could route requests to an untrusted server. <br>
Mitigation: Set SELL_THE_NEWS_MCP_ENDPOINT only to servers the user or organization trusts. <br>
Risk: Returned market news, options data, and market-impact analysis can be incomplete, delayed, or incorrect. <br>
Mitigation: Treat outputs as informational retrieval results and verify important financial conclusions against authoritative sources before acting. <br>


## Reference(s): <br>
- [Sell The News MCP endpoint](https://mcp.sellthenews.org/mcp) <br>
- [ClawHub listing](https://clawhub.ai/nitansde/sell-the-news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only retrieval from a remote endpoint; wrapper scripts accept JSON arguments and print parsed JSON responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
