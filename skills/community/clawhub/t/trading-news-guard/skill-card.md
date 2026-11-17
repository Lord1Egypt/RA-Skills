## Description:

Provides agents with trading-news blackout awareness for high-impact events such as NFP, CPI, FOMC, and ECB so they can decide whether to enter a trade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-agent operators use this skill to add a pre-entry reminder for high-impact market news blackout windows. The skill supplies status-oriented guidance; the agent remains responsible for deciding whether to skip or place a trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is documentation-only and should not be treated as a functioning trading safety control by itself.

Mitigation: Confirm the actual news data source and freshness before using the skill in any live or automated trading flow.

Risk: The artifact wording is inconsistent about whether the check is local-only or API-backed.

Mitigation: Configure the trading agent to fail closed and skip trading whenever news status cannot be verified.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with JSON and Python-style pseudocode examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable code is included in the artifact.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
