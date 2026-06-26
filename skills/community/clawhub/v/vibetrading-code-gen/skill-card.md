## Description: <br>
Generate executable Hyperliquid trading strategy code from natural language prompts. Use when a user wants to create automated trading strategies for Hyperliquid exchange based on their trading ideas, technical indicators, or VibeTrading signals. The skill generates complete Python code with proper error handling, logging, and configuration using actual Hyperliquid API wrappers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhaonan00](https://clawhub.ai/user/liuhaonan00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-system builders use this skill to turn natural-language Hyperliquid strategy ideas into Python strategy files, configuration, requirements, usage instructions, and optional backtest artifacts. It supports reviewable strategy development but does not certify that generated strategies are safe, profitable, or ready for live funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategies can produce and run live Hyperliquid exchange automation with weak safety boundaries. <br>
Mitigation: Review generated strategy code manually and run it in a sandbox or Hyperliquid testnet before considering any live trading. <br>
Risk: API credentials used by generated strategies could expose trading authority. <br>
Mitigation: Use least-privilege API keys with no withdrawal authority, small limits, and a separate account. <br>
Risk: The validator and sample backtests do not prove strategy safety, profitability, or production readiness. <br>
Mitigation: Treat validation and backtests as preliminary checks only; add live-trading confirmation, dry-run behavior, explicit risk limits, and a kill switch before using real funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuhaonan00/vibetrading-code-gen) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Hyperliquid API endpoint](https://api.hyperliquid.xyz) <br>
- [Hyperliquid testnet API endpoint](https://api.hyperliquid-testnet.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python strategy files, JSON configuration, requirements text, Markdown usage instructions, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code may call Hyperliquid APIs and should be reviewed, sandboxed, and tested on testnet before any live trading use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
