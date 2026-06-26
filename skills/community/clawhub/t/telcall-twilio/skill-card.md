## Description: <br>
Make emergency phone calls via Twilio. Use when you need to call someone and play a voice message programmatically (e.g., server down alerts, security notifications). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnvipstar](https://clawhub.ai/user/cnvipstar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure Twilio credentials and trigger voice-call alerts for urgent operational or security notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Twilio phone calls that may incur charges. <br>
Mitigation: Require explicit confirmation before each call and limit use to approved destination numbers and Twilio accounts. <br>
Risk: The Twilio Auth Token is stored locally as a long-lived credential. <br>
Mitigation: Protect the configuration file, rotate the token when needed, and avoid entering secrets in terminals or logs that may be recorded. <br>
Risk: Message text is inserted into TwiML before the call request is sent. <br>
Mitigation: XML-escape and validate message text before building TwiML. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cnvipstar/telcall-twilio) <br>
- [Twilio](https://www.twilio.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq to configure Twilio credentials and initiate phone calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
