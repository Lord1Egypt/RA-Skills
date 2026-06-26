## Description: <br>
LLM-driven crypto perpetual futures trading on Bybit. Analyzes 200+ market features across 8 timeframes with strategy-aware output, then you decide whether to trade. Supports DEMO and LIVE modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[natanhoffmann](https://clawhub.ai/user/natanhoffmann) <br>

### License/Terms of Use: <br>
Proprietary - purchase required for full access <br>


## Use Case: <br>
External users and developers use QuantClaw to analyze Bybit crypto perpetual futures across multiple strategies and timeframes, review structured market signals, and optionally execute demo or live trades through the external CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external paid CLI can use Bybit API keys to place leveraged futures orders. <br>
Mitigation: Use demo/testnet keys first, inspect the downloaded source and checksum before running it, and do not provide keys with withdrawal permission. <br>
Risk: Switching from demo to live trading can expose real funds to market and execution risk. <br>
Mitigation: Keep DEMO mode as the default and require explicit interactive user confirmation before any LIVE mode use. <br>


## Reference(s): <br>
- [QuantClaw ClawHub listing](https://clawhub.ai/natanhoffmann/quant-claw) <br>
- [QuantClaw full version and verification download](https://anomalysystems.gumroad.com/l/wugjom) <br>
- [uv Python package manager](https://github.com/astral-sh/uv) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Bybit API credentials and defaults to DEMO mode; LIVE mode requires explicit interactive user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
