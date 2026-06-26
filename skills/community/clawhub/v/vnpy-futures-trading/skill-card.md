## Description: <br>
Supports VeighNa (vnpy) futures trading execution, day and night session management, CSI300 data download, and Alpha101/LightGBM factor research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to generate guidance, code, shell commands, and configuration for VeighNa/ZVT data collection, A-share factor research, backtesting, RPC client-server workflows, and futures trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the trading scope is confused and includes live or RPC trading behavior without clear user-facing safeguards. <br>
Mitigation: Use the skill only in a sandbox or paper-trading environment until the skill identity, broker credential handling, RPC exposure, explicit live-order confirmation, and risk limits are documented. <br>
Risk: Generated trading workflows can place orders or expose broker-connected services if used against live infrastructure. <br>
Mitigation: Require explicit user confirmation before live order execution, keep credentials outside generated files, restrict RPC services to trusted networks, and enforce pre-trade risk limits. <br>
Risk: The artifact includes skill-file persistence behavior that is not clearly opt-in. <br>
Mitigation: Treat persistence as disabled unless the user explicitly requests it and review any generated file-writing path before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/vnpy-futures-trading) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Implementation Wisdom](references/WISDOM.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for target market, data provider, strategy type, time range, and target entity IDs before producing outputs.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
