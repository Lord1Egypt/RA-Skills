## Description: <br>
Use when the user wants to charge users for actions using @pump-fun/agent-payments-sdk to build Solana payment transactions, verify on-chain invoice payments, or integrate Solana wallet adapters for agent payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Solana-based payment gates to agent workflows, including invoice creation, wallet signing, transaction submission, and server-side payment verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment flows can use incorrect mint, currency, amount, RPC, or framework assumptions. <br>
Mitigation: Collect and confirm all required payment settings before writing code or configuration. <br>
Risk: Private keys or secret key material could be exposed if handled by generated code. <br>
Mitigation: Never request, log, print, or return private keys; build unsigned transactions and require users to sign with their own wallet. <br>
Risk: Client-only payment checks can be spoofed. <br>
Mitigation: Verify every invoice on the server with matching invoice parameters before delivering the paid service. <br>
Risk: Installing unreviewed packages or using an untrusted RPC provider can expand supply-chain and transaction risks. <br>
Mitigation: Confirm the npm package and RPC provider before installation, align dependency versions with the SDK, and review wallet transactions before signing. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/Maliot100X/clawpump-v2/tree/main/base-skills/tokenized-agents) <br>
- [Wallet integration reference](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/references/WALLET_INTEGRATION.md) <br>
- [Scenario tests and troubleshooting reference](https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/references/SCENARIOS.md) <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/tokenized-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, shell, and environment configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to collect required payment, mint, RPC, and framework inputs before generating implementation guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
