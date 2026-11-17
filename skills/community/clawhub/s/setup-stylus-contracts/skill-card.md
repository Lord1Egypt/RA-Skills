## Description:

Set up a Stylus smart contract project with OpenZeppelin Contracts for Stylus on Arbitrum.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up Arbitrum Stylus smart contract projects, add OpenZeppelin Stylus dependencies, follow import and storage conventions, and run basic build and deploy commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends mutable installer and package-install commands that can execute code during setup.

Mitigation: Review setup commands before use, prefer official Rust and package-manager guidance, and pin cargo-stylus to a reviewed version with locked dependencies when possible.

Risk: Deploying contracts requires access to a private key file.

Mitigation: Use a private key file with restrictive permissions, avoid raw private keys on the command line, and prefer a hardware wallet or keystore when available.

## Reference(s):

- [OpenZeppelin Contracts for Stylus repository](https://github.com/OpenZeppelin/rust-contracts-stylus)
- [openzeppelin-stylus crate](https://crates.io/crates/openzeppelin-stylus)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, TOML, and Rust code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, dependency, import, build, ABI export, and deploy guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
