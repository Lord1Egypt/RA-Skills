## Description: <br>
Set up real-time voice conversations. Phone calls, voice agents, live speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to choose and configure a real-time voice setup for web voice chat, phone calls, or voice-agent workflows across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys, telephony tokens, and account credentials may be exposed if copied into committed configuration files. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing real secrets, and rotate any credential that was exposed. <br>
Risk: Public webhook endpoints for voice calls can receive unwanted traffic or trigger unexpected cost. <br>
Mitigation: Use inbound allowlists or pairing where available, validate provider webhooks, and monitor provider usage and call costs. <br>
Risk: Optional voice plugins or memory-backed phone skills may expand access to calls, memory, or external services. <br>
Mitigation: Review and scan each optional plugin or skill before enabling phone calls or memory-backed conversations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/talk) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Twilio](https://www.twilio.com/) <br>
- [Telnyx](https://telnyx.com/) <br>
- [ElevenLabs](https://elevenlabs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown] <br>
**Output Format:** [Markdown with YAML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides provider setup guidance and example configuration snippets; does not execute provider integrations itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
