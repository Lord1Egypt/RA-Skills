## Description: <br>
Manage invoices, contacts, bills, payments, and accounting records in Xero via the Xero API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and accounting operators use this skill to work with Xero accounting records from an agent chat, including invoices, bills, contacts, payments, items, accounts, bank transactions, journals, organisation data, and tracking categories. The skill is intended for workflows that need Xero reads plus carefully confirmed accounting writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide write actions that affect financial records, including invoices, bills, payments, contacts, accounts, bank transactions, and journals. <br>
Mitigation: Preview write operations, confirm details with the user before execution, and verify tax, currency, status, and accounting effects in Xero when needed. <br>
Risk: The skill depends on OAuth access and connected Xero organisation scope. <br>
Mitigation: Use the ClawLink connection flow, confirm the active Xero integration before tool calls, and avoid asking users to paste API credentials into chat. <br>
Risk: The security evidence is clean but still advises reviewing visible instructions and credentials or tools before use. <br>
Mitigation: Review the skill instructions and requested tools before installation, and scan the release evidence as part of deployment review. <br>


## Reference(s): <br>
- [Xero API Documentation](https://developer.xero.com/documentation/) <br>
- [Xero API Overview](https://developer.xero.com/documentation/api/overview) <br>
- [Xero OAuth 2.0 Guide](https://developer.xero.com/documentation/auth-and-reporting/xero-oauth2) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/xero-accounting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to preview and confirm Xero write actions before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
