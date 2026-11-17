## Description:

Manage a stock and crypto watchlist with target and stop alerts using live AISA price checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a stock and crypto watchlist, set target, stop, and signal alerts, and run live AISA-backed checks from a Python command-line client. The generated BUY/HOLD/SELL signals are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_BASE_URL can route the AISA API key and watchlist tickers to a non-AISA endpoint.

Mitigation: Run with AISA_BASE_URL unset or set only to an explicitly trusted endpoint, and treat the AISA API key as a credential with possible billing or account impact.

Risk: Watchlist tickers are sent to the configured AISA endpoint during live checks.

Mitigation: Use the skill only where sharing the selected ticker symbols with the configured endpoint is acceptable.

Risk: Generated BUY/HOLD/SELL signals may be incomplete or inaccurate.

Mitigation: Treat generated signals as informational support rather than financial advice or automated trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/stock-watchlist-aisa-api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY. Watchlist state is stored locally unless CLAWDBOT_STATE_DIR is set.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
