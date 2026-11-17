## Description:

Search and manage SaaS Telegram contacts, view recent incoming messages, and update contact stages, tags, or notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuewalton](https://clawhub.ai/user/samuewalton)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to search SaaS Telegram contacts, review recent incoming messages, and manage contact records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an embedded backend token in source.

Mitigation: Remove reusable tokens from source and require users to configure credentials securely before use.

Risk: The security scan reports plaintext localhost HTTP transport.

Mitigation: Use a safer authenticated transport for contact and message operations.

Risk: The skill can change contact records without clear safeguards.

Mitigation: Require explicit user confirmation before updating stages, tags, or notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuewalton/skills/telegram-analyzer)
- [Publisher profile](https://clawhub.ai/user/samuewalton)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text and JSON responses from contact and message tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return contact search results, recent incoming messages, or contact update outcomes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
