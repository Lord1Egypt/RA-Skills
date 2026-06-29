## Description: <br>
Analyzes smart-transit, rail, highway, ETC, signal-system, and traffic electromechanical procurement notices, awards, companies, brands, prices, and market trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External procurement, business development, and market analysis users use this skill to query transportation infrastructure bid and award data, analyze suppliers and purchasers, compare brands and prices, and identify potential opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact zhiliaobiaoxun.com services and send device or user identifiers during automatic registration. <br>
Mitigation: Prefer a manually provisioned ZLBX_API_KEY and approve any automatic registration path before installation or use. <br>
Risk: The skill can write a local API credential to ~/.zlbx/config.json. <br>
Mitigation: Review local credential files after first use and restrict file access to trusted users. <br>
Risk: Procurement contact data may appear in query results. <br>
Mitigation: Share outputs only with authorized users and apply the organization's data handling rules before redistribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/smart-transit-rail-bid-analyzer) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Auto-registration flow reference](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with JSON request examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse an API key in ~/.zlbx/config.json when no credential is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
