## Description:

Reviews the current A-share market by combining index performance, sector heatmaps, limit-up and limit-down activity, style rotation, and market temperature into a structured market analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agent operators use this skill to generate a same-day, multi-dimensional review of the A-share market. It is intended for broad market recap reports, not individual stock deep dives or bond, fund, futures, or foreign-exchange analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly instructs agents to run the latest npm version of daxiapi-cli during use.

Mitigation: Pin and review a trusted daxiapi-cli version before operational use instead of relying on @latest.

Risk: API token setup examples may expose secrets if tokens are pasted directly into shell commands or retained in logs.

Mitigation: Use a secret store, hidden input, or carefully scoped environment variable, and avoid sharing terminal history or logs that may contain tokens.

Risk: Market recap output may be mistaken for personalized investment advice.

Mitigation: Keep conclusions data-grounded and neutral, preserve the disclaimer and risk warnings, and avoid deterministic predictions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-market-review)
- [Daxiapi data service](https://daxiapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown market-review report with tables, concise analysis, cited data-source commands, risk notices, and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to use daxiapi CLI data and to include data timing, risk warnings, and a disclaimer in generated reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
