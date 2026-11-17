## Description:

This skill helps an agent check local Tailscale status and list connected tailnet devices by using the host machine's Tailscale CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sahil1005](https://clawhub.ai/user/sahil1005)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect Tailscale connectivity, local node details, peer counts, and connected device status from an agent session. It is useful when the host already has Tailscale installed, authenticated, and available on PATH.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status output may expose tailnet hostnames, Tailscale IP addresses, and online presence.

Mitigation: Install only in trusted agent environments and avoid sharing generated status output outside the intended operational context.

Risk: The skill depends on the host's existing Tailscale CLI session and permissions.

Mitigation: Confirm the CLI is installed, authenticated to the intended tailnet, and runnable by the ClawBot user before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sahil1005/skills/tailscale-orchestrator)
- [Tailscale CLI installation](https://tailscale.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-formatted status summaries derived from Tailscale CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports connection state, local node details, peer count, device names, Tailscale IP addresses, and online status when available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
