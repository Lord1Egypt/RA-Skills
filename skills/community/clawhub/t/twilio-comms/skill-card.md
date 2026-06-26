## Description: <br>
Twilio SMS, Voice, WhatsApp, and Verify (2FA) - send messages, make calls, and run verification flows from the CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Twilio communication workflows from an agent-accessible CLI, including SMS, voice calls, WhatsApp messages, and Verify code checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live Twilio credentials to contact real recipients, make calls, send messages, and trigger verification codes. <br>
Mitigation: Use a dedicated Twilio subaccount or limited credentials, review every send, call, and Verify command before execution, and use only authorized recipient numbers. <br>
Risk: Listing messages or call recordings can expose communication content inside the agent session. <br>
Mitigation: Run listing and recording commands only when the session is authorized to handle that content, and avoid them when message or recording data is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fr3kstyle/twilio-comms) <br>
- [Twilio Console](https://console.twilio.com) <br>
- [Twilio REST API](https://api.twilio.com/2010-04-01) <br>
- [Twilio Voice TwiML demo](https://demo.twilio.com/docs/voice.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Twilio account credentials in environment variables before commands can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
