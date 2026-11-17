## Description:

用优稿专用改写服务降低文章模板化和 AI 特征，保留事实、数字、名称与核心原意。适用于降 AI 率、自然化表达、保留文风改写；可按授权串联真实检测，不承诺固定分数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要改写中文文章的用户及其 AI 助手，用于通过优稿服务生成保留核心原意的候选稿、核对事实与引用，并交付可继续编辑的稿件。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preparing a price quote sends the article text to Yougao, even if execution is not approved.

Mitigation: Submit only text authorized for Yougao to receive; use a key limited to rewriting, add detection permission only when needed, and set a spending limit.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/yougao-rewrite)
- [Yougao API documentation](https://yougao.top/ai.md)
- [API reference](artifact/references/api.md)
- [Assistant run guide](artifact/references/client.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [Markdown article candidate with a brief change summary and web editing link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the original, checks facts and attribution, and does not promise a fixed AI-detection score; detection is a separate task.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
