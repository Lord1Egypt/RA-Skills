## Description:

通过创蓝短信平台发送模板短信。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoweige1101](https://clawhub.ai/user/xiaoweige1101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send approved Chuanglan template SMS messages from an agent workflow after configuring Chuanglan API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS API credentials may be exposed or mishandled in some setups.

Mitigation: Prefer OpenClaw-managed secrets and avoid storing CHANGLAN_PASSWORD in a broadly readable .env file.

Risk: Changing CHANGLAN_API_URL can send credentials and recipient data to an untrusted destination.

Mitigation: Leave the default endpoint in place unless the replacement destination is fully trusted.

Risk: The command can send paid SMS messages and transmit recipient phone data to the SMS provider.

Mitigation: Limit who can run the skill, verify recipients and templates before sending, and monitor SMS usage or quotas.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoweige1101/skills/send-sms)
- [Chuanglan Website](https://www.chuanglan.com/)
- [Chuanglan Registration](https://www.chuanglan.com/register)
- [SMS Signature Real-Name Documentation](https://doc.chuanglan.com/document/9OHGKZG716OXFI9O)
- [Chuanglan SMS API Documentation](https://doc.chuanglan.com/document/HAQYSZKH9HT5Z50L)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, Configuration]

**Output Format:** [Plain text command output with markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, openssl, CHANGLAN_ACCOUNT, and CHANGLAN_PASSWORD.]

## Skill Version(s):

1.0.7 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
