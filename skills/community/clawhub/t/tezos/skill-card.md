## Description:

Provides expert Tezos blockchain development guidance for security-first smart contract development, FA1.2/FA2 token standards, gas optimization, and production deployment patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efekucuk](https://clawhub.ai/user/efekucuk)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when building Tezos L1 smart contracts, implementing FA1.2/FA2 token standards, optimizing gas usage, reviewing contract security, and preparing deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command authority and blockchain CLI usage can enable package installation or Tezos actions that spend fees, originate contracts, transfer assets, or target mainnet.

Mitigation: Use the ClawHub-reviewed version or a pinned, checksummed release; remove or narrow npm access; and require explicit confirmation before any octez-client action with financial or mainnet impact.

Risk: Production-oriented deployment guidance can be misapplied to live Tezos contracts without adequate review.

Mitigation: Run comprehensive tests and dry runs on Shadownet, review contract security boundaries, and obtain professional audit coverage for high-value contracts before mainnet deployment.

Risk: The included FA2 operator pattern is reported as unsafe because authorization is not scoped to token_id.

Mitigation: Do not copy the FA2 operator pattern as-is; fix token_id-scoped authorization and add tests for operator permissions before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/efekucuk/skills/tezos)
- [Tezos Docs](https://docs.tezos.com)
- [LIGO](https://ligolang.org)
- [OpenTezos](https://opentezos.com)
- [Tezos Token Standards](https://gitlab.com/tezos/tzip)
- [TzKT Explorer](https://tzkt.io)
- [Tezos Testnet Registry](https://teztnets.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline LIGO and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include smart contract examples, security checklists, deployment steps, and blockchain CLI commands.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
