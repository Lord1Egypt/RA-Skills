## Description:

Provides structured cryptocurrency token research for EVM chains including Base, Ethereum, Arbitrum, and Solana, with deep-research, shallow-screening, and monitoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xartex](https://clawhub.ai/user/0xartex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to collect token fundamentals, market data, holder information, security signals, and social context for cryptocurrency research reports and watchlists. It supports quick screening and deeper due diligence, but its outputs should be reviewed before any financial decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make external token-research API calls and write local research files.

Mitigation: Install only when that network and file-writing behavior is acceptable, and review generated files before relying on them.

Risk: The skill includes a call and direct-message workflow and references an external ape-call.sh script for WATCH or APE tokens.

Mitigation: Do not allow notification workflows or the external script unless they are explicitly configured and approved.

Risk: Automated token research can produce incomplete or misleading investment signals.

Mitigation: Treat results as research assistance, cross-check critical facts, and require human review before any trading or investment action.

## Reference(s):

- [Token Research ClawHub Listing](https://clawhub.ai/0xartex/skills/token-research)
- [README](artifact/README.md)
- [API Reference](artifact/api_reference.md)
- [Usage Examples](artifact/example_usage.md)
- [DexScreener Token API](https://api.dexscreener.com/latest/dex/tokens/CHAIN/TOKEN_ADDRESS)
- [GoPlus Token Security API](https://api.gopluslabs.io/api/v1/token_security/CHAIN_ID?contract_addresses=TOKEN_ADDRESS)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and watchlist entries, with shell commands and JSON API data when the helper script is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local research directories, JSON data files, summaries, reports, and monthly watchlist entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
