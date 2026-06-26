## Description: <br>
Provides a Telnyx Call Control SIP voice interface for answering phone calls with an AI assistant, natural conversation, function calling, and voice-controlled tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up a phone-accessible assistant over Telnyx SIP calls for hands-free assistant access, reminders, weather checks, workspace-memory lookup, and voice-controlled tool execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a persistent phone-accessible assistant with local tool authority. <br>
Mitigation: Install only for intentional voice access, restrict who can call, add webhook validation, and require a caller PIN or allowlist before enabling use. <br>
Risk: Voice-triggered tools can search workspace files, change reminders, and send messages with limited safeguards. <br>
Mitigation: Gate or disable sensitive tool actions, limit WORKSPACE_DIR to non-sensitive files, and review local gateway token access before deployment. <br>
Risk: Automatic tunnel and Telnyx app setup can expose a public webhook and relies on a Telnyx API key. <br>
Mitigation: Use a scoped Telnyx key, review automatic tunnel and app setup, and remove or restrict public access when the assistant is not in use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teamtelnyx/telnyx-voice-sip) <br>
- [Telnyx Call Control documentation](https://developers.telnyx.com/docs/voice/call-control) <br>
- [Telnyx Inference documentation](https://developers.telnyx.com/docs/inference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, and TELNYX_API_KEY; produces setup guidance and persistent server-management commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
