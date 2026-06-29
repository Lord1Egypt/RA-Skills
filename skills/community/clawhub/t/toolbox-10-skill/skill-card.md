## Description: <br>
集合四大高频实用图像工具：去水印/OCR文字识别/图片压缩/标准证件照生成。一站式解决日常图片处理需求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local image utilities for watermark removal, OCR text extraction, image compression, and standard ID photo generation from user-provided image files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python image-processing scripts and writes derived files to user-selected or default output paths. <br>
Mitigation: Review input and output paths before execution and inspect generated files before relying on them. <br>
Risk: Dependencies are installed with unpinned package names and OCR/background-removal model files may download on first use. <br>
Mitigation: Use an isolated virtual environment and allow network access only when dependency or model download behavior is expected. <br>
Risk: Watermark removal can be misused on content the user is not authorized to modify. <br>
Mitigation: Use the watermark-removal workflow only for images where removal is lawful and authorized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/toolbox-10-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; Python scripts return JSON status, text OCR output, and processed image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local image paths and writes derived image or text files; OCR and ID-photo features may download model files on first use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
