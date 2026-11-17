## Description:

使用 Nano Banana Pro 设计和编辑信息流封面，通过单一焦点、可兑现的信息缺口、短标题安全区和缩略图测试提高点击意愿，而不制造标题党。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content teams use this skill to generate or edit social, video, podcast, course, and article cover images with a single visual focus, a truthful information gap, and thumbnail readability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images are sent to AI Hive for image generation.

Mitigation: Use only approved, non-sensitive inputs and avoid uploading private or unlicensed images.

Risk: Running init stores an AI Hive API key in a local configuration file.

Mitigation: Use environment variables where possible, keep local configuration permissions restricted, and rotate keys if exposure is suspected.

Risk: The security evidence reports a filename handling flaw that could allow compromised API results to write outside the intended download folder.

Mitigation: Run the skill with a dedicated output directory and avoid sensitive working directories until filename sanitization and output-directory containment are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/viral-cover-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Images]

**Output Format:** [Markdown guidance with bash commands; generated image files are downloaded by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the fixed public_model_nano_banana_pro image model, optional reference images, batch size, routing mode, and model parameters such as aspect_ratio.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
