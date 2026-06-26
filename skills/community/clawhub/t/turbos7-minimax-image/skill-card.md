## Description: <br>
Generates images with MiniMax from text prompts or from a reference image plus a prompt, with support for multiple aspect ratios, selected styles, batch generation, and local file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbos7](https://clawhub.ai/user/turbos7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to generate MiniMax images from natural-language prompts or transform a supplied reference image into a new image. It is useful when an agent needs to produce image assets and return the saved local file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MiniMax API key and sends prompts to the MiniMax image-generation service. <br>
Mitigation: Store MINIMAX_API_KEY securely, avoid printing or committing it, and monitor MiniMax API usage for unexpected activity. <br>
Risk: Image-to-image requests may send local reference images to MiniMax. <br>
Mitigation: Do not use private, regulated, copyrighted, or otherwise sensitive reference images unless the user is allowed to share them with MiniMax. <br>
Risk: Generated images are saved locally and may remain after the task is complete. <br>
Mitigation: Review generated files in ~/.openclaw/workspace/assets/images and delete images that are no longer needed. <br>


## Reference(s): <br>
- [MiniMax Image API Reference](references/image-api.md) <br>
- [MiniMax API key page](https://platform.minimaxi.com/user-center/basic-information/interface-key) <br>
- [ClawHub skill page](https://clawhub.ai/turbos7/turbos7-minimax-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown or plain text guidance with Python and shell command examples; runtime scripts save generated JPEG files locally and print file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under ~/.openclaw/workspace/assets/images by default with text2img or img2img filename prefixes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
