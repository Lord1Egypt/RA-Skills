## Description: <br>
Private agent-to-agent payments on Solana using zero-knowledge proofs. Deposit, withdraw, list pools, and estimate fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentzeny](https://clawhub.ai/user/agentzeny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to operate SNAP private payment workflows on Solana, including listing pools, depositing funds, withdrawing funds, estimating withdrawal fees, and checking shielded balances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate real Solana payment workflows and may move funds. <br>
Mitigation: Use small test amounts and a limited wallet first, and require explicit approval before every deposit or withdrawal. <br>
Risk: Withdrawals and balance checks use sensitive shielded-fund secrets such as notes and viewing keys. <br>
Mitigation: Keep notes and viewing keys out of logs and shared prompts, and require approval before any command uses them. <br>
Risk: The evidence notes missing shared helper code and external SDK behavior that should be reviewed before deployment. <br>
Mitigation: Review the full SNAP SDK and helper implementation before using the skill with production funds. <br>
Risk: Untrusted RPC or relayer endpoints can affect transaction handling and privacy assumptions. <br>
Mitigation: Use trusted RPC and relayer endpoints configured explicitly through the skill environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentzeny/snap-private-payments) <br>
- [SNAP SDK](https://www.npmjs.com/package/snap-solana-sdk) <br>
- [SNAP Website](https://agentzeny.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text responses, JSON pool listings, and setup/configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Solana transaction signatures, fee estimates, pool listings, or shielded balance text depending on the command.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
