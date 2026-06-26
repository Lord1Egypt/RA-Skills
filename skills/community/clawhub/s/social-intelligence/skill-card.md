## Description: <br>
Social Intelligence gives AI agents MCP-based access to Xpoz social media research across Twitter, Instagram, Reddit, and TikTok for search, monitoring, lead discovery, sentiment analysis, influencer research, and CSV export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External researchers, marketers, sales teams, and AI agents use this skill to query Xpoz social media data, monitor brands, find leads and experts, analyze sentiment, discover influencers, and export CSV datasets through MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Xpoz queries, results, and authentication material are sent to Xpoz's hosted service. <br>
Mitigation: Install only if this hosted-service data flow is acceptable, authenticate through the xpoz-setup skill, and protect credentials from logs or shared transcripts. <br>
Risk: Exported social media datasets may contain personal data or sensitive user content. <br>
Mitigation: Minimize bulk exports, store CSV files securely, restrict redistribution, and delete data when it is no longer needed. <br>
Risk: Social media research and exports can create compliance risk under platform terms or applicable privacy rules. <br>
Mitigation: Confirm the planned use complies with platform terms, organizational policy, and applicable privacy requirements before exporting or sharing results. <br>


## Reference(s): <br>
- [Social Intelligence on ClawHub](https://clawhub.ai/atyachin/social-intelligence) <br>
- [Xpoz](https://xpoz.ai) <br>
- [xpoz-setup skill](https://clawhub.ai/skills/xpoz-setup) <br>
- [xpoz-social-search skill](https://clawhub.ai/skills/xpoz-social-search) <br>
- [social-sentiment skill](https://clawhub.ai/skills/social-sentiment) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, CSV exports] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, xpoz-setup authentication, network access to mcp.xpoz.ai, and an Xpoz account; searches may export CSV datasets up to 64K rows per query.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
