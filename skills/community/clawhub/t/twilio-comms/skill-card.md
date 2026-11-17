## Description:

Twilio SMS, Voice, WhatsApp, and Verify (2FA) - send messages, make calls, and run verification flows from the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Twilio credentials and run CLI workflows for SMS, WhatsApp, outbound voice calls, message and call status checks, recordings, and Verify 2FA flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use live Twilio credentials to send messages, place calls, and start verification flows for real recipients.

Mitigation: Use test credentials or restricted Twilio numbers where possible, confirm recipient consent and expected charges before execution, and review commands before running them.

Risk: Twilio account secrets, verification codes, recipient numbers, and message content may be sensitive.

Mitigation: Protect Twilio environment variables and verification codes, avoid logging secrets, and avoid sending untrusted text as voice-call messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fr3kstyle/skills/twilio-comms)
- [Twilio Console](https://console.twilio.com)
- [Twilio Voice demo TwiML](https://demo.twilio.com/docs/voice.xml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with bash commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Twilio account environment variables; commands may contact real recipients and create account charges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
