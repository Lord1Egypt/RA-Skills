## Description: <br>
Visual inspection helper for VLM and OCR workflows that helps an agent create clearer intermediate images through rotation, cropping, zooming, enhancement, or format conversion before re-analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testlbin](https://clawhub.ai/user/testlbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a vision model or OCR workflow needs a clearer second-pass view of an image, especially for unreadable text, ambiguous characters, low contrast, rotated content, or a relevant subregion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing sensitive images can expose their contents if base64 output is sent to an untrusted model or tool. <br>
Mitigation: Use the helper only on images intended for analysis, and send base64 output only to trusted receiving systems. <br>
Risk: Image transformations can alter visibility or context enough to produce misleading second-pass interpretation. <br>
Mitigation: Apply the smallest useful transformation and re-analyze the processed image before adding further edits. <br>
Risk: The helper depends on Pillow for local image parsing and transformation. <br>
Mitigation: Install Pillow from a trusted package environment and keep the runtime dependencies maintained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/testlbin/vlm-image-helper) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Presets](references/presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files, configuration] <br>
**Output Format:** [Markdown guidance with CLI commands; processed image files or base64 image strings from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pillow and processes images locally from file paths, raw base64 strings, or data URIs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
