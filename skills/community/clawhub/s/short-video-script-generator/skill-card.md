## Description:

AI短视频脚本生成工具，支持多平台、多时长，自动生成hook、镜头、文案、BGM、CTA完整方案，支持脚本管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[baolige2023](https://clawhub.ai/user/baolige2023)

### License/Terms of Use:

MIT-0

## Use Case:

External short-video creators use this skill to generate Chinese-language scripts for platforms such as Douyin, Kuaishou, WeChat Channels, Xiaohongshu, YouTube Shorts, and TikTok. The skill drafts a hook, shot plan, voiceover, subtitles, background music suggestion, and CTA for 15, 30, or 60 second videos, with local script history and export support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill ships exposed provider credentials and unsafe payment/session controls.

Mitigation: Rotate provider keys, load secrets from a managed secret store or environment, and require server-side payment verification before every billable generation.

Risk: The security review says the web app should not be run as-is with real users or real billing.

Mitigation: Disable debug mode, bind privately or use production deployment controls, and complete a security review before handling real users or payments.

Risk: Prompts are sent to SiliconFlow for script generation.

Mitigation: Disclose the external AI provider to users before generation and avoid submitting sensitive or confidential topics.

Risk: The security guidance calls for safe DOM rendering.

Mitigation: Render generated script fields with safe text handling or sanitization before displaying AI-produced content in the browser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baolige2023/skills/short-video-script-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Chinese script content returned as JSON, rendered in a web UI, and exportable as Markdown/text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hook, shot descriptions, voiceover, subtitles, BGM suggestion, CTA, platform, duration, and local history records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
