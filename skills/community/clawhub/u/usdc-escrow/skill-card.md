## Description: <br>
Trustless USDC escrow for agent-to-agent payments on Base. Create, release, dispute escrows via simple commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeroaddresss](https://clawhub.ai/user/zeroaddresss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage USDC escrow payments between agents on Base Sepolia. It supports escrow creation, lookup, release, dispute, dispute resolution, and expired escrow claims through shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can invoke escrow actions that move or affect funds through the API. <br>
Mitigation: Require explicit human approval before create, release, dispute, resolve, or claim-expired commands are executed. <br>
Risk: The skill depends on trust in the operator of api.payclawback.xyz and the configured escrow endpoint. <br>
Mitigation: Install only when the operator is trusted, and verify the API endpoint, network, and contract details before use. <br>
Risk: Escrow descriptions and command parameters may expose sensitive transaction context. <br>
Mitigation: Avoid confidential descriptions and verify escrow IDs, recipients, amounts, and deadlines before submitting commands. <br>


## Reference(s): <br>
- [USDC Escrow API Documentation](references/api-docs.md) <br>
- [Verified Base Sepolia Escrow Contract](https://sepolia.basescan.org/address/0x2a27844f3775c3a446d32c06f4ebc3a02bb52e04) <br>
- [USDC Escrow ClawHub Listing](https://clawhub.ai/zeroaddresss/usdc-escrow) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; commands call the configured escrow API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
