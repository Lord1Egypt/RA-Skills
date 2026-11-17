## Description:

Trade crypto on Weex exchange through a Telegram bot, enabling agents to check prices, view balances, run DCA strategies, and execute grid trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tesseraeventures](https://clawhub.ai/user/tesseraeventures)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to guide setup and operation of Weex trading through @WEEXonTONbot, including price checks, balance review, DCA strategies, grid strategies, and authenticated Weex API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables live crypto trading through a third-party Telegram bot that can place automated trades.

Mitigation: Review the workflow before use, start with very small trading limits, and monitor active strategies closely.

Risk: The bot asks users to send exchange API credentials to a third-party service.

Mitigation: Use a dedicated API key with withdrawals disabled, never share keys in group chats, and revoke the key immediately if anything seems wrong.

Risk: The artifact claims message deletion and encrypted storage, but those operational security claims are not independently verified by the evidence.

Mitigation: Do not rely on the artifact alone to verify deletion, encryption, or custody behavior; assess the service before connecting real accounts.

## Reference(s):

- [Weex V3 API Reference](references/weex-api.md)
- [Weex API Documentation](https://www.weex.com/en/api)
- [WEEXonTONbot Telegram Bot](https://t.me/WEEXonTONbot)
- [ClawHub Skill Page](https://clawhub.ai/tesseraeventures/skills/weex-trading)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls]

**Output Format:** [Markdown instructions with Telegram bot commands and REST API endpoint details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes live trading setup and credential-handling guidance; no generated files are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
