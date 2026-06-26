## Description: <br>
Connect and authenticate with an Ethereum wallet to manage Teneo rooms, discover and invite AI agents, send messages, and handle x402 micropayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HunterDrop22](https://clawhub.ai/user/HunterDrop22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill as a practical guide for integrating the Teneo SDK with wallet authentication, room and agent management, real-time messaging, and paid agent requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys may be exposed if copied into code, logs, prompts, or shared configuration. <br>
Mitigation: Keep private keys in secure environment variables or a secret manager and avoid pasting live keys into examples or agent conversations. <br>
Risk: Paid x402 agent requests can spend USDC unintentionally. <br>
Mitigation: Use a dedicated low-balance or test wallet, verify SDK and agent behavior independently, and require explicit approval plus a small budget cap before paid requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HunterDrop22/tyt) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/HunterDrop22) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet, WebSocket, room, agent, payment, environment variable, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
