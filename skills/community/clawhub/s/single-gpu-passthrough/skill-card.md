## Description:

Comprehensive skill for the author's single-GPU passthrough setup: Fedora 44 bootc atomic host with Intel i5-12400F, NVIDIA RTX 2060 12GB (TU106), QEMU 10.2.2, libvirt 12.0.0, Wayland (niri on greetd), covering hook scripts, kernel config, libvirt domain XML, virsh operations, and troubleshooting for single-GPU VFIO passthrough to a Win10 VM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and operate single-GPU VFIO passthrough on a Fedora bootc Linux host with QEMU and libvirt. It provides host configuration guidance, lifecycle hook scripts, VM XML guidance, validation commands, and troubleshooting steps for passing an NVIDIA GPU to a Windows 10 VM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The startup hook stops the display manager, kills desktop processes, unloads NVIDIA modules, and can terminate an active graphical session or unsaved work.

Mitigation: Verify the VM name, PCI device IDs, display manager, and script paths first; test from a secondary console or remote shell and keep a recovery path before enabling the hook.

Risk: The scripts require root-level host changes for GPU detach, module unload, device reattach, and display restart.

Mitigation: Review each command against the target host, confirm backups or recovery access, and apply the scripts only on a machine intentionally dedicated to single-GPU passthrough.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/single-gpu-passthrough)
- [Metadata homepage](https://github.com/mina-atef-00/agent-skills)
- [qemu-hook.sh](references/qemu-hook.sh)
- [vfio-startup.sh](references/vfio-startup.sh)
- [vfio-teardown.sh](references/vfio-teardown.sh)
- [Risingprism single-GPU passthrough guide](https://gitlab.com/risingprismtv/single-gpu-passthrough)
- [QEMU system emulation documentation](https://www.qemu.org/docs/master/system/)
- [libvirt hooks documentation](https://libvirt.org/hooks.html)
- [libvirt domain XML format](https://libvirt.org/formatdomain.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash, XML, and systemd configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes host-specific paths, PCI device identifiers, VM name assumptions, and operational checks that must be reviewed before use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
