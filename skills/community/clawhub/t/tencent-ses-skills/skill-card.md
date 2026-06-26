## Description: <br>
Tencent Cloud SES skill for sending email, managing sender domains and addresses, querying delivery status, managing templates, and diagnosing DNS authentication issues through Tencent Cloud APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Tencent Cloud SES email workflows, including sender-domain verification, sender-address setup, template or custom-content email sending, delivery-status checks, and SPF, DKIM, DMARC, and MX diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud API credentials and the security evidence warns that users may be asked to provide SecretId or SecretKey in chat. <br>
Mitigation: Do not paste SecretId or SecretKey into chat; configure credentials through environment variables or a secret manager using a dedicated low-scope CAM subaccount. <br>
Risk: The skill can send email and create or modify SES resources such as domains, sender addresses, and templates. <br>
Mitigation: Require dry-run previews and explicit user confirmation before sending email or creating, updating, or deleting SES resources. <br>
Risk: Leaked or overprivileged cloud credentials could affect Tencent Cloud resources or incur costs. <br>
Mitigation: Use least-privilege CAM access, enable IP restrictions where possible, rotate keys, and avoid main-account credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencent-ses-skills) <br>
- [Tencent Cloud SES API reference](references/api_reference.md) <br>
- [Mail domain DNS authentication guide](references/dns_guide.md) <br>
- [SES skill security setup guide](references/security_setup_guide.md) <br>
- [Tencent Cloud SES product documentation](https://cloud.tencent.com/document/product/1288) <br>
- [Tencent Cloud CAM IP restriction documentation](https://cloud.tencent.com/document/product/598/38037) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SES and DNS scripts produce JSON to stdout and diagnostic logs to stderr; write actions should use dry-run previews and explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
