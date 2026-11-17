## Description:

Scans TRON tokens and TRX for supply, market cap, price, ratings, launch time, holders, supply changes, and related token due diligence signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to query TronScan MCP for TRON token due diligence, TRX market metrics, holder analysis, and token supply checks from token names or contract addresses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet address and holder lookups can expose public-chain balances, transfers, counterparties, and behavior patterns.

Mitigation: Use address-level history, holder analysis, or wallet profiling only when that public-chain exposure is intended.

Risk: Token safety or authenticity conclusions can be misleading if based on a single token field.

Mitigation: Combine TronScan risk, project tag, display eligibility, holder distribution, and provenance signals before presenting a safety judgment.

## Reference(s):

- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan Developer API](https://tronscan.org/#/developer/api)
- [ClawHub Skill Page](https://clawhub.ai/sshnii/skills/tronscan-token-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown or plain text summaries with structured token metrics and risk notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public token, holder, transfer, and wallet analytics sourced from TronScan MCP.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
