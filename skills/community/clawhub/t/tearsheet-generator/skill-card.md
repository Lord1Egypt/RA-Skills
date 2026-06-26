## Description: <br>
Generate professional QuantStats-style tearsheets with custom SVG visualizations, MAE analysis, leverage recommendations, and trade lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahuserious](https://clawhub.ai/user/ahuserious) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative strategy analysts use this skill to generate trading strategy performance tearsheets, inspect MAE and liquidation-risk metrics, and produce follow-up backtest verification artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a local Backtests Python path that may not exist or may point to code outside the reviewed artifact. <br>
Mitigation: Inspect or replace the local dependency path before running the skill, and run it only in an environment where the dependency source is trusted. <br>
Risk: Leverage recommendations and liquidation buffers may be mistaken for financial advice or live exchange risk controls. <br>
Mitigation: Treat the outputs as informational analysis only, validate results against trusted trade data and independent backtests, and apply separate financial risk review before any live trading use. <br>
Risk: Generated reports can overwrite prior artifacts that share the same strategy name and output directory. <br>
Mitigation: Choose an output directory under user control and back up existing reports before rerunning the workflow. <br>


## Reference(s): <br>
- [QuantStats](https://github.com/ranaroussi/quantstats) <br>
- [Tearsheet Generator Reference Index](artifact/references/index.md) <br>
- [MAE Analysis Reference](artifact/references/mae_analysis.md) <br>
- [Leverage Math Reference](artifact/references/leverage_math.md) <br>
- [HTML Templates Reference](artifact/references/html_templates.md) <br>
- [ClawHub release page](https://clawhub.ai/ahuserious/tearsheet-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples; generated workflows produce HTML, JSON, CSV, Python configuration, and text report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include strategy comparison tearsheets, metrics exports, verification reports, optimized configuration files, and leverage-analysis guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
