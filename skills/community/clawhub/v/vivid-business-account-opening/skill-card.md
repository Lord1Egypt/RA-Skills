## Description: <br>
Open a Vivid Business account via a remote MCP server by collecting legal entity data in chat and generating a pre-filled onboarding URL after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanlee000](https://clawhub.ai/user/stanlee000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to start Vivid Business onboarding by providing legal entity details and receiving a pre-filled onboarding link. The skill is intended for explicit user-requested account-opening flows, not autonomous outreach or account creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured legal entity data is sent to Vivid's remote onboarding service. <br>
Mitigation: Review the collected-data summary, verify country and legal-entity details, and require explicit user confirmation before calling the remote tool. <br>
Risk: Uploaded documents may contain sensitive information beyond the fields needed for onboarding. <br>
Mitigation: Extract only required fields locally, do not send raw documents to the MCP server, and summarize extracted data without echoing full document contents. <br>
Risk: Users may provide credentials or unrelated financial information in chat. <br>
Mitigation: Do not request or accept passwords, API keys, bank account numbers, or unrelated financial information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stanlee000/vivid-business-account-opening) <br>
- [Vivid MCP repository](https://github.com/vivid-money/vivid-mcp) <br>
- [Vivid privacy policy](https://vivid.money/en-eu/privacy-policy/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and an onboarding URL returned by the remote MCP tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before sending structured legal entity data to the remote MCP server.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
