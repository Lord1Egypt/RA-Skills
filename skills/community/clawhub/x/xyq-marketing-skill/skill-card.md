## Description:

使用小云雀公开营销 API，根据商品图文生成剧情广告、品牌大片或达人带货营销视频；上传素材、提交营销成片、查询进度、下载交付结果及查询积分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ydtincle](https://clawhub.ai/user/ydtincle)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create Xiaoyunque marketing videos from product images and natural-language campaign instructions. It guides upload, generation, status checks, result download, and balance checks through the public marketing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads and generation requests send user-selected product assets and instructions to a third-party marketing API.

Mitigation: Use the skill only for assets approved for Xiaoyunque processing, review dry-run output before execution, and keep the access key local.

Risk: Live generation and balance-related API calls may consume account credits.

Mitigation: Submit with --execute only after the user has authorized generation, and use balance checks or dry runs when cost or quota is uncertain.

Risk: Secrets could be exposed if copied into chat, request files, command arguments, or logs.

Mitigation: Configure XYQ_ACCESS_KEY in the local environment and avoid placing credentials in user-visible prompts or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ydtincle/skills/xyq-marketing-skill)
- [Marketing API Contract](references/api.md)
- [Product image to marketing video example](examples/product-video.md)
- [Xiaoyunque API page](https://xyq.jianying.com/cli?tab=api)
- [Formal API documentation](https://bytedance.larkoffice.com/docx/CQOYdJNLioLz6fxRzKXcCsKLnJh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, files]

**Output Format:** [Markdown guidance with bash commands, JSON request and response output, and downloaded media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a locally configured XYQ_ACCESS_KEY for live API calls; dry-run preview is available before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
