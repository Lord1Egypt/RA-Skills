## Description:

Wall Street Quant Team is a multi-agent quantitative investment analysis skill for stock research, trend analysis, behavior-finance review, risk assessment, and AI-assisted strategy development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate specialist agent roles for investment research, stock and market analysis, quantitative strategy exploration, and risk review. It produces analysis-oriented outputs and should be controlled carefully before any connection to brokerage, account, automation, file, or external-skill tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment-analysis outputs could be mistaken for trade instructions or used with brokerage, account, automation, or file tools.

Mitigation: Treat the skill as analysis-only unless explicit controls prohibit live orders, require per-action confirmation, and redact logs and traces.

Risk: External advisor skills could add unverified behavior or advice.

Mitigation: Load only reviewed advisor skills and require explicit user confirmation before using them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/e2e5g/skills/wall-street-quant-team)
- [Investment Analysis Guide](references/investment-analysis-guide.md)
- [Workflow Orchestration Guide](references/workflow-orchestration.md)
- [Stock Data Usage Guide](references/stock-data-usage.md)
- [Trend Analysis Guide](references/trend-analysis.md)
- [AI Quant Guide](references/ai-quant-guide.md)
- [Behavior Finance Guide](references/behavior-finance.md)
- [Advisor Invitation Guide](references/advisor-invitation.md)
- [Cost Control Strategy](references/cost-control.md)
- [Monitoring System Guide](references/monitoring-system.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown investment-analysis reports and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk notices and analysis-only recommendations; no live trade execution is evidenced.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
