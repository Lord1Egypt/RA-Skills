## Description:

Interact with the Xero accounting API using the `xero` CLI tool to manage contacts, invoices, quotes, credit notes, payments, bank transactions, items, manual journals, tracking categories, currencies, tax rates, reports, and organisation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xeroapi](https://clawhub.ai/user/xeroapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance operations users can use this skill to guide an agent in running the Xero CLI for accounting workflows, including reading organisation data and preparing approved changes to financial records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can access financial data in a Xero organisation.

Mitigation: Use read-only scopes when possible and confirm the active organisation/profile before any command.

Risk: Write commands can create or change accounting records.

Mitigation: Review IDs and target records with read-only commands first, then require explicit user approval before each write.

Risk: Token storage settings can weaken credential protection on Linux, WSL, SSH, or headless systems.

Mitigation: Prefer OS keychain storage, treat file-based fallback and passphrase settings as sensitive, and review relevant environment variables before use.

Risk: Global npm installation affects the user's local toolchain.

Mitigation: Review the npm install command before running it and install only when the user intends to use the Xero CLI.

## Reference(s):

- [Xero command line homepage](https://github.com/XeroAPI/xero-command-line#readme)
- [Xero command line source](https://github.com/XeroAPI/xero-command-line)
- [TOON format](https://github.com/toon-format/toon)
- [ClawHub skill page](https://clawhub.ai/xeroapi/skills/xero-command-line)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to prefer TOON for parsing CLI read/list results, JSON when explicitly needed, and tables for user-facing summaries.]

## Skill Version(s):

0.0.6 (source: server release metadata, created 2026-05-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
