## Description:

Diagnose Yggdrasil installation and daemon status for IPv6 P2P connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jing-yilin](https://clawhub.ai/user/jing-yilin)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check whether Yggdrasil-backed IPv6 peer-to-peer connectivity is available, interpret connectivity states, and guide installation or troubleshooting when the daemon is missing or unreachable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and troubleshooting can require powerful system and network privileges.

Mitigation: Review before installing, prefer official or distribution-maintained Yggdrasil packages, verify release keys or checksums, and avoid piping remote content into sudo.

Risk: Running the gateway or daemon with broad privileges can expand the impact of a compromised process.

Mitigation: Do not run the full OpenClaw gateway as root; grant only the minimum network capability needed for the Yggdrasil daemon, such as the specific TUN or network capability required by the platform.

## Reference(s):

- [Yggdrasil Installation Guide](references/install.md)
- [ClawHub Skill Page](https://clawhub.ai/jing-yilin/skills/yggdrasil)
- [OpenClaw Homepage](https://github.com/ReScienceLab/declaw)
- [Yggdrasil Releases](https://github.com/yggdrasil-network/yggdrasil-go/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific installation steps and connectivity-state interpretation.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
