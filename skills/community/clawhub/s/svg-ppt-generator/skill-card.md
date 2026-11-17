## Description:

SVG-based PPT generator with 9 themes, 8 layouts, 30+ charts, and 600+ icons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddpie](https://clawhub.ai/user/ddpie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn presentation requests, outlines, source documents, or data into styled SVG slides and editable PowerPoint decks. It guides topic, duration, style, outline confirmation, generation, and optional review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Included tooling can fetch arbitrary URLs insecurely when processing source material.

Mitigation: Use the skill in a sandboxed workspace with restricted outbound network access, especially for untrusted URLs or documents.

Risk: SVG image references can embed local files without enough containment.

Mitigation: Avoid untrusted SVG image references and review or sanitize SVG inputs before conversion.

Risk: Project environment files may expose unrelated secrets during processing.

Mitigation: Use an isolated project .env and do not store unrelated credentials in the workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ddpie/skills/svg-ppt-generator)
- [PPT Master Assets Index](ppt-master-assets/INDEX.md)
- [PPT Master Toolset README](ppt-master-assets/scripts/README.md)
- [Shared SVG Standards](ppt-master-assets/references/shared-standards.md)
- [SVG Image Embedding](ppt-master-assets/references/svg-image-embedding.md)
- [SVG Pipeline Tools](ppt-master-assets/scripts/docs/svg-pipeline.md)
- [Conversion Tools](ppt-master-assets/scripts/docs/conversion.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SVG, Python, shell command, and PowerPoint file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create 16:9 SVG slide files and convert them into native editable PPTX decks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
