## Description:

微信公众号内容创作与改写技能。用于公众号选题、标题优化、正文写作、重写润色、公众号排版、封面图提示词生成。适用于需要“更像真人写作”的场景：口语化表达、故事化结构、观点明确、可读性强；也适用于把已有素材整理为可发布的公众号文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyc0616c-oss](https://clawhub.ai/user/dyc0616c-oss)

### License/Terms of Use:


## Use Case:

External content creators and account operators use this skill to draft, rewrite, polish, format, and title WeChat public-account articles in a conversational Chinese style, including publishing-ready layout text and cover-image prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated articles may include ChainThink branding, crypto-focused risk text, a WeChat group invitation, QR-code placement, and an external ChainThink link by default.

Mitigation: Review and edit publishing-ready output before posting so branding, calls to action, QR placement, and external links match the account owner, audience, and publication policy.

Risk: The security verdict is suspicious because promotional material can be inserted without clear user opt-in.

Mitigation: Install and use the skill only when that promotion is intended; otherwise remove or override the fixed promotional sections before publication.

Risk: The skill can produce opinionated market or crypto commentary that readers may interpret as advice.

Mitigation: Fact-check claims, preserve appropriate risk disclaimers, avoid unsupported performance claims, and confirm that generated commentary reflects the publisher's editorial standards.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyc0616c-oss/skills/wechat-article-crayon)
- [Style fingerprint](references/style-fingerprint.md)
- [Title patterns](references/title-patterns.md)
- [Opening and ending library](references/opening-ending-library.md)
- [Banned phrases](references/banned-phrases.md)
- [ChainThink news link referenced by the skill](https://www.chainthink.cn/news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with article drafts, formatted publishing text, cover-image prompts, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese-language article variants, title candidates, outlines, summaries, social snippets, calls to action, QR-code placement guidance, and externally linked promotional text.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
