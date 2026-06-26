## Description: <br>
x402 payment layer for AI agents - charge USDC per skill call. Meta-skill that wraps any skill with per-call pricing and on-chain payment verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strouddustinn-bot](https://clawhub.ai/user/strouddustinn-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add per-call USDC payments, HTTP 402 responses, and payment ledger tracking to agent skills or APIs. It is intended for monetizing skill calls while keeping payment limits, wallet handling, and verification controls explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real funds and depends on wallet credentials. <br>
Mitigation: Use a dedicated low-balance wallet, protect private keys outside code, configure strict max_price limits, and call only trusted endpoints. <br>
Risk: Payment verification is described as on-chain but the artifact behavior does not fully validate USDC transfer sender, recipient, amount, and replay durability. <br>
Mitigation: Do not rely on it as a production paywall until verification decodes and checks USDC transfer details and replay records are stored durably. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/strouddustinn-bot/x402-paywall) <br>
- [Agent Economy docs](https://agent-economy.io/docs) <br>
- [x402 spec](https://x402.dev) <br>
- [Agent Economy issues](https://github.com/agent-economy/agent-economy/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration instructions, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with Python examples, JSON response examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration guidance for wrapping skills with a paywall, configuring networks and prices, verifying payments, and tracking payments in SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
