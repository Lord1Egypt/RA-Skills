## Description:

SkillPay adds credit-based payments to OpenClaw skills so builders can register paid skills, charge per call, track earnings, and withdraw USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adjusternwachukwu-bot](https://clawhub.ai/user/adjusternwachukwu-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and skill builders use SkillPay to add pay-per-use credit flows to OpenClaw skills, including user credit purchases, builder registration, per-call charges, earnings checks, and USDC withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable user and builder payment credentials can act as bearer secrets.

Mitigation: Treat `sp_usr_...` and `sp_bld_...` values as sensitive credentials, avoid sharing them with untrusted skills, and rotate or revoke them when exposure is suspected.

Risk: Deposit, withdrawal, and payment commands can move credits or funds if run with valid credentials.

Mitigation: Verify the amount, account, destination wallet, and revocation options before running payment-related commands.

## Reference(s):

- [SkillPay ClawHub listing](https://clawhub.ai/adjusternwachukwu-bot/skills/skill-pay)
- [SkillPay API base](https://skillpay.gpupulse.dev/api/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint examples and bearer-token usage patterns.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
