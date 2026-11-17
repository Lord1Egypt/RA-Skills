## Description:

Interact with the Kraken cryptocurrency exchange for spot and futures market data, account information, order management, and WebSocket streams through the tentactl binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askbeka](https://clawhub.ai/user/askbeka)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and trading operators use this skill to inspect Kraken market data, review account state, stream live data, and prepare or execute spot and futures trading actions. Authenticated account and trading workflows require Kraken API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated tools can place, cancel, transfer, or withdraw real funds when API keys have those permissions.

Mitigation: Use read-only Kraken API keys unless trading is required, avoid withdrawal or transfer permissions, dry-run orders with validate=true where supported, and require explicit manual approval before live trading actions.

Risk: The install path uses an unpinned tentactl binary, which can change behavior across versions.

Mitigation: Pin and verify the tentactl version or release artifact before deployment and review changes before upgrading.

Risk: Long-lived Kraken credentials may be stored in ~/.tentactl.env.

Mitigation: Prefer a credential manager or short-lived secrets where possible, restrict file permissions, rotate keys, and remove credentials when the skill is no longer needed.

Risk: Recurring automation examples can repeatedly trigger trading decisions.

Mitigation: Require explicit limits, expiry, monitoring, and manual approval controls before enabling recurring trading workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/askbeka/skills/tentactl)
- [Tools Reference](references/tools.md)
- [tentactl Source](https://github.com/askbeka/tentactl)
- [tentactl Releases](https://github.com/askbeka/tentactl/releases)
- [Kraken API Key Management](https://www.kraken.com/u/security/api)
- [Kraken](https://www.kraken.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Kraken market, account, trading, and WebSocket tools through tentactl; authenticated workflows depend on local Kraken credentials.]

## Skill Version(s):

0.3.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
