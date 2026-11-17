## Description:

Query DeFi yield opportunities across chains using the yieldsllama CLI, powered by the DeFi Llama API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lolieatapple](https://clawhub.ai/user/lolieatapple)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query, filter, sort, and compare DeFi yield pools by token, chain, APY, TVL, and asset exposure. It helps an agent present yield comparisons with context about APY sustainability, liquidity, chain risk, and protocol risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance asks users to execute mutable remote code before installing dependencies.

Mitigation: Inspect the installer and source first, use a pinned reviewed release or commit, and verify checksums or signatures before building.

Risk: The documented install path copies an unverified built binary into a system-wide PATH location.

Mitigation: Prefer a user-local install path such as $HOME/.local/bin and install only after reviewing the source and dependencies.

Risk: Yield data can be volatile and high APY pools may reflect low liquidity, temporary incentives, or elevated protocol and chain risk.

Mitigation: Present APY with TVL, base-versus-reward APY, chain, and protocol context, and avoid treating query results as investment advice.

## Reference(s):

- [Rust Toolchain Installation](https://www.rust-lang.org/tools/install)
- [DeFi Llama Yields API Endpoint](https://yields.llama.fi)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local data.json cache for up to 12 hours and depends on DeFi Llama API availability.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
