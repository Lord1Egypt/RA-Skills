## Description:

A proxy service that wraps external web pages with Glancify, enabling interactive content visualization and keyword extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO specialists, researchers, and content analysts use this skill to wrap public web pages with Glancify and retrieve keyword or topic information for content analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit arbitrary URLs to a third-party proxy service.

Mitigation: Use it only with public, non-sensitive web pages unless the provider documents stronger privacy handling and destination restrictions.

Risk: URLs containing secrets, authenticated paths, intranet hosts, personal documents, or cloud metadata endpoints could expose sensitive information.

Mitigation: Do not provide private intranet links, authenticated URLs, personal documents, cloud metadata endpoints, or URLs with secrets in query strings.

## Reference(s):

- [Glancify API route](https://api.toolweb.in/tools/glancify)
- [Glancify API docs](https://api.toolweb.in:8167/docs)
- [ToolWeb](https://toolweb.in)
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-glancify)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON, Markdown]

**Output Format:** [Markdown with HTTP examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may route supplied URLs through a third-party web proxy service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
