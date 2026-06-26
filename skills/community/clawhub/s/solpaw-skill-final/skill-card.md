## Description: <br>
Launch Solana tokens on Pump.fun via the SolPaw platform with a 0.1 SOL one-time fee, using the configured wallet as the claimed on-chain creator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LvcidPsyche](https://clawhub.ai/user/LvcidPsyche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to configure an OpenClaw agent to launch Solana tokens on Pump.fun through SolPaw, including agent registration, fee payment, token metadata, image handling, transaction signing, and launch status retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires private-key-capable wallet authority and can initiate high-impact token-launch actions. <br>
Mitigation: Use only a dedicated low-balance wallet, never a main wallet private key, and require explicit user approval before any payment, signing, or launch submission. <br>
Risk: Launch fees and token deployments may be irreversible once submitted. <br>
Mitigation: Manually confirm the fee recipient, exact SOL amounts, token name, symbol, metadata, image, initial buy amount, and final transaction contents before signing. <br>
Risk: Evidence notes inconsistent local-mode versus server-signed launch documentation, which affects who is the on-chain creator. <br>
Mitigation: Prefer local unsigned-transaction signing, verify the decoded transaction creator before submission, and do not rely on the creator claim until the publisher resolves the mismatch. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LvcidPsyche/solpaw-skill-final) <br>
- [SolPaw website](https://solpaw.fun) <br>
- [SolPaw API Reference](references/api-docs.md) <br>
- [SolPaw API documentation](https://solpaw.fun/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, TypeScript examples, configuration snippets, and JSON-shaped API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, SOLPAW_API_KEY, SOLPAW_CREATOR_WALLET, and SOLANA_PRIVATE_KEY; launches require Solana wallet funds and user confirmation.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
