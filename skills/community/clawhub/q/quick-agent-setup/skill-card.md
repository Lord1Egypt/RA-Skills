## Description: <br>
Interactive setup for adding Feishu bot accounts and binding them to OpenClaw agents with account-level or group-level routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vimself](https://clawhub.ai/user/vimself) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to register a new Feishu bot account, choose account-level or group-level routing, and bind messages to a selected OpenClaw agent. It is intended for live OpenClaw configuration workflows where the user can review credentials, bindings, and restart impact before applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu App Secret is stored in the local OpenClaw configuration. <br>
Mitigation: Review where OpenClaw configuration and backups are stored, restrict file access, and remove or protect backups that contain secrets. <br>
Risk: The skill modifies live OpenClaw routing and restarts the Gateway. <br>
Mitigation: Confirm the account ID, routing mode, agent binding, DM policy, and expected restart window before applying the configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text output with configuration changes and recovery commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json, create a backup, set session.dmScope, and restart the OpenClaw Gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
