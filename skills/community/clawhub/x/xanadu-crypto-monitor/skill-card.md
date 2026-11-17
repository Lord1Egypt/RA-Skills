## Description:

Provides CLI workflows for cryptocurrency prices, price alerts, on-chain market metrics, and portfolio tracking, with whale tracking noted as requiring additional blockchain API support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saintlittlefish](https://clawhub.ai/user/saintlittlefish)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run crypto market-monitoring commands, configure local alerts, review market and on-chain metrics, and track simple portfolio holdings from public APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a billing module with an exposed SkillPay key and weak user-control boundaries.

Mitigation: Remove or fix the billing files before use, rotate the exposed key, and require explicit user confirmation plus server-side authorization before any charge.

Risk: Alerts and portfolio holdings are stored locally, which can reveal user trading interests or holdings on a shared system.

Mitigation: Document the local storage path and advise users to protect, inspect, or delete ~/.openclaw/crypto-monitor data according to their privacy requirements.

Risk: Market and on-chain outputs depend on public API availability and may be delayed, incomplete, or unavailable under rate limits.

Mitigation: Treat outputs as informational monitoring data and verify important trading or operational decisions against trusted sources.

## Reference(s):

- [Xanadu Crypto Monitor on ClawHub](https://clawhub.ai/saintlittlefish/skills/xanadu-crypto-monitor)
- [CoinGecko API](https://api.coingecko.com/api/v3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON alert and portfolio files under ~/.openclaw/crypto-monitor when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
