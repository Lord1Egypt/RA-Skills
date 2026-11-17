## Description:

Chinese-language A-share stock screening guidance that uses volume-price behavior, capital flows, chip structure, margin financing changes, technical patterns, and valuation re-rating signals to identify candidate stocks for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosqu1to3zz](https://clawhub.ai/user/mosqu1to3zz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce Chinese-language A-share screening reports, candidate stock recommendations, stock-specific trading-logic analysis, and chip-structure diagnostics. Outputs should be treated as informational financial analysis, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce stock picks or trading-oriented analysis that users may mistake for personalized financial advice.

Mitigation: Treat outputs as informational only, verify market data independently, and apply qualified human review before making trading decisions.

Risk: Screening quality depends on current market data and the skill's framework can be wrong when market conditions invalidate its assumptions.

Mitigation: Use current, reliable data sources and require the agent to surface uncertainty, conflicting signals, and risk notes in recommendations.

## Reference(s):

- [Datang Power case study](references/case-study-datang.md)
- [Ganfeng Lithium case study](references/case-study-ganfeng.md)
- [Stock screening reference](references/stock-screening.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown reports with scored tables, narrative analysis, risk notes, and optional shell command prompts for scheduled screening.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language financial screening content focused on A-share market candidates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
