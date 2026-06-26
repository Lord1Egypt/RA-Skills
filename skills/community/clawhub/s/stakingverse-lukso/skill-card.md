## Description: <br>
Stake LYX tokens on Stakingverse for LUKSO liquid staking, including staking, unstaking, claiming rewards, and checking sLYX balances through the deposit, withdrawal request, and oracle-claim pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LUKSOAgent](https://clawhub.ai/user/LUKSOAgent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Stakingverse LUKSO liquid-staking actions, including staking LYX, requesting unstake, claiming processed withdrawals, and checking sLYX or claimable balances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill signs real LUKSO mainnet transactions that can move or lock assets. <br>
Mitigation: Review each transaction before execution, start with a small amount, and confirm gas costs and unstaking delays. <br>
Risk: The scripts use a raw controller private key for transaction signing. <br>
Mitigation: Use a dedicated low-permission controller key and avoid storing or pasting long-lived private keys in shell history. <br>
Risk: Incorrect vault, Universal Profile, or Key Manager addresses could cause irreversible asset effects. <br>
Mitigation: Independently verify the Stakingverse vault and account addresses before running stake, unstake, or claim commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LUKSOAgent/stakingverse-lukso) <br>
- [Stakingverse app](https://app.stakingverse.io) <br>
- [Stakingverse docs](https://docs.stakingverse.io) <br>
- [LUKSO docs](https://docs.lukso.tech) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute or describe LUKSO mainnet staking, unstaking, claim, and balance-check operations when configured with wallet credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
