## Description:

Upgrade Stylus smart contracts using OpenZeppelin proxy patterns on Arbitrum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and review upgradeable Arbitrum Stylus smart contracts using UUPS, Beacon, and ERC-1967 proxy patterns. It supports storage compatibility checks, access-control design, initialization safety, reactivation planning, and upgrade-path testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract upgrade guidance can permanently affect assets, permissions, or upgrade authority if applied incorrectly.

Mitigation: Independently verify storage layout, access controls, initialization guards, and deployment transactions before using the guidance on production contracts.

Risk: Proxy initialization can be front-run or repeated if deployment and initialization are separated or unguarded.

Mitigation: Pass initialization calldata through the proxy constructor for an atomic deployment and include a re-initialization guard.

Risk: Stylus WASM contracts can become uncallable if required reactivation is missed.

Mitigation: Include annual and post-protocol-upgrade WASM reactivation in the contract maintenance plan.

## Reference(s):

- [OpenZeppelin rust-contracts-stylus repository](https://github.com/OpenZeppelin/rust-contracts-stylus)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Rust code snippets, shell commands, checklists, and configuration advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; users should independently verify upgrade transactions before production use.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
