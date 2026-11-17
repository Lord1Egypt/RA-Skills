## Description:

ProxyGate CLI router directs ProxyGate-related requests to the appropriate setup, status, buying, selling, jobs, or update sub-skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this router to select the correct ProxyGate sub-skill for setup, wallet and balance checks, marketplace buying, seller operations, bounties, jobs, and CLI or SDK updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger conditions may route unrelated requests into sub-skills that can touch wallets, payments, tunnels, listings, withdrawals, or jobs.

Mitigation: Install only for ProxyGate-specific routing and verify explicit ProxyGate intent before routing.

Risk: Downstream sub-skills may support account-changing or financial operations.

Mitigation: Require confirmation before wallet, payment, withdrawal, listing, tunnel, or job actions.

## Reference(s):

- [ProxyGate gateway documentation](https://gateway.proxygate.ai/docs)
- [ProxyGate gateway](https://gateway.proxygate.ai)
- [ClawHub skill page](https://clawhub.ai/jwelten/skills/proxygate)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and routing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes ProxyGate requests to specialized sub-skills and may propose CLI commands for wallet, payments, listings, tunnels, and jobs.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
