## Description: <br>
Sends single or bulk SMS messages through the CloudSMS API using a Channel ID, Auth Key, recipient list, message content, and optional signature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picccabo-art](https://clawhub.ai/user/picccabo-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send transactional or operational SMS messages to one or more domestic or international recipients through a CloudSMS account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send bulk real-world SMS messages using sensitive account credentials without a required confirmation step. <br>
Mitigation: Require a manual review of the exact recipients, message body, signature, and recipient count before each send, and provide the Auth Key only through a protected secret mechanism when possible. <br>
Risk: The script disables configured HTTP and HTTPS proxies before contacting the SMS API. <br>
Mitigation: Review network policy before use and run the skill only in environments where direct API access is approved. <br>
Risk: Misuse could send unsolicited, sensitive, or incorrect messages to up to 100 recipients in one operation. <br>
Mitigation: Limit use to approved messaging workflows, avoid sensitive or unsolicited content, and verify the recipient list before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/picccabo-art/sms-sender) <br>
- [Publisher profile](https://clawhub.ai/user/picccabo-art) <br>
- [CloudSMS API endpoint](https://cpaas-sms.cmidict.com:1820/uips) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command execution and JSON API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SMS send status, tracking UID details when returned by the API, error descriptions, and troubleshooting hints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
