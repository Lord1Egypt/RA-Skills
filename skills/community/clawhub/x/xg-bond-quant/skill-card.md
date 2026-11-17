## Description:

小果可转债量化分析助手 helps agents support convertible-bond quantitative analysis, including historical market data, technical factor data, strategy backtesting, and portfolio analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, quantitative researchers, and strategy developers use this skill to ask an agent for convertible-bond data access patterns, factor selection, backtest setup, and portfolio analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be exposed when used with an untrusted server, non-HTTPS transport, query strings, or logs.

Mitigation: Use only trusted servers and test credentials unless HTTPS is enforced and secrets are removed from query strings and logs.

Risk: Remote mutation, deletion, community publishing, simulation, and account-scoped data actions can affect user data or strategy records.

Mitigation: Require explicit human confirmation before an agent calls deletion, publishing, simulation, or account data endpoints.

Risk: Custom-code-style data functions can expand the execution and data access surface.

Mitigation: Review custom function inputs and remote account permissions before allowing autonomous calls, especially for get_user_def_data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li152/skills/xg-bond-quant)
- [Publisher profile](https://clawhub.ai/user/li152)
- [xg_quant_trader tutorial](https://gitcode.com/qq_50882340/xg_quant_trader)
- [xg_factor reference](references/xg_factor.txt)
- [xg_quant API reference](references/xg_tdx_func.txt)
- [factor table](references/因子表.txt)
- [strategy helper reference](references/xg_factor_trader.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe API requests, DataFrame transformations, factor calculations, backtest parameters, and risk review steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
