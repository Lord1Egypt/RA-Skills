## Description:

RingBot helps an agent prepare and initiate outbound AI phone calls for tasks such as ordering by phone, making reservations, scheduling appointments, and customer service calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbessoni](https://clawhub.ai/user/gbessoni)

### License/Terms of Use:


## Use Case:

External users and developers use RingBot to configure outbound AI voice calling and provide the destination phone number, call purpose, and context needed for a call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad real-world outbound calling capability without enough consent, privacy, or confirmation boundaries.

Mitigation: Require explicit confirmation of the phone number, call purpose, caller identity, and any sensitive context before a call is placed.

Risk: Outbound calls can create legal, privacy, or abuse risk in bulk lead, patient, reminder, or recurring-call workflows.

Mitigation: Use those workflows only with clear authorization and appropriate legal, privacy, and consent controls.

## Reference(s):

- [RingBot ClawHub Skill Page](https://clawhub.ai/gbessoni/skills/ringbot)
- [Twilio](https://twilio.com)
- [LiveKit Cloud](https://cloud.livekit.io)
- [Groq Console](https://console.groq.com)
- [Groq Orpheus TTS Terms](https://console.groq.com/playground?model=canopylabs%2Forpheus-v1-english)
- [Talkforce AI](https://talkforceai.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include setup guidance, environment variable names, service commands, and outbound call API requests using a destination phone number, purpose, and context.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
