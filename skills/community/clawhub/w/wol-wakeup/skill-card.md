## Description:

WoL Wakeup lets an OpenClaw agent manage Wake-on-LAN devices and wake saved machines through keyword-triggered chat commands and guided workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xunone11](https://clawhub.ai/user/xunone11)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to list, add, remove, and wake LAN devices from chat messages. It is intended for trusted local-network automation where target devices support Wake-on-LAN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent local message hook can process Wake-on-LAN commands and may be exposed to misuse if authentication is weak, disabled, or reused from published examples.

Mitigation: Run the hook only for trusted local users, bind it to localhost, generate and rotate a unique hook token, and avoid using the published fixed token.

Risk: The skill stores device data and workflow state under ~/.openclaw and logs message-related hook activity.

Mitigation: Protect ~/.openclaw files with private permissions, use a least-privilege service account, and disable or redact message-body logging where practical.

Risk: Wake-on-LAN commands can affect physical devices on the local network.

Mitigation: Restrict who can send WoL commands, keep the saved device list limited to intended machines, and use the skill only on trusted local networks.

## Reference(s):

- [WoL Wakeup on ClawHub](https://clawhub.ai/xunone11/skills/wol-wakeup)
- [Publisher profile](https://clawhub.ai/user/xunone11)
- [Default OpenClaw hook endpoint](http://127.0.0.1:8765/hook)
- [Default OpenClaw hook health endpoint](http://127.0.0.1:8765/health)
- [README](artifact/README.md)
- [Workflow guide](artifact/WORKFLOW.md)
- [Integration guide](artifact/INTEGRATION_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text responses with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local device-management responses and Wake-on-LAN actions; requires python3 and the wakeonlan package.]

## Skill Version(s):

1.0.0 (source: server release evidence, frontmatter, changelog released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
