## Description: <br>
Send email through Resend.com's HTTPS API from native Node.js with dry-run output by default and explicit send gating for real messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwestburg](https://clawhub.ai/user/jwestburg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to draft and, after explicit approval, send outbound email through Resend. It is suited for simple notifications and generated report delivery where recipients, headers, subject, and body are reviewed before a real send. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real email send can externally disclose unintended content or reach the wrong recipient. <br>
Mitigation: Keep the default dry-run flow, review the exact body and all delivery headers, require explicit approval before adding --send, and keep RESEND_ALLOWED_TO narrow. <br>
Risk: The runtime needs a Resend API key to send email. <br>
Mitigation: Provide RESEND_API_KEY only through the process environment, prefer a least-privilege key for a verified sender or domain, and avoid sharing dry-run logs that contain reviewed message content. <br>
Risk: Network timeouts or read errors after a request is sent may leave delivery status ambiguous. <br>
Mitigation: Check the Resend dashboard before retrying to reduce duplicate-send risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jwestburg/resend-send-native-node) <br>
- [Resend](https://resend.com) <br>
- [Resend domains](https://resend.com/domains) <br>
- [Resend pricing](https://resend.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run and send receipts can include recipient lists, subject, content type, body byte count, body SHA-256 values, allowlist status, and Resend message ID for successful real sends.] <br>

## Skill Version(s): <br>
1.0.12 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
