## Description:

Manage a Talkspresso business (services, appointments, products, clients, earnings, calendar) using the Talkspresso REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baron-talkspresso](https://clawhub.ai/user/baron-talkspresso)

### License/Terms of Use:


## Use Case:

External Talkspresso business users use this skill to manage business operations such as profiles, services, digital products, appointments, clients, earnings, calendar availability, files, messaging, and related account workflows through the Talkspresso REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad Talkspresso account changes, including services, products, appointments, profile, calendar availability, files, messaging, and pricing.

Mitigation: Use a limited-scope API key if available and review account-changing commands before execution.

Risk: Destructive or outward-facing actions may delete content, cancel bookings, approve bookings, send messages or email invitations, upload files, or change public business information.

Mitigation: Require explicit user confirmation before delete, cancel, approve, send-message, send-email, file-upload, pricing, profile, or availability changes.

Risk: The skill requires a Talkspresso API key that can authorize business account operations.

Mitigation: Store the key in the TALKSPRESSO_API_KEY environment variable, avoid exposing it in prompts or logs, and rotate it if it is disclosed.

## Reference(s):

- [Talkspresso API Reference](references/api.md)
- [Talkspresso Skill Page](https://clawhub.ai/baron-talkspresso/skills/talkspresso)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TALKSPRESSO_API_KEY and expects Talkspresso API responses wrapped in a data field.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
