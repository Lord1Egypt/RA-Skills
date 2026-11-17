## Description:

Guides agents through running preinstalled RDK X5 /app demos, including Python AI inference samples, 40-pin GPIO examples, C++ multimedia demos, and the bundled BPU model library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when working on RDK X5 hardware to run installed sample applications, inspect available BPU models, compile multimedia demos, and troubleshoot common Python or demo-runtime issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples run local hardware, camera, RTSP, GPIO, or multimedia commands that may affect connected devices or require elevated privileges.

Mitigation: Review each command before running it, use sudo only for trusted local sample scripts, and run the skill on the intended RDK X5 device.

Risk: RTSP examples can expose credentials when usernames and passwords are typed directly into command lines.

Mitigation: Use test credentials, avoid pasting real secrets into shell history, and prefer safer credential handling where the local workflow supports it.

Risk: Using a conda or virtualenv Python can cause RDK X5 hardware libraries such as hobot_dnn to be unavailable.

Mitigation: Use the system Python path documented by the skill when running hardware demos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/skills/rdk-x5-app)
- [ClawHub publisher profile](https://clawhub.ai/user/katherineedwards2475)
- [artifact/SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-oriented hardware demo guidance for RDK X5 /app samples]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
