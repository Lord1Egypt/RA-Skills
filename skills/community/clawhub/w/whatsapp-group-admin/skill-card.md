## Description: <br>
Group administration utilities - info, stats, invite link parsing, and creation templates <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcosRippel](https://clawhub.ai/user/MarcosRippel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect cached WhatsApp group metadata, list groups with member counts, parse invite links, and create JSON templates for group setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local OpenClaw WhatsApp state and expose cached group IDs, names, and member counts in the conversation. <br>
Mitigation: Install only when that local state access is acceptable; prefer parse-link or create-template when local state is not needed, and run list or info only when you explicitly want cached group metadata displayed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MarcosRippel/whatsapp-group-admin) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output and markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read local OpenClaw WhatsApp state when listing groups or showing group information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
