## Description:

Revolut Business API CLI for accounts, balances, transactions, counterparties, payments, FX exchange, CSV export, and OAuth token refresh for business accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianhaberl](https://clawhub.ai/user/christianhaberl)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and finance users with a Revolut Business account use this skill to inspect account data, export transactions, manage counterparties, initiate payments, exchange currency, and move funds between business accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Revolut Business financial data and perform money-moving operations.

Mitigation: Use tightly scoped Revolut permissions and payment limits, review commands before execution, and avoid bypassing confirmations with --yes.

Risk: Local private keys and OAuth tokens are sensitive and are stored under the user's Revolut state directory.

Mitigation: Store credentials with strict owner-only permissions or in a secure secret store, and never share private keys, tokens, or client assertion JWTs.

Risk: The authoritative security guidance calls out a setup command-injection issue and weak guardrails.

Mitigation: Fix or mitigate the setup command-injection issue before use, require confirmation for FX and transfers, and pin dependencies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/christianhaberl/skills/revolut-business)
- [Publisher Profile](https://clawhub.ai/user/christianhaberl)
- [Revolut Business API Endpoint](https://b2b.revolut.com/api/1.0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV]

**Output Format:** [CLI text output, JSON responses, CSV exports, and Markdown setup guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write OAuth tokens, private keys, certificates, configuration, and optional CSV exports to local files.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
