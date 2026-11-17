## Description:

小果(微信:xg_quant)基金量化分析助手专注于基金量化分析工具，基于小果量化策略系统，提供基金历史行情数据、基金因子数据、基金策略回测、基金组合分析等核心功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[li152](https://clawhub.ai/user/li152)

### License/Terms of Use:

MIT-0

## Use Case:

External fund investors, asset allocation researchers, and quant strategy developers use this skill to retrieve ETF fund market and factor data, run common quantitative backtests, and compare or optimize fund portfolios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends account credentials to a configured service.

Mitigation: Install only for trusted servers, prefer HTTPS, avoid logging full request URLs, and use low-privilege or throwaway credentials.

Risk: The skill includes actions that can delete simulated or community strategy data and invoke custom factor or strategy behavior.

Mitigation: Do not invoke deletion, simulated/community strategy, or custom-code endpoints without explicit review and approval.

Risk: Quant-finance outputs can be mistaken for investment recommendations.

Mitigation: Treat historical factors, backtests, and portfolio optimization outputs as analysis inputs and review assumptions before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/li152/skills/xg-fund-quant)
- [GitCode Usage Tutorial](https://gitcode.com/qq_50882340/xg_quant_trader)
- [Factor Field Reference](artifact/references/因子表.txt)
- [Fund Factor API Reference](artifact/references/xg_factor_trader.txt)
- [Technical Indicator Function Reference](artifact/references/xg_tdx_func.txt)
- [Alpha Factor Reference](artifact/references/alpha.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, tabular factor and strategy parameter references, and risk review guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
