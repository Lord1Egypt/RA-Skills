## Description: <br>
Sends text, image, and file messages through OpenClaw's WeChat channel for direct, scheduled, and batch messaging when the recipient already has an existing chat history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntaffffff](https://clawhub.ai/user/ntaffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to prepare and run OpenClaw WeChat message sends for text, images, and files. It is intended for workflows where the exact recipient, message, and attachment can be confirmed before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages while consent and contact-safety controls may not be tightly enforced. <br>
Mitigation: Require confirmation of the exact recipient, message, and attachment before every send, and avoid global authorization for group, scheduled, bulk, or file-sending actions. <br>
Risk: Scheduled, group, or bulk messaging can create spam, harassment, or account-restriction risk. <br>
Mitigation: Use a contact allowlist, validate recipients before sending, apply conservative rate limits, and do not use the skill for unsolicited outreach. <br>
Risk: File or image sending can expose sensitive local content. <br>
Mitigation: Confirm attachment paths and contents before sending, avoid sensitive personal or confidential data, and restrict allowed attachment locations where possible. <br>


## Reference(s): <br>
- [WeChat Sender on ClawHub](https://clawhub.ai/ntaffffff/wechat-sender-dxx) <br>
- [WeChat API Reference](artifact/references/wechat-api.md) <br>
- [WeChat Rate Limits](artifact/references/rate-limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recipient, message type, content or file path, authorization, contact-list, and rate-limit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
