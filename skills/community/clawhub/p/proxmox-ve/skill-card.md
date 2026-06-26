## Description: <br>
Use Proxmox VE (PVE) through the `pvesh`, `qm`, and `pct` CLIs for cluster, node, VM, and LXC inspection plus routine lifecycle work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect Proxmox VE clusters, nodes, QEMU VMs, and LXC containers, and to perform routine lifecycle work after read-first checks and explicit confirmation for disruptive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide privileged Proxmox administration and may propose disruptive VM or container actions. <br>
Mitigation: Use least-privilege access, prefer read-only discovery first, and require explicit confirmation before stops, resets, rollbacks, deletes, or POST API actions. <br>
Risk: The bundled remote API helper disables TLS certificate verification by default. <br>
Mitigation: Enable TLS verification with valid certificates before using remote API scripts outside controlled local environments. <br>
Risk: API token credentials are required for remote access. <br>
Mitigation: Provide credentials through environment variables, avoid hardcoding or echoing secrets, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [Proxmox VE command and auth reference](references/commands-and-auth.md) <br>
- [ClawHub skill page](https://clawhub.ai/jimpang8/proxmox-ve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, Python examples, JSON API output, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Proxmox CLI commands, API paths, environment-variable setup, and status-check summaries.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
