## Description: <br>
一键生成多平台爆款文案 - 小红书/抖音/公众号/知乎 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bandwe](https://clawhub.ai/user/Bandwe) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Content creators, marketers, and agent operators use this skill to generate platform-tailored Chinese social-media copy, titles, and tags for Xiaohongshu, Douyin, WeChat, and Zhihu from a topic and optional audience, tone, length, and keyword inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill embeds a third-party LLM API key. <br>
Mitigation: Revoke and rotate the embedded key before use, remove it from the source, and require users to provide their own credential through environment configuration. <br>
Risk: The security scan says prompts may be sent to DashScope without clearly informing users. <br>
Mitigation: Do not use the skill with confidential prompts unless the DashScope path is removed or gated behind explicit user consent and clear disclosure. <br>
Risk: Generated social-media copy may be inaccurate, misleading, or unsuitable for a platform or audience. <br>
Mitigation: Review generated copy, titles, and tags before publication and verify factual claims independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bandwe/social-media-copywriter-generator) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Release notes v0.1.0](artifact/RELEASE-v0.1.0.md) <br>
- [DashScope compatible chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown-formatted social media copy, title lists, and platform-specific tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated content to a local output file when an output path is supplied; supports platform, tone, length, keywords, audience, title-only, and no-tag options.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
