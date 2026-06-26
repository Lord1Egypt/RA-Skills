## Description: <br>
Generate QoderWork-style presentations. Automatically matches 14 templates based on your topic and outputs an editable .pptx file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jackwang2999](https://clawhub.ai/user/Jackwang2999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to turn a requested topic, audience, and key points into a structured QoderWork-style PowerPoint deck with editable slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs npm/Puppeteer tooling and writes presentation artifacts into the current project's output directory. <br>
Mitigation: Install and run it only in a trusted project environment, review generated files, and run it from the intended working directory. <br>
Risk: Optional image search or image generation can contact external services and may expose sensitive presentation topics. <br>
Mitigation: Use local images or non-sensitive topics when external image sourcing is not appropriate. <br>
Risk: The pipeline clears output/filled during generation. <br>
Mitigation: Keep important generated slide HTML outside output/filled or back it up before re-running the pipeline. <br>


## Reference(s): <br>
- [QoderWork PPT skill instructions](artifact/SKILL.md) <br>
- [QoderWork PPT README](artifact/pptx/README.md) <br>
- [Content generation rules](artifact/pptx/rules/content-rules.md) <br>
- [Template matching rules](artifact/pptx/rules/template-matching.md) <br>
- [Template manifest](artifact/pptx/templates/manifest.json) <br>
- [Lucide icons](https://lucide.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, JSON slide data, filled HTML files, downloaded or generated image files, and editable PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates project-root output files including output/content.md, output/slides.json, output/images/, output/filled/*.html, and output/presentation.pptx or timestamped presentation files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
