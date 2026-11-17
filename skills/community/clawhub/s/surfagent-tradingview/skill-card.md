## Description:

TradingView platform skill for SurfAgent, covering chart workflows, proof rules, blockers, and when to use the TradingView adapter over generic browser control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surfagentapp](https://clawhub.ai/user/surfagentapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agents through TradingView chart inspection, market data reads, indicator checks, alerts, drawings, Pine editor workflows, and proof-backed chart changes through SurfAgent adapter workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-directed TradingView workflows may change watchlists, alerts, drawings, or Pine editor state when the user requests those actions.

Mitigation: Review requested changes and require adapter state, data, or screenshot proof before treating a TradingView task as complete.

Risk: Chart or technical-analysis claims can be misleading if they are based only on navigation, clicks, or an unverified rendered chart.

Mitigation: Use the skill's proof standard: verify chart state with adapter reads, verify market or indicator data with adapter data outputs, and capture visual proof when the task is visual.

## Reference(s):

- [SurfAgent homepage](https://surfagent.app)
- [ClawHub skill page](https://clawhub.ai/surfagentapp/skills/surfagent-tradingview)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown skill instructions with workflow checklists and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TradingView adapter availability for the referenced tv_* workflows and emphasizes state, data, or visual proof before completion claims.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
