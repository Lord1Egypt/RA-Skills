## Description: <br>
基于 VectorBT 框架的向量化回测与因子研究工具，支持多市场数据批量回测、策略参数优化和统计套利分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative finance practitioners use this skill to generate guidance and code for VectorBT/ZVT-style market data ingestion, factor research, signal generation, portfolio backtesting, performance analysis, and plotting across A-share, Hong Kong, and crypto workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers broad finance automation beyond VectorBT backtesting, including live signaling, documentation automation, credentialed providers, and saved-skill creation. <br>
Mitigation: Install only when that broad scope is intended, use an isolated virtual environment, and review generated commands and files before running them. <br>
Risk: Credentialed data providers, broker integrations, crypto workflows, or wallet-related actions could expose sensitive credentials or create unintended financial operations. <br>
Mitigation: Avoid broker credentials unless necessary, keep secrets outside generated code, and require explicit human approval for any command or configuration that accesses accounts, wallets, or paid data providers. <br>
Risk: Generated backtests and strategy guidance can be misleading if market data, timing assumptions, trading costs, slippage, or look-ahead controls are wrong. <br>
Mitigation: Treat generated analysis as draft work, validate assumptions against the referenced constraints and locks, and review results before using them for trading decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/vectorbt-vectorized) <br>
- [Human Summary](artifact/human_summary.md) <br>
- [Use Cases](artifact/references/USE_CASES.md) <br>
- [Semantic Locks](artifact/references/LOCKS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, configuration snippets, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose finance automation workflows that require user review before execution] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
