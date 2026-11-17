## Description:

Unified multi-platform AI image generation with a dropdown selector for Volcengine Seedream, Alibaba Qwen Image, and Google Gemini (Nano Banana) models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sangjiexun](https://clawhub.ai/user/sangjiexun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate or edit images through a unified image-generation workflow that can route requests to Volcengine Ark, Alibaba DashScope, or Google Gemini models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends prompts and image data through a local proxy to selected third-party image providers.

Mitigation: Use the skill only with providers approved for the intended data, and avoid including secrets or sensitive content in prompts or image inputs.

Risk: API keys may be retained locally in `~/.openclaw-dev/uni-image-config.json` without documented protections.

Mitigation: Use restricted provider keys with billing limits, rotate keys if exposed, and check or delete the local configuration file when key retention is not desired.

Risk: The security summary notes that proxy and injection scripts should be verified before use.

Mitigation: Review the installed package contents before execution and run the skill only in environments where the local proxy behavior is acceptable.

## Reference(s):

- [ClawHub uni-image release page](https://clawhub.ai/sangjiexun/skills/uni-image)
- [Project homepage from skill manifest](https://github.com/sangjiexun/openclaw-skill-UniImage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include provider model selection, API key setup, and local proxy usage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
