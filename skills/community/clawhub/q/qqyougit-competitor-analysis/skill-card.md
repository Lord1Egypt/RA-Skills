## Description:

帮助用户基于公开信息拆解竞品定位、功能差异、定价策略和用户口碑，并输出结构化竞品分析报告、定位图谱、SWOT交叉策略和行动路线图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business, product, and strategy teams use this skill to perform public-source competitor analysis across positioning, features, pricing, user sentiment, SWOT strategy, and roadmap recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Competitor data can become stale or incomplete, especially pricing, product features, market share, and user sentiment.

Mitigation: Use public web research for current data, cite sources, include a data cutoff date, and label unsupported findings as unverified.

Risk: Users may include confidential strategy, customer data, or non-public business information in the analysis prompt.

Mitigation: Avoid sharing confidential or non-public business information unless it is intended to be used in the generated analysis.

Risk: Competitive recommendations may be misleading if based on too few competitors or narrow feedback channels.

Mitigation: Cover direct, indirect, and potential competitors when possible, and use multiple public feedback channels before drawing strategy conclusions.

## Reference(s):

- [competitor-analysis detailed reference](artifact/references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougit-competitor-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured as a competitor analysis report with tables, matrices, SWOT strategy, positioning map, and roadmap sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese output by default; analysis should cite public sources and include a data cutoff date.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
