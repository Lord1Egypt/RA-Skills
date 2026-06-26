## Description: <br>
Screen markets across 6 asset classes using TradingView data with API pre-filters, pandas computed signals, and YAML-driven strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukebaze](https://clawhub.ai/user/lukebaze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and traders use this skill to run one-time market screens or YAML-defined computed signals across TradingView asset classes and receive markdown result tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency drift may affect reproducibility in financial workflows because dependencies are version-ranged. <br>
Mitigation: Use a locked or reviewed dependency set before installation in high-assurance workflows. <br>
Risk: Generated screening signals can be mistaken for trading recommendations. <br>
Mitigation: Treat results as informational and review market context before acting on any screen result. <br>
Risk: Custom YAML expression signals may encode incorrect or unintended logic. <br>
Mitigation: Review custom signal expressions before running them and rely on the skill's expression validation as a guardrail, not as full strategy validation. <br>


## Reference(s): <br>
- [TradingView Screener API Guide](references/tvscreener-api-guide.md) <br>
- [Computed Signals Guide](references/computed-signals-guide.md) <br>
- [Strategy Templates](references/strategy-templates.md) <br>
- [Field Presets](references/field-presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown tables with command examples and YAML signal configurations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TradingView data through tvscreener; results are informational market screens, not trading recommendations.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
