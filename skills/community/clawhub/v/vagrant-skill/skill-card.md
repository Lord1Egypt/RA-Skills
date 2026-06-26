## Description: <br>
Disposable VMs for safe testing with sudo access, Docker, Go, nested KVM, and repeatable destroy-and-recreate workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpoley](https://clawhub.ai/user/jpoley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create disposable Vagrant-based Ubuntu VMs for isolated build, test, networking, Docker, systemd, and privileged experimentation without modifying the host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated Vagrantfile template may forward the user's SSH agent into a VM used for risky experimentation. <br>
Mitigation: Review the generated Vagrantfile before use and disable SSH agent forwarding unless it is explicitly required. <br>
Risk: Credentials, project files, or other host data copied or forwarded into the VM can be accessed by code running inside the VM. <br>
Mitigation: Treat synced project data and forwarded credentials as available to VM workloads, and limit what is synced or forwarded for untrusted tests. <br>
Risk: Destroying the VM removes VM-local state and work products. <br>
Mitigation: Copy needed VM-local work back to the project or another durable location before running vagrant destroy -f. <br>
Risk: The skill can propose repository infrastructure changes such as Vagrantfiles, .gitignore updates, and provisioning scripts. <br>
Mitigation: Review and approve generated repository file changes before committing or relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jpoley/vagrant-skill) <br>
- [Platform Setup Reference](references/platform-setup.md) <br>
- [VM Contents Reference](references/vm-contents.md) <br>
- [microvm-sandbox to daax: Security Layer Integration](docs/microvm-sandbox-for-daax.md) <br>
- [microvm-sandbox to nanofuse: Reuse Analysis](docs/microvm-sandbox-vs-nanofuse.md) <br>
- [Agent Skills standard](https://agentskills.io) <br>
- [bats-core](https://github.com/bats-core/bats-core) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify a Vagrantfile, .gitignore entries, provisioning scripts, and commands to run inside a VM.] <br>

## Skill Version(s): <br>
0.7.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
