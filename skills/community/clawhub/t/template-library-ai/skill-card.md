## Description:

Templatebased Writing helps an agent collect user requirements, select or create document templates, fill template placeholders, and deliver formatted DOCX, PPTX, or PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueheng-rgb](https://clawhub.ai/user/yueheng-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to guide an agent through template selection, document-content collection, placeholder filling, and final file delivery for papers, reports, resumes, and presentations. It supports both built-in template workflows and user-provided or newly created templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive documents may be routed through an unsafe and under-disclosed external workflow.

Mitigation: Do not upload private, regulated, school, resume, or business documents until the service uses HTTPS, explains retention and deletion, and asks for explicit upload consent.

Risk: API keys and payment proof may be sent to the current plaintext backend.

Mitigation: Do not provide API keys, trade numbers, or payment proof until the backend uses HTTPS and the payment flow is reviewed.

Risk: Users may install a release that does not match the reviewed artifact.

Mitigation: Use a pinned install command whose slug and version match the reviewed artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yueheng-rgb/skills/template-library-ai)
- [API reference](artifact/references/api.md)
- [Pricing reference](artifact/references/pricing.md)
- [Template guidance](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with structured content fields, shell commands, JSON API payloads, and delivered document file paths or download links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference DOCX, PPTX, and PDF files through local scripts or remote template-generation APIs.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
