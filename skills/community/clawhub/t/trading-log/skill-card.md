## Description:

Trading Log records stock buy and sell transactions, calculates holdings and profit/loss, and can refresh live A-share and Hong Kong stock quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wtjjacobj](https://clawhub.ai/user/wtjjacobj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Trading Log to record stock transactions, review current holdings, and generate realized and unrealized profit/loss reports from a local JSON ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading history is stored in a plaintext Desktop JSON file.

Mitigation: Store only records appropriate for local plaintext storage, protect Desktop backups, and remove or redact the ledger before sharing the machine or files.

Risk: Live quote refresh sends stock symbols to Tencent quote endpoints.

Mitigation: Use live price commands only when symbol disclosure to Tencent is acceptable; use non-live position views when it is not.

Risk: Malformed trade entries or clear-position commands can distort local profit/loss records.

Mitigation: Review command arguments before execution and keep a backup of the ledger before edits, imports, or clear-position operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wtjjacobj/skills/trading-log)
- [Tencent quote endpoint used for live prices](https://qt.gtimg.cn/q=sh600519,sz000001,...)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local plaintext JSON trading ledger on the user's Desktop.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
