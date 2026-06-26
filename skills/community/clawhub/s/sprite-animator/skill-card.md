## Description: <br>
Generate animated pixel art sprites from any image using AI. Send a photo, get a 16-frame animated GIF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awlevin](https://clawhub.ai/user/awlevin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, artists, and game creators use this skill to turn a source image into a 16-frame pixel-art animation workflow that can produce looping GIF sprite output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime package is fetched by uv when the command is run. <br>
Mitigation: Confirm trust in the `sprite-animator` package before installation and pin the package version where practical. <br>
Risk: Input images are processed by Gemini. <br>
Mitigation: Avoid personal, sensitive, or proprietary images unless third-party Gemini processing is acceptable. <br>
Risk: The workflow requires a Gemini API key. <br>
Mitigation: Use a limited API key or quota where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awlevin/sprite-animator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the invoked tool can produce GIF, sprite sheet, and frame image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; input images are processed by Gemini.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
