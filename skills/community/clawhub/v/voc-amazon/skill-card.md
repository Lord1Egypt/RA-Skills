## Description:

通过 ARI 分析 Amazon 商品评论，生成 VOC 洞察、趋势和运营建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product operators use this skill to collect and analyze product reviews, identify customer pain points and buying motivations, and create VOC reports with trend and listing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview requests may spend credits, and unanswered requests may resume without fresh approval.

Mitigation: Enable and verify ask-before-every-charge, use the dedicated quote command for price checks, and approve recurring monitoring costs separately. Do not rely on omitting --confirm to prevent charges.

## Reference(s):

- [ARI CLI and API Reference](references/reference.md)
- [VOC洞察Amazon on ClawHub](https://clawhub.ai/funewa/skills/voc-amazon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown reports and concise conversational summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-backed insights with sample and time-window caveats; reports may cover pain points, buying motivations, user profiles, trends, and listing recommendations.]

## Skill Version(s):

1.5.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
