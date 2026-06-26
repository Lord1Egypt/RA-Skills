## Description: <br>
Queries TTPOS restaurant operating data through the ttpos-agent API and helps agents generate business, order, payment, menu item, member, shift, and time-period reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BenDaye](https://clawhub.ai/user/BenDaye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and support agents use this skill to query authorized TTPOS restaurant reporting data, build scoped SQL requests, and summarize sales, order, payment, item, member, shift, and time-period results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API key to access restaurant reporting data. <br>
Mitigation: Use a dedicated, least-privilege key when available, store it only in the skill configuration, and revoke it when access is no longer needed. <br>
Risk: Broad or imprecise reporting queries can expose more business or member detail than needed. <br>
Mitigation: Scope requests to specific merchants and date ranges, avoid unnecessary member-level details, and keep single-query ranges limited. <br>
Risk: Incorrect SQL or stale schema assumptions can produce misleading reports. <br>
Mitigation: Fetch the ttpos-agent query guide before constructing SQL, prefer documented statistics tables, apply delete-time filtering, and use limits for larger result sets. <br>


## Reference(s): <br>
- [TTPOS Agent on ClawHub](https://clawhub.ai/BenDaye/ttpos-agent) <br>
- [BenDaye ClawHub Profile](https://clawhub.ai/user/BenDaye) <br>
- [Light Bridge Service](https://claw.doge6.com) <br>
- [ttpos-agent Web Panel](https://claw.doge6.com/web/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, SQL, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries with API request examples and scoped SQL query guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LIGHT_BRIDGE_API_KEY and uses LIGHT_BRIDGE_URL for ttpos-agent API requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
