## Description:

Advertised as automated DeFi yield farming across multiple chains, but reviewed evidence shows the artifact is a local CLI configuration stub rather than implemented on-chain automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew00ita](https://clawhub.ai/user/matthew00ita)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Web3 users may use this release as a paid CLI-style setup aid for wallet, risk, APY threshold, and chain configuration. The security review warns not to rely on it for portfolio protection, yield optimization, fund management, or automated exits without reviewed implementation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release makes strong DeFi automation and financial-performance claims, but the inspected code is described by the security review as a local configuration stub.

Mitigation: Do not rely on this release for portfolio protection, yield optimization, fund management, or automated exits unless the publisher provides reviewed implementation evidence.

Risk: Wallet metadata is stored locally by the CLI.

Mitigation: Use only public wallet addresses, avoid entering private keys or seed phrases, and review local configuration files before sharing logs or workspaces.

Risk: Financial-risk disclosure is unclear for a paid DeFi automation release.

Mitigation: Treat outputs as non-advisory configuration text and independently evaluate protocol, market, bridge, smart-contract, and tax risk before acting.

Risk: Install and dependency reproducibility problems are noted in the security guidance.

Mitigation: Install only from trusted, reviewed sources and require pinned package and dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthew00ita/skills/web3-yield-automator-pro)
- [Publisher profile](https://clawhub.ai/user/matthew00ita)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; stores wallet metadata, risk settings, APY threshold, and chain selections in a local JSON configuration file.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
