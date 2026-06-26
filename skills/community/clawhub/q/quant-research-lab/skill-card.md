## Description: <br>
A multi-agent quantitative strategy research workflow that helps coding agents design, backtest, risk-assess, optimize, and document trading strategies across specialized role templates. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[yili1992](https://clawhub.ai/user/yili1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and quantitative researchers use this skill to structure strategy research through role-based pipelines for strategy design, backtesting, risk management, factor modeling, execution design, and compliance review. Outputs are research drafts and should not be treated as financial, investment, or trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive broker credentials, API keys, account numbers, confidential trading plans, or user-provided strategy context may be captured in local research context or passed to subagents. <br>
Mitigation: Do not provide broker credentials, API keys, account numbers, or confidential trading plans unless the user accepts that they may be stored in the project state file and shared with subagents. <br>
Risk: Generated strategies, backtests, risk models, execution logic, and trading-system code may be incomplete, incorrect, or unsuitable for live trading. <br>
Mitigation: Treat outputs as research drafts requiring independent testing, compliance review, and paper trading before any real use. <br>
Risk: The skill can activate from natural-language quant research requests and may process unintended inputs. <br>
Mitigation: Prefer explicit /quant-research-lab invocation and review the intended market, capital, and research focus before running pipelines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yili1992/quant-research-lab) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Hermes Agent](https://hermes.nousresearch.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, formulas, pseudocode, code blocks, and QAGATE summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce strategy drafts, backtest designs, risk checks, execution plans, compliance notes, and local research-context summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
