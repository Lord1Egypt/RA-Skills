## Description:

Issue and verify SX# agent passports for cryptographic identity with hash-chain integrity and Merkle anchoring on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register AI agents with SputnikX, retrieve SX# passports and profiles, and verify event or Merkle proofs through documented HTTP endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends the provided agent identifier and display name to SputnikX as a third-party service.

Mitigation: Review submitted identifiers before use and avoid sending sensitive or confidential data unless approved.

Risk: Registration may return an API key that should be treated as sensitive.

Mitigation: Store generated keys in an approved secret store and avoid pasting them into shared logs, prompts, or tickets.

Risk: Some verification endpoints are described as paid.

Mitigation: Confirm cost authorization before invoking paid event-proof or Merkle-root verification endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drivenbymyai-max/skills/sx-agent-passport)
- [SputnikX Soul Ledger](https://soulledger.sputnikx.xyz)
- [SputnikX Soul API Base URL](https://soul.sputnikx.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown guidance with curl command examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return API keys and includes guidance for paid verification endpoints; the inspected artifact contains no local executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
