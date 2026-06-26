## Description: <br>
Helps agents build Python-based quantitative investing workflows for ZVT, including data collection, strategy backtesting, portfolio rebalancing, and trade execution guidance across A-share, Hong Kong, and crypto markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance engineers use this skill to ask an agent for ZVT-based Python code and guidance for market data collection, factor construction, backtesting, portfolio analytics, and rebalancing or trade execution workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live-trading or purchase-capable workflows, which could lead to unintended orders or financial loss. <br>
Mitigation: Use paper trading or backtests by default, require explicit order-by-order confirmation before broker-connected actions, and review generated trade logic before execution. <br>
Risk: The skill may require broker or data-provider credentials and OAuth tokens. <br>
Mitigation: Use an isolated Python environment, keep credentials out of prompts and generated files, and provide tokens only through secure local environment configuration. <br>
Risk: The security summary flags inconsistent live-trading and backtesting descriptions with weak user-facing safety boundaries. <br>
Mitigation: Treat outputs as review-needed finance guidance, pin dependencies, use a dedicated ZVT_HOME, and validate strategy behavior against the documented semantic locks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/robo-advisor-python) <br>
- [Human Summary](human_summary.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](references/WISDOM.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python code snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include finance workflow assumptions, market/provider choices, and precondition checks for ZVT-based execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
