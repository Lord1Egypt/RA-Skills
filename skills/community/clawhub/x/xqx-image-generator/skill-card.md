## Description: <br>
Uses Ark (Volcengine Doubao) text-to-image through an OpenAI-compatible API for short captions and structured creative or poster-style briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hidebug](https://clawhub.ai/user/hidebug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflows use this skill to send image prompts to Volcengine Ark and receive a generated image URL. It supports direct short prompts and longer prompt briefs loaded from a workspace prompt file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Volcengine Ark using the caller's API key, so confidential prompt content may leave the local workspace. <br>
Mitigation: Use the skill only when sending the prompt text to Ark is acceptable for the workflow, and avoid placing sensitive or confidential prompt text in the workspace prompt file. <br>
Risk: ARK_API_KEY is a sensitive credential required at runtime. <br>
Mitigation: Provide the key through private environment configuration or a secret manager, and do not commit it to shared files, repositories, wikis, or synchronized folders. <br>
Risk: The skill returns an image URL rather than a local file, and generated links may be temporary. <br>
Mitigation: Have the calling workflow fetch or persist the image outside the skill when durable local storage is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hidebug/xqx-image-generator) <br>
- [Volcengine Ark OpenAI-compatible API base URL](https://ark.cn-beijing.volces.com/api/v3) <br>
- [Ark image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text stdout with progress logs and the final generated image URL on the last line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ARK_API_KEY and ARK_IMAGE_MODEL environment variables; the skill returns a URL and does not download image files.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
