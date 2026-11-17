## Description:

使用 Seedream 5.0 Lite 按远看、中看、近看三档阅读设计海报底图，并通过 AI Hive 从文字或授权参考图生成营销、活动、课程、餐饮、发布会和社媒海报素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, marketers, and agent operators use this skill to plan poster composition by viewing distance, generate no-text or low-text poster backgrounds, and preserve space for approved final copy. It supports text prompts and authorized reference images for event, course, product, food, launch, and social media poster workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images are sent to AI Hive, and an AI Hive API key may be stored locally.

Mitigation: Use only non-sensitive prompts and authorized reference images, protect the API key, and prefer a dedicated output directory.

Risk: API responses can direct uploads, downloads, and output file paths.

Mitigation: Perform maintainer review for URL validation, filename sanitization, and dependency pinning before broad deployment.

Risk: Generated posters may include random text, dates, prices, brands, or altered reference assets.

Mitigation: Generate no-text base images where possible, typeset approved final copy manually, and inspect outputs at 10%, 25%, and 100% before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-poster)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key, can upload authorized reference images, and saves generated image outputs to a configured directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
