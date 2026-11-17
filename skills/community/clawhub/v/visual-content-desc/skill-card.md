## Description:

Generates accessible text descriptions, alt text, and figure text for medical images and charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic writers use this skill to produce concise descriptions, alt text, and figure text for medical visuals when image type and key visual features are provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical visuals can contain protected health information or other sensitive clinical data.

Mitigation: Use only authorized images, de-identify patient information where possible, and confirm privacy or compliance obligations before processing.

Risk: Descriptions of medical visuals may be incomplete or misleading if key features are missing or incorrect.

Mitigation: Require image_type and key_features inputs, state assumptions, and have qualified reviewers verify outputs before clinical or regulated use.

Risk: Generated outputs may be saved in the workspace and become visible to collaborators with workspace access.

Mitigation: Keep outputs in approved workspace locations and avoid including sensitive identifiers in generated descriptions.

## Reference(s):

- [Visual Content Desc - References](references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/visual-content-desc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance and JSON-shaped description fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns description, alt_text, figure_text, and image_type fields when the packaged script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
