## Description:

A Model Context Protocol calculator skill that routes arithmetic, roots, trigonometry, logarithms, statistics, combinatorics, number theory, complex numbers, matrices, numerical analysis, finance, unit conversion, and geometry calculations to the XiaoBenYang remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to answer calculator and mathematics requests through a broad set of MCP-style tool functions backed by the XiaoBenYang service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculator inputs are sent to the XiaoBenYang remote API.

Mitigation: Avoid submitting sensitive financial, business, or personal data unless the provider is trusted for that use.

Risk: The service API key is stored in a local plaintext .env file.

Mitigation: Use a scoped and rotatable key, restrict local file access, and rotate the key if the workspace is shared or exposed.

Risk: The scanner noted stale gaokao/search_schools references in the package.

Mitigation: Review those references before relying on the release in a controlled or production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-calculator)
- [XiaoBenYang API key page](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration guidance]

**Output Format:** [Markdown summaries of JSON-like API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends calculator inputs to the XiaoBenYang remote API.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
