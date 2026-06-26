## Description: <br>
WORKSTATION.md guides an agent to create, access, manage, and publish content from a temporary public Linux server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renning22](https://clawhub.ai/user/renning22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to provision a temporary Ubuntu server, connect over SSH, run commands, copy files, and expose web content through a public workstation.md URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to create and control a public Linux server with root access. <br>
Mitigation: Use it only for tasks where public server creation is intended, and confirm the workstation name, SSH key, and deployment before provisioning. <br>
Risk: Public hosting can expose private files, secrets, or unfinished services. <br>
Mitigation: Use a dedicated throwaway SSH key, keep secrets out of served directories, and destroy the workstation when the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renning22/workstation) <br>
- [Publisher profile](https://clawhub.ai/user/renning22) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational steps for creating, using, extending, and destroying a public Linux workstation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
