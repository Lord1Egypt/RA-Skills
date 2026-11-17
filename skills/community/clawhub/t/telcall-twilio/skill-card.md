## Description:

Make emergency phone calls via Twilio. Use when you need to call someone and play a voice message programmatically (e.g., server down alerts, security notifications).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnvipstar](https://clawhub.ai/user/cnvipstar)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure Twilio credentials and trigger spoken phone alerts for incidents such as server outages or security notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real paid phone calls through Twilio.

Mitigation: Before each call, confirm the destination number, spoken message, and expected cost.

Risk: Twilio credentials are stored on disk in the skill configuration.

Mitigation: Use a limited Twilio API key where possible, keep the configuration file private, avoid setup on shared or recorded terminals, and rotate the token if exposed.

Risk: Untrusted or markup-like message text can be inserted into TwiML/XML.

Mitigation: Do not pass untrusted message text unless the script is updated to escape TwiML/XML content safely.

## Reference(s):

- [TelCall Twilio on ClawHub](https://clawhub.ai/cnvipstar/skills/telcall-twilio)
- [Twilio](https://www.twilio.com)
- [Twilio Voice Calls API Endpoint](https://api.twilio.com/2010-04-01/Accounts/${ACCOUNT_SID}/Calls.json)
- [Publisher GitHub Profile](https://github.com/cnvipstar)
- [Publisher X Profile](https://x.com/pingfanbufan)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text]

**Output Format:** [Shell execution with terminal text output and a local JSON configuration file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; places calls through Twilio using credentials stored in ~/.openclaw/workspace/telcall-twilio/config/twilio.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
