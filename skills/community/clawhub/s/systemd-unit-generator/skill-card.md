## Description: <br>
Generate, validate, and lint systemd unit files (.service, .timer, .socket, .mount) with hardening and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to generate service, timer, and socket unit files, validate existing systemd units, and lint them for operational and hardening issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated unit files can change service privileges, startup behavior, network exposure, or persistence when installed and enabled. <br>
Mitigation: Review generated unit files before placing them under systemd directories or enabling them. <br>
Risk: Services may run with broader privileges than needed if no explicit user or group is configured. <br>
Mitigation: Set --user and --group for least privilege where the service does not require root. <br>
Risk: Socket units can listen on public interfaces when a broad address is generated. <br>
Mitigation: Use explicit localhost bindings when sockets should not be publicly reachable. <br>
Risk: Documentation may overstate mount-generation or hardening coverage. <br>
Mitigation: Check the actual generated output and do not rely on documentation claims alone. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated systemd unit-file text or JSON validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated unit files when the --output option is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
