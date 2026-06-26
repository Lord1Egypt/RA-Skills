## Description: <br>
Stock Entry Analyzer helps agents analyze stock or fund entry timing with BIAS, moving averages, MACD, RSI, KDJ, volume, fund-flow, and valuation signals, then produce a checklist and composite score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuli4](https://clawhub.ai/user/liuli4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agent workflows use this skill to screen single or multiple equities or funds for potential entry conditions and generate concise markdown reports. Its outputs are informational analysis and should not be treated as personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some helper scripts can read a local Eastmoney API key from the OpenClaw vault. <br>
Mitigation: Review credential access before installation and run only in environments where that credential use is expected. <br>
Risk: Some scripts can pass the broader process environment to another local data script. <br>
Mitigation: Run the skill with a minimal environment and avoid exposing unrelated secrets to scheduled or automated runs. <br>
Risk: Scheduled monitoring could amplify incorrect thresholds, stale market data, or misleading entry signals. <br>
Mitigation: Keep automated monitoring disabled until credential handling and threshold consistency have been reviewed, and require human review before acting on outputs. <br>
Risk: The reports may be mistaken for personalized financial advice. <br>
Mitigation: Present outputs as informational technical analysis and pair them with independent financial review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuli4/stock-entry-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/liuli4) <br>
- [Indicator reference](references/indicators.md) <br>
- [Liu Chenming method reference](references/liu-chenming-method.md) <br>
- [Scoring rules](references/scoring-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with scores, checklists, tables, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on current market data and configured data-source skills; conclusions can change as prices and indicators update.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and README; artifact/_meta.json reports 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
