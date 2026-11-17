## Description:

使用 Seedream 5.0 Lite 为授权图片替换背景，并重新匹配主体边缘、尺度、透视、光向、接触阴影、反射和景深，让合成结果适配电商与营销渠道。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and commerce content teams use this skill to replace backgrounds for authorized product and portrait images while preserving subject identity, logos, text, perspective, lighting, shadows, reflections, and depth of field.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images and prompts are sent to AI Hive for processing.

Mitigation: Use the skill only for authorized images and prompts that are appropriate to send to AI Hive.

Risk: The helper requires an AI Hive API key that may be stored locally.

Mitigation: Use a virtual environment, protect local key storage, prefer documented configuration paths, and do not run the script as root.

Risk: Background replacement can create misleading context for people, places, brands, or events.

Mitigation: Confirm rights and authorization before editing, preserve subject identity, and avoid edits that imply false location, affiliation, role, capability, or factual context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-background-replace)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash command examples; generated image files are downloaded by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and at least one explicitly selected input image for generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
