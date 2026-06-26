## Description: <br>
Chat with your finances from Treeline Money. Query balances, spending, budgets, and transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-schrag](https://clawhub.ai/user/zack-schrag) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect local Treeline Money financial data, answer questions about balances, spending, budgets, and transactions, and guide setup or imports with user confirmation for changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent read sensitive local Treeline financial data. <br>
Mitigation: Install and use it only when comfortable with agent access to local finance data; start in demo mode when unsure. <br>
Risk: Some Treeline commands can change local data, sync accounts, import transactions, restore backups, tag records, compact data, run write-enabled SQL, or save user skills. <br>
Mitigation: Require explicit user confirmation before running mutating commands and review paths and contents before allowing persistent writes. <br>
Risk: Encrypted databases require user-controlled unlocking and may expose credentials if handled in-chat. <br>
Mitigation: Have the user unlock the database directly through Treeline or their own terminal; do not handle credentials in the agent conversation. <br>


## Reference(s): <br>
- [Treeline Money](https://treeline.money) <br>
- [Treeline Download](https://treeline.money/download) <br>
- [Bank Sync Guide](https://treeline.money/docs/integrations/bank-sync/) <br>
- [CSV Import Guide](https://treeline.money/docs/integrations/csv-import/) <br>
- [Treeline CLI macOS download](https://github.com/treeline-money/treeline/releases/latest/download/tl-macos-arm64) <br>
- [Treeline CLI Linux download](https://github.com/treeline-money/treeline/releases/latest/download/tl-linux-x64) <br>
- [Treeline CLI Windows download](https://github.com/treeline-money/treeline/releases/latest/download/tl-windows-x64.exe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-aware command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should be concise and mobile-readable; CLI commands should prefer JSON output where available.] <br>

## Skill Version(s): <br>
26.5.2402 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
