## Description:

网站开发辅助决策系统会根据产品类型和名称，分析竞品、市场、流量、用户、商业模式、成本和推广策略，并生成多维度可行性评估 HTML 报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and product teams use this skill to evaluate whether a proposed website is worth building and to produce a feasibility report with scoring, cost, promotion, risk, and technical recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted content that can execute as active HTML or JavaScript.

Mitigation: Avoid opening reports made from untrusted inputs, do not host generated reports under an authenticated site, and require HTML escaping for all dynamic fields before treating the skill as low risk.

Risk: The skill relies on web search results and public estimates that may be incomplete or stale.

Mitigation: Review cited market, traffic, and competitor assumptions before using the report for investment or launch decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/website-decision)
- [Project homepage from ClawHub metadata](https://github.com/bettermen/website-decision)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash and Python examples, plus generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a local HTML feasibility report from structured analysis inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
