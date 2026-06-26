## Description: <br>
Generates or modifies Python quantitative trading strategy code for the Guojin PTRADE platform using bundled API references and strategy templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weistiger](https://clawhub.ai/user/weistiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading users use this skill to draft, adapt, and explain PTRADE-compatible Python strategies from templates and API reference material before backtesting or simulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PTRADE strategies may place live market orders when connected to a live trading account. <br>
Mitigation: Review every generated strategy and test it in backtest or simulation before enabling live execution. <br>
Risk: A bundled template may sell all account positions or rebalance positions not created by the generated strategy. <br>
Mitigation: Restrict sell and rebalance logic to strategy-owned holdings and confirm position filters before running the code. <br>
Risk: The evidence security guidance identifies a moving-average template bug. <br>
Mitigation: Fix and retest the moving-average template logic before using generated strategies for trading decisions. <br>
Risk: Margin, futures, fund-transfer, and notification credential APIs can increase operational or financial exposure. <br>
Mitigation: Do not enable those capabilities without explicit limits, credential controls, and monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/weistiger/ptrade-strategy) <br>
- [README](artifact/README.md) <br>
- [Knowledge Base Document Index](artifact/kb_ref.md) <br>
- [PTRADE Strategy Templates](artifact/templates/) <br>
- [IMA Knowledge Base](https://ima.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and concise usage notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated strategy code should be reviewed, backtested, and adjusted before live trading.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
