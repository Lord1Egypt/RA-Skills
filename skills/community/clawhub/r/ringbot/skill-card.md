## Description: <br>
RingBot helps agents make outbound AI phone calls for businesses, food orders, reservations, appointments, and similar voice-call tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gbessoni](https://clawhub.ai/user/gbessoni) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operators use RingBot to ask an agent to place real outbound calls for food orders, reservations, appointments, customer service, reminders, personal messages, and lead qualification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound phone calls that may affect third parties or create unwanted contact. <br>
Mitigation: Require explicit user approval for each call or schedule, confirm the destination and purpose before dialing, and provide a clear way to stop future calls. <br>
Risk: Provider credentials and Twilio spending can be exposed or abused if the backend is not reviewed and constrained. <br>
Mitigation: Review the RingBot backend before installation, scope provider keys narrowly, monitor usage, and set spending or rate limits for Twilio and related services. <br>
Risk: Sensitive medical, personal, marketing, or recurring calls may require consent, legal authority, and minimal data handling. <br>
Mitigation: Avoid these use cases unless consent and legal authority are documented, collected data is minimized, and retention and cancellation expectations are clear. <br>


## Reference(s): <br>
- [RingBot ClawHub page](https://clawhub.ai/gbessoni/ringbot) <br>
- [Twilio](https://twilio.com) <br>
- [LiveKit Cloud](https://cloud.livekit.io) <br>
- [Groq Console](https://console.groq.com) <br>
- [Groq Orpheus TTS terms](https://console.groq.com/playground?model=canopylabs%2Forpheus-v1-english) <br>
- [TalkForce AI](https://talkforceai.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides call setup instructions, environment variable guidance, and local API request examples.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
