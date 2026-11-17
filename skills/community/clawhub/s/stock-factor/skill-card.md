## Description:

Stock Factor helps agents inspect and update a curated A-share equity factor library with 1,101 factors across 18 families, QuantAll task JSON, Excel IC/IR result tables, and an HTML report generator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifochen](https://clawhub.ai/user/mifochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and agent users use this skill to browse A-share stock factors, inspect IC/IR screening results, generate factor-analysis reports, and rerun factor tasks through a local QuantAll environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external QuantAll package and local localhost MCP connector.

Mitigation: Install QuantAll only from a trusted source and version, preferably in a dedicated virtual environment under a non-admin account, and review the connector before enabling it.

Risk: Factor calculations depend on the selected local market database and its coverage.

Mitigation: Point DB_setting.json only at the intended database and verify available fields, sample coverage, and data freshness before relying on results.

Risk: Broad process-kill actions can interrupt unrelated Python processes.

Mitigation: Avoid broad process termination unless the user has confirmed which Python process belongs to QuantAll.

Risk: IC/IR tables are screening signals and may be misleading if treated as final trading strategy evidence.

Mitigation: Review factor definitions, rerun analyses on current data, check redundancy, and validate candidates with independent backtests before investment use.

## Reference(s):

- [ClawHub stock-factor skill page](https://clawhub.ai/mifochen/skills/stock-factor)
- [Skill definition](SKILL.md)
- [Report generator](scripts/gen_report.py)
- [TA-Lib function reference](https://ta-lib.org/functions/)
- [Alpha101 source formulas](scripts/因子初始参考文件/Alpha101.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline Python, JSON, and shell snippets; local artifacts include task JSON, Excel result tables, and a self-contained HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [QuantAll execution depends on a trusted local installation, an intended market database, and the localhost MCP connector.]

## Skill Version(s):

1.3.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
