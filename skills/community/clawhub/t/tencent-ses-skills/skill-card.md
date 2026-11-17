## Description:

Helps agents use Tencent Cloud Simple Email Service to manage sender domains, sender addresses, templates, email sending, delivery status checks, and DNS authentication diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Tencent Cloud SES resources, send template-based or custom emails, inspect delivery status, and troubleshoot DNS authentication records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Cloud API credentials could be exposed if pasted into chat or stored in workspace files.

Mitigation: Configure credentials directly in a local environment or secret manager, avoid sharing SecretId or SecretKey in chat, and rotate keys if exposure is suspected.

Risk: The skill can perform high-impact email and SES account actions, including sends and resource changes.

Mitigation: Require dry-run previews and explicit user confirmation before sends, creates, updates, or deletes, and verify domains, templates, recipients, and sender addresses from live account queries.

Risk: Broad permissions, insecure endpoints, or unpinned dependencies increase account and supply-chain exposure.

Mitigation: Use a narrowly scoped CAM policy with IP restrictions where possible, keep HTTPS endpoints, avoid untrusted SES endpoints, and install dependencies in a pinned isolated environment.

## Reference(s):

- [Tencent SES skill page](https://clawhub.ai/tencent-adm/skills/tencent-ses-skills)
- [Tencent Cloud SES API Reference](references/api_reference.md)
- [Mail Domain DNS Authentication Guide](references/dns_guide.md)
- [SES Skill Security Setup Guide](references/security_setup_guide.md)
- [Tencent Cloud SES product documentation](https://cloud.tencent.com/document/product/1288)
- [Tencent Cloud SendEmail API documentation](https://cloud.tencent.com/document/product/1288/51034)
- [Tencent Cloud sender domain DNS verification documentation](https://cloud.tencent.com/document/product/1288/60652)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations should be previewed with dry-run and require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
