## Description: <br>
Packaged as a self-hosted crypto portfolio tracker, this skill primarily guides agents through ZVT quantitative strategy, backtesting, data-provider setup, and Sphinx documentation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and finance automation users can use this skill to ask an agent for portfolio-tracking or quantitative trading workflow guidance, including market/provider selection, backtesting code, data collection steps, and documentation configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as a Rotki crypto tracker, but the artifact instructions mainly describe ZVT stock backtesting, trading workflows, and Sphinx documentation setup. <br>
Mitigation: Review the skill behavior against the artifact files before installation and treat the label as untrusted when deciding whether the skill fits a crypto portfolio-tracking use case. <br>
Risk: The skill can guide an agent toward finance backtesting, trading-code generation, provider setup, and purchase-capable or wallet-related workflows. <br>
Mitigation: Require explicit human approval before using paid providers, wallet credentials, exchange APIs, or any live trading or purchase action. <br>
Risk: Generated commands or code may install packages, write workspace files, or configure local finance tooling. <br>
Mitigation: Run commands in a controlled workspace, inspect generated code and configuration before execution, and avoid exposing production secrets. <br>
Risk: Financial calculations, market data, and tax or PnL outputs may be incomplete or inaccurate if source data, identifiers, or arithmetic choices are wrong. <br>
Mitigation: Validate monetary calculations, market identifiers, data-provider results, and reports against trusted records before making financial, accounting, or tax decisions. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/tangweigang-jpg/rotki-crypto-tracker) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](artifact/references/WISDOM.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include finance workflow assumptions, provider choices, and precondition checks that require user review before execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
