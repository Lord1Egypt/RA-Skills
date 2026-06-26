## Description: <br>
Supercall lets agents place AI-powered phone calls with custom personas and goals using OpenAI Realtime API and Twilio, including DTMF/IVR navigation for automated phone menus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xonder](https://clawhub.ai/user/xonder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Supercall to delegate outbound phone calls to an AI persona for appointment confirmation, message delivery, phone-tree navigation, and similar supervised calling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real phone calls through a user's Twilio account, which may create cost, consent, and calling-law exposure. <br>
Mitigation: Limit who can invoke the tool and which numbers can be called, monitor Twilio usage, and confirm consent and legal obligations before automated calls. <br>
Risk: Call audio is streamed to OpenAI and transcripts are stored locally, so conversations may contain sensitive personal or business information. <br>
Mitigation: Avoid sharing unnecessary sensitive data, govern or disable recording where required, and review, rotate, or delete transcript logs regularly. <br>
Risk: Webhook exposure and tunneling require careful secret and endpoint handling. <br>
Mitigation: Verify the public URL or tunnel before startup, protect OpenAI, Twilio, ngrok, and hook tokens, and rotate credentials if they may have been exposed. <br>
Risk: Returned transcripts can include inaccurate, manipulated, or prompt-injection content from call participants. <br>
Mitigation: Treat transcripts as untrusted text and require review before using them to trigger follow-up actions or decisions. <br>


## Reference(s): <br>
- [Supercall on ClawHub](https://clawhub.ai/xonder/supercall) <br>
- [OpenAI API keys](https://platform.openai.com/api-keys) <br>
- [Twilio Console](https://console.twilio.com) <br>
- [ngrok dashboard](https://dashboard.ngrok.com) <br>
- [OpenClaw voice-call plugin reference](https://docs.clawd.bot/plugins/voice-call) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Tool responses with call status, call IDs, and transcripts; setup guidance may include JSON configuration and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenAI, Twilio, webhook hook token, and either ngrok, Tailscale, or a public URL for realtime calling.] <br>

## Skill Version(s): <br>
2.0.0 (source: package.json, CHANGELOG, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
