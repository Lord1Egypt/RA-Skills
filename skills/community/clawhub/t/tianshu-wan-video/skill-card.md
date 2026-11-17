## Description:

Generates videos with Alibaba Qwen Wan 2.6 from text prompts or image URLs using Node.js.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can call a Node.js helper to submit text-to-video or image-to-video jobs to Alibaba DashScope and retrieve the resulting video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional image URLs are sent to Alibaba DashScope when the skill is explicitly run.

Mitigation: Use only prompts, media URLs, and source images approved for processing by DashScope; avoid sensitive, confidential, private internal, or proprietary content unless approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/tianshu-wan-video)
- [Alibaba DashScope API endpoint used by the skill](https://dashscope.aliyuncs.com/api/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Plain text console output containing VIDEO_URL: <url>]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; supports text-to-video and image-to-video modes with prompt, optional image URL, duration, and resolution settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
