## Description:

Manage RunPod GPU cloud instances - create, start, stop, connect to pods via SSH and API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewharp](https://clawhub.ai/user/andrewharp)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage RunPod GPU pods, connect to them over SSH, mount pod filesystems with SSHFS, and find common service proxy URLs while working with remote GPU infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use RunPod API configuration and SSH keys to access cloud GPU pods.

Mitigation: Install and use it only when you trust RunPod and intend to give the agent access to the configured RunPod account and SSH credentials.

Risk: Mounting a pod exposes that remote filesystem locally and may allow the agent to inspect or modify pod files.

Mitigation: Mount only pods you intend to work with, verify the pod ID before mounting, and unmount the filesystem when finished.

Risk: First-time SSH connections to newly created pods require host-key acceptance.

Mitigation: Use the script's isolated RunPod known_hosts file and investigate unexpected host-key changes on reconnect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrewharp/skills/runpod)
- [RunPod user settings](https://console.runpod.io/user/settings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RunPod API, SSH, and SSHFS commands that operate on remote GPU pods.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
