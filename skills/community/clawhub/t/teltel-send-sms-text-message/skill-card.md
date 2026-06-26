## Description: <br>
Send single or bulk SMS text messages through the TelTel.io REST API using bundled Node.js scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TelTel-call-center](https://clawhub.ai/user/TelTel-call-center) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operators use this skill to send individual or bulk SMS messages from a TelTel account after configuring an API key, sender, recipients, and message body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real SMS messages through the configured TelTel account, including bulk messages. <br>
Mitigation: Use dry-run or explicit confirmation before bulk sends, and verify sender, recipient list, and message text before execution. <br>
Risk: SMS bodies may expose sensitive, regulated, or personal information to TelTel and message recipients. <br>
Mitigation: Avoid sending secrets or sensitive personal information unless the user is authorized to share it and the recipients are intended. <br>
Risk: The TelTel API key authorizes message sending from the account. <br>
Mitigation: Keep TELTEL_API_KEY in environment variables or the skills UI secret field and avoid placing it in prompts, scripts, logs, or message bodies. <br>


## Reference(s): <br>
- [TelTel homepage](https://www.teltel.io/) <br>
- [ClawHub skill page](https://clawhub.ai/TelTel-call-center/teltel-send-sms-text-message) <br>
- [TelTel-call-center publisher profile](https://clawhub.ai/user/TelTel-call-center) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples and JSON responses from the TelTel API scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run output for single and bulk send commands before sending messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
