## Description:

Converts Chinese TDX indicator formulas into Python quantitative-analysis code and guidance, with mappings for 100+ functions, 30+ indicators, and trading strategies for backtesting, data analysis, and signal generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative analysts use this skill to migrate TDX formulas into pandas/numpy-based Python workflows for indicator calculation, backtesting, analysis, and signal generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula conversion can produce executable Python from user-supplied formula files.

Mitigation: Only convert trusted formula files and review generated Python before running it.

Risk: Examples and generated workflows may create or overwrite local Excel files.

Mitigation: Use explicit output paths and review file writes before execution.

Risk: Some documented future-looking functions can make backtests appear stronger than live results.

Mitigation: Avoid functions such as ZIG, BACKSET, PEAK, and TROUGH in live trading workflows.

Risk: Examples may fetch market data as part of quantitative-analysis workflows.

Mitigation: Run examples only in environments where external data access is expected and permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-tdx-python)
- [Publisher profile](https://clawhub.ai/user/li152)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Python formula-conversion code and file-output guidance for pandas/numpy workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
