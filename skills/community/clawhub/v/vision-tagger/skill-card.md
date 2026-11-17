## Description:

Tags and annotates images on macOS using Apple Vision to detect faces, bodies, hands, OCR text, barcodes, scene labels, rectangles, and saliency regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sagarjhaa](https://clawhub.ai/user/sagarjhaa)

### License/Terms of Use:


## Use Case:

Developers and image-workflow users use this skill for local macOS image analysis, photo tagging, document scanning, posture checks, accessibility descriptions, and annotated visual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image analysis outputs may expose sensitive content such as faces, body pose, OCR text, and barcode payloads.

Mitigation: Analyze only images the user owns or has consent to process, and treat generated JSON and annotated images as potentially sensitive.

Risk: Setup runs local macOS installation and dependency commands, including Pillow installation.

Mitigation: Review setup commands before execution and prefer a virtual environment with a pinned, reviewed Pillow version.

## Reference(s):

- [Vision Tagger ClawHub Skill Page](https://clawhub.ai/sagarjhaa/skills/vision-tagger)
- [Vision Tagger Homepage](https://clawhub.ai/skills/vision-tagger)

## Skill Output:

**Output Type(s):** [text, json, code, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with shell commands; generated analysis is JSON with optional annotated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS 12+, Xcode Command Line Tools, Python 3, Pillow, and local image files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
