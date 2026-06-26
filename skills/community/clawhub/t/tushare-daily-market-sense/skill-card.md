## Description: <br>
Generates structured after-market A-share research reports from Tushare Pro daily market data, local sentiment history, and deterministic evidence packs, with modules for market trend, turnover concentration, money effect, heavy-volume declines, and feature-group analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinfi-codex](https://clawhub.ai/user/chinfi-codex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market analysts and agent developers use this skill to generate disciplined A-share daily market reviews, including trend interpretation, concentration checks, money-effect analysis, downside risk grouping, and optional HTML report rendering. It is designed for research reporting and explicitly avoids buy, sell, stop-loss, target-price, automated trading, and portfolio-optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A helper script can print the PostgreSQL connection URL, which may expose credentials in terminal or CI logs. <br>
Mitigation: Use only low-privilege local database credentials and avoid running migrate_stock_to_pg.py until DSN logging is fixed or log exposure is acceptable. <br>
Risk: The package can modify local stock-data tables during migration or data refresh workflows. <br>
Mitigation: Run it against a dedicated local database or disposable schema, and back up any existing stock-data tables before migration. <br>
Risk: Some report inputs can come from Sohu, JRJ, or AKShare rather than only Tushare. <br>
Mitigation: Treat generated reports as market-analysis drafts and verify important data points or source assumptions before publication or operational use. <br>
Risk: Generated HTML includes inline JavaScript and embedded report chart data. <br>
Mitigation: Review generated HTML before sharing it externally and open it only in an environment appropriate for local report artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinfi-codex/tushare-daily-market-sense) <br>
- [Skill instructions](SKILL.md) <br>
- [Report template](reference/report_template.md) <br>
- [Output discipline](reference/methodology/output_discipline.md) <br>
- [Market trend methodology](reference/methodology/module1_trend.md) <br>
- [Turnover concentration methodology](reference/methodology/module2_concentration.md) <br>
- [Money effect methodology](reference/methodology/module3_money_effect.md) <br>
- [Heavy-volume decline methodology](reference/methodology/module4_decline.md) <br>
- [Feature groups methodology](reference/methodology/module5_feature_groups.md) <br>
- [PostgreSQL connection notes](scripts/_shared/POSTGRESQL.md) <br>
- [HTML report renderer notes](scripts/_shared/html_report/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports, JSON evidence/context files, optional self-contained HTML reports, and shell commands for local data/report generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files, Tushare and market-data dependencies, and optional PostgreSQL-backed stock data; outputs are reporting artifacts and not trading instructions.] <br>

## Skill Version(s): <br>
2.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
