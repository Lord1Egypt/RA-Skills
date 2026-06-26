## Description: <br>
Interact with Xero accounting software to manage invoices, contacts, accounts, payments, and bank transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TeddyEngel](https://clawhub.ai/user/TeddyEngel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to authenticate with Xero and manage accounting records through CLI commands that return JSON. It supports common accounting workflows such as listing tenants, creating invoices and contacts, recording payments, attaching receipts, and allocating credits or prepayments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Xero accounting access can modify financial records, including invoices, payments, bank transactions, allocations, attachments, and reconciliation state. <br>
Mitigation: Use a test tenant first, limit Xero app scopes where possible, and require explicit human review before create, authorize, void, delete, allocate, reconcile, or attach operations. <br>
Risk: Reusable OAuth tokens are stored locally in plaintext at data/tokens.json. <br>
Mitigation: Protect or delete the token file after use, run auth logout when finished, and revoke the Xero app if access is no longer needed. <br>


## Reference(s): <br>
- [Xero API Examples Reference](references/api-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/TeddyEngel/xero-cli) <br>
- [Publisher profile](https://clawhub.ai/user/TeddyEngel) <br>
- [Project homepage](https://github.com/TeddyEngel/XeroCli) <br>
- [Xero developer app management](https://developer.xero.com/app/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through the bundled CLI and generally return JSON for agent parsing.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
