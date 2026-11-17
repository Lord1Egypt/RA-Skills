## Description:

QuantAll gives an agent a local A-share market analysis workflow for vectorized factor analysis, strategy backtesting, IC analysis, stock screening, visualization, and optional DuckDB data maintenance through MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mifochen](https://clawhub.ai/user/mifochen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly need quantitative A-share analysis, such as factor testing, strategy backtesting, IC analysis, stock selection, visualization, or preparing a local DuckDB-backed market database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to create a local virtual environment, install packages, modify MCP configuration, and start a localhost MCP service.

Mitigation: Require explicit user consent before local setup or service startup, and review all configuration changes before applying them.

Risk: The optional UpdateStock workflow reads and writes DuckDB databases and uses a Tushare token that may be stored locally.

Mitigation: Use a dedicated database path, back up important data, store the Tushare token carefully, and rotate it if exposure is suspected.

Risk: The security review warns against running untrusted JSON task files or Python scripts through QuantAll.

Mitigation: Only execute task files or Python scripts from trusted sources after reviewing their contents and expected filesystem effects.

Risk: The security review specifically advises against using the sandbox-disable workaround.

Mitigation: Keep sandbox protections enabled and resolve installation conflicts by rebuilding the virtual environment or using standard package management steps.

## Reference(s):

- [QuantAll playbook](references/quantall_playbook.md)
- [ClawHub release page](https://clawhub.ai/mifochen/skills/quant-all-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, Python snippets, MCP configuration JSON, and summarized analysis results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local process startup, local file creation, MCP configuration changes, DuckDB reads/writes, and summarized quantitative analysis outputs.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
