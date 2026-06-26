## Description: <br>
Autonomously monitor live sports games and execute micro-bets on one-touch barrier options with instant mockUSDC settlement on Solana Devnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigabit-eth](https://clawhub.ai/user/gigabit-eth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use this skill to register with Optionns, inspect live sports markets, and execute or monitor Solana Devnet mockUSDC micro-bets. It is intended for devnet-only experimentation with autonomous sports trading workflows, not real funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad authority to sign and submit Solana devnet transactions automatically. <br>
Mitigation: Use only throwaway devnet wallets, avoid real private keys and mainnet RPC endpoints, and define explicit spending and stop conditions before using autonomous mode. <br>
Risk: The skill depends on a remote Optionns API and stores credentials and a devnet keypair locally. <br>
Mitigation: Review api.optionns.com trust, run in an isolated environment, keep generated files permission-restricted, and rotate or delete credentials after use. <br>


## Reference(s): <br>
- [Optionns API Reference](references/api.md) <br>
- [Optionns Homepage](https://optionns.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/gigabit-eth/sports) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local credential, keypair, and position log files during use.] <br>

## Skill Version(s): <br>
1.0.24 (source: ClawHub release evidence; artifact metadata reports 1.0.23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
