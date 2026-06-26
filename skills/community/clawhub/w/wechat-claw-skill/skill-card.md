## Description: <br>
微信公众号文章全自动写作与发布。从信息搜集、AI配图规划、报刊级 HTML 排版、到草稿创建和发布的完整流程。适用于 AI 日报、财经周报、深度分析、新闻资讯类文章。内置多种模板，并提供本地渲染、校验、图片规划和发布流水线脚本。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[th3ee9ine](https://clawhub.ai/user/th3ee9ine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to turn structured article JSON and source bundles into WeChat-ready HTML, image plans, validation results, drafts, and optional publishing actions. It is intended for AI daily briefings, financial reviews, deep analysis, product releases, industry radar, and breaking-news article workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendered articles or generated drafts may contain inaccurate, unsuitable, or policy-sensitive content. <br>
Mitigation: Inspect the rendered HTML and WeChat draft before creating or publishing any live article. <br>
Risk: The optional pipeline can delegate image generation, search, upload, draft creation, and publishing to separate helper skills or scripts. <br>
Mitigation: Review those helper skills or scripts separately, start with --dry-run, and enable --create-draft or --publish only after confirming the target account and content. <br>
Risk: Images and article text may create copyright, attribution, or account-compliance issues. <br>
Mitigation: Verify source rights, image rights, captions, and WeChat CDN image handling before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/th3ee9ine/wechat-claw-skill) <br>
- [README](README.md) <br>
- [English documentation](docs/README.en.md) <br>
- [OpenClaw integration guide](docs/openclaw.en.md) <br>
- [Writing guide](references/writing-guide.md) <br>
- [Title formulas](references/title-formulas.md) <br>
- [Image prompts](references/image-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON article structures, bash commands, and generated HTML or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can render and validate WeChat article HTML, plan image prompts, collect source bundles, and optionally delegate image generation and WeChat draft or publish actions to separate helper scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact/SKILL.md frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
