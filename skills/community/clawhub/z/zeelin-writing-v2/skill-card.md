## Description:

自媒体写作助手，提供完整的10步创作流程：需求分析→知识搜索→选题讨论→风格学习→创作初稿→三遍审校(降AI味)→封面配图→HTML排版→发布草稿箱→归档，支持公众号、小红书、视频逐字稿多平台内容创作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese self-media creators and marketing teams use this skill to plan, draft, revise, format, and archive articles or scripts for WeChat Official Accounts, Xiaohongshu, and video transcripts. It also supports brief creation, topic selection, style adaptation, cover-image workflow guidance, HTML conversion, and optional publishing preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can over-automate local reading, draft creation, and publishing preparation.

Mitigation: Review requested file access and require a separate confirmation before publishing drafts or using platform credentials.

Risk: Setup instructions may store API keys persistently in shell startup files or local configuration.

Mitigation: Use restricted, manually managed API keys and avoid storing secrets in shell startup files.

Risk: The bundled brand persona may steer content toward a specific commercial voice and call to action.

Mitigation: Use the persona only when that voice is intended, and review drafts for brand, accuracy, and platform-policy fit before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-writing-v2)
- [Reference document index](references/README.md)
- [Brief template](references/brief-template.md)
- [Brand persona](references/用户人设.md)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with file paths, shell commands, generated article drafts, brief documents, HTML conversion output, and JSON manifests from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local project folders, Markdown files, HTML files, image assets, and draft publishing artifacts when the user authorizes those workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
