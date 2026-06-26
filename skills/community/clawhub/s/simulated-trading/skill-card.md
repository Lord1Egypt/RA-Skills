## Description: <br>
A simulated trading skill for creating portfolios, placing and matching buy and sell orders, managing market data, and calculating NAV and portfolio performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenge791](https://clawhub.ai/user/stevenge791) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run paper-trading workflows, including portfolio setup, simulated stock or ETF orders, order matching, NAV snapshots, and performance analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The price refresh flow reads an EM_API_KEY value and the release is tagged as requiring sensitive credentials. <br>
Mitigation: Pass EM_API_KEY only for the specific run when possible and avoid storing long-lived credentials in a shell profile. <br>
Risk: Portfolio symbols may be sent to Eastmoney by default during automatic price refresh. <br>
Mitigation: Use --no-refresh when portfolio symbols should remain local or when cached prices are sufficient. <br>
Risk: Delete commands can permanently remove local simulated-trading data. <br>
Mitigation: Back up the SQLite database and verify portfolio or symbol identifiers before running delete operations. <br>


## Reference(s): <br>
- [Database schema reference](references/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/stevenge791/simulated-trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise text or Markdown guidance with shell commands; the included scripts emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database and can refresh market prices through Eastmoney when configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
