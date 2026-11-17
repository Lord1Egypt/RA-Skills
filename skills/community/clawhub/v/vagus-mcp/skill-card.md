## Description:

Connects an OpenClaw agent to an Android phone through the VAGUS MCP server for sensor readings, inferred device context, and governed phone actions such as haptics, notifications, text-to-speech, clipboard writes, SMS, URL opening, and calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[embodiedsystems-org](https://clawhub.ai/user/embodiedsystems-org)

### License/Terms of Use:


## Use Case:

External users and developers use VAGUS MCP to give OpenClaw agents phone-based physical-world awareness and user-contact actions after pairing with an Android device. The skill is useful when an agent needs context such as motion, location, attention state, battery, connectivity, screen state, notifications, or clipboard state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Continuous phone telemetry can expose sensitive motion, location, attention, notification, and clipboard context.

Mitigation: Use the skill only with a phone you control, enable only the minimum VAGUS app permissions needed, and avoid the always-running daemon pattern unless continuous monitoring is deliberate.

Risk: Phone action tools can send SMS messages, write clipboard content, open URLs, or create calendar events.

Mitigation: Require direct user intent before allowing SMS, clipboard writes, URL opening, or calendar creation.

Risk: Installing mutable remote code can introduce unaudited dependency or source changes.

Mitigation: Install from a pinned, reviewed release or commit with audited dependencies instead of cloning the latest repository state.

## Reference(s):

- [VAGUS Homepage](https://withvagus.com)
- [VAGUS Android App](https://play.google.com/store/apps/details?id=com.vagus.app)
- [ClawHub Skill Listing](https://clawhub.ai/embodiedsystems-org/skills/vagus-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with bash commands and JSONL command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands exchange JSONL with the VAGUS MCP server; phone permissions determine available resources and tools.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
