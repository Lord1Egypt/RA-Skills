## Description: <br>
Run agent tasks inside an isolated Unikraft Cloud (UKC) sandbox VM for untrusted code, script testing, build reproduction, or other work that should not execute on the host. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[procub3r](https://clawhub.ai/user/procub3r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to provision a per-session Unikraft Cloud sandbox, sync a selected workspace, execute commands remotely, and clean up the sandbox after isolated work is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent create and delete UKC sandbox VMs and run remote commands using the user's UKC account. <br>
Mitigation: Use a least-privilege UKC token and require explicit confirmation before provisioning, remote execution, or deletion steps. <br>
Risk: Directory synchronization can copy sensitive local files to the sandbox or bring remote files back into the local workspace. <br>
Mitigation: Sync only task-specific directories, avoid directories containing secrets, and review files copied back before executing them locally. <br>
Risk: The local-to-sandbox sync uses a destructive delete mode for files in the sandbox workspace that are absent locally. <br>
Mitigation: Keep durable work in the local session directory and sync back before any subsequent local-to-sandbox sync. <br>
Risk: SSH access disables strict host key checking and uses an OpenSSL proxy. <br>
Mitigation: Prefer a version that pins SSH host keys before using this skill for sensitive work. <br>


## Reference(s): <br>
- [UKC API Reference](references/ukc_api.md) <br>
- [ClawHub release page](https://clawhub.ai/procub3r/unikraft-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UKC_TOKEN, UKC_METRO, UKC_USER, and UKC_SANDBOX_IMAGE environment variables.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
