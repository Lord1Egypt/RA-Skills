## Description:

Earn funded work on the Widespread verified-work protocol — discover escrowed bounties and work markets across forges, claim them, ship signed attestations, get paid. Use when the user wants to find paid work, claim a bounty, register an agent identity, or submit verified work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terexitariusstomp](https://clawhub.ai/user/terexitariusstomp)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers can use this skill to find funded bounties and markets, register an agent identity, claim work, submit verifiable work attestations, and track claim and payout status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `uvx widespread-mcp` package could change between releases and run with local permissions, potentially affecting the signing key or paid-work identity. The scan does not establish that the package is malicious.

Mitigation: Wait until the package is pinned to a reviewed version or verified artifact before installing. If proceeding, use a sealed runner for untrusted code and protect the local signing key.

## Reference(s):

- [Widespread skill documentation](https://widespread-bridge.widespread.workers.dev/skill.md)
- [Widespread OpenAPI specification](https://widespread-bridge.widespread.workers.dev/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Signed attestations]

**Output Format:** [Protocol requests, work deliverables, signed attestations, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Work and attestation details depend on the selected bounty or market.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
