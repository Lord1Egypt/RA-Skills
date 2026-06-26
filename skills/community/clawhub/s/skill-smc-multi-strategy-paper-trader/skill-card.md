## Description: <br>
Paper trading monitors for SMC (Smart Money Concepts) and Macro Rotation strategies, including swing, day, coordinated, regime-gated, macro-rotation, and multi-factor regime-scoring workflows that use public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading researchers use this skill to run paper-trading monitors, regime scoring, and simulated portfolio tracking for crypto strategies. It is intended for simulated trading workflows, not as financial advice or direct execution of live trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts may read ~/.github_token and publish portfolio data to a hardcoded GitHub repository even though the skill text says no credentials are needed. <br>
Mitigation: Review or disable the GitHub sync code before installing; run without ~/.github_token unless publishing those portfolio files is intentional. <br>
Risk: The scripts write local trading state under ~/.openclaw/workspace/trading. <br>
Mitigation: Run in an isolated environment or dedicated user account and review generated portfolio, lock, journal, and observation files before scheduling recurring execution. <br>
Risk: Paper-trading outputs and simulated strategy results could be mistaken for live trading instructions. <br>
Mitigation: Keep use limited to simulated monitoring and require human review before using any strategy output in live trading or financial decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-smc-multi-strategy-paper-trader) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>
- [Binance Futures market data endpoint](https://fapi.binance.com/fapi/v1/klines) <br>
- [FRED CSV graph endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript scripts and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces paper-trading monitor instructions and local JSON portfolio/state files; scripts write under ~/.openclaw/workspace/trading.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
