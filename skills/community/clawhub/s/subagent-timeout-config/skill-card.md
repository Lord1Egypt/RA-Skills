## Description: <br>
Configures OpenClaw subagent timeout fields atomically with preset or custom profiles, TTL validation, backup, dry-run preview, and optional gateway restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose quick, normal, patient, or custom timeout profiles and apply them to subagent runtime settings without manually editing JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the OpenClaw configuration file and change timeout behavior. <br>
Mitigation: Use --dry-run first, confirm the target config path, and rely on the automatic backup before applying changes. <br>
Risk: The default apply flow may restart the OpenClaw gateway and interrupt active work. <br>
Mitigation: Use --no-restart when a restart should be deferred, then restart the gateway manually at an appropriate time. <br>
Risk: A broad timeout request could lead an agent to choose an unintended profile. <br>
Mitigation: Confirm the intended profile or custom values before execution. <br>


## Reference(s): <br>
- [subagent-timeout-config on ClawHub](https://clawhub.ai/songhonglei/subagent-timeout-config) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw JSON configuration and optionally restart the gateway after validation and backup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
