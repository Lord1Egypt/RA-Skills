## Description:

This skill helps agents support stock quantitative analysis workflows using XG Quant interfaces for historical and intraday market data, factor and financial data, strategy backtesting, and portfolio analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

Stock investors, quantitative researchers, and strategy developers use this skill to request market data, calculate technical factors, inspect financial and index data, run stock strategy backtests, and analyze portfolios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account credentials may be handled insecurely.

Mitigation: Use only trusted servers over HTTPS and avoid entering reusable passwords or authorization codes unless transport and logging protections are confirmed.

Risk: Deletion operations and custom-code data features can change data or execute risky workflows.

Mitigation: Require explicit human approval before deletion calls or get_user_def_data, and review requested operations before allowing an agent to proceed.

Risk: Bundled scripts can overwrite generated data files and accept file paths for formula conversion.

Mitigation: Run scripts in a dedicated workspace with reviewed inputs and backups for any important generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-stock-quant)
- [Publisher profile](https://clawhub.ai/user/li152)
- [xg_quant_trader tutorial](https://gitcode.com/qq_50882340/xg_quant_trader)
- [alpha factor reference](references/alpha.txt)
- [XG factor reference](references/xg_factor.txt)
- [XG factor trader reference](references/xg_factor_trader.txt)
- [XG TDX function reference](references/xg_tdx_func.txt)
- [Factor table reference](references/因子表.txt)
- [Factor calculation test reference](references/因子计算测试.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API usage examples, workflow guidance, and quantitative-analysis code snippets; outputs should not be treated as financial advice.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
