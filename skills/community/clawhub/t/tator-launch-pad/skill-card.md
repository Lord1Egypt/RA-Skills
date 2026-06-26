## Description: <br>
Helps agents launch and manage tokens through Tator Easy Mode or direct Clanker, Flaunch, and Pump.fun integrations, including fee strategy, claiming, recipient updates, and security guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azep-ninja](https://clawhub.ai/user/azep-ninja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and token builders use this skill to evaluate token-launch strategy, choose between Tator Easy Mode and direct platform integrations, prepare launch or fee-management calls, and understand the operational and security tradeoffs before signing transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real token launches and fee-management transactions that may be irreversible once signed and broadcast. <br>
Mitigation: Require explicit human approval before signing or broadcasting any transaction, and inspect all returned unsigned transactions before approval. <br>
Risk: Direct Mode requires wallet-key handling and blockchain RPC access in the user's own infrastructure. <br>
Mitigation: Use a dedicated low-balance launch wallet, store secrets in a secrets manager, pin dependencies, verify contract addresses, and keep keys out of plaintext files. <br>
Risk: Easy Mode sends the public wallet address, prompt, and provider name to the Tator API. <br>
Mitigation: Avoid putting sensitive business or personal data in prompts, and review returned transactions locally before signing. <br>


## Reference(s): <br>
- [Token Launcher - Tator Launch Pad on ClawHub](https://clawhub.ai/azep-ninja/tator-launch-pad) <br>
- [Tator API documentation](https://docs.tator.bot) <br>
- [Direct Mode reference](REFERENCE.md) <br>
- [Clanker v4 direct mode reference](references/clanker.md) <br>
- [Flaunch direct mode reference](references/flaunch.md) <br>
- [Pump.fun direct mode reference](references/pumpfun.md) <br>
- [Clanker SDK docs](https://clanker.gitbook.io/clanker-documentation/sdk/v4.0.0) <br>
- [Flaunch builder docs](https://docs.flaunch.gg/for-builders) <br>
- [Pump.fun public docs](https://github.com/pump-fun/pump-public-docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API examples, JSON payloads, shell commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; Easy Mode returns unsigned transactions for local signing, while Direct Mode guides SDK and wallet integration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
