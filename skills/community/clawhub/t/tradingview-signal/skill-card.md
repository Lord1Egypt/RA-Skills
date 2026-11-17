## Description:

Parse TradingView trading signal text into structured trade details and risk/reward analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanuei](https://clawhub.ai/user/sanuei)

### License/Terms of Use:

ISC

## Use Case:

Developers and trading-tool users can pass signal text to extract symbol, direction, entry price, stop loss, take profit, and risk/reward. Use caution with URL-only inputs because server security evidence says advertised URL parsing is billable but nonfunctional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger external billing calls and charge users before parsing a signal.

Mitigation: Confirm user consent, billing expectations, and failure handling before deployment.

Risk: Server security evidence reports an exposed billing API key in the package.

Mitigation: Rotate the key, remove packaged secrets, and require runtime secret injection before use.

Risk: Advertised TradingView URL support appears billable but nonfunctional.

Mitigation: Disable or fix URL-only input before charging users for that path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanuei/skills/tradingview-signal)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON-like object with parsed trade fields, risk/reward rating, timestamp, billing balance, and recommendation text when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [URL-only input returns a note rather than parsed trade details; successful execution includes remaining billing balance.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
