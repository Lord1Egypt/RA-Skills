## Description: <br>
Practical image generation workflow for Volcengine/ARK-compatible APIs for poster creation, text-to-image generation, reference-image generation, local image upload, multi-image runs, and automatic result downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinhuadeng](https://clawhub.ai/user/jinhuadeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to run Volcengine/ARK-compatible image generation from prompts, reference images, and local image files, then save generated results locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local reference images are sent to a remote Volcengine/ARK-compatible API and may include sensitive content. <br>
Mitigation: Use scoped API keys, verify the endpoint, and avoid private or regulated reference images. <br>
Risk: Failed requests may expose prompts or base64-encoded local image data in logs or chat output. <br>
Mitigation: Review error output before sharing it and redact prompts, request payloads, and encoded image data when needed. <br>
Risk: Generated image URLs are downloaded automatically to the Desktop by default. <br>
Mitigation: Set download options to disable automatic downloads or redirect output to an approved directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinhuadeng/volcengine-image-studio) <br>
- [Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a remote image API, download returned images to local files, and report saved paths or API errors.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
