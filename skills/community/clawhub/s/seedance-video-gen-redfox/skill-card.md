## Description:

基于 Seedance 2.0 模型的 AI 视频生成器，输入关键词/描述文案即可生成 MP4 视频。支持文生视频、首帧/尾帧/参考图生视频、分辨率/比例/时长控制。使用 Seedance 视频生成、AI 视频、text-to-video 时调用此 Skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, product teams, and creative professionals use natural-language prompts and optional image URLs to generate short MP4 videos, then check task progress or download completed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review warns that video downloads can expose the API key to an unchecked download server.

Mitigation: Wait for a fix that downloads through a separate session without API credentials and validates HTTPS destinations and redirects; if already used, consider rotating the key.

Risk: Prompts and reference-image URLs are sent to RedFox for hosted processing.

Mitigation: Submit only content you are authorized to share.

## Reference(s):

- [RedFox API key setup](https://redfox.hk/settings/api-keys?source=clawhub)
- [ClawHub skill release](https://clawhub.ai/redfox-data/skills/seedance-video-gen-redfox)

## Skill Output:

**Output Type(s):** [Video files (MP4), Task status and result details]

**Output Format:** [MP4 video with task status and result details as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional synchronized audio, 480p or 720p resolution, multiple aspect ratios, 4–15 second duration, and image references.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
