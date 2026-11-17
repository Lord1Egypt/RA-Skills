## Description:

根据用户提示词，实现文生图、文生视频、图生视频，制作的素材用于地震应急数字化演练。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daixihu2026](https://clawhub.ai/user/daixihu2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate realistic 16:9 images or 15-second videos for earthquake emergency digital drills, optionally using one preloaded asset image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation prompts, task metadata, and one selected asset image may be sent to Alibaba Cloud OSS and the referenced aggregation API.

Mitigation: Do not place sensitive or proprietary images in the skill assets directory unless they are intended for upload to those third-party services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daixihu2026/skills/wenshengtu)
- [Wuyin Keji generation API documentation](https://api.wuyinkeji.com/doc/60)
- [Wuyin Keji result API documentation](https://api.wuyinkeji.com/doc/36)

## Skill Output:

**Output Type(s):** [guidance, API calls, files]

**Output Format:** [Markdown guidance with generated image or MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses at most one selected asset image when available; video defaults are 16:9, 15 seconds, and large clarity.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
