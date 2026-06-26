## Description: <br>
Generate styled QR codes (SVG/PNG/JPG) with custom colors, shapes, and error correction, then display the generated file to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HeXavi8](https://clawhub.ai/user/HeXavi8) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and operators use this skill to generate styled QR code files for URLs, contact data, WiFi credentials, print assets, signage, and other text payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated QR images, chat previews, workspace files, and default filenames can reveal sensitive payloads. <br>
Mitigation: Avoid encoding real secrets unless they are intended to be visible, and use an explicit neutral output filename for private payloads. <br>
Risk: QR codes may fail to scan if styling, size, print quality, or error correction settings are inappropriate for the target use. <br>
Mitigation: Use higher error correction, larger sizes, simpler styling, or the documented format recommendations for print, signage, logo overlays, and dense payloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HeXavi8/qrcode) <br>
- [Sharp installation documentation](https://sharp.pixelplumbing.com/install) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Generated SVG, PNG, or JPG files with Markdown display guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are saved to the workspace root; filenames may be user-specified or auto-generated from sanitized input text.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
