## Description:

九维雷达V3.0终极选股系统 is a Chinese A-share stock-selection skill that scores equities across valuation, drawdown, quality, industry momentum, sentiment, network structure, expectation gap, timing, and market-cap elasticity to support educational screening and portfolio analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcz5221-svg](https://clawhub.ai/user/lcz5221-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to rank Chinese A-share stock pools, produce single-stock nine-dimension scoring reports, scan for high-scoring candidates, and outline portfolio allocation and risk controls. Outputs should be treated as educational analysis, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock screening and portfolio guidance may be mistaken for personalized financial advice.

Mitigation: Present results as educational analysis, require independent review, and keep the bundled risk disclaimer visible in user-facing reports.

Risk: The release includes an IDE Claude tab state file that server security evidence flags as potentially affecting agent permission prompts.

Mitigation: Remove artifact/.idea/claudeCodeTabState.xml before opening the project in an IDE with Claude integration.

Risk: Automated scans depend on current third-party market data and can produce stale or incomplete rankings when data is missing or delayed.

Mitigation: Require current inputs or a configured data interface before scoring, and cross-check high-ranked candidates before acting on outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lcz5221-svg/skills/v3-0)
- [九维雷达V3.0评分标准细则](artifact/九维雷达评分体系.md)
- [九维雷达V3.0实战操作手册](artifact/实战操作手册.md)
- [九维雷达V3.0扫描系统使用说明](artifact/扫描脚本说明.md)
- [System README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with ranking tables, score breakdowns, Python-style snippets, shell setup commands, and CSV export guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current market and fundamentals data supplied by the user or an external data interface; automated scanning references pandas, numpy, and Tushare configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
