## Description: <br>
Yfinance Market Data helps agents retrieve Yahoo Finance market data for stocks, indices, foreign exchange, and cryptocurrency, including history, quotes, calendars, fundamentals, screening, and live crypto streaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and finance-oriented agents use this skill to fetch, repair, screen, cache, and stream market data, then generate analysis or code for data collection, backtesting, and quant strategy workflows. Review generated workflows before allowing broker, paid-provider, local-write, or live-trading actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scope extends beyond simple Yahoo Finance lookup into quant strategy generation, ZVT workflows, and backtesting. <br>
Mitigation: Use it only when a broader finance and quant assistant is intended, and review each proposed workflow against the user's stated task before execution. <br>
Risk: Some workflows may request broker or paid-provider credentials. <br>
Mitigation: Require explicit user approval before using credentials, keep secrets out of generated code, and prefer environment variables or secured configuration. <br>
Risk: Generated workflows may install packages, initialize local data, write result files, or save skill files. <br>
Mitigation: Review commands, paths, and file diffs before execution, and restrict writes to the intended workspace. <br>
Risk: Financial data and generated analysis may be delayed, incomplete, or unsuitable for live trading decisions. <br>
Mitigation: Verify market data independently and avoid live trading or investment decisions based only on this skill's output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/yfinance-market-data) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](references/WISDOM.md) <br>
- [Seed Reference](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration notes, and generated workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, date range, and target entities before producing executable finance-data or backtesting workflows.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
