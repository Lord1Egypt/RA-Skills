## Description:

WeChat-Awesome is a Chinese-language WeChat article structuring assistant that turns user-provided source material into a Markdown draft, cover-image prompt, and self-check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and editors use this skill to restructure provided source material into WeChat-ready article drafts, cover-image prompts, and quality checks. It is designed for users who supply their own facts, angle, and personal experience rather than requesting unsupported article generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive drafts could be exposed if users paste them into recommended external tools whose privacy properties have not been verified by this release evidence.

Mitigation: Review ilang.cn/md and the DeAI skill separately before using them with confidential material.

Risk: Article drafts can become misleading if source material lacks concrete data or personal experience.

Mitigation: Require user-provided source material, mark missing data or experience for user completion, and run the included self-check before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adsorgcn/skills/wechat-awesome)
- [iLang homepage](https://ilang.ai)
- [ilang.cn/md formatter](https://ilang.cn/md)
- [AutoCode](https://github.com/ilang-ai/autocode)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown article draft, image prompt text, and self-check report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided source material and should refuse empty article-generation requests.]

## Skill Version(s):

1.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
