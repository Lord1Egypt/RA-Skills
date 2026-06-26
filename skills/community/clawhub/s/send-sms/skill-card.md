## Description: <br>
通过创蓝短信平台发送模板短信。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoweige1101](https://clawhub.ai/user/xiaoweige1101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send approved Chuanglan SMS templates to one or more phone numbers from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends real external SMS messages that may create cost, compliance, or customer-impact risk. <br>
Mitigation: Use it only with an intended Chuanglan account, verify recipients and templates before sending, and require human review for bulk sends. <br>
Risk: SMS API credentials are required and could be exposed if stored in plaintext. <br>
Mitigation: Prefer OpenClaw or OS secret storage, restrict access to any credential file, and avoid committing CHANGLAN_ACCOUNT or CHANGLAN_PASSWORD. <br>
Risk: Template variables may contain regulated or sensitive personal data. <br>
Mitigation: Avoid putting secrets or regulated personal data in template variables unless the deployment has appropriate authorization and controls. <br>
Risk: A changed CHANGLAN_API_URL could redirect SMS payloads or credentials to an unintended endpoint. <br>
Mitigation: Verify CHANGLAN_API_URL before use and keep the default Chuanglan endpoint unless an approved endpoint is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoweige1101/send-sms) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xiaoweige1101) <br>
- [Chuanglan website](https://www.chuanglan.com/) <br>
- [Chuanglan registration](https://www.chuanglan.com/register) <br>
- [SMS signature real-name documentation](https://doc.chuanglan.com/document/9OHGKZG716OXFI9O) <br>
- [Chuanglan SMS API documentation](https://doc.chuanglan.com/document/HAQYSZKH9HT5Z50L) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Command-line output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, openssl, CHANGLAN_ACCOUNT, and CHANGLAN_PASSWORD; sends real SMS messages through the configured Chuanglan API endpoint.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
