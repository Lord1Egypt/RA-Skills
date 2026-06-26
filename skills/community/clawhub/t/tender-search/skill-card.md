## Description: <br>
Tender Search helps agents search and analyze tender notices, award results, company procurement activity, competitor overlap, supplier opportunities, market rankings, and price trends using the ZhiLiao BiaoXun tender data APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business analysts use this skill to find tender and award notices, analyze buyers and suppliers, research competitors, identify expiring projects, and summarize market or pricing trends for procurement and bidding decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may send device and user-environment identifiers to the vendor for automatic account creation. <br>
Mitigation: Set ZLBX_API_KEY manually before use or review the auto-registration behavior with the user before allowing network calls. <br>
Risk: The skill can persist an API key under ~/.zlbx/config.json. <br>
Mitigation: Review the local config file after use and delete or rotate the stored key when persistent credentials are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/tender-search) <br>
- [Search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Auto-registration reference](references/auto-register.md) <br>
- [ZhiLiao BiaoXun API base URL](https://mcp-server.zhiliaobiaoxun.com/api_v2/{tool_name}) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown summaries with JSON request examples and API-derived analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read an API key from ZLBX_API_KEY or ~/.zlbx/config.json; if neither exists, the artifact describes automatic registration and local API-key persistence.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
