## Description: <br>
Tag and annotate images using Apple Vision framework (macOS only). Detects faces, bodies, hands, text (OCR), barcodes, objects, scene labels, and saliency regions. Use for image analysis, photo tagging, posture monitoring, or any task requiring computer vision on images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sagarjhaa](https://clawhub.ai/user/sagarjhaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users who work with local image analysis use this skill to detect and tag faces, bodies, hands, OCR text, barcodes, scene labels, objects, and saliency regions, or to generate annotated image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image analysis can expose sensitive information from people, IDs, documents, screens, QR codes, or private text. <br>
Mitigation: Use the skill only on images the user is allowed to analyze, and review OCR or barcode output as untrusted data rather than instructions. <br>
Risk: Setup installs Pillow and compiles a local Swift binary. <br>
Mitigation: Run setup only in a trusted Python and macOS environment with Xcode Command Line Tools available. <br>
Risk: The skill depends on Apple Vision and macOS-specific tooling. <br>
Mitigation: Deploy only on macOS 12 or later with swiftc and python3 installed. <br>


## Reference(s): <br>
- [Vision Tagger on ClawHub](https://clawhub.ai/sagarjhaa/vision-tagger) <br>
- [Skill homepage](https://clawhub.ai/skills/vision-tagger) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON analysis output, annotated image files, and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on macOS with Apple Vision; annotated-image output requires Pillow and a compiled Swift binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
