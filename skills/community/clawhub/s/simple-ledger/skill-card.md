## Description: <br>
Ledger assistant: a simple expense tracker for daily spending. Log expenses, check balances, track budgets, and manage investments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsag1](https://clawhub.ai/user/tsag1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a local personal-finance ledger, track budgets and goals, and monitor investment records with optional market-data refreshes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directly changes local personal-finance CSV/JSON files. <br>
Mitigation: Back up the ledger directory before use, review proposed changes, and require confirmation for destructive or investment write operations. <br>
Risk: Optional market-data refreshes can reveal queried securities to third-party market-data providers. <br>
Mitigation: Enable network-backed quote refresh only when that disclosure is acceptable; routine ledger, budget, and report tasks can remain local. <br>
Risk: Financial summaries and investment calculations may be incomplete or unsuitable as financial advice. <br>
Mitigation: Use outputs for recordkeeping and basic analysis, and verify calculations before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsag1/simple-ledger) <br>
- [User guide](references/user_guide.md) <br>
- [Ledger format](references/ledger_format.md) <br>
- [Budget guide](references/budget_guide.md) <br>
- [Investment guide](references/invest_guide.md) <br>
- [Financial benchmarks](references/financial_benchmarks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples and local CSV/JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local ledger, budget, goal, and investment files under the user's ledger data directory; market-data refresh is opt-in.] <br>

## Skill Version(s): <br>
102.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
