## Description: <br>
Launch Solana tokens on Pump.fun via the SolPaw platform. 0.1 SOL one-time fee. Your wallet is the onchain creator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LvcidPsyche](https://clawhub.ai/user/LvcidPsyche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and launch Solana tokens on Pump.fun through SolPaw, including API registration, fee payment, image upload, local transaction signing, and submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid, irreversible token launches using wallet authority. <br>
Mitigation: Use a dedicated low-balance wallet, set external spending limits, and verify the platform wallet, fee amount, token metadata, creator address, and decoded transaction before signing or submitting. <br>
Risk: The security review reports a mismatch between the promised local-creator flow and the included SDK launch flow. <br>
Mitigation: Use the documented Local Mode flow and avoid the included SDK launchToken flow until the Local Mode versus server-signed endpoint mismatch is fixed. <br>
Risk: The skill requires API keys and wallet private-key material in the agent environment. <br>
Mitigation: Do not use a main wallet private key; keep credentials scoped to this workflow and review the action before the agent signs or submits any transaction. <br>


## Reference(s): <br>
- [SolPaw homepage](https://solpaw.fun) <br>
- [SolPaw API Reference](references/api-docs.md) <br>
- [ClawHub skill page](https://clawhub.ai/LvcidPsyche/solpaw-skill-v2) <br>
- [Pump.fun](https://pump.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, TypeScript, JSON, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, a SolPaw API key, Solana wallet configuration, and local review before signing paid onchain transactions.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
