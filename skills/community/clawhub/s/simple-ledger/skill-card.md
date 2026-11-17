## Description:

Log expenses, check balances, track budgets, set savings goals, and monitor stock/fund/ETF investments from natural language. Plain-text CSV storage, multi-account, offline-first with optional real-time quotes via opt-in network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsag1](https://clawhub.ai/user/tsag1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to record personal spending, query balances, manage budgets, track savings goals, and monitor investment holdings from natural-language prompts backed by local CSV/JSON files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some script reads and writes may not enforce the declared ledger-folder boundary.

Mitigation: Keep ledger data under ~/.openclaw/workspace/data/ledger/**, avoid arbitrary file paths, and review execution before enabling the skill.

Risk: Local finance records are modified directly in persistent CSV/JSON files.

Mitigation: Back up ledger data regularly and review parsed entries before write or delete operations.

Risk: Optional live quote features use akshare and public market-data services, which can reveal queried security names or codes.

Mitigation: Use offline mode by default, enable network access only when needed, and consider pinning or isolating akshare before live quote use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsag1/skills/simple-ledger)
- [User Guide](references/user_guide.md)
- [Ledger File Format](references/ledger_format.md)
- [Budget Management Guide](references/budget_guide.md)
- [Savings Goal Guide](references/goal_guide.md)
- [Investment Tracking Guide](references/invest_guide.md)
- [Investment Command Reference](references/invest_api.md)
- [Financial Benchmarks](references/financial_benchmarks.md)
- [Financial Education Reference](references/education.md)
- [AkShare](https://akshare.xyz)
- [Sina Finance](https://finance.sina.com.cn)
- [Eastmoney](https://www.eastmoney.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands; scripts update local CSV/JSON ledger files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 scripts; investment quote features require akshare and explicit network opt-in.]

## Skill Version(s):

104.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
