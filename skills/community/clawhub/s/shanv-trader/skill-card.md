## Description: <br>
Provides AI-assisted semi-automatic stock trading with signal scanning, trade confirmation, risk control, execution, and position monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and trading-agent operators use this skill to scan stock signals, prepare trade suggestion cards, execute confirmed buy or sell actions, and monitor portfolio risk alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect brokerage or trading workflows if execution scripts are connected to a live account. <br>
Mitigation: Review the skill before use and require a separate human confirmation process before running execute_trade.py against a live account. <br>
Risk: The security evidence identifies weak safety controls and an unsafe shell command path in stock-price handling. <br>
Mitigation: Fix the shell=True stock-price call and strengthen risk controls before trusting the skill with real portfolio data. <br>
Risk: Local trade logs and portfolio records may contain sensitive financial data. <br>
Mitigation: Review local log handling and protect generated trade, suggestion, and portfolio files according to the user's data-security requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/shanv-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with generated JSON log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trade suggestion cards, position-monitoring summaries, confirmation prompts, and local trade or suggestion records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
