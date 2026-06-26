## Description: <br>
Generate images from text prompts or input images using the ZenMux Vertex AI-compatible API with Gemini image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkthinking](https://clawhub.ai/user/thinkthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative users use this skill to generate images from prompts, edit existing images, and control model, aspect ratio, and resolution through a command-line script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional input images are sent to ZenMux for generation. <br>
Mitigation: Use the skill only with prompts and images that are acceptable to share with ZenMux. <br>
Risk: Providing the API key with the --api-key flag can expose it in shell history. <br>
Mitigation: Set ZENMUX_API_KEY in the environment instead of passing the key on the command line. <br>
Risk: The script can create output directories and write generated image files locally. <br>
Mitigation: Choose output paths deliberately and review generated files before reuse. <br>


## Reference(s): <br>
- [ZenMux](https://zenmux.ai) <br>
- [ClawHub skill page](https://clawhub.ai/thinkthinking/zenmux-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; the Python script writes generated image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZENMUX_API_KEY; supports optional input image, model, aspect ratio, image size, temperature, token limit, and output path settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
