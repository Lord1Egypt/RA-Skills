## Description:

Provides an MCP-style interface for generating QuickChart-compatible chart image links through the Xiaobenyang service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit QuickChart-compatible chart parameters and receive a chart image link or related API result for presentation in an agent response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an API key in a plaintext .env file in the working directory.

Mitigation: Use a disposable or tightly scoped API key, avoid sharing or committing the workspace, and rotate the key if the workspace may have been exposed.

Risk: The skill sends API-key-authenticated requests and chart parameters to a configurable third-party service.

Mitigation: Confirm XBY_GAOKAO_BASE_URL points only to the intended provider before use.

Risk: Release security evidence says the documentation is inconsistent about what service the skill uses.

Mitigation: Verify the intended provider, endpoint, and data handling expectations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/quick-chart)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown or JSON-derived text containing a chart image link, success status, and message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends chart parameters to a configurable third-party service.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
