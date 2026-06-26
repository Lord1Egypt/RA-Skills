## Description: <br>
Read incoming SMS or email messages, including OTPs, verification codes, verification links, and incoming mail; do not use it for sending email or managing credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users operating a Ravi identity use this skill to let an agent inspect incoming SMS and email after triggering verification, two-factor authentication, confirmation, or other inbound-message workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose OTPs, magic links, verification URLs, phone numbers, and full email bodies to the agent. <br>
Mitigation: Use it only for the specific inbox or verification task the user requested, and avoid displaying, logging, storing, forwarding, or reusing message contents unless explicitly requested. <br>
Risk: An agent could select a stale or unrelated message when extracting an OTP or verification link. <br>
Mitigation: Check sender, timestamp, thread, and context before using a code or link, and poll briefly when a newly triggered message has not arrived yet. <br>


## Reference(s): <br>
- [Ravi Inbox API schema](https://ravi.id/docs/schema/inbox.json) <br>
- [Ravi Messages API schema](https://ravi.id/docs/schema/messages.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface sensitive SMS and email contents, including OTPs and verification links.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
