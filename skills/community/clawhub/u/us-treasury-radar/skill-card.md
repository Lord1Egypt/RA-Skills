## Description:

Provides a US Treasury debt and foreign-holdings risk report that combines TreasuryDirect data with estimated TIC-style demand indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai157isme-lgtm](https://clawhub.ai/user/kai157isme-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance-focused agent users use this skill to generate an indicative US Treasury supply-and-demand report with risk signals. The report is suitable for monitoring and discussion, not as authoritative financial data or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The financial report can present hard-coded or estimated market data as a live monitoring signal.

Mitigation: Verify TreasuryDirect and TIC figures independently before using the output for financial analysis or investment decisions.

Risk: The skill may trigger on broad finance-related phrases and outputs Chinese text.

Mitigation: Deploy it where Chinese-language financial reporting is expected and constrain invocation triggers if broad finance prompts would be inappropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kai157isme-lgtm/skills/us-treasury-radar)
- [TreasuryDirect current debt API](https://www.treasurydirect.gov/NP_WS/debt/current)
- [TreasuryDirect federal securities holdings API](https://www.treasurydirect.gov/NP_WS/feddata/current)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese text report with tabular console output and risk-signal commentary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live API-derived values when available and fallback or estimated values for some holdings data. Treat outputs as indicative and verify financial figures independently.]

## Skill Version(s):

4.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
