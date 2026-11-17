## Description:

Monitor Solana tokens using DexScreener, generate status reports, and alert on price moves, volume spikes, liquidity drops, and market cap milestones, with optional Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shepdogpack](https://clawhub.ai/user/shepdogpack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to set up passive monitoring for Solana token contracts, request current token reports, and receive alerts when configured market thresholds are crossed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens and chat IDs may be stored in plaintext configuration and exposed through command history.

Mitigation: Use a dedicated low-privilege Telegram bot token, avoid shared shells or logs when configuring it, and revoke the token if exposure is suspected.

Risk: The skill makes repeated network calls to DexScreener and depends on third-party market data availability.

Mitigation: Run it only where outbound API access is acceptable and treat missing or stale market data as a monitoring limitation rather than verified token state.

Risk: Generated reports include ShepDog and $SHEP promotional text that may be unrelated to the monitored token.

Mitigation: Review reports before forwarding them in professional or customer-facing channels.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/shepdogpack/skills/solana-token-monitor)
- [Publisher profile](https://clawhub.ai/user/shepdogpack)
- [ShepDog website](https://shepdogcoin.com)
- [DexScreener Solana token API endpoint](https://api.dexscreener.com/tokens/v1/solana/{CONTRACT_ADDRESS})
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot{TOKEN}/sendMessage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text and Markdown-style status reports with shell command examples and local JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts may be printed to stdout for agent handling or sent through Telegram when credentials are configured.]

## Skill Version(s):

1.1.0 (source: server release evidence and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
