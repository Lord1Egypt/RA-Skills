## Description:

Screen markets across 6 asset classes using TradingView data. API pre-filters + pandas computed signals. YAML-driven strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukebaze](https://clawhub.ai/user/lukebaze)

### License/Terms of Use:


## Use Case:

Developers and market analysts use this skill to run TradingView-backed market screens and YAML-driven technical signals across stocks, crypto, forex, bonds, futures, and coins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies are specified as version ranges and may resolve to newer package versions during installation.

Mitigation: Pin and hash dependencies before higher-assurance or repeatable deployments.

Risk: Screening filters and strategy parameters are sent through the TradingView/tvscreener data path.

Mitigation: Use only screening inputs that are acceptable to share with that external market-data path.

Risk: Custom YAML expressions can affect computed signal filtering behavior.

Mitigation: Review signal YAML expressions before execution and keep them within the documented field and operator patterns.

## Reference(s):

- [TradingView Screener API Guide](references/tvscreener-api-guide.md)
- [Computed Signals Guide](references/computed-signals-guide.md)
- [Strategy Templates](references/strategy-templates.md)
- [Field Presets](references/field-presets.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables with CLI command snippets and YAML strategy configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TradingView/tvscreener market data and supports JSON filters, column selection, sorting, limits, timeframes, and YAML signal files.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
