## Description:

Integrate OpenClaw with Xerolite - IBKR. Use when: querying Xerolite API, placing orders, searching contracts, fetching portfolio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xero-flex](https://clawhub.ai/user/xero-flex)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to let an OpenClaw agent call the Xerolite REST API for order placement, contract search, and portfolio inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live order commands can execute trades through a connected Interactive Brokers account.

Mitigation: Require human confirmation or a paper-trading workflow before any live order command.

Risk: A Xerolite agentic API key can authorize trading endpoints.

Mitigation: Use a tightly scoped credential, prefer environment-variable injection, and avoid passing the key with --api-key where it may enter shell history.

Risk: A custom API URL can direct commands to an unintended or untrusted service.

Mitigation: Use localhost or HTTPS-only trusted endpoints for XEROLITE_API_URL.

## Reference(s):

- [Xerolite REST API Reference](references/API.md)
- [Xerolite product page](https://www.xeroflex.com/xerolite/)
- [TradingView](https://www.tradingview.com/)
- [Interactive Brokers](https://www.interactivebrokers.com/)
- [ClawHub skill page](https://clawhub.ai/xero-flex/skills/xerolite)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and XEROLITE_AGENTIC_API_KEY; command output is the HTTP status and API response body.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
