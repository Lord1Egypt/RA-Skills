## Description:

调用优稿检测服务分析文章 AI 特征，并交付三类占比、送检原文与分段报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

创作者、编辑和需要评估文章 AI 特征的用户可提交完整文章，查看人工特征、疑似 AI、AI 特征占比及分段报告，并导出检测文件。结果是模型分析参考，不能证明作者身份或原创性。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted articles are sent to Yougao for analysis, and local exports retain their full text.

Mitigation: Submit only text approved for that service, and protect exported reports like the original article.

Risk: A reused account connection may incur charges; live service permission enforcement was not tested by this review.

Mitigation: Use a detection-only key with an appropriate spending limit, and confirm its scope before submitting an article.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dunkong/skills/yougao-detect)
- [优稿 AI 与 API 接入指南](https://yougao.top/ai.md)
- [优稿 API contract](https://yougao.top/api/v1/openapi.json)
- [共用运行指南](references/client.md)
- [API 手册](references/api.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, Text]

**Output Format:** [HTML delivery page and plain-text detection report, with a text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes three feature ratios and segmented findings where available; each report corresponds to the submitted text version.]

## Skill Version(s):

1.4.0 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
