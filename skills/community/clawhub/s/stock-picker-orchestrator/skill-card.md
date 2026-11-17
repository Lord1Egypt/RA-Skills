## Description:

Acts as a meta-orchestrator that routes stock-analysis requests across data, macro/news, backtesting, earnings quality, valuation, portfolio analytics, and risk skills under explicit budget controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agent builders use this skill to route stock-analysis requests through budget-aware screening, macro/news context, valuation, portfolio analytics, and risk-management workflows. It frames recommendations with assumptions, confidence, gaps, risk flags, and governance status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can draft financial recommendation labels and target weights that may be mistaken for trading authorization.

Mitigation: Treat outputs as research, require human review for decisions, and keep broker execution disabled.

Risk: The skill may coordinate costly or broad data and news collection through dependent skills.

Mitigation: Confirm budgets before deeper runs, reuse cached artifacts, and stop scope expansion when remaining call budget is low.

Risk: Missing or unavailable dependent skills can leave macro, valuation, portfolio, or risk context incomplete.

Mitigation: Report missing modules, carry gaps into the final answer, and cap confidence when required inputs are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/stock-picker-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with structured sections for fetched data, pipeline choice, assumptions, results, confidence, risks, next steps, and governance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are recommendation framing and workflow guidance only; broker execution is disabled.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
