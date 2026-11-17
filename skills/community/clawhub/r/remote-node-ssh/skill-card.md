## Description:

Run commands and transfer files between an OpenClaw Gateway (VPS) and a paired local node, using the node protocol when connected and least-privilege SSH when not.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkfaris94](https://clawhub.ai/user/jkfaris94)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to choose between OpenClaw node protocol and least-privilege SSH for command execution, file transfer, status checks, and recovery on an already paired local node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides remote command execution and file transfer to a paired node.

Mitigation: Install only for intentional paired-node administration, keep command allowlists narrow, and review commands before execution.

Risk: SSH fallback can expand access if configured with root, shared keys, disabled host-key checks, or broad network exposure.

Mitigation: Use a dedicated non-root account, key-only login, verified host keys, IdentitiesOnly, and a private route such as Tailscale, LAN, or VPN.

Risk: File synchronization can overwrite or remove remote data if applied without inspection.

Mitigation: Preview rsync transfers before applying them and avoid delete-style operations unless explicitly reviewed.

## Reference(s):

- [Remote Node SSH homepage](https://github.com/jkfaris94/remote-node-ssh)
- [Hybrid Gateway setup dependency](https://github.com/jkfaris94/hybrid-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for an agent; it does not itself execute commands or transfer files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
