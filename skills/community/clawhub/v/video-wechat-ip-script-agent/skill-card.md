## Description:

生成适合视频号发布的爆款IP内容方案：选题、标题、钩子、口播脚本、镜头建议、封面文案、发布文案、评论引导，以及医美场景下的基础合规改写。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangfu20171212-hue](https://clawhub.ai/user/yangfu20171212-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, medical-aesthetics operators, and personal-brand teams use this skill to generate Chinese WeChat Channels topics, hooks, spoken scripts, shot suggestions, cover copy, publishing captions, comment prompts, style rewrites, and basic medical-aesthetics compliance rewrites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and draft content to a configured model endpoint.

Mitigation: Install only when the configured model endpoint is trusted; avoid untrusted MODEL_BASE_URL or OPENAI_BASE_URL values and prefer a gateway-specific API key.

Risk: Generated medical-aesthetics marketing copy may contain incorrect, exaggerated, or non-compliant claims.

Mitigation: Review outputs before publication and use the compliance action to identify risky wording and safer alternatives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangfu20171212-hue/skills/video-wechat-ip-script-agent)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON content with Chinese topic, script, rewrite, or compliance-review fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output shape depends on the requested action: topics, script, rewrite, or compliance.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
