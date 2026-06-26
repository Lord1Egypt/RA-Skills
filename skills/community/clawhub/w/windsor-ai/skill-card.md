## Description: <br>
Connect to Windsor.ai MCP for natural language access to 325+ data sources including Facebook Ads, GA4, HubSpot, Shopify, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosarturoleon](https://clawhub.ai/user/carlosarturoleon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, analytics, and revenue operations users use this skill to query connected Windsor.ai business data, inspect available sources, compare campaign and sales performance, and generate reports from natural language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may involve external business-data access through Windsor.ai. <br>
Mitigation: Install only when the agent should use Windsor.ai for analytics questions, review connected business systems, and avoid broad analytics prompts unless that external access is intended. <br>
Risk: The skill requires WINDSOR_API_KEY to access connected Windsor.ai data. <br>
Mitigation: Use a scoped API key where possible and store it in a secrets manager or restricted-permission environment file. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/carlosarturoleon/windsor-ai) <br>
- [Windsor.ai](https://windsor.ai) <br>
- [Windsor.ai MCP Endpoint](https://mcp.windsor.ai/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Windsor.ai MCP with WINDSOR_API_KEY and the user's connected account data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
