## Description:

Give your agent web intelligence — screenshot any URL, extract structured page data, detect page changes, and analyze websites via the SnapAPI REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boehner](https://clawhub.ai/user/boehner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide agents in calling SnapAPI for screenshots, page analysis, metadata extraction, PDF generation, HTML rendering, page monitoring, batch URL processing, and usage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill can send requested URLs, page content, rendered HTML, and monitor targets to the third-party SnapAPI service.

Mitigation: Use it only for data approved for SnapAPI processing; do not submit internal, authenticated, secret-bearing, regulated, or confidential content without approval.

Risk: The skill mentions installing an optional native plugin.

Mitigation: Verify the optional native plugin source before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boehner/skills/snapapi)
- [SnapAPI documentation](https://snapapi.tech/docs)
- [SnapAPI website and API key](https://snapapi.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SNAPAPI_API_KEY and sends requested URLs or rendered content to the SnapAPI service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
