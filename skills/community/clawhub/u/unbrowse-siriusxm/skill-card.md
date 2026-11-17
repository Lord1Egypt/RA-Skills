## Description:

Connects agents to Unbrowse tools for searching SiriusXM, opening channel pages, and reading pages on siriusxm.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unbrowse](https://clawhub.ai/user/unbrowse)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents looking for SiriusXM information can search, inspect channel details, and summarize pages from siriusxm.com through Unbrowse's remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote service offers cloud browsing and login autofill beyond the advertised read-only SiriusXM tools.

Mitigation: Review the available tools before connecting, and require explicit user confirmation before any sign-in or account action.

Risk: The service can create new tools and perform actions that change an account or make purchases.

Mitigation: Require explicit user confirmation before tool compilation, purchases, deletions, or other changes; check the outcome before retrying an uncertain action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/unbrowse/skills/unbrowse-siriusxm)
- [Unbrowse SiriusXM site tools](https://unbrowse.ai/sites/siriusxm.com)
- [Unbrowse SiriusXM OpenAPI description](https://unbrowse.ai/api/v1/sites/siriusxm.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include search matches, channel details, and page summaries or links.]

## Skill Version(s):

1.0.1 (source: ClawHub release and server metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
