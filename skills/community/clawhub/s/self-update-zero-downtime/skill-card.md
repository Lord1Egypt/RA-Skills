## Description: <br>
Updates a global npm installation of OpenClaw with release-note review, backup, npm install, service restart, health check, and rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luffertlu](https://clawhub.ai/user/luffertlu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they deliberately want an agent to update OpenClaw itself while preserving a fallback path. It is intended for npm global installations on Linux systems, with checks for install type, path consistency, prefix writability, service restart, and rollback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change installed OpenClaw code and restart services. <br>
Mitigation: Use it only after an explicit request naming OpenClaw, review the target version and release notes, and require user confirmation before execution. <br>
Risk: Loose activation could apply an OpenClaw self-update to a generic update request. <br>
Mitigation: Do not run the skill for generic update prompts; scope activation to OpenClaw self-update requests only. <br>
Risk: Incorrect npm or systemd path detection could affect the wrong installation or leave the service inconsistent. <br>
Mitigation: Confirm the detected npm global directory, systemd service, running directory, install type, and npm prefix writability before proceeding. <br>
Risk: A failed upgrade can interrupt the OpenClaw service. <br>
Mitigation: Keep the side-by-side backup, use the built-in health check, and be prepared to rollback and restart the previous service version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luffertlu/self-update-zero-downtime) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with shell commands and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local upgrade logs and rollback guidance for the OpenClaw service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
