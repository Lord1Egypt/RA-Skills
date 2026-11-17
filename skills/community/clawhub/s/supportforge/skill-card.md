## Description:

AI customer support via SupportForge API — ticket creation, auto-replies, routing, knowledge base search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

Developers and support teams use this skill to create support tickets, generate or send replies, route issues, and search a support knowledge base through the SupportForge API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer support content, email addresses, and API credentials may be sent to an external SupportForge/Voss endpoint.

Mitigation: Use the skill only after approving that endpoint for the relevant data, and avoid submitting sensitive support content unless your policy permits it.

Risk: Setting SUPPORTFORGE_API_URL to an untrusted host could redirect support data and credentials.

Mitigation: Keep SUPPORTFORGE_API_URL unset or set it only to an approved SupportForge endpoint.

Risk: The email auto-signup path can expose a generated API key in logs or agent transcripts.

Mitigation: Prefer a pre-provisioned SUPPORTFORGE_API_KEY stored in an approved secret manager and avoid the SUPPORTFORGE_EMAIL auto-signup path.

## Reference(s):

- [ClawHub SupportForge skill page](https://clawhub.ai/jbennett111/skills/supportforge)
- [SupportForge API key endpoint](https://anton.vosscg.com/v1/keys)
- [SupportForge ticket creation endpoint](https://anton.vosscg.com/v1/tickets/create)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke external SupportForge API endpoints using SUPPORTFORGE_API_KEY, SUPPORTFORGE_EMAIL, and optional SUPPORTFORGE_API_URL environment variables.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
