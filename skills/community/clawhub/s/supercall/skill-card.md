## Description:

Supercall lets an agent place AI-powered outbound phone calls with custom personas and goals using OpenAI Realtime API and Twilio, including DTMF/IVR navigation for phone menus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xonder](https://clawhub.ai/user/xonder)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Supercall to let an agent make outbound phone calls, confirm appointments, deliver messages, retrieve call status, and navigate automated phone menus. It is intended for users who can manage Twilio, OpenAI, webhook, consent, and transcript-handling requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real outbound calling and audio processing can create legal, financial, and misuse exposure.

Mitigation: Use a dedicated Twilio number and OpenAI key with spending limits, obtain required consent, follow calling and recording laws, and avoid critical or safety-sensitive use.

Risk: Public webhook and media-stream exposure can route callbacks or audio to unintended endpoints if tunnel or public URL settings are wrong.

Mitigation: Prefer localhost or a tightly controlled tunnel, verify the public URL before starting, keep hook tokens secret, and rotate credentials if exposure is suspected.

Risk: Call audio and transcripts may contain sensitive information and may be retained locally or by service providers.

Mitigation: Review, rotate, and delete local call logs, avoid sharing sensitive data through the call persona, and verify Twilio retention and deletion controls before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xonder/skills/supercall)
- [ClawHub publisher profile](https://clawhub.ai/user/xonder)
- [OpenAI API keys](https://platform.openai.com/api-keys)
- [Twilio Console](https://console.twilio.com)
- [ngrok dashboard](https://dashboard.ngrok.com)
- [OpenClaw voice_call attribution](https://docs.clawd.bot/plugins/voice-call)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration]

**Output Format:** [Structured tool results and call transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate real outbound phone calls, return call status, list active calls, end calls, and expose transcripts from completed calls.]

## Skill Version(s):

2.0.0 (source: package.json, CHANGELOG, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
