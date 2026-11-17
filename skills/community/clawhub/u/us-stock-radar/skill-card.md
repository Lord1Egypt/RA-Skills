## Description:

Professional US stock radar for screening, deep dives, and watchlist alerts using public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spyfree](https://clawhub.ai/user/spyfree)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen US equities, run ticker deep dives, and monitor watchlists with heuristic signal grades, confidence, timestamps, and data-gap caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public web requests to market-data providers, so data may be delayed, unavailable, rate-limited, or incomplete.

Mitigation: Review availability, data_gaps, degraded_mode, confidence, and timestamps before relying on any output.

Risk: Signal grades are heuristic market analysis and can be mistaken for investment advice or trade recommendations.

Mitigation: Treat grades as triage signals only; do not connect the skill to brokerage credentials, trading systems, or portfolio mutation workflows.

## Reference(s):

- [Metrics Reference](references/metrics.md)
- [US Stock Radar ClawHub page](https://clawhub.ai/spyfree/skills/us-stock-radar)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown narrative with optional JSON payloads from the skill script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes as_of_utc, mode, event_mode, availability, data_gaps, degraded_mode, confidence, sources, and heuristic caveats.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
