## Description: <br>
Connects an OpenClaw agent to a user's Android phone through the VAGUS MCP server so it can read permitted sensor and device context and perform enabled phone actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[embodiedsystems-org](https://clawhub.ai/user/embodiedsystems-org) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to pair an agent with an Android phone for physical-world context, user communication, and governed device actions such as haptics, notifications, text-to-speech, clipboard updates, SMS, URL opening, and calendar event creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive phone context and perform phone actions when permissions are enabled. <br>
Mitigation: Install only if you trust VAGUS, keep sensitive app permissions disabled unless needed, and require explicit approval before SMS, clipboard writes, URL opening, calendar changes, text-to-speech, or notifications. <br>
Risk: Continuous subscriptions or daemon workflows can create ongoing monitoring and retained sensor logs. <br>
Mitigation: Use always-on monitoring only when intentional, prefer short subscription windows for focused tasks, and delete or rotate sensor logs when they are no longer needed. <br>
Risk: Stored session tokens and relay connectivity can keep the phone connection available beyond the immediate task. <br>
Mitigation: Protect the stored VAGUS session file, remove it when access is no longer needed, and re-pair only with a fresh user-provided code. <br>


## Reference(s): <br>
- [VAGUS Homepage](https://withvagus.com) <br>
- [VAGUS Android App](https://play.google.com/store/apps/details?id=com.vagus.app) <br>
- [ClawHub Skill Listing](https://clawhub.ai/embodiedsystems-org/vagus-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands stream JSONL responses from the VAGUS connection script when reading resources, subscribing to updates, or calling phone tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
