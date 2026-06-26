## Description: <br>
基于A股行情数据计算SAR抛物线指标，并用机构资金流向近似替代ZJTJ庄家抬轿指标，实现四维选股策略。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohanyang92](https://clawhub.ai/user/haohanyang92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to draft Python-based A-share screening workflows that calculate SAR trend signals and approximate ZJTJ-style institutional activity signals. It supports single-stock analysis, batch screening, and concise buy-signal summaries for further human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce buy recommendations from heuristic technical and fund-flow signals. <br>
Mitigation: Treat recommendations as screening aids only, verify market data and calculations independently, and do not use the output as financial advice or as the sole basis for trading decisions. <br>
Risk: The ZJTJ signal is an approximation of a paid indicator and may differ from the original indicator. <br>
Mitigation: Review the approximation logic before use and compare it with independent indicators or domain expertise when evaluating stocks. <br>
Risk: The cited data source and documented/code behavior may be unstable or mismatched. <br>
Mitigation: Check AkShare availability, validate returned fields for the target market, and test the workflow on known examples before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haohanyang92/zjtj-sar-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python code blocks and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include heuristic stock-screening signals, SAR values, ZJTJ approximation scores, volume checks, and recommendation flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
