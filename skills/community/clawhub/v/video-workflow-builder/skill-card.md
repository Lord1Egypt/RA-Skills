## Description:

Video Workflow Builder creates tailored, installable video-creation workflow skills for selected content platforms after researching the user's platform, niche, and persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charriotzed](https://clawhub.ai/user/charriotzed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a complete, installable agent workflow for video account planning, including topic selection, scripts, titles, covers, and platform-specific operating guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route agents through local network fetchers and configurable gateways.

Mitigation: Install only from a trusted publisher, verify every gateway hostname, restrict network access where possible, and avoid non-local HTTP endpoints.

Risk: The skill handles API keys, Aliyun credentials, Douyin session files, and .env configuration.

Mitigation: Use dedicated low-privilege credentials, keep secrets in git-ignored local files, exclude session files from shared backups, and rotate keys if exposure is suspected.

Risk: Generated workflow state and downstream skill files may propagate unsafe or inaccurate instructions.

Mitigation: Review and scan each generated workflow before installation, especially scripts, environment templates, and platform-specific guidance.

Risk: Generated finance-oriented video workflows could produce personalized trading or investment advice.

Mitigation: Require human and compliance review for finance workflows and avoid personalized trading recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charriotzed/skills/video-workflow-builder)
- [README](README.md)
- [Quick start](快速上手.md)
- [Douyin platform reference](references/platforms/douyin.md)
- [Bilibili platform reference](references/platforms/bilibili.md)
- [Xiaohongshu platform reference](references/platforms/xiaohongshu.md)
- [Shipinhao platform reference](references/platforms/shipinhao.md)
- [Baijiahao platform reference](references/platforms/baijiahao.md)
- [Topic selection methodology](references/methodology/topic-selection.md)
- [Script writing methodology](references/methodology/script-writing.md)
- [Title craft methodology](references/methodology/title-craft.md)
- [Cover design methodology](references/methodology/cover-design.md)
- [DailyHotApi](https://github.com/imsyy/DailyHotApi)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus generated skill files, Python scripts, and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an installable downstream skill directory after user confirmation; may use configured network, search, ASR, image-generation, and content-archive services.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
