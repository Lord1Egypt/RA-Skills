## Description:

Tencent Cloud SMS Skill helps agents send domestic and international SMS, manage SMS signatures and templates, monitor package usage, and query delivery or reply status through Tencent Cloud SMS APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide Tencent Cloud SMS workflows, including one-off or bulk sends, signature and template review, quota monitoring, and delivery or reply status investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports automatic installation of unpinned packages.

Mitigation: Run the skill in an isolated virtual environment and preinstall reviewed dependency versions before use.

Risk: The security scan reports broad local configuration-file searches for cloud credentials.

Mitigation: Use a dedicated low-privilege Tencent Cloud CAM subaccount, provide credentials only through the intended environment variables, and avoid storing reusable secrets in generic shell or system config files.

Risk: SMS sends and signature or template changes can cost money or affect customers.

Mitigation: Review dry-run previews, recipients, message content, templates, signatures, and account quotas before approving any live operation.

## Reference(s):

- [Tencent Cloud SMS Documentation](https://cloud.tencent.com/document/product/382)
- [Tencent Cloud SMS Quick Start - Domestic SMS](https://cloud.tencent.com/document/product/382/37745)
- [Tencent Cloud SMS Quick Start - International, Hong Kong, Macao, and Taiwan SMS](https://cloud.tencent.com/document/product/382/37797)
- [Tencent Cloud SMS API Limits and Specifications](references/api-limits.md)
- [Tencent Cloud SMS Common Error Codes](references/error-codes.md)
- [ClawHub Skill Release Page](https://clawhub.ai/tencent-adm/skills/tencentcloud-sms-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SMS sending and signature or template changes can affect a Tencent Cloud account and should be previewed and confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
