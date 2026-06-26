## Description: <br>
Analyzes user-provided images with the Minimax Coding Plan VLM API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbos1314](https://clawhub.ai/user/xbos1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to ask questions about image URLs, local image files, or base64 image data and receive natural-language visual analysis from Minimax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs, local image contents, base64 image data, and prompts are sent to the Minimax vision API. <br>
Mitigation: Use the skill only with data approved for Minimax processing, avoid confidential or personal images unless the data handling terms are acceptable, and prefer a dedicated Minimax API key. <br>
Risk: Local image paths are read from disk and converted to base64 before API submission. <br>
Mitigation: Review the image path before execution and pass only the intended file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xbos1314/understand-image-minimax) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text analysis printed to stdout, with errors printed to stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the MINIMAX_API_KEY environment variable; supports JPEG, PNG, GIF, WebP, HTTP(S) URLs, local paths, and data URL base64 inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
