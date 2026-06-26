## Description: <br>
Manage Ravi contacts by listing, searching, creating, updating, deleting, and resolving names to email addresses or phone numbers before sending messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Ravi contact records and resolve a recipient's name to an email address or phone number before email or SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contacts are stored in plaintext, so contact fields may expose sensitive notes, credentials, API keys, or other secrets if misused. <br>
Mitigation: Store only contact information in contact fields; use dedicated password or secret storage for credentials and API keys. <br>
Risk: Creating, updating, deleting, or marking contacts as trusted can affect downstream email and SMS routing. <br>
Mitigation: Review contact changes and trusted-contact flag updates before applying them. <br>


## Reference(s): <br>
- [Contacts API Reference](https://ravi.id/docs/schema/contacts.json) <br>
- [ClawHub skill page](https://clawhub.ai/raunaksingwi/ravi-contacts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference contact fields including email address, phone number, display name, nickname, and trusted-contact status.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
