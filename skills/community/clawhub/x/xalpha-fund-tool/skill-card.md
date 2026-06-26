## Description: <br>
xalpha supports multi-market fund portfolio analysis, including A/C share class cost comparison, convertible bond valuation, portfolio performance attribution, and fund correlation analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investment analysts use this skill to build xalpha and ZVT fund or quant workflows across A-share, Hong Kong, crypto, and fund portfolio analysis. It helps with share-class cost comparisons, convertible bond valuation, backtesting, data collection, correlation analysis, and portfolio performance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents as a fund-analysis helper but can support broader quant, backtesting, data-fetching, package-install, and skill-saving workflows. <br>
Mitigation: Review generated scripts, package changes, data downloads, and saved skill files before execution or reuse. <br>
Risk: Workflows may write market-data caches or other files under ~/.zvt or ZVT_HOME. <br>
Mitigation: Run in an isolated project environment, set ZVT_HOME to a workspace-specific path, and review filesystem writes before using persistent data. <br>
Risk: Provider or broker credentials may be requested for data access or trading-related workflows. <br>
Mitigation: Use simulation or read-only credentials unless live trading is explicitly intended and separately verified. <br>


## Reference(s): <br>
- [Xalpha Fund Tool on ClawHub](https://clawhub.ai/tangweigang-jpg/xalpha-fund-tool) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated scripts or workflow steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
