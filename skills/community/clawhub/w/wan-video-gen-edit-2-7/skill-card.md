## Description:

Video Generation and Editing with Wan 2.7 series models. Supports text2video, image2video (first-frame, first+last-frame, video-continuation), reference2video, and video-editing capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisyejh](https://clawhub.ai/user/krisyejh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to prepare and run Alibaba DashScope Wan 2.7 video generation and editing tasks, then retrieve task status and generated video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, media URLs, local files, and voice samples to Alibaba DashScope.

Mitigation: Use only prompts, media, and reference voices that the user is authorized to submit; avoid private files, internal URLs, and voice samples without explicit consent.

Risk: Local-file inputs may be base64-encoded and uploaded through API requests.

Mitigation: Hosts should restrict or patch local-file upload behavior before broad agent use, and require user confirmation before submitting local paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krisyejh/skills/wan-video-gen-edit-2-7)
- [Alibaba ModelStudio Model Market](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market)
- [wan2.7-t2v API Documentation](references/wan2.7-t2v-api-doc.md)
- [wan2.7-i2v API Documentation](references/wan2.7-i2v-api-doc.md)
- [wan2.7-r2v API Documentation](references/wan2.7-r2v-api-doc.md)
- [wan2.7-videoedit API Documentation](references/wan2.7-videoedit-api-doc.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses containing task IDs, statuses, and generated video URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and the python3 requests package; generated task IDs and video URLs are time-limited according to the skill documentation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
