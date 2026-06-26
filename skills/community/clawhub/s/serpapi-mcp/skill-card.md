## Description: <br>
Run SerpAPI searches via SerpAPI's MCP server using mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merlintxu](https://clawhub.ai/user/merlintxu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to run SerpAPI-backed web searches through MCP and return SerpAPI JSON for follow-up analysis or automation. Teams can optionally log search queries and result summaries to Airtable when that data flow is intentionally enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and returned results are sent to SerpAPI. <br>
Mitigation: Use the skill only for searches appropriate for SerpAPI processing and avoid highly sensitive search terms. <br>
Risk: Optional Airtable logging can store queries and full result JSON outside the agent environment. <br>
Mitigation: Keep SERP_LOG_AIRTABLE disabled unless logging is intentional, and use a least-privilege Airtable token scoped to the intended base and table. <br>
Risk: The runtime depends on the external mcporter CLI. <br>
Mitigation: Install mcporter from a trusted source and verify it before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/merlintxu/serpapi-mcp) <br>
- [SerpAPI AI Overview API](https://serpapi.com/google-ai-overview-api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON returned to stdout, with Markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and SerpAPI API credentials; Airtable logging is optional and disabled unless configured.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
