## Description: <br>
Interact with the Xero accounting API using the `xero` CLI tool. Manage contacts, invoices, quotes, credit notes, payments, bank transactions, items, manual journals, tracking categories, currencies, tax rates, reports, and organisation details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xeroapi](https://clawhub.ai/user/xeroapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, finance operators, and accounting teams use this skill to let an agent work with Xero organisation data through the Xero CLI. It supports read workflows, reporting, and user-approved accounting writes such as invoices, contacts, payments, and journals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Xero organisation and financial data through OAuth credentials. <br>
Mitigation: Grant only the OAuth scopes needed for the task and install the skill only when agent access to the Xero organisation is intended. <br>
Risk: Write commands can create, update, or delete accounting records in the wrong organisation if profile selection is mistaken. <br>
Mitigation: Confirm the active organisation with `xero org details`, use explicit profiles when applicable, and require a clear user-approved write summary before execution. <br>
Risk: File-based or environment-variable token key fallbacks can weaken credential protection on shared or remotely administered machines. <br>
Mitigation: Prefer keychain-backed token storage and avoid file or environment-variable fallbacks unless the user understands the tradeoff. <br>


## Reference(s): <br>
- [Xero command line homepage](https://github.com/XeroAPI/xero-command-line#readme) <br>
- [Xero command line source](https://github.com/XeroAPI/xero-command-line) <br>
- [TOON format](https://github.com/toon-format/toon) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend TOON, JSON, CSV, or table output depending on parsing and presentation needs.] <br>

## Skill Version(s): <br>
0.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
