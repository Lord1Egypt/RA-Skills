## Description: <br>
Uses the rembg AI model to remove image backgrounds and produce transparent-background PNG files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JustZeroX](https://clawhub.ai/user/JustZeroX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to remove backgrounds from single images or batches of images and save transparent PNG outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has avoidable code-execution risks when processing image paths. <br>
Mitigation: Review or patch path handling before processing images from untrusted sources or archives. <br>
Risk: Installation creates a persistent virtual environment, downloads rembg models, installs Python packages, and may modify PATH or shell startup files. <br>
Mitigation: Install only after reviewing those persistent environment changes, and check shell configuration or Windows PATH afterward. <br>


## Reference(s): <br>
- [rembg detailed guide](references/rembg-guide.md) <br>
- [u2net model download used by rembg](https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill creates transparent PNG image files as runtime artifacts.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
