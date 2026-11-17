## Description:

Use Ranklybee's confirmed Backlink Submission Profile to prepare and carry out compliant backlink submissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazhiyu0235](https://clawhub.ai/user/dazhiyu0235)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to prepare website submissions to directories, communities, resource pages, and launch platforms through Ranklybee. It uses a confirmed profile and requires the user's approval for each external submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A submission can publish business or profile information to a third-party destination.

Mitigation: Show the selected destination and exact profile content, then obtain explicit approval before creating a job or making the final submission. Use only confirmed profile details and do not invent claims.

Risk: Creating a job consumes one of the Project's daily attempts, including when an attempt fails or its result is uncertain.

Mitigation: Check readiness and capacity before creating a job, reuse the same idempotency key for retries, and do not repeat an ambiguous final submission.

Risk: Broad account permissions or exposed credentials could grant unnecessary access.

Mitigation: Use only the required backlink-submission read and submit permissions, and never ask the user to paste or save an API token.

## Reference(s):

- [Ranklybee MCP setup guide](https://ranklybee.com/docs/mcp)
- [Ranklybee MCP permission recovery](https://ranklybee.com/docs/mcp#reconnect-with-submission-permissions)
- [ClawHub skill listing](https://clawhub.ai/dazhiyu0235/skills/ranklybee-backlink-submission)

## Skill Output:

**Output Type(s):** [API Calls, Submission guidance, Email drafts]

**Output Format:** [Structured Ranklybee requests with Markdown guidance or a reviewable email draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before external submission; mailto sources remain draft-only; a Project can use up to 15 attempts per local calendar day.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
