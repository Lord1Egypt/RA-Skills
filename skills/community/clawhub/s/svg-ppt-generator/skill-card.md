## Description: <br>
SVG-based PPT generator with 9 themes, 8 layouts, 30+ charts, and 600+ icons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddpie](https://clawhub.ai/user/ddpie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Presentation authors and agents use this skill to turn topics, outlines, or source content into editable PowerPoint decks. The workflow guides topic, duration, style, and outline choices before generating SVG slides and converting them into native DrawingML PPTX output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local PPT generation writes temporary and project files and may run local converters. <br>
Mitigation: Run the skill in a controlled workspace and review output paths before generation. <br>
Risk: Optional external AI image generation can disclose prompt content to the selected provider. <br>
Mitigation: Use external image generation only with an explicit provider choice and non-sensitive prompts. <br>
Risk: SVG, image, and document helpers may process files supplied by the user. <br>
Mitigation: Avoid running the image-processing helpers on untrusted files. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/ddpie/svg-ppt-generator) <br>
- [PPT Master Assets Index](artifact/ppt-master-assets/INDEX.md) <br>
- [Shared SVG Standards](artifact/ppt-master-assets/references/shared-standards.md) <br>
- [SVG Image Embedding](artifact/ppt-master-assets/references/svg-image-embedding.md) <br>
- [SVG to PPTX Conversion Script](artifact/ppt-master-assets/scripts/svg_to_pptx.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Conversational guidance plus generated SVG slide files and editable PPTX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local temporary/project files for SVG generation, PPTX conversion, and optional visual review artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
