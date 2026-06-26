## Description: <br>
Send emails through the UniProfit OpenClaw-compatible API with a user-created `mail_send` API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieziqing](https://clawhub.ai/user/xieziqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to deliver already-approved email content through a verified UniProfit mail account. It is for actual email delivery only after sender, recipient, subject, and final body are known. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real email content and recipient details are sent to the configured UniProfit endpoint. <br>
Mitigation: Use an HTTPS UniProfit API base URL that the operator trusts and confirm the recipient and final body before sending. <br>
Risk: A broad or untrusted mail credential could allow unintended email delivery. <br>
Mitigation: Use a scoped `mail_send` key and validate that it is configured for the intended UniProfit mail account before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xieziqing/uniprofit-mail-assistant) <br>
- [API Reference](references/api.md) <br>
- [Mail Constraints](references/mail-constraints.md) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown or plain text status with optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports recipient, send status, and record or message id when the UniProfit API returns them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
