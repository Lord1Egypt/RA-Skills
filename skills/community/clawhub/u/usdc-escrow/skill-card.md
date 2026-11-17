## Description:

Trustless USDC escrow for agent-to-agent payments on Base. Create, release, dispute escrows via simple commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeroaddresss](https://clawhub.ai/user/zeroaddresss)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to create, inspect, release, dispute, resolve, and reclaim USDC escrows for agent-to-agent payments on Base Sepolia.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Escrow create, release, resolve, and claim commands can affect funds through unauthenticated API calls.

Mitigation: Require explicit human approval before fund-moving commands and verify the escrow ID, beneficiary address, amount, and deadline before execution.

Risk: The skill depends on a third-party escrow API and configurable backend URL.

Mitigation: Verify ESCROW_API_URL, the Base Sepolia network, and the documented escrow contract before use.

## Reference(s):

- [USDC Escrow API Documentation](references/api-docs.md)
- [Base Sepolia Escrow Contract](https://sepolia.basescan.org/address/0x2a27844f3775c3a446d32c06f4ebc3a02bb52e04)
- [ClawHub Skill Page](https://clawhub.ai/zeroaddresss/skills/usdc-escrow)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; ESCROW_API_URL can override the default API backend.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
