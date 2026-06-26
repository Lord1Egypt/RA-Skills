## Description: <br>
Generate images from text prompts using xAI's Grok API with options for output format, batch size, and automatic media attachment in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mexicanamerican](https://clawhub.ai/user/mexicanamerican) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to request images from xAI's Grok image-generation API, save or return generated images, and attach resulting media in agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed bundle is missing the main xai-gen executable that would handle API keys, prompts, network calls, and generated files. <br>
Mitigation: Review or obtain the executable from a trusted source before installing the skill or providing an xAI API key. <br>
Risk: Prompts are expected to be sent to xAI's API for image generation. <br>
Mitigation: Avoid confidential or personal data in prompts and review xAI account and data-handling requirements before use. <br>
Risk: Persisting XAI_API_KEY in shell profiles can expose the key as local plaintext. <br>
Mitigation: Use a dedicated limited-scope key where possible and persist it only if local plaintext exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mexicanamerican/xai-image-gen) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration] <br>
**Output Format:** [CLI text output with MEDIA file paths, saved image files, or base64 image text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XAI_API_KEY and network access to xAI; generated image behavior depends on the external API and the missing executable should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
