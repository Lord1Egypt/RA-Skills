## Description:

Deploy a SuperRare Sovereign ERC-721 collection on Ethereum or Base via Bankr. Uses the official RARE factory createSovereignBatchMint path, dry-runs by default, and records auditable deploy receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare and run SuperRare Sovereign ERC-721 collection deployments on Ethereum mainnet, Sepolia, Base, or Base Sepolia through Bankr signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Bankr API key can be sent to a locally configurable, unvalidated API endpoint.

Mitigation: Inspect Bankr config files that can set apiUrl and prefer the official Bankr endpoint before using real credentials.

Risk: Broadcast deployment actions are irreversible on-chain and may spend funds or deploy a live collection.

Mitigation: Use dry-run first and enable --broadcast or DRY_RUN=0 only after checking the chain, factory address, calldata, and configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaigotchi/skills/superrare-deploy)
- [Publisher profile](https://clawhub.ai/user/aaigotchi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON receipt files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cast, jq, curl, and BANKR_API_KEY; dry-run is the default.]

## Skill Version(s):

0.2.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
