## Description: <br>
Automated Trading System with Multi-Strategy Voting <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[pikachu022700](https://clawhub.ai/user/pikachu022700) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-system evaluators use this skill to run a paper-trading cryptocurrency strategy demo with multi-strategy voting, simulated position management, live market-data lookups, and optional status dashboards. It should not be used for real financial decisions or connected to exchange credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals may be incorrect, simplified, or misleading if treated as financial advice. <br>
Mitigation: Use the skill only as a demo or paper-trading tool and independently review any signal before making financial decisions. <br>
Risk: Connecting real exchange credentials or relying on the demo for live account trading could cause financial loss. <br>
Mitigation: Do not provide exchange credentials and keep operation limited to simulated capital and paper-trading workflows. <br>
Risk: The optional dashboard can expose status endpoints if served on an untrusted network. <br>
Mitigation: Bind the dashboard to localhost or add access controls before running it in any shared or networked environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pikachu022700/quant-trading-system) <br>
- [ClawHub metadata homepage](https://clawhub.com/quant-trading-system) <br>
- [Hyperliquid market-data API endpoint](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [CLI text and JSON responses, with optional HTTP JSON dashboard endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses simulated capital and paper-trading positions; live market-data lookups may affect displayed prices and generated signals.] <br>

## Skill Version(s): <br>
6.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
