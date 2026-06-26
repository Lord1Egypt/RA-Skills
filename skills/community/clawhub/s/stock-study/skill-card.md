## Description: <br>
Senior equity research analysis for single tickers, including company overview, Wall Street consensus, institutional activity, and analyst upgrades or downgrades with source-dated metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickzhou](https://clawhub.ai/user/rickzhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to structure single-stock equity research into company overview, consensus, analyst action, and institutional-activity sections with cited market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial metrics or market data may be unavailable, stale, or unsupported by the agent environment. <br>
Mitigation: Confirm each cited metric has a real source and date, flag stale data clearly, and do not assume premium data access such as Bloomberg or FactSet unless the environment provides it. <br>
Risk: Generated equity research could be mistaken for authoritative financial advice. <br>
Mitigation: Use the output as a research template and verify conclusions against current, authoritative financial sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rickzhou/stock-study) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with headers, citations, and tables for quantitative data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires source and date for each metric, flags data older than 30 days, and should not fabricate unavailable numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
