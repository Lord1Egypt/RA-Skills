## Description: <br>
Sends template-based SMS messages through the Chuanglan SMS platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuanglanyunzhi](https://clawhub.ai/user/chuanglanyunzhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send approved Chuanglan SMS templates from an agent workflow. It supports single or comma-separated recipient phone numbers, a template ID, and optional JSON template variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real paid SMS messages, including bulk sends. <br>
Mitigation: Use a dedicated low-quota Chuanglan account and require human confirmation before bulk or customer-facing sends. <br>
Risk: SMS account credentials are required and may be loaded from environment variables or a local .env file. <br>
Mitigation: Keep credentials out of untrusted .env files, rotate them regularly, and restrict the account with IP whitelisting where available. <br>
Risk: Changing CHANGLAN_API_URL can redirect requests and credentials to another endpoint. <br>
Mitigation: Only set CHANGLAN_API_URL when the endpoint is trusted and expected for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chuanglanyunzhi/sms-send) <br>
- [Chuanglan Website](https://www.chuanglan.com/) <br>
- [Chuanglan Registration](https://www.chuanglan.com/register) <br>
- [SMS Signature Real-Name Documentation](https://doc.chuanglan.com/document/9OHGKZG716OXFI9O) <br>
- [Chuanglan SMS API Documentation](https://doc.chuanglan.com/document/HAQYSZKH9HT5Z50L) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [CLI text status messages with Chuanglan message IDs and success counts; configuration uses environment variables or a local .env file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, openssl, CHANGLAN_ACCOUNT, and CHANGLAN_PASSWORD; sends real paid SMS messages through the configured Chuanglan endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.6 and skill.json reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
