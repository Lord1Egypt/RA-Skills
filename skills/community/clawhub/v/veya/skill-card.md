## Description:

Operate VEYA, the post-quantum execution and proof layer for AI agents on Robinhood Chain, through the hosted VEYA MCP server (51 veya_* tools). Prove and anchor content as BLAKE3 commitments on Veya.sol, verify transactions and commitments, create ML-DSA-44 identities and signatures, manage environments, agents, tool policy and Kyber-768 secure routing, run 2-of-3 consensus and AES-256-GCM sealed execution, store agent memory, browse the public registry, and send on-chain writes from your own wallet. Use when the user mentions VEYA, veyanet, Veya.sol, Robinhood Chain, on-chain proof or attestation of agent work, BLAKE3 commitments, ML-DSA, Kyber, post-quantum signatures, sealed or protected execution, agent consensus, or any veya_ tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veyanet](https://clawhub.ai/user/veyanet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use VEYA to create and verify content proofs, manage agent environments and policies, coordinate protected execution, and submit or inspect attestations on Robinhood Chain. The skill guides tool selection and workflows for these tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet and signing secrets are sent to the hosted service, and the documentation understates when submitted content leaves the device.

Mitigation: Start with public verification and non-sensitive inputs. Do not submit a primary wallet key or reusable signing identity; prefer reviewed local signing and hash confidential content locally.

Risk: On-chain writes can commit transactions using the selected network and wallet.

Mitigation: Verify the network and transaction details before approving any write.

Risk: Optional packages may introduce supply-chain risk.

Mitigation: Pin and review optional packages before running them.

## Reference(s):

- [VEYA documentation](https://veyanet.tech/docs)
- [VEYA product and API keys](https://app.veyanet.tech)
- [VEYA MCP server](https://mcp.veyanet.tech/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance and structured JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proof digests, transaction hashes, signatures, and public verification links.]

## Skill Version(s):

1.2.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
