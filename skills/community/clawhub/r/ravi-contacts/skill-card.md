## Description:

Manage contacts associated with your identity: list, search, create, update, and delete contacts, and resolve names to email or phone details before messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain Ravi contacts and resolve a person's name to an email address or phone number before sending email or SMS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contacts are stored in plaintext, so sensitive secrets or credentials could be exposed if entered into contact fields.

Mitigation: Use this skill only for contact details, and use dedicated password or secret-management skills for credentials and API keys.

Risk: Recipient lookup can return multiple contacts or no matching contact, which could lead to sending a message to the wrong person if unresolved.

Mitigation: Confirm the intended recipient when multiple matches are found, and ask the user for the email address or phone number when no match exists.

## Reference(s):

- [Contacts API Reference](https://ravi.id/docs/schema/contacts.json)
- [ClawHub Skill Page](https://clawhub.ai/raunaksingwi/skills/ravi-contacts)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Ravi CLI contact records and asks the user to disambiguate when contact search returns multiple matches.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
