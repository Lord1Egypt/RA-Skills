## Description:

Microsoft Qlib helps agents support quantitative finance workflows such as financial data analysis, trading strategy development, backtesting, portfolio optimization, risk modeling, and machine learning for market prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawyerieong-cpuai](https://clawhub.ai/user/sawyerieong-cpuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quantitative researchers, and finance-focused agents use this skill to install and work with Qlib for stock data analysis, factor research, strategy backtesting, model training, portfolio optimization, and risk modeling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs the Qlib Python package without pinning a package version.

Mitigation: Install in a virtual environment or container, pin and review the Qlib package version before use, and avoid running installation from a privileged account.

Risk: Quantitative finance outputs can be mistaken for investment advice or relied on without adequate validation.

Mitigation: Review model assumptions, data quality, and backtest methodology before using results in financial decisions.

## Reference(s):

- [Qlib GitHub Repository](https://github.com/microsoft/qlib)
- [Qlib Documentation](https://qlib.readthedocs.io/)
- [Qlib Official Site](https://microsoft.github.io/qlib/)
- [ClawHub Skill Page](https://clawhub.ai/sawyerieong-cpuai/skills/qlib-ms)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Qlib installation guidance, example Python snippets, analysis steps, and finance workflow recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
