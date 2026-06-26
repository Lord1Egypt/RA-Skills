## Description: <br>
Install, configure, start, stop, and verify local or remote development infrastructure across Windows, Linux, and macOS by executing commands through a unified workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, run, and verify local or remote environment setup tasks for common infrastructure services across Windows, Linux, and macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute commands that modify local or remote services. <br>
Mitigation: Review the proposed command plan before execution, run changes in small verified steps, and approve privilege escalation explicitly. <br>
Risk: Example remote nodes use administrative accounts. <br>
Mitigation: Keep example nodes disabled until intentionally configured and prefer least-privilege accounts over root or Administrator. <br>
Risk: The MinIO recipe contains a placeholder root password. <br>
Mitigation: Replace placeholder credentials before use and avoid storing secrets in config.json. <br>
Risk: State persistence can capture sensitive command output or operational details. <br>
Mitigation: Record only short non-sensitive summaries in config.json and keep credentials in external secret stores referenced by authRef. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/universal-shell-deployer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command plans, shell commands, verification steps, and configuration update summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update config.json state while guiding verified deployment steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
