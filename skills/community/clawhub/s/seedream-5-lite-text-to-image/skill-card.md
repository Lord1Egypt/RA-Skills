## Description:

使用 Seedream 5.0 Lite 从纯文字建立视觉实验卡，快速比较构图、叙事、媒介、色板和渠道比例，再收敛为可交付图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, educators, marketers, and developers use this skill to turn text-only visual briefs into Seedream 5.0 Lite image-generation tasks through AI Hive. It supports concept illustration, packaging exploration, educational backgrounds, architectural mood concepts, social media image series, and similar AIGC image workflows without using reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key and sends text prompts to AI Hive.

Mitigation: Use a scoped, revocable key; avoid sending sensitive prompt content; and run the helper in an isolated environment.

Risk: The helper downloads generated result files without enforcing a maximum file size.

Mitigation: Choose an output directory with enough available space and monitor generated downloads during large batches.

Risk: Generated concept, product, architectural, or news-style images could be mistaken for real-world evidence.

Mitigation: Label generated or conceptual images clearly and review outputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-text-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands and generated image files downloaded by the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses text prompts, optional model parameters, batch size, routing mode, and an output directory; downloaded result size is not capped by the script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
