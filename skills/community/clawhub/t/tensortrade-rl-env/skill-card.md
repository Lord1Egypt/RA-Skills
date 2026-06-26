## Description: <br>
Provides multi-market backtesting and reinforcement-learning trading environment support, including multi-exchange wallet portfolio management, Plotly trading visualization, and RL agent training and evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quant researchers use this skill to generate guidance, code, configuration, and commands for market data collection, strategy backtesting, feature research, trading environment setup, visualization, and RL trading-agent evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release has a suspicious security verdict because the advertised TensorTrade identity conflicts with ZVT-focused setup and guidance. <br>
Mitigation: Review the skill before installation and validate generated trading code, data paths, and framework assumptions before use. <br>
Risk: The skill may request wallet, broker, or paid data-provider credentials for finance workflows. <br>
Mitigation: Use an isolated Python environment and do not provide sensitive credentials until the generated code and intended data flows have been reviewed. <br>
Risk: Generated commands or package installation steps could change the local execution environment. <br>
Mitigation: Require explicit confirmation before running package installs or shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/tensortrade-rl-env) <br>
- [Human summary](artifact/human_summary.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Known use cases](artifact/references/USE_CASES.md) <br>
- [Semantic locks and preconditions](artifact/references/LOCKS.md) <br>
- [Domain constraints](artifact/references/CONSTRAINTS.md) <br>
- [Component capability map](artifact/references/COMPONENTS.md) <br>
- [Anti-patterns](artifact/references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code, command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference finance and backtesting constraints, semantic locks, anti-patterns, and component maps from bundled reference files.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
