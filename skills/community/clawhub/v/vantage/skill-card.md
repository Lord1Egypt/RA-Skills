## Description: <br>
Vantage is an autonomous signal-to-execution trading agent for Hyperliquid perpetual futures that uses public market signals, optional LLM decisioning, Kelly-style sizing, paper mode, setup checks, and signed live order execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morebetterclaw](https://clawhub.ai/user/morebetterclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to configure, validate, and run a local Hyperliquid perpetual futures trading loop with paper trading available before live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real live trades with a Hyperliquid private key. <br>
Mitigation: Start in paper mode, run the setup validator, use a limited-risk wallet, and set strict position and account-risk caps before live trading. <br>
Risk: Optional OpenAI decisioning may send trading signal data to a cloud API when OPENAI_API_KEY is configured. <br>
Mitigation: Use local Ollama or the rule-based fallback unless cloud processing of trading signals is acceptable. <br>
Risk: THORChain routing output can affect cross-chain fund movement decisions. <br>
Mitigation: Independently verify each destination address, memo, amount, fee, and slippage value before moving funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/morebetterclaw/vantage) <br>
- [Publisher profile](https://clawhub.ai/user/morebetterclaw) <br>
- [MoreBetter Studios products](https://morebetterstudios.com/products) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [CLI text, setup guidance, shell commands, logs, and JSON quote or market-data output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in paper mode or place live Hyperliquid orders when a private key and risk limits are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
