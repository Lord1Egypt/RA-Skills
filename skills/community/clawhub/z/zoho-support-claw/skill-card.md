## Description:

Integrates Zoho Desk with OpenClaw to ingest support tickets, store local embeddings, analyze open tickets, and draft support replies using OpenAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pretid](https://clawhub.ai/user/pretid)

### License/Terms of Use:

MIT

## Use Case:

Support teams and developers use this skill to connect Zoho Desk ticket history with an agent workflow that generates embeddings and drafts replies for open support tickets. Human review is required before using generated drafts with customers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support ticket content may be sent to OpenAI for embeddings and draft generation.

Mitigation: Confirm OpenAI processing is approved for the ticket data and redact sensitive fields before embedding or draft generation.

Risk: Local embeddings and ticket context are stored in data/embeddings.json.

Mitigation: Protect the file with appropriate access controls and delete or rotate it regularly.

Risk: Zoho access depends on configured OAuth credentials and domain settings.

Mitigation: Use least-privilege Zoho tokens and restrict ZOHO_DOMAIN to known Zoho Desk domains.

Risk: Generated replies can be incorrect or unsuitable for customer communication.

Mitigation: Require human review before sending any draft response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pretid/skills/zoho-support-claw)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON results and command-line logs, with draft reply text generated for each analyzed ticket]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft replies are generated from open ticket details and similar closed-ticket context; local embeddings are stored in data/embeddings.json.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
