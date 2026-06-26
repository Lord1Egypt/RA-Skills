## Description: <br>
Sends user-authorized transactional email via uSpeedo API with ACCESSKEY credentials, resolves the sender when needed, and requires explicit confirmation of sender, recipients, subject, and content before sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[code-by-ai](https://clawhub.ai/user/code-by-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send user-authorized transactional or notification email through the uSpeedo API after credentials, sender, recipients, subject, and content are confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive ACCESSKEY credentials and can send real email through uSpeedo. <br>
Mitigation: Use environment variables or a secure secret mechanism, prefer test or least-privilege keys, avoid unnecessary sensitive message bodies, and require final confirmation of sender, recipients, subject, and exact content before sending. <br>
Risk: HTML email content may contain active or unsafe patterns. <br>
Mitigation: Prefer plain text when possible and reject or rewrite HTML containing scripts, iframes, forms, inline event handlers, or javascript URLs before sending. <br>
Risk: A missing or ambiguous sender could cause email to be sent from the wrong address. <br>
Mitigation: Resolve the sender with GetSenderList when the user does not provide one, then present the resolved sender for confirmation with the rest of the send parameters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/code-by-ai/uspeedo-email-sending-channel) <br>
- [uSpeedo Homepage](https://uspeedo.com/?ChannelCode=OpenClaw) <br>
- [uSpeedo GetSenderList API Reference](https://uspeedo.com/docs/products/email/api/GetSenderList) <br>
- [uSpeedo Email API Key Management](https://console.uspeedo.com/email/setting?type=apiKeys&ChannelCode=OpenClaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACCESSKEY_ID and ACCESSKEY_SECRET; sends only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
