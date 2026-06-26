## Description: <br>
Send transactional emails (alerts, reports, receipts, notifications) via the Truncus API when a workflow needs to deliver email to a recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codevanmoose](https://clawhub.ai/user/codevanmoose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send transactional emails such as alerts, reports, receipts, onboarding messages, and scheduled digests through the Truncus API. It is intended for explicit user-requested sends with recipient confirmation and idempotent delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real outbound email and may expose sensitive information through recipients, subject lines, body content, attachments, metadata, or tracking settings. <br>
Mitigation: Review recipients, subject, body, attachments, metadata, and tracking settings before each send; avoid secrets, regulated data, or internal incident details unless approved. <br>
Risk: A Truncus API key with broad permissions could be misused if exposed. <br>
Mitigation: Use a least-privilege Truncus API key and install only from the reviewed source. <br>
Risk: Local development simulation can print email content to the terminal. <br>
Mitigation: Avoid testing with sensitive content in local dev mode or ensure terminal logs are protected. <br>
Risk: Unintended or duplicate emails can create operational or privacy impact. <br>
Mitigation: Send only after an explicit user request, confirm recipients when needed, and use a unique idempotency key for every send attempt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codevanmoose/truncus-email) <br>
- [Skill homepage](https://github.com/codevanmoose/truncus-openclaw-skill) <br>
- [Truncus API](https://truncus.co) <br>
- [Truncus send endpoint](https://truncus.co/api/v1/emails/send) <br>
- [Truncus email details endpoint](https://truncus.co/api/v1/emails/{id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown and plain text with JSON payloads and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated email subject, body content, metadata, Truncus API request details, send status, and message identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
