## Description:

SaaS辅助决策助手 helps users assess SaaS product ideas across market demand, user profile, pain points, competition, monetization, acquisition, marketing, cost, and technical feasibility, then produces an interactive HTML feasibility report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Product founders, product managers, and SaaS teams use this skill to research and score a SaaS product concept, then generate a feasibility report for MVP, pricing, acquisition, architecture, and go-to-market decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may include user-provided or web-sourced text that is not escaped by the report generator.

Mitigation: Treat generated reports as untrusted files and open them in a constrained browser context until HTML escaping is added.

Risk: The skill requests broad read, write, edit, shell, web search, and web fetch capabilities without clear output-path limits.

Mitigation: Run it in a scoped workspace, set explicit output paths, and review shell and file-write actions before execution.

Risk: Market, pricing, MRR, ARR, LTV, CAC, and competitor conclusions are based on public sources and benchmark estimates that may be incomplete or stale.

Mitigation: Validate generated recommendations with current sources, customer interviews, and first-party financial assumptions before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/saas-decision)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, code, shell commands, HTML files, guidance]

**Output Format:** [Single-file responsive HTML report with supporting analysis text and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web research and benchmark-style estimates; generated reports should be reviewed before relying on product, market, or financial conclusions.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
