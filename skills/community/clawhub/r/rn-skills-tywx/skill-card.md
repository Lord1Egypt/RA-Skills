## Description:

Rn Skills helps agents create Xiaohongshu fashion and neo-Chinese aesthetics posts by scouting trends, selecting topics, drafting copy, generating Tongyi Wanxiang images, and archiving local outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykabps1314](https://clawhub.ai/user/ykabps1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate Xiaohongshu posts in the fashion and neo-Chinese aesthetics niche, including trend scouting, topic scoring, copywriting, image generation, local metadata, and publishing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell-based curl/cp calls and hard-coded local output paths can execute unintended shell behavior or write outside the intended project.

Mitigation: Replace shell calls with safe Python APIs and require user-approved project-local output paths before use.

Risk: The image helper reads ~/.zshrc for credentials and can make many paid DashScope API calls.

Mitigation: Remove shell-profile credential parsing, use explicit environment-variable handling, and enforce user confirmation plus job limits for paid image generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ykabps1314/skills/rn-skills-tywx)
- [Claude Code](https://claude.com/claude-code)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/)
- [DashScope image synthesis endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis)
- [DashScope task status endpoint](https://dashscope.aliyuncs.com/api/v1/tasks/{task_id})

## Skill Output:

**Output Type(s):** [text, markdown, images, JSON, files, guidance]

**Output Format:** [Markdown status summary plus generated post copy, PNG image files, and metadata JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default flow generates 2 posts and up to 12 images per run when DashScope credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
