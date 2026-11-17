## Description:

Fetches Upbit market data through CLI commands for trading pairs, candles, recent trades, tickers, orderbooks, and watchlist tickers with JSON responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuns9](https://clawhub.ai/user/kuns9)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve Upbit quotation data for market monitoring, reporting, and workflows that need pairs, candles, trades, tickers, orderbooks, or configured watchlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because it asks users to configure exchange API secrets and includes dormant authentication code for public-only market-data commands.

Mitigation: Review before installing, keep Upbit accessKey and secretKey blank unless audited private API support is required, and do not use trading or withdrawal-capable exchange keys in the JSON config.

Risk: The security guidance recommends a version with unused auth code removed and dependencies pinned with a committed lockfile.

Mitigation: Prefer a release that removes dormant authentication behavior and includes pinned dependency artifacts before using it in higher-trust environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kuns9/skills/upbit-market-data-skill)
- [Upbit REST API Guide](https://docs.upbit.com/kr/reference/rest-api-guide)
- [Upbit Authentication Reference](https://docs.upbit.com/kr/reference/auth)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON responses from a Node.js CLI, with command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Success responses are written to stdout as {"ok": true, "result": ...}; errors are written to stderr as {"ok": false, "error": ...} with exit code 1.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact package.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
