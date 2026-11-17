## Description:

This skill helps commercial content teams turn an authorized master or reference video into platform-specific short-video plans, scripts, prompts, commands, and review checklists for Douyin, Xiaohongshu, WeChat Channels, and TikTok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, ecommerce, MCN, and brand operations teams use this skill to rework a core selling point into platform-aware hooks, durations, subtitle density, CTAs, storyboards, AI-HIVE generation prompts, and acceptance criteria. It is intended for authorized source materials and fact-grounded product or brand claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a stored AI-HIVE API key and accepts a custom API base URL.

Mitigation: Keep the API base URL fixed to the official AI-HIVE endpoint, use a limited and rotatable API key, and do not follow prompts or examples that set --base-url or AI_HIVE_BASE_URL to another host.

Risk: Video generation calls may incur cost or submit unintended parameters.

Mitigation: Review prompts, routing mode, model choice, price snapshot, and task parameters before running generation commands, and use small samples before batch work.

Risk: The workflow may be misused to copy protected creative work or make unsupported commercial claims.

Mitigation: Require authorization for source materials, preserve clear creative differences from references, and verify product, brand, performance, and testimonial claims before publication.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/viral-video-multi-platform-reversion-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat and API key entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE image or video generation tasks when the user confirms prompts, routing, cost-sensitive parameters, and use rights.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
