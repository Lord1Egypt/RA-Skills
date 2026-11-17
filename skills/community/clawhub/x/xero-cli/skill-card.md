## Description:

Interact with Xero accounting software - manage invoices, contacts, accounts, payments, and bank transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teddyengel](https://clawhub.ai/user/teddyengel)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance operators use this skill to let an agent manage Xero accounting data through a CLI, including invoices, contacts, accounts, payments, bank transactions, tenant selection, and allocations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make write-capable changes to financial records, including create, update, delete, void, allocation, and file-attachment operations.

Mitigation: Use a test Xero organization first and require explicit user approval before any command that changes records or uploads files.

Risk: OAuth tokens are stored in a local tokens.json file with weak controls.

Mitigation: Secure or relocate the token file, avoid sharing the workspace, and clear tokens when access is no longer needed.

Risk: Broad OAuth scopes and production credentials could expose sensitive accounting data.

Mitigation: Restrict Xero OAuth scopes where possible and avoid production credentials until dependencies and runtime are reviewed and pinned.

## Reference(s):

- [Xero API Examples Reference](references/api-examples.md)
- [Xero Developer App Management](https://developer.xero.com/app/manage)
- [XeroCli Homepage](https://github.com/TeddyEngel/XeroCli)
- [ClawHub Xero Cli Skill Page](https://clawhub.ai/teddyengel/skills/xero-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [JSON responses and Markdown instructions with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XERO_CLIENT_ID and XERO_CLIENT_SECRET; commands may read, create, update, delete, void, allocate, and attach files in Xero.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence and target metadata; bundled CLI reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
