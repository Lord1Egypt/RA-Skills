## Description:

Wallet-aware Raven Atlas transfer operations for NGN payouts that help an agent check wallet balance, resolve Nigerian bank accounts, enforce explicit confirmation tokens, and execute idempotent confirmed transfers to bank beneficiaries or merchant settlement accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmacmak](https://clawhub.ai/user/fmacmak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run confirmation-gated Raven Atlas NGN payouts to Nigerian bank beneficiaries or merchant settlement accounts while checking wallet funds, resolving account names, and verifying transfer status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real NGN transfers after confirmation.

Mitigation: Require human review for each confirmed transfer, verify balance and account lookup first, use the exact confirmation token, and check settlement status before any resend decision.

Risk: A configured API base can receive the Raven API key and transfer details.

Mitigation: Use the default Raven endpoint unless the replacement endpoint is fully controlled and trusted, store the API key in a locked-down secret source, and prefer a restricted Raven API key where available.

Risk: Local idempotency state can persist transfer reference metadata.

Mitigation: Keep state files owner-only, exclude the state directory from sync and backups, or set RAVEN_DISABLE_LOCAL_STATE=1 when local persistence is unsuitable.

## Reference(s):

- [Raven NGN Transfers on ClawHub](https://clawhub.ai/fmacmak/skills/raven-transfer)
- [Workflow](references/workflow.md)
- [Command Reference](references/commands.md)
- [Safety and Reliability](references/safety.md)
- [Installation](references/install.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results use a success or failure JSON envelope and include normalized balance, fee, total debit, status, and reference fields when available.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
