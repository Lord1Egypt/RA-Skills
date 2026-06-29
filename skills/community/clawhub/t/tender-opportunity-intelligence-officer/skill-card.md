## Description: <br>
An agent skill for procurement opportunity intelligence, expiring-project discovery, competitor tracking, company analysis, and market research using Zhiliaobiaoxun tender data APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, business development, channel, and market-intelligence teams use this skill to find near-term tender opportunities, track competitor wins, identify potential customers or bidders, and analyze procurement trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can register a device with an external service when no API key is configured, sending device-identifying metadata during first use. <br>
Mitigation: Prefer manually creating an account and setting ZLBX_API_KEY before use; use the automatic registration path only after accepting the device-binding behavior. <br>
Risk: The skill can write an API key to ~/.zlbx/config.json for later reuse. <br>
Mitigation: Protect the local configuration file, avoid sharing it, and remove or rotate the stored key if the environment is shared or no longer trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/tender-opportunity-intelligence-officer) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Automatic registration flow](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with API-backed tender intelligence, JSON request and response snippets, and concise operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write a local API-key configuration file and call external Zhiliaobiaoxun APIs when no user-provided API key is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
