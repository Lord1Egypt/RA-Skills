## Description:

Remove watermarks from images using Florence-2 detection + IOPaint (LaMa) inpainting. Supports batch processing and manual/automatic modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and listing-photo operators use this skill to detect watermark regions in image files and produce inpainted output images for authorized image cleanup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to remove watermark and provenance markings from images.

Mitigation: Use it only on images the user owns or is expressly authorized to modify, and review intended use before execution.

Risk: The skill loads third-party models and mutable model code during execution.

Mitigation: Run in an isolated environment and pin, review, and approve dependencies and model sources before installation or use.

Risk: The skill can preserve EXIF metadata in generated images.

Mitigation: Disable or strip EXIF metadata before sharing outputs when location, device, or other sensitive metadata may be present.

Risk: Output images, masks, and result summaries may overwrite existing files at the selected output paths.

Mitigation: Keep backups and use separate output directories or suffixes for batch processing.

## Reference(s):

- [IOPaint Model Comparison for Watermark Removal](references/model-comparison.md)
- [ClawHub Skill Page](https://clawhub.ai/snowsand-enterprises/skills/snowsand-watermark-remover)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown guidance with inline shell commands and a Python script; runtime outputs image files, mask PNG files, and JSON summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes single images or directories and can run in dry-run mode to produce detection masks without inpainting.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
