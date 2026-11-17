## Description:

Helps users stake LYX, request unstaking, claim processed withdrawals, and check sLYX balances on Stakingverse liquid staking for LUKSO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luksoagent](https://clawhub.ai/user/luksoagent)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Stakingverse LUKSO liquid staking workflows, including staking LYX, checking sLYX balances, requesting unstake, and claiming processed withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a wallet or controller private key and can send LUKSO mainnet transactions involving real funds.

Mitigation: Review before installing or running it with real funds, use a dedicated low-value least-privileged controller key when possible, and never paste private keys into scripts, repositories, shell history, logs, or shared automation.

Risk: On-chain staking, unstaking, and claiming actions can incur gas costs and may be irreversible after submission.

Mitigation: Verify the LUKSO mainnet, Universal Profile, Key Manager, vault address, and amount before every run.

Risk: The security evidence reports ABI defects in the unstake and claim scripts and notes that SKILL.md references a check-claim.js file that is not present.

Mitigation: Inspect and test the scripts against the intended Stakingverse contracts before relying on unstake or claim flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luksoagent/skills/stakingverse-lukso)
- [Stakingverse App](https://app.stakingverse.io)
- [Stakingverse Docs](https://docs.stakingverse.io)
- [LUKSO Docs](https://docs.lukso.tech)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of scripts that read wallet, Universal Profile, controller, and LUKSO RPC configuration from environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
