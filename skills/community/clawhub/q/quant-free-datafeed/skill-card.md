## Description:

量化交易系统免费数据源替换方法论，替换付费数据源，保持接口完全兼容

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative-trading engineers use this skill to replace a paid market-data feed with free data sources while preserving the existing data-layer interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or degraded free market-data feeds can affect strategy decisions in a trading system.

Mitigation: Validate data quality, coverage, and failover behavior before using the replacement data layer in production.

Risk: The skill depends on third-party market-data libraries and services whose availability, limits, or terms may change.

Mitigation: Review each listed data provider and monitor health checks, failures, and fallback behavior after deployment.

Risk: The guidance is narrowly scoped to the data acquisition layer and should not alter order, strategy, or risk logic.

Mitigation: Keep changes limited to the data provider interface and review downstream trading behavior separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterliu-512/skills/quant-free-datafeed)
- [Publisher profile](https://clawhub.ai/user/peterliu-512)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with architecture notes, dependency lists, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
