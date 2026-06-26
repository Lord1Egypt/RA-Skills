## Description: <br>
Sends text or HTML email through the Resend API with support for multiple recipients, CC, BCC, and bulk-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aprilvkuo](https://clawhub.ai/user/aprilvkuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and automation agents use this skill to send notifications, alerts, newsletters, and workflow emails through a Resend account without configuring SMTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real outbound email through the user's Resend account. <br>
Mitigation: Require manual review of recipients, subject, body, CC/BCC, and bulk sends before execution. <br>
Risk: Email content or recipient lists may disclose sensitive or regulated information. <br>
Mitigation: Avoid sensitive or regulated content unless intentionally approved for the account and use case. <br>
Risk: A broadly scoped Resend API key could increase impact if exposed or misused. <br>
Mitigation: Use a dedicated least-privilege Resend API key and rotate it according to account policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aprilvkuo/resend-email-sender) <br>
- [Resend](https://resend.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Plain text status messages and markdown usage examples with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RESEND_API_KEY and can optionally use RESEND_FROM; sends requests to the Resend email API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
