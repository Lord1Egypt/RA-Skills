## Description: <br>
Helps an agent build and run daily quant strategy backtests with Zipline/ZVT workflows, including market data setup, factor research, trading simulation, and performance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to generate code, commands, and guidance for daily backtests across A-share, Hong Kong, and crypto workflows. It supports data-provider selection, strategy setup, factor computation, trade simulation, and result visualization while prompting for market, data source, strategy type, time range, and target instruments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose commands, credential prompts, memory use, or output paths that need review before execution. <br>
Mitigation: Run it in an isolated Python environment and review each command, prompt, memory operation, and output path before approving it. <br>
Risk: Some workflows may involve paid providers, broker credentials, or purchase-capable integrations. <br>
Mitigation: Prefer free or read-only data sources and avoid broker or paid-provider credentials unless the task explicitly requires them. <br>
Risk: The artifact includes a documentation-deployment path in addition to backtesting workflows. <br>
Mitigation: Do not run documentation deployment steps until the exact files, destinations, and publication target have been confirmed. <br>
Risk: Backtest outputs can be misleading if look-ahead bias, missing data, transaction costs, slippage, or T+1 trading rules are handled incorrectly. <br>
Mitigation: Apply the artifact's semantic locks and constraints, including next-bar execution, nonzero costs and slippage, data-quality checks, and A-share T+1 restrictions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/zipline-daily-backtest) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Wisdom](references/WISDOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code, shell command snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Python backtest code, data setup commands, provider-specific configuration notes, and performance-analysis guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
