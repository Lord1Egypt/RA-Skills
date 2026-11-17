## Description:

通过创蓝短信平台发送模板短信。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuanglanyunzhi](https://clawhub.ai/user/chuanglanyunzhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with a Chuanglan SMS account use this skill to send approved template SMS messages to one or more phone numbers, optionally filling template variables from JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and endpoint controls require review before installation.

Mitigation: Use OpenClaw-managed secrets, avoid the .env file path, run only from a trusted non-writable skill directory, and keep SMS credentials scoped to the official Chuanglan HTTPS endpoint.

Risk: SMS sends can affect recipients or incur account charges if phone numbers, templates, or variables are wrong.

Mitigation: Confirm destination numbers, use only approved Chuanglan templates, and test template variables before broader sends.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chuanglanyunzhi/skills/sms-send)
- [Chuanglan Website](https://www.chuanglan.com/)
- [Chuanglan SMS API Documentation](https://doc.chuanglan.com/document/HAQYSZKH9HT5Z50L)
- [Chuanglan SMS Signature Real-Name Documentation](https://doc.chuanglan.com/document/9OHGKZG716OXFI9O)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, Configuration guidance]

**Output Format:** [CLI text output from a shell command that sends JSON over HTTPS to the Chuanglan SMS API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, openssl, CHANGLAN_ACCOUNT, and CHANGLAN_PASSWORD; accepts phone, template, and optional vars JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact versions differ: SKILL.md 1.0.6, skill.json 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
