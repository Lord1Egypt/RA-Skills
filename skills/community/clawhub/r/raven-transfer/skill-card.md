## Description: <br>
Wallet-aware Raven Atlas transfer operations for NGN payouts. Use when an agent must check wallet balance, resolve Nigerian bank accounts, enforce explicit confirmation tokens, and execute idempotent confirmed transfers to bank beneficiaries or merchant settlement accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fmacmak](https://clawhub.ai/user/Fmacmak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check Raven NGN wallet balances, resolve Nigerian bank accounts, preview payouts, and execute confirmed bank or merchant settlement transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real NGN payouts. <br>
Mitigation: Install only for intentional Raven payout workflows, keep implicit invocation disabled, and require the agent to show recipient, amount, fee, total debit, and balance impact before any --confirm command. <br>
Risk: Credential exposure could allow unauthorized Raven API use. <br>
Mitigation: Use a dedicated least-privilege Raven key when available and prefer RAVEN_API_KEY_FILE with owner-only file permissions. <br>
Risk: Local state may retain transfer metadata. <br>
Mitigation: Exclude scripts/.state from backups or shared repositories, rely on owner-only permissions, or set RAVEN_DISABLE_LOCAL_STATE=1 when local idempotency state should be disabled. <br>
Risk: Duplicate or premature retries could create unintended payouts. <br>
Mitigation: Use confirmation tokens and idempotency references, do not auto-retry transfer submissions, and check transfer-status plus wallet balance before any resend decision. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Command Reference](references/commands.md) <br>
- [Safety and Reliability](references/safety.md) <br>
- [Installation](references/install.md) <br>
- [Raven Transfer on ClawHub](https://clawhub.ai/Fmacmak/raven-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return normalized JSON envelopes with transfer, balance, fee, status, and settlement fields when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
