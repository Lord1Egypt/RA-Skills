## Description:

US stock and crypto trading via Alpaca API. Paper trading (simulated) and real trading supported. Real-time quotes, orders, positions, RSI strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Alpaca account data, retrieve stock and crypto market data, and prepare or execute Alpaca orders through command-line scripts. The skill supports paper trading by default but can operate against live trading endpoints when configured with live credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real stock or crypto orders when configured with live Alpaca credentials.

Mitigation: Use paper-trading credentials by default, require explicit user confirmation for each order, and audit the scripts before enabling live trading.

Risk: Underdocumented aggressive and momentum strategy scripts can place automated trades.

Mitigation: Do not run strategy scripts with live credentials unless they have been reviewed, modified to require confirmation, and constrained by clear position and loss limits.

Risk: Brokerage credentials are loaded from environment variables or per-user JSON files.

Mitigation: Validate credential paths, restrict file access to the intended user, and keep API keys out of logs, shared prompts, and committed files.

Risk: Configuration can switch from paper trading to live trading by changing the Alpaca base URL.

Mitigation: Require a separate live-mode opt-in and endpoint allowlist before allowing requests to live trading endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/storyclaw-alpaca-trading)
- [ClawHub publisher profile](https://clawhub.ai/user/patches429)
- [Alpaca paper trading API endpoint](https://paper-api.alpaca.markets)
- [Alpaca live trading API endpoint](https://api.alpaca.markets)
- [Alpaca market data API endpoint](https://data.alpaca.markets)
- [Alpaca account setup](https://app.alpaca.markets/brokerage/new-account)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Alpaca API credentials; output may include account, position, order, quote, bar, RSI, and strategy status information.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
