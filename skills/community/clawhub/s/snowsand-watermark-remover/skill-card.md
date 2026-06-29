## Description: <br>
Remove watermarks from images using Florence-2 detection + IOPaint (LaMa) inpainting. Supports batch processing and manual/automatic modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process media they own or are authorized to modify, especially MLS listing photos, by detecting watermark regions and inpainting them. It supports single-image and batch workflows with dry-run detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill removes or restores watermarks from image media, which can be misused on media the user is not authorized to modify. <br>
Mitigation: Use only on media the user owns or has explicit authorization to modify, as stated by the security guidance. <br>
Risk: Processing may download and run external model code or dependencies such as Florence-2, IOPaint, and optional OCR packages. <br>
Mitigation: Install dependencies from trusted package indexes, review model and dependency trust settings, and run in an isolated environment before operational use. <br>
Risk: Automated detection and inpainting can leave visible artifacts or miss watermarks. <br>
Mitigation: Use dry-run detection, inspect generated outputs, and adjust confidence, padding, or model selection before relying on processed images. <br>


## Reference(s): <br>
- [IOPaint Model Comparison for Watermark Removal](references/model-comparison.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with bash commands; execution can produce cleaned image files, mask images, and JSON batch summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Original images are not modified in place; output depends on selected detection threshold, padding, model, and device.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
