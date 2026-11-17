## Description:

API账单太贵？6级优化评分体系+7步诊断流程，逐项审计token消耗并量化优化，支持模型路由、预算预测和紧急降本方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent builders, and operations teams use this skill to audit token usage, estimate API costs, compare model-routing options, and produce prioritized cost-reduction plans. It is especially relevant for prompt-heavy, RAG, agent, and batch-call workflows where token spend needs quantified optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a dated model-price table from June 2026, so budget estimates may become inaccurate as provider pricing changes.

Mitigation: Verify current model prices before relying on generated cost comparisons, forecasts, or savings estimates.

Risk: Broad cost-optimization triggers may activate during nearby model-selection or budget discussions.

Mitigation: Review whether the user is asking for token-cost optimization before applying its recommendations.

Risk: Optimization advice can reduce cost at the expense of output quality or task coverage.

Mitigation: Use the artifact's stated A/B validation and quality-check constraint before adopting aggressive reductions.

## Reference(s):

- [Token消耗优化器 - 详细参考 v1.3.0](artifact/references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougitcom-token-optimizer)
- [Publisher profile](https://clawhub.ai/user/qqyougitcom)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Chinese Markdown with tables, checklists, estimates, and occasional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include model cost comparisons, budget forecasts, optimization priorities, ROI estimates, and emergency cost-reduction steps.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
