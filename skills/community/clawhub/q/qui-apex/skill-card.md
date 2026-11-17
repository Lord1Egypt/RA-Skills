## Description:

Trade and monitor ApeX perpetual futures. Check balances, view positions with P&L, place/cancel orders, execute market trades, or submit trade reward enrollments. Use when the user asks about ApeX trading, portfolio status, crypto positions, activity enrollments, or wants to execute trades on ApeX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Apex to monitor ApeX perpetual futures portfolios, analyze market momentum, and prepare or execute ApeX orders through agent-guided shell commands. Because it can place or cancel real trades, users should treat agent outputs as proposals and confirm trading actions explicitly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel live ApeX perpetual futures orders when credentials are provided.

Mitigation: Use testnet first and require explicit user confirmation before any trade, close, cancel, reward enrollment, or reward submission.

Risk: The skill handles ApeX API credentials, an Omni seed, and sensitive account data.

Mitigation: Use the least-privileged ApeX API key possible, never reuse the Omni seed elsewhere, and protect or remove any generated trading-state.json file.

Risk: Generated market signals may be incorrect, stale, or incomplete.

Mitigation: Treat market signals as informational only and independently review price, position size, and account exposure before acting.

## Reference(s):

- [ApeX Omni API Reference](artifact/references/api.md)
- [ApeX Omni mainnet API](https://omni.apex.exchange)
- [ApeX Omni testnet API](https://qa.omni.apex.exchange)
- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/qui-apex)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from CLI commands plus Markdown guidance for chat presentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market analysis, portfolio summaries, order details, and command suggestions; trading commands require ApeX credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
