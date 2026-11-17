## Description:

Deploys a ProbeChain Rydberg testnet Agent node and provides commands to install, start, verify, stop, and inspect the node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[probebuilders](https://clawhub.ai/user/probebuilders)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and node operators use this skill to deploy and manage a ProbeChain Rydberg testnet Agent node on macOS, Linux, or Windows through WSL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a hot local blockchain node while handling node credentials and a local keystore.

Mitigation: Use a dedicated low-value testnet account and machine profile, do not reuse passwords, and treat ~/rydberg-agent/password.txt and the keystore as sensitive.

Risk: The setup fetches release artifacts and network configuration during installation.

Mitigation: Review the generated start-bg.sh before running it, prefer immutable pinned releases, verify downloaded artifacts, and validate bootnode data where possible.

## Reference(s):

- [ProbeChain homepage](https://probechain.org)
- [Rydberg Mainnet repository](https://github.com/ProbeChain/Rydberg-Mainnet)
- [ClawHub skill page](https://clawhub.ai/probebuilders/skills/rydberg-agent-node)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes node status output, install/start/stop/log commands, and operational guidance.]

## Skill Version(s):

2.5.1 (source: server release metadata; artifact frontmatter remains 2.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
