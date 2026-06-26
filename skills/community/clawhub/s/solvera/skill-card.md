## Description: <br>
Guides agents through discovering Solvera marketplace intents, submitting offers, and fulfilling verified on-chain outcomes using safe transaction-building practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[densmirnov](https://clawhub.ai/user/densmirnov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to interact with Solvera's on-chain outcome marketplace: polling open intents, filtering opportunities, preparing offers, and building fulfillment transactions while keeping signing local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace transactions can involve financial loss if the network, contract, calldata, token addresses, amounts, deadlines, or gas costs are wrong. <br>
Mitigation: Keep private keys local, verify all transaction details, enforce token allowlists and minimum reward thresholds, and require explicit human approval before signing or broadcasting. <br>
Risk: An agent may act on stale or expired marketplace state if API responses are old or the service is unavailable. <br>
Mitigation: Fetch configuration before use, confirm intent state and ttlSubmit or ttlAccept windows before signing, and validate relevant on-chain state when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/densmirnov/solvera) <br>
- [Solvera API base URL](https://solvera.markets/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint lists, JSON request examples, and transaction-builder response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safe filtering checks, local-signing requirements, and on-chain fallback guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
