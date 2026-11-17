## Description:

Creates and operates disposable Vagrant Ubuntu VMs so agents and developers can test privileged commands, Docker workloads, networking, systemd services, and project builds away from the host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpoley](https://clawhub.ai/user/jpoley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to create disposable Vagrant VMs for build, test, Docker, networking, firewall, systemd, and KVM-oriented experimentation. It is useful when work needs root access or isolation from the host environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forwarding the host SSH agent into the VM can expose host credentials to code running inside the sandbox.

Mitigation: Disable SSH agent forwarding by default and only enable it for trusted workflows that require it.

Risk: Mutable installer and plugin sources can change between runs, which may alter the VM contents unexpectedly.

Mitigation: Pin installer, package, and provider plugin versions and prefer verified downloads with stable checksums.

Risk: Checksum verification that continues when expected hashes are unavailable weakens supply-chain assurance.

Mitigation: Make checksum verification fail closed for downloaded toolchains and document any deliberate exception.

Risk: The isolation posture can be weaker than the skill's safety wording suggests when host credentials or synced project data are exposed to the VM.

Mitigation: Review generated Vagrantfiles before use, avoid passing host secrets into the VM, and destroy disposable VMs after risky testing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpoley/skills/vagrant-skill)
- [Platform Setup Reference](references/platform-setup.md)
- [VM Contents Reference](references/vm-contents.md)
- [microvm-sandbox to daax: Security Layer Integration](docs/microvm-sandbox-for-daax.md)
- [microvm-sandbox to nanofuse: Reuse Analysis](docs/microvm-sandbox-vs-nanofuse.md)
- [Agent Skills Standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and Vagrantfile or provisioning snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for a local Vagrant workflow and depend on an installed provider such as Parallels, libvirt, or VirtualBox.]

## Skill Version(s):

0.7.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
