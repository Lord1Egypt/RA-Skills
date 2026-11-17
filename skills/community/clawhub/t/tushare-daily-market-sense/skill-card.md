## Description:

Generates structured post-market A-share research reports from Tushare Pro daily market data, covering index trend, sentiment, turnover concentration, money-effect themes, high-volume decline risk, and feature-group observations without giving buy/sell advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinfi-codex](https://clawhub.ai/user/chinfi-codex)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, developers, and agents use this skill to assemble daily China A-share market reviews from Tushare Pro data. It is suited for post-market trend, sentiment, turnover concentration, money-effect, high-volume decline, and feature-group analysis, not for automated trading or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write local market-data files and mutate a PostgreSQL market-data store.

Mitigation: Review before running against a real database, use a dedicated low-privilege database, and keep backups or run in a disposable workspace for first use.

Risk: A migration path can expose database credentials in logs.

Mitigation: Avoid production credentials, inspect migration logs for secrets, and rotate any password that may have appeared in logs.

Risk: The workflow may read a local .env file for Tushare credentials.

Mitigation: Run from a clean skill workspace and avoid directories that contain unrelated .env files or secrets.

Risk: Generated HTML can include report text links and should not be assumed safe when text is external or user supplied.

Mitigation: Treat generated HTML as untrusted, review links before sharing or hosting, and avoid opening it in privileged browser contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinfi-codex/skills/tushare-daily-market-sense)
- [Publisher profile](https://clawhub.ai/user/chinfi-codex)
- [Market report template](artifact/reference/report_template.md)
- [Output discipline](artifact/reference/methodology/output_discipline.md)
- [Market trend methodology](artifact/reference/methodology/module1_trend.md)
- [Turnover concentration methodology](artifact/reference/methodology/module2_concentration.md)
- [Money effect methodology](artifact/reference/methodology/module3_money_effect.md)
- [High-volume decline methodology](artifact/reference/methodology/module4_decline.md)
- [Feature groups methodology](artifact/reference/methodology/module5_feature_groups.md)
- [PostgreSQL setup notes](artifact/scripts/_shared/POSTGRESQL.md)
- [HTML report renderer notes](artifact/scripts/_shared/html_report/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown market report with JSON evidence packs and optional self-contained HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces temporary evidence and module-context files during drafting; final retained outputs are the Markdown report and optional HTML report.]

## Skill Version(s):

2.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
