## Description: <br>
Solpaw helps agents launch Solana tokens on Pump.fun through the SolPaw platform using API calls, metadata upload, fee payment, and transaction submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LvcidPsyche](https://clawhub.ai/user/LvcidPsyche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to prepare and launch Solana token listings through SolPaw and Pump.fun. It is intended for workflows that require explicit approval before payment, signing, or token launch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for wallet secrets and can participate in token launches involving a 0.1 SOL platform fee. <br>
Mitigation: Use a low-balance or test wallet, keep wallet secrets out of shared contexts, and require explicit user approval before payment, signing, or launch. <br>
Risk: The security review reports a mismatch between local-signing claims and a shipped launch path that appears to use server-side signing, which can affect on-chain creator attribution. <br>
Mitigation: Do not provide SOLANA_PRIVATE_KEY or send the fee until the maintainer resolves the mismatch; require the /tokens/launch-local plus /tokens/submit flow and independently confirm the platform wallet. <br>
Risk: Token names, symbols, descriptions, or images may be misleading, offensive, or otherwise inappropriate. <br>
Mitigation: Review token content before launch and enforce explicit approval for the final name, symbol, description, and image. <br>


## Reference(s): <br>
- [SolPaw API Reference](references/api-docs.md) <br>
- [SolPaw Documentation](https://solpaw.fun) <br>
- [ClawHub Skill Page](https://clawhub.ai/LvcidPsyche/solpaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, TypeScript snippets, and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOLPAW_API_KEY, SOLPAW_CREATOR_WALLET, SOLANA_PRIVATE_KEY, and curl; launch workflows involve payment and transaction signing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
