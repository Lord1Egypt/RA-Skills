## Description: <br>
TinkerClaw WhatsApp guides an agent through WhatsApp messaging, group management, history search, and multi-agent discussion controls for OpenClaw's WhatsApp channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[globalcaos](https://clawhub.ai/user/globalcaos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and operate WhatsApp-backed OpenClaw agents for messaging, group administration, contact and history workflows, and coordinated multi-agent discussions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent effective control over a linked WhatsApp account. <br>
Mitigation: Use it only with accounts authorized for automation, review helper scripts before running them, and restrict agent access to intended chats and groups. <br>
Risk: The contact export and group inspection behavior can expose contact, membership, and group data. <br>
Mitigation: Run exports manually, limit use to groups where participants have consented, and avoid collecting data from sensitive personal or business chats. <br>
Risk: Messaging and group-management actions can send messages, change participants, or alter group settings at scale. <br>
Mitigation: Confirm recipients and group IDs before execution, use rate limits, and keep a human approval step for administrative actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/globalcaos/whatsapp-ultimate) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Baileys WhatsApp Web API](https://github.com/WhiskeySockets/Baileys) <br>
- [TinkerClaw project reference](https://github.com/globalcaos/tinkerclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with command examples and helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw WhatsApp channel configuration and a linked WhatsApp account.] <br>

## Skill Version(s): <br>
4.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
