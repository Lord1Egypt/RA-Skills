## Description:

seo-images helps agents audit and optimize web images for SEO and performance, including alt text, file size, modern formats, responsive markup, lazy loading, CLS prevention, image SERP research, and WebP/AVIF or metadata workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and site operators use this skill to inspect web image implementation, prioritize image optimization work, and generate practical recommendations or commands for format conversion, metadata handling, and responsive delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to modify image files or write metadata in place.

Mitigation: Use explicit target folders, review generated commands before execution, and keep backups before metadata writes or conversions.

Risk: Broad wildcards in file-optimization commands can affect more images than intended.

Mitigation: Avoid broad wildcards unless the target set has been reviewed and confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-images)
- [Google Merchant Center AI-generated content policy](https://support.google.com/merchants/answer/14743464)
- [IPTC DigitalSourceType vocabulary](https://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with audit tables, prioritized recommendations, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested file-optimization commands and metadata-write workflows for explicit target images or folders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
