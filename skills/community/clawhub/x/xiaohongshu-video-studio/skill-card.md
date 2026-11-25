## Description:

分析小红书视频链接并生成转录、内容总结、结构拆解、分镜脚本、原创口播脚本或生成提示词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketers use the skill to turn Xiaohongshu video links into transcripts, analysis, reusable scripts, and generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's setup guidance asks users to paste a full Cue API key into chat.

Mitigation: Keep the key out of chat and configure it locally using a protected config file or environment variable; rotate it if it has been exposed.

Risk: The skill includes referral and purchase prompts as part of its credit guidance.

Mitigation: Use the skill only if you trust the Cue service and are comfortable with its reported promotional flow.

Risk: The security assessment is partial because some local references could not be resolved.

Mitigation: Treat the assessment as incomplete and review unresolved references before relying on the skill.

## Reference(s):

- [Cue Omni Reader online experience](https://cuecue.cn/hub/omni-reader)
- [ClawHub skill release](https://clawhub.ai/panting09266-ai/skills/xiaohongshu-video-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured JSON, Guidance]

**Output Format:** [Markdown transcripts, analysis reports, scripts, prompts, and optional structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include segmented transcripts, analysis tables, storyboard scripts, and reusable prompt sequences based on the supplied video link.]

## Skill Version(s):

1.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
