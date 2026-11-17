## Description:

Use Proxmox VE through local PVE CLI commands and optional Python API helpers for cluster, node, VM, LXC, snapshot, and routine lifecycle administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to inspect Proxmox VE clusters, discover nodes and guests, check VM and container status, and perform routine lifecycle or snapshot tasks with read-first guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled remote API helper sends powerful Proxmox API tokens while TLS verification is disabled by default.

Mitigation: Prefer local pvesh, qm, and pct commands when possible; for remote API use, enable TLS verification or explicitly configure trusted certificates before using production tokens.

Risk: Proxmox lifecycle and snapshot commands can stop, reboot, roll back, or delete guest state if used with the wrong target.

Mitigation: Use read-only discovery first, confirm node, guest type, VMID, and exact disruptive action, then re-check status after the operation.

Risk: Broad Proxmox credentials could expose cluster-wide administration capabilities.

Mitigation: Use narrowly scoped Proxmox API tokens and avoid broad cluster-admin credentials for routine inspection or automation.

## Reference(s):

- [Proxmox VE skill page](https://clawhub.ai/jimpang8/skills/proxmox-ve)
- [jimpang8 publisher profile](https://clawhub.ai/user/jimpang8)
- [Proxmox VE command and auth reference](references/commands-and-auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, JSON API output guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Proxmox CLI commands, Python helper invocations, API paths, environment variable guidance, and status summaries.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
