## Description: <br>
Pay-per-call API gateway skill that calls paid APIs for LLMs, image and video generation, travel, crypto, web search, and similar tasks through x402 micropayments with a local policy engine for spend controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentc22](https://clawhub.ai/user/agentc22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to route natural-language requests to paid external APIs while returning results and cost information to the agent. It is intended for workflows where a configured wallet may spend small amounts on API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically spend from a funded wallet when broad everyday requests are routed to paid APIs. <br>
Mitigation: Use a dedicated low-balance wallet and require user confirmation that shows the selected service and estimated cost before paid calls. <br>
Risk: Without a configured policy file, spending limits are not enforced beyond the wallet balance. <br>
Mitigation: Set X402_POLICY_PATH to a strict policy with per-transaction caps, daily caps, rate limits, and recipient allowlists before use. <br>
Risk: Disabling autopreflight can bypass policy checks before payment signing. <br>
Mitigation: Keep X402_AUTOPREFLIGHT enabled and treat policy limits as authoritative. <br>
Risk: The EVM private key signs payment transactions. <br>
Mitigation: Store only a dedicated wallet key in EVM_PRIVATE_KEY or EVM_PRIVATE_KEY_FILE and never use a primary wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentc22/x402engine) <br>
- [Publisher profile](https://clawhub.ai/user/agentc22) <br>
- [x402engine homepage](https://x402engine.app) <br>
- [x402 service catalog](https://x402engine.app/.well-known/x402.json) <br>
- [README](artifact/README.md) <br>
- [Policy example](artifact/POLICY.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language responses with structured service result data and cost context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid API result data, selected service metadata, and wallet or policy error reason codes.] <br>

## Skill Version(s): <br>
1.3.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
