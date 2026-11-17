## Description:

Enables agents to use the XXYY Open API for on-chain token trading, token launches, wallet checks, PNL queries, token scans, and market data queries on Solana, Ethereum, BSC, and Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmy-holiday](https://clawhub.ai/user/jimmy-holiday)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to prepare and execute XXYY Open API calls for crypto trading, wallet inspection, token discovery, token launch, trade status, PNL, and market intelligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The XXYY API key can authorize wallet-funded trading actions.

Mitigation: Install only when wallet-spending access is intended; keep the key out of logs and public channels, rotate it after suspected exposure, and manually verify wallet, chain, amount, fees, and launch parameters before any transaction.

Risk: The same API key is used for both read and trading workflows, with no separate read-only mode documented.

Mitigation: Treat all use as transaction-capable access and apply XXYY IP allowlisting where available.

Risk: A configurable API destination can redirect credential-bearing requests away from the default XXYY host.

Mitigation: Keep XXYY_API_BASE_URL unset unless the destination is fully trusted and controlled.

## Reference(s):

- [XXYY homepage](https://www.xxyy.io)
- [XXYY API key management](https://www.xxyy.io/apikey)
- [ClawHub skill page](https://clawhub.ai/jimmy-holiday/skills/xxyy-trade-skill)
- [Publisher profile](https://clawhub.ai/user/jimmy-holiday)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XXYY_API_KEY and curl; may use XXYY_API_BASE_URL when explicitly trusted.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
