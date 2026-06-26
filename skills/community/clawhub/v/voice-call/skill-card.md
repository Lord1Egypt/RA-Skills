## Description: <br>
Start voice calls via the OpenClaw voice-call plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to initiate, continue, check, or end voice calls through an enabled OpenClaw voice-call plugin configured for Twilio, Telnyx, Plivo, or mock mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live calls can contact real people, incur telephony costs, and send message content to third-party providers. <br>
Mitigation: Use mock mode for testing, confirm the destination number and message before live calls, and require allowlists or approval steps for real recipients. <br>
Risk: Telephony provider credentials may enable unauthorized calls if broadly exposed. <br>
Mitigation: Keep Twilio, Telnyx, or Plivo credentials restricted and install the skill only when the voice-call plugin is intentionally used. <br>
Risk: Call content may include sensitive information. <br>
Mitigation: Avoid sensitive content unless necessary and review messages before sending them through live telephony providers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danielsinewe/voice-call) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline CLI commands and tool action names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the OpenClaw voice-call plugin to be enabled and configured before live provider calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
