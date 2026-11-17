## Description:

文档扫描增强 helps agents enhance single document or image inputs with scene-specific operations such as clarity improvement, watermark removal, shadow removal, crop rectification, and contract or document scan cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation teams use this skill to route one document or image at a time to a supported enhancement scene and receive a processed image path or JSON result. It is intended for document cleanup, image quality enhancement, and scan-like processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document images may be sent to an unspecified external scan service, which can expose sensitive personal, financial, contractual, or confidential content.

Mitigation: Use only images intended for that provider, avoid private IDs, contracts, receipts, and confidential documents unless the provider is trusted, and review data handling before deployment.

Risk: Broad activation or ambiguous image-enhancement requests could trigger the skill outside its stated document-scanning purpose.

Mitigation: Narrow activation text and require explicit document or image enhancement intent before running the skill.

Risk: The skill relies on scan-service credentials and command execution, creating credential exposure or unintended execution risk if deployed loosely.

Mitigation: Store SCAN_WEBSERVICE_KEY in environment or platform secrets, rotate it if exposed, and keep execution limited to the documented scene arguments.

## Reference(s):

- [ClawHub skill listing: quark-scan-free](https://clawhub.ai/thcjp/skills/quark-scan-free)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance, Configuration]

**Output Format:** [Markdown guidance with bash command examples and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful processing may return a local processed-image path; each invocation handles a single image input.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
