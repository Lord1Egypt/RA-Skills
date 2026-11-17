## Description:

Automatically extracts product images from product URLs, generates HTML promotional email templates, manages saved assets, and can optionally send emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szzg007](https://clawhub.ai/user/szzg007)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and ecommerce developers use this skill to turn product pages into reusable promotional email assets. It supports product image collection, HTML email generation, asset cataloging, report creation, and optional email delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports embedded SMTP credentials and disabled mail security checks.

Mitigation: Remove and rotate the exposed SMTP credential, load secrets from a protected configuration source, and restore TLS certificate and hostname verification before using email sending.

Risk: The release security guidance reports weak safeguards around writing and sending generated content.

Mitigation: Require explicit approval before any send action, validate recipients and path inputs, and inspect generated email content before delivery.

Risk: Generated HTML values and downloaded assets may be retained on disk under the configured asset directory.

Mitigation: Escape dynamic HTML values, restrict asset paths to the intended workspace, and define a retention or cleanup policy for downloaded images and generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/szzg007/skills/szzg007-product-promotion)
- [README](README.md)
- [Code System](references/CODE_SYSTEM.md)
- [Usage Examples](references/USAGE_EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with shell commands, generated HTML email files, markdown reports, image files, and JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated images, emails, reports, and metadata under the configured product-promotion asset directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
