## Description: <br>
Manage RunPod GPU cloud instances - create, start, stop, connect to pods via SSH and API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewharp](https://clawhub.ai/user/andrewharp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage RunPod GPU instances, connect over SSH, mount pod filesystems with SSHFS, and access common web service ports during remote GPU work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a RunPod account, including pod lifecycle actions that may affect cost or availability. <br>
Mitigation: Use limited credentials where possible and review state-changing or costly pod actions before running them. <br>
Risk: The skill can mount remote pod filesystems over SSHFS, exposing local access to pod files. <br>
Mitigation: Mount only selected pods and unmount SSHFS mounts when finished. <br>


## Reference(s): <br>
- [RunPod pod management on ClawHub](https://clawhub.ai/andrewharp/runpod) <br>
- [RunPod user settings](https://console.runpod.io/user/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides commands and filesystem paths for RunPod CLI, SSH, SSHFS mounts, and proxy URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
