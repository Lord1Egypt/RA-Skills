## Description:

Screens markets across six asset classes using TradingView data, API pre-filters, pandas computed signals, and YAML-driven strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nomadrex](https://clawhub.ai/user/nomadrex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run one-time TradingView market screens or YAML-defined signal scans for stocks, crypto, forex, bonds, futures, and coins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies are resolved from PyPI at install time.

Mitigation: Install in an isolated environment and review or pin dependency versions before production use.

Risk: Screening output can be incomplete or misleading if YAML strategies contain invalid fields or computed expressions.

Mitigation: Review YAML strategies before use and check stderr warnings for fields or expressions that failed to filter as expected.

Risk: Market screening output is informational and may not reflect a complete investment decision process.

Mitigation: Validate results against independent data and apply human review before taking trading or investment action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nomadrex/skills/tv-signal-screener)
- [TradingView Screener API Guide](artifact/references/tvscreener-api-guide.md)
- [Computed Signals Guide](artifact/references/computed-signals-guide.md)
- [Strategy Templates](artifact/references/strategy-templates.md)
- [Field Presets](artifact/references/field-presets.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with command-line arguments and YAML strategy configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs through local Python scripts that fetch TradingView market data and print screening or signal results.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
