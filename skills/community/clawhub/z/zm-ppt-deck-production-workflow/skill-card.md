## Description:

ZM PPT/Deck 正式生产流程。用于把课程课件、行业专场、招商/培训/沙龙 Deck 的需求、大纲、页面合同、素材分级、样页确认、视觉生产、PPT/HTML 组装、渲染审核、返工和交付包归档串成稳定流水线。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Deck producers, trainers, consultants, and agents use this skill to coordinate formal PPT/HTML deck production from requirement capture and outline approval through visual generation, PPTX assembly, rendered review, compression, upload records, and delivery package archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Branding and footer rules may carry Zhumeng or insurance-event assumptions into decks for other clients.

Mitigation: Review and edit branding standards, logo placement, footer text, and event-specific defaults before using the skill for client or non-Zhumeng decks.

Risk: Upload records can expose file tokens, links, destination nodes, or retention details.

Mitigation: Confirm upload destinations and sharing scope before use, record only necessary token or link details, and handle those records as sensitive delivery metadata.

Risk: PPTX inspection can print or write deck text and metadata to local JSON or stdout.

Mitigation: Avoid running inspection on confidential decks unless local JSON/stdout output is acceptable, and remove generated inspection artifacts when no longer needed.

Risk: Generated visuals could be mistaken for real logos, people, QR codes, product screens, cases, or data.

Mitigation: Use real or official assets for identity, product, QR, case, and data evidence; when assets are missing, keep explicit placeholders until the user supplies approved materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-ppt-deck-production-workflow)
- [README](artifact/README.md)
- [Full PPT production workflow](artifact/workflows/full-ppt-production-workflow.md)
- [Interactive production workflow](artifact/workflows/interactive-production-workflow.md)
- [Real asset and image generation boundary](artifact/standards/real-asset-and-image-generation-boundary-v1.md)
- [Compression and upload standard](artifact/standards/compression-upload-standard-v1.md)
- [Delivery package structure](artifact/templates/project_structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions and templates, JSON audit results, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deck production gates, page contract templates, review checklists, PPTX inspection output, compression output, and delivery package verification output.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
