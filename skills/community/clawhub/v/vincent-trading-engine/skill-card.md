## Description: <br>
Strategy-driven automated trading for Polymarket and HyperLiquid, including trading strategies, stop-loss rules, take-profit rules, trailing stops, and automated strategy monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to create, activate, monitor, pause, and archive automated trading strategies and protective trade rules for Polymarket and HyperLiquid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to manage live automated trading and place real trades with wallet or venue API credentials. <br>
Mitigation: Use restricted wallet or API permissions, strict spend and position limits, and human approval wherever available before enabling live strategies. <br>
Risk: Automated strategies and trade rules can continue running after activation and may act on changing market signals. <br>
Mitigation: Test with minimal size or simulation first, monitor active strategies, and confirm pause, cancel, and archive procedures before deployment. <br>
Risk: LLM and market-data driven monitoring can create unexpected cost or trading activity. <br>
Mitigation: Verify the CLI package and version, monitor costs and event logs, and set conservative polling, wake-frequency, and exposure limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glitch003/vincent-trading-engine) <br>
- [Vincent homepage](https://heyvincent.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the @vincentai/cli package and may require wallet or venue API credentials.] <br>

## Skill Version(s): <br>
1.0.69 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
