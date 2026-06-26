## Description: <br>
QuickBooks Online CLI tool for managing customers, invoices, payments, bills, vendors, accounts, items, expenses, journal entries, deposits, transfers, estimates, purchase orders, and financial reports through the Intuit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulbudveit](https://clawhub.ai/user/paulbudveit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Finance and operations users and their agents use this skill to inspect and manage QuickBooks Online accounting records, run reports, support month-end workflows, and prepare bookkeeping actions through command-line operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, void, send, import, and otherwise modify real QuickBooks accounting records. <br>
Mitigation: Use a QuickBooks sandbox first and require explicit user approval before any accounting operation that changes, sends, imports, transfers, pays, voids, deletes, batches, or changes preferences. <br>
Risk: The artifact installs external code from an unpinned GitHub repository before building a Docker image. <br>
Mitigation: Pin or inspect the repository source before building and installing. <br>
Risk: QuickBooks client credentials and OAuth tokens are required for operation. <br>
Mitigation: Protect the .env file and OAuth tokens, and avoid exposing credentials in logs, prompts, or shared workspaces. <br>


## Reference(s): <br>
- [QuickBooks Online CLI source](https://github.com/claw4business/quickbooks-online-cli) <br>
- [QuickBooks developer portal](https://developer.intuit.com) <br>
- [ClawHub skill page](https://clawhub.ai/paulbudveit/quickbooks-online) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands default to JSON output for agent consumption and may also produce table, CSV, or workspace files when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
