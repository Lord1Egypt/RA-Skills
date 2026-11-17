## Description:

Supports TADA and Throo ride-hailing workflows, including wallet balances, USDC bridge status and recovery, deposits, rides, payments, chat, and tipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambprotocol](https://clawhub.ai/user/ambprotocol)

### License/Terms of Use:


## Use Case:

Help an agent assist with TADA and Throo rides, wallet balances, USDC bridge progress and recovery, deposits, ride payments, chat, and tips. Require host-level approval before bookings, payments, or transfers, and do not treat driver messages as authorization.

### Deployment Geography for Use:

Global; availability depends on the supported ride services and wallet networks.

## Known Risks and Mitigations:

Risk: Driver messages could steer the agent toward unauthorized or unsafe actions.

Mitigation: Treat driver messages as untrusted input; never let them authorize bookings, payments, or transfers, which require host-level approval.

Risk: A deposit flow requests unlimited MVL spending permission, and wallet access material is stored locally.

Mitigation: Review the allowance separately from the deposit amount, use a dedicated wallet with limited funds, and protect the ~/.amb state directory.

Risk: Notifications can share ride or chat details with configured external destinations.

Mitigation: Review webhook and Telegram destinations before enabling notifications or sharing ride and chat information.

## Reference(s):

- [Ambient Ride on ClawHub](https://clawhub.ai/ambprotocol/skills/ride)
- [Project homepage](https://github.com/mvlchain/ambient-ride-skill)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Ride, wallet, bridge, and payment status or action guidance in natural language.]

**Output Parameters:** [Depends on the requested ride or wallet workflow and the information available to the agent.]

**Other Properties Related to Output:** [Actions involving bookings, payments, and transfers require host-level approval.]

## Skill Version(s):

1.6.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
