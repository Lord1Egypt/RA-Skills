## Description:

Generate QoderWork-style presentations, automatically match 14 templates based on the user's topic, and output an editable .pptx file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwang2999](https://clawhub.ai/user/jackwang2999)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a presentation topic and requirements into a structured QoderWork-style PowerPoint deck. The agent plans slide content, maps it to built-in templates, fills HTML slides, and converts them into an editable PPTX file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide JSON, prompts, web content, or shared documents may influence rich text rendered in Chromium.

Mitigation: Review generated content before conversion and run the skill only in a restricted workspace.

Risk: The conversion pipeline may read arbitrary local files through image paths or fetch arbitrary URLs.

Mitigation: Avoid arbitrary local image paths, keep sensitive files out of the workspace, and disable or tightly control outbound network access.

Risk: Dependencies and browser-based rendering increase exposure if the package stack is stale.

Mitigation: Update and review the dependency stack before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackwang2999/skills/qoderwork-ppt-jack)
- [README](artifact/pptx/README.md)
- [Content Rules](artifact/pptx/rules/content-rules.md)
- [Template Matching Rules](artifact/pptx/rules/template-matching.md)
- [Template Manifest](artifact/pptx/templates/manifest.json)
- [Lucide Icons](https://lucide.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON slide data, HTML intermediate files, generated assets, and editable PPTX output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces intermediate content.md, slides.json, filled HTML files, optional images, and a timestamped presentation .pptx in the output directory.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
