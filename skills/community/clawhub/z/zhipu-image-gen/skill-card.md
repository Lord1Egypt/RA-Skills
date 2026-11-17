## Description:

AI text-to-image generation using Zhipu AI's GLM-Image model for Chinese and English prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeteenager](https://clawhub.ai/user/codeteenager)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate PNG images from text prompts through Zhipu AI's GLM-Image API, with options for image size, output directory, and watermark behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Zhipu AI's third-party API and may contain sensitive or proprietary content.

Mitigation: Avoid using secrets, private personal data, or proprietary content in prompts, and review applicable provider terms before deployment.

Risk: Use of ZHIPU_API_KEY can incur third-party API billing charges.

Mitigation: Scope and monitor the API key, and deploy only where Zhipu AI image generation is intended.

Risk: Unusual quotes or JSON-like text in prompts may cause malformed or unintended API requests until request construction is hardened.

Mitigation: Avoid untrusted prompt text or harden JSON request construction before accepting arbitrary prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeteenager/skills/zhipu-image-gen)
- [Zhipu AI open platform](https://open.bigmodel.cn/)
- [Zhipu AI image generations endpoint](https://open.bigmodel.cn/api/paas/v4/images/generations)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, API Calls]

**Output Format:** [PNG image file plus shell status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY, curl, and jq; generated image filenames use glm_image_YYYYMMDD_HHMMSS.png.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
