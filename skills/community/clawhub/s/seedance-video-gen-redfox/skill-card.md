## Description:

基于 Seedance 2.0 模型，可按提示词或参考图片生成 MP4 视频，并控制分辨率、画面比例和时长。

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators, product managers, and content teams use natural-language prompts or reference images to generate short video assets, adjust output settings, and check or download completed tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the skill suspicious because its API key may be sent to an unvalidated media-download destination; prompts and reference-image URLs are also sent to an external service, and the scan was partial.

Mitigation: Avoid installation until the API key is kept out of media-download requests and downloads are restricted to verified HTTPS destinations; consider whether you are comfortable sending prompts and reference-image URLs to the external service.

## Reference(s):

- [RedFox API key setup](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox video API configuration](https://redfox-hk.oss-cn-hangzhou.aliyuncs.com/skill-specs/video-gen/spec.json)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [MP4 video files and task status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional synchronized audio and last-frame image URL; configurable resolution, aspect ratio, and duration.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
