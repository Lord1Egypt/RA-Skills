## Description:

将用户合法提供的真实商品评价整理为可执行的需求洞察：保留原始资料字段，提炼常见诉求、正负反馈主题与详情页补充点，适合中文小店、小说作者和自媒体创作者复盘自有反馈；资料缺少评价文本或关键上下文时明确指出缺口，不编造结论，也不用于公开同款比价或平台评论抓取。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

中文小店经营者、小说作者和自媒体创作者可用它复盘自己有权提供的商品或作品评价，整理可复核的用户诉求、正负反馈和页面补充建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review material may include personal details or information the user is not authorized to share.

Mitigation: Use only reviews the user is authorized to provide and remove personal details before submission.

Risk: Suggested themes or page claims may overstate what the supplied reviews support.

Mitigation: Keep conclusions tied to the provided evidence and verify product claims before using suggestions publicly.

Risk: A passing packaging self-test could be mistaken for proof that qualitative analysis is accurate.

Mitigation: Treat the self-test as a packaging and example check; review analysis quality against authorized real material.

## Reference(s):

- [ClawHub release](https://clawhub.ai/xxjrq/skills/shop-review-miner-cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown report with evidence summaries, tables, and validation questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only supplied review material; reports missing required input and stops analysis when needed.]

## Skill Version(s):

1.0.1 (source: server-resolved release, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
