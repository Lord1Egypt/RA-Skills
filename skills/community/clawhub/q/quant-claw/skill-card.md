## Description:

LLM-driven crypto perpetual futures trading on Bybit. Analyzes 200+ market features across 8 timeframes with strategy-aware output, then you decide whether to trade. Supports DEMO and LIVE modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natanhoffmann](https://clawhub.ai/user/natanhoffmann)

### License/Terms of Use:

Proprietary - purchase required for full access

## Use Case:

External developers and crypto traders use QuantClaw to analyze Bybit perpetual futures with strategy-aware market features and then decide whether to place demo or live trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can interact with Bybit API keys and place live crypto perpetual futures trades.

Mitigation: Start with Bybit demo or testnet keys, keep withdrawal permissions disabled, and use live keys only after explicitly choosing live trading.

Risk: The reviewed artifact is a stub and the paid QuantClaw CLI source was not included in the artifact review.

Mitigation: Inspect the purchased source, verify the provided SHA256 checksum, and run it in an isolated environment before supplying credentials.

Risk: Financial market analysis and strategy output may be incorrect or unsuitable for the user's account risk.

Mitigation: Treat outputs as decision support, review risk gates and stop-loss settings manually, and avoid autonomous live trade execution.

## Reference(s):

- [QuantClaw ClawHub listing](https://clawhub.ai/natanhoffmann/skills/quant-claw)
- [QuantClaw full version](https://anomalysystems.gumroad.com/l/wugjom)
- [uv project manager](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading analysis, account and order command examples, and setup guidance for uv, quantclaw, and Bybit API credentials.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
