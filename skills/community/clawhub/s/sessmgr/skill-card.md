## Description: <br>
Manage OpenClaw sessions by naming, listing, switching, creating, renaming, saving, and deleting them to persist and recover context by name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[detain](https://clawhub.ai/user/detain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to assign memorable names to local work sessions, list saved sessions, and switch back to prior context without searching for session IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad plain-English triggers could accidentally create, switch, or restore persistent work sessions. <br>
Mitigation: Prefer explicit /sessmgr commands for create, save, delete, rename, and switch actions. <br>
Risk: The skill manages persistent local session name mappings, which may matter for users who rely on strict workspace separation. <br>
Mitigation: Review before installing in strict-separation environments and confirm the intended session name before switching or restoring context. <br>


## Reference(s): <br>
- [Sessmgr on ClawHub](https://clawhub.ai/detain/sessmgr) <br>
- [Publisher profile](https://clawhub.ai/user/detain) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text status messages, tabular session listings, and session control tokens.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local OpenClaw session name mappings under ~/.openclaw/agents/main/sessions/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
