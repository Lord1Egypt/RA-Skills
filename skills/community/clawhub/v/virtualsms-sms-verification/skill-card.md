## Description: <br>
Real SIM-card phone numbers for SMS verification across 2000+ services and 145+ countries via the VirtualSMS MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[virtualsms](https://clawhub.ai/user/virtualsms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure agents to obtain real-SIM phone numbers, buy verification numbers, receive OTP codes, and manage SMS verification orders for accounts they own or are explicitly allowed to manage. <br>

### Deployment Geography for Use: <br>
Global, subject to VirtualSMS country availability and applicable law. <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables paid access to real-SIM OTP and account-verification workflows. <br>
Mitigation: Use it only for lawful, authorized verification on accounts the user owns or is explicitly allowed to manage, and require explicit confirmation before number purchases or OTP retrieval. <br>
Risk: VirtualSMS API keys, phone numbers, order details, and OTP codes are sensitive. <br>
Mitigation: Store credentials in the host client's MCP configuration, avoid exposing or logging OTP data, and treat returned account and transaction details as sensitive. <br>
Risk: Hosted or npm-based MCP access depends on external VirtualSMS infrastructure and package behavior. <br>
Mitigation: Review the external MCP server or npm package before use and set spending controls or operational limits where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/virtualsms/virtualsms-sms-verification) <br>
- [VirtualSMS Project](https://virtualsms.io) <br>
- [VirtualSMS MCP Setup](https://virtualsms.io/mcp) <br>
- [virtualsms-mcp npm Package](https://www.npmjs.com/package/virtualsms-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, text] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and SMS/OTP results from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make MCP tool calls that purchase phone numbers, wait for or poll SMS codes, and return order metadata; requires a VirtualSMS API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
