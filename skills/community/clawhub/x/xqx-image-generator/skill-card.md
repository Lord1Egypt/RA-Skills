## Description:

Uses Ark (Volcengine Doubao) text-to-image through an OpenAI-compatible API for short captions and long structured creative or poster-style prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hidebug](https://clawhub.ai/user/hidebug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill in agent workflows to request image generation via Volcengine Ark for avatars, covers, posters, and illustration assets. It supports direct short prompts and file-based long prompt briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Volcengine Ark for image generation.

Mitigation: Avoid including secrets or highly sensitive personal or business information in prompts.

Risk: Long prompts may be stored temporarily in the workspace and printed in process logs.

Mitigation: Clear wdatas/xqx-img-prompt.txt and relevant logs after use when prompt confidentiality matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hidebug/skills/xqx-image-generator)
- [Volcengine Ark API base URL](https://ark.cn-beijing.volces.com/api/v3)
- [Volcengine Ark image generations endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text stdout with progress logs and a final image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY and ARK_IMAGE_MODEL; --file mode reads ./wdatas/xqx-img-prompt.txt; the skill returns an image URL and does not download image files.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
