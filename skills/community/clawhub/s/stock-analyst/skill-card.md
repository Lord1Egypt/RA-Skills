## Description: <br>
股票综合分析，融合基本面分析、技术分析、量化与行为金融分析三大体系，为投资者提供多维度的选股和择时建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris3cano-ship-it](https://clawhub.ai/user/chris3cano-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to produce structured stock and market analyses covering fundamentals, technical signals, quantitative and behavioral factors, conclusions, ratings, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically write report files and run a local browser/server PDF workflow after analysis. <br>
Mitigation: Disable or override the automatic PDF workflow unless the user explicitly requests an exported report, and review file paths before execution. <br>
Risk: Financial analysis may be incomplete, stale, or misleading if public market data is unavailable or misunderstood. <br>
Mitigation: Verify stock data and investment conclusions independently; treat outputs as informational and not financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris3cano-ship-it/stock-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis report with optional HTML/PDF report workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill asks the agent to generate a stock analysis report and may create local HTML/PDF files after analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
