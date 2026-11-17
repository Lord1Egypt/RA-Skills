## Description:

Automatically creates a recursive neural memory network, stores it on IPFS, and anchors its Merkle root on Base chain as an ERC-8004 identity NFT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidadong2359](https://clawhub.ai/user/weidadong2359)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to convert local agent memory files into a layered memory graph, persist the resulting data locally or through IPFS, and anchor verifiable memory identifiers on Base chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive agent memory, private user data, proprietary logs, or issue content may be ingested into persistent memory artifacts and publication workflows.

Mitigation: Review and redact memory files before installing or running the skill, and use an isolated workspace that does not contain secrets or private data.

Risk: Wallet and sponsor-key handling can authorize Base chain transactions or expose credentials if stored in generated configuration.

Mitigation: Provide keys only through environment variables, avoid storing RMN_SPONSOR_KEY in generated config, and use limited-funds wallets.

Risk: Shell command execution and suggested external installer commands require human review before use.

Mitigation: Review commands before execution, avoid curl-to-bash installers, and install dependencies through trusted, pinned channels.

Risk: Restored memory and visualization output may contain untrusted data from IPFS, chain metadata, or local files.

Mitigation: Verify integrity checks and inspect restored JSON before feeding it to an agent or using it in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidadong2359/skills/rmn-soul)
- [ERC-8004 registration reference](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON and configuration file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local rmn-soul-data JSON files and may issue IPFS and Base chain transactions when configured.]

## Skill Version(s):

1.0.1 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
