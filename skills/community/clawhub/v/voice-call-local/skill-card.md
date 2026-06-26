## Description: <br>
Start voice calls via the OpenClaw voice-call plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deichmann181](https://clawhub.ai/user/deichmann181) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an OpenClaw agent start, continue, inspect, and end voice calls through a configured telephony provider or a mock provider for development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can place real outbound voice calls, which may contact unintended recipients, disclose private content, or create provider charges. <br>
Mitigation: Require explicit confirmation of the recipient, message, and provider before each real call, and use the mock provider before enabling live telephony. <br>
Risk: Live providers require sensitive telephony credentials such as Twilio, Telnyx, or Plivo secrets. <br>
Mitigation: Use dedicated least-privilege credentials where possible, store them only in approved secret/configuration systems, restrict access, and rotate them on exposure or ownership changes. <br>
Risk: The artifact does not document recipient limits or privacy safeguards for call content. <br>
Mitigation: Set organizational recipient allowlists or approval gates, avoid sensitive call content unless authorized, and review call behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deichmann181/voice-call-local) <br>
- [Publisher profile](https://clawhub.ai/user/deichmann181) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for voice_call actions and OpenClaw voicecall CLI usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
