## Description:

Generate professional QuantStats-style tearsheets with custom SVG visualizations, performance reports, MAE analysis, leverage recommendations, and trade lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahuserious](https://clawhub.ai/user/ahuserious)

### License/Terms of Use:


## Use Case:

Developers and quantitative trading analysts use this skill to generate HTML and JSON performance tearsheets from strategy trade data, then review MAE, leverage, liquidation-buffer, and verification outputs before acting on any configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a hard-coded external Backtests directory that is outside the reviewed package.

Mitigation: Install only when that directory is trusted and controlled, or replace the dependency with a bundled or pinned implementation before use.

Risk: Leverage, liquidation, and optimized-configuration outputs can be mistaken for live-trading instructions.

Mitigation: Treat outputs as analytical backtest material, not financial advice, and require human review before using them in trading systems.

Risk: The skill can write reports and configuration files to user-supplied output paths.

Mitigation: Review output paths and generated files before allowing writes or backtest runs.

## Reference(s):

- [Tearsheet Generator ClawHub Skill Page](https://clawhub.ai/ahuserious/skills/tearsheet-generator)
- [ahuserious ClawHub Publisher Profile](https://clawhub.ai/user/ahuserious)
- [QuantStats Project](https://github.com/ranaroussi/quantstats)
- [MAE Analysis Deep Dive](references/mae_analysis.md)
- [Leverage Mathematics Reference](references/leverage_math.md)
- [HTML Templates Reference](references/html_templates.md)
- [Tearsheet Generator Reference Index](references/index.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance plus generated HTML reports, JSON metrics, text reports, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include strategy comparison HTML, metrics JSON, verification JSON, optimized configuration JSON, and optimization reports.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
