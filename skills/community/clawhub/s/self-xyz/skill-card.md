## Description:

Integrate Self (self.xyz), a privacy-first identity protocol using zero-knowledge proofs to verify passports and ID cards across frontend QR flows, backend proof verification, and Celo smart contract verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xturboblitz](https://clawhub.ai/user/0xturboblitz)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add privacy-preserving passport or ID-card verification, age checks, nationality checks, OFAC screening, KYC-style flows, Sybil resistance, and Celo on-chain verification using Self.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Identity verification examples can lead developers to collect or expose sensitive identity attributes beyond what is needed.

Mitigation: Use explicit privacy notices, request the minimum disclosures required for the use case, define strict retention rules, and avoid placing raw identity fields on-chain unless public permanent exposure is intended.

Risk: The smart contract example may be copied without binding the verified address to the proof subject or another trusted identity signal.

Mitigation: Review contract code before deployment and cryptographically bind verified addresses to the proof subject or another trusted identity signal.

Risk: Unpinned dependency versions can change verification behavior over time.

Mitigation: Pin dependency versions and review Self package changes before updating production integrations.

## Reference(s):

- [Frontend Integration](artifact/references/frontend.md)
- [Backend Integration](artifact/references/backend.md)
- [Smart Contract Integration](artifact/references/contracts.md)
- [ClawHub Skill Page](https://clawhub.ai/0xturboblitz/skills/self-xyz)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, Solidity, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration guidance and examples for frontend, backend, and on-chain verification flows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
