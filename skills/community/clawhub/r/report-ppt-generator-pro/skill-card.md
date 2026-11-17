## Description:

Generates professional, editable PowerPoint presentations from text manuscripts, style examples, optional images, and AI-generated illustrations with an interactive HTML preview before PPTX export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loommo](https://clawhub.ai/user/loommo)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers can use this skill to convert report manuscripts and visual style examples into polished PowerPoint presentations. It is especially suited for work reports that need style extraction, slide outlining, HTML preview, optional AI illustrations, and editable PPTX export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary remote images and embed local image files without strong boundaries.

Mitigation: Use trusted manuscripts and image sources, avoid untrusted remote image URLs, and prefer local images kept in a dedicated project folder.

Risk: The release needs review because URL restrictions, local path containment, pinned dependencies, and preview scope are not clearly bounded.

Mitigation: Review before installation and ask the publisher to add URL restrictions, local path containment, pinned dependencies, and clearer preview/export scoping.

Risk: Optional AI illustration generation depends on external Gemini access through nanobanana-skill.

Mitigation: Configure credentials only for trusted environments and review generated images before embedding them in presentations.

## Reference(s):

- [Style Extraction Guide](artifact/references/style-extraction.md)
- [Work Report Layout Templates](artifact/references/work-report-layouts.md)
- [Image Handling Guide](artifact/references/image-handling.md)
- [AI Illustration Prompts](artifact/references/ai-illustration-prompts.md)
- [Report Ppt Generator Pro on ClawHub](https://clawhub.ai/loommo/skills/report-ppt-generator-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON, HTML, CSS, JavaScript, and shell command snippets; generated artifacts may include HTML previews, image files, and editable PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided manuscripts, style images, and optional image sources; optional AI illustration generation depends on nanobanana-skill and Gemini API configuration.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata; artifact package.json reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
