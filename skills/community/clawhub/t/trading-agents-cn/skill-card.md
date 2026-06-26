## Description: <br>
Trading Agents Cn helps agents build LLM-assisted quantitative analysis workflows for China A-shares, including batch stock comparison, backtest signal generation, factor research, and OpenAI-compatible LLM adapter templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative analysts use this skill to generate A-share analysis and backtesting code, compare multiple securities, design factor strategies, and configure OpenAI-compatible LLM providers for TradingAgents-style workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill includes under-scoped internal-message crawling, persistent storage, and broad execution triggers. <br>
Mitigation: Review those capabilities before installation, run the skill in an isolated Python environment, and disable or avoid crawling workflows unless authorization, storage, retention, and deletion requirements are explicit. <br>
Risk: The evidence flags sensitive credentials and wallet-related capability tags. <br>
Mitigation: Provide only scoped credentials, keep secrets out of prompts and logs, and avoid broker-connected or live-trading use unless independently authorized. <br>
Risk: Generated trading and backtesting outputs can be misleading if market rules, data quality, or look-ahead constraints are mishandled. <br>
Mitigation: Validate generated strategies against the bundled semantic locks, domain constraints, and independent financial review before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/trading-agents-cn) <br>
- [Use cases](references/USE_CASES.md) <br>
- [Semantic locks](references/LOCKS.md) <br>
- [Domain constraints](references/CONSTRAINTS.md) <br>
- [Component capability map](references/COMPONENTS.md) <br>
- [Anti-patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading analysis guidance, backtesting workflow steps, and provider configuration templates.] <br>

## Skill Version(s): <br>
0.3.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
