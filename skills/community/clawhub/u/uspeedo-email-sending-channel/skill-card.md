## Description:

Sends user-authorized transactional email via uSpeedo API with ACCESSKEY credentials, resolving a default sender through GetSenderList when needed and requiring explicit confirmation before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[code-by-ai](https://clawhub.ai/user/code-by-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send user-approved transactional or notification emails through uSpeedo after configuring ACCESSKEY_ID and ACCESSKEY_SECRET. It helps collect and confirm sender, recipient, subject, content, and credential requirements before making uSpeedo email API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ACCESSKEY_ID or ACCESSKEY_SECRET could be exposed through chat history, logs, or echoed request data.

Mitigation: Use environment variables or a secure secret mechanism, avoid pasting long-lived credentials into chat, and do not echo authorization headers or raw credential-bearing payloads.

Risk: Email could be sent to the wrong recipients or from an unintended sender.

Mitigation: Resolve the sender before sending and require explicit user confirmation of sender, recipients, subject, and final content in the current turn.

Risk: Raw HTML email content can contain unsafe active content or be used for abusive email.

Mitigation: Prefer plain text, reject risky HTML patterns, and refuse deceptive, phishing, credential-harvesting, or policy-violating send requests.

## Reference(s):

- [uSpeedo Homepage](https://uspeedo.com/?ChannelCode=OpenClaw)
- [uSpeedo GetSenderList API](https://uspeedo.com/docs/products/email/api/GetSenderList)
- [uSpeedo Email API Key Management](https://console.uspeedo.com/email/setting?type=apiKeys&ChannelCode=OpenClaw)
- [uSpeedo Domain Setting](https://console.uspeedo.com/email/setting?type=domain)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON, JavaScript, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before sending and should report only user-safe API outcomes.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence; source SKILL.md frontmatter remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
