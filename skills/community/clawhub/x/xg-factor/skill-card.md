## Description:

小果量化因子库 is a Python quantitative factor calculation system that integrates hundreds of technical indicators, Alpha factors, and trading signals for stocks, ETFs, and convertible bonds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and quantitative researchers use this skill to calculate technical indicators, Alpha factors, trading signals, and risk-return metrics, then produce standardized factor datasets for analysis, screening, and backtesting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch factor calculations can write or overwrite local result files.

Mitigation: Run the skill in a dedicated project directory, review output paths before batch jobs, and avoid force recalculation unless overwriting generated files is acceptable.

Risk: Generated formula or code-like output may be unsafe if executed without review.

Mitigation: Treat generated formulas and code snippets as untrusted until reviewed before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-factor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local factor calculations that write Pandas DataFrame, Excel, JSON, or Parquet outputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
