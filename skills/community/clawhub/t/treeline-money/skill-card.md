## Description:

Chat with your finances from Treeline Money. Query balances, spending, budgets, and transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-schrag](https://clawhub.ai/user/zack-schrag)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query local Treeline Money data for balances, net worth, spending, budgets, transactions, and CSV import guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a native Treeline CLI from latest-release links rather than a pinned artifact.

Mitigation: Verify the CLI source and version before use, and prefer a pinned release artifact for repeatable deployments.

Risk: The agent may read sensitive local financial data from the user's Treeline database.

Mitigation: Use read-only commands by default, keep financial details within the conversation, and avoid storing account meanings or preferences unless the user explicitly chooses what is saved.

Risk: Write-capable commands can modify local financial records or backups.

Mitigation: Require explicit user confirmation before write operations and use dry-run variants for sync or import previews.

Risk: Encrypted databases require user credentials or keychain access to unlock.

Mitigation: Have the user unlock the database outside the agent conversation; the agent should not handle credentials or attempt unlock steps.

Risk: Financial aggregates can be misleading if queries ignore Treeline conventions for signs, transfers, tags, or balance snapshots.

Mitigation: Use the Treeline query cookbook and JSON CLI output for canonical calculations and parseable results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-schrag/skills/treeline-money)
- [Treeline Money](https://treeline.money)
- [Treeline bank sync documentation](https://treeline.money/docs/integrations/bank-sync/)
- [Treeline CSV import documentation](https://treeline.money/docs/integrations/csv-import/)
- [Treeline query cookbook for AI agents](https://docs.treeline.money/ai-agents/query-cookbook/)
- [Treeline CLI macOS download](https://github.com/treeline-money/treeline/releases/latest/download/tl-macos-arm64)
- [Treeline CLI Linux download](https://github.com/treeline-money/treeline/releases/latest/download/tl-linux-x64)
- [Treeline CLI Windows download](https://github.com/treeline-money/treeline/releases/latest/download/tl-windows-x64.exe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local tl CLI; read-only queries should use --json, while write actions require user confirmation.]

## Skill Version(s):

26.8.1901 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
