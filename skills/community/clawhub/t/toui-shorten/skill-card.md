## Description:

Shorten URLs with toui.io and read their click stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebrecht](https://clawhub.ai/user/thebrecht)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create toui.io short links through the toui MCP server or REST API and to check click statistics for existing short codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback curl template can mishandle crafted URLs or titles if an agent pastes raw values into shell or JSON snippets.

Mitigation: Prefer the toui MCP tool path; when REST is used, validate and JSON-escape URL and title values or send them through a structured API client.

Risk: The REST path may require a TOUI_API_KEY, and stats require a broader full-scope key.

Mitigation: Use minimally scoped credentials, avoid exposing API keys in command output, and use full-scope keys only when click statistics are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thebrecht/skills/toui-shorten)
- [toui homepage](https://toui.io)
- [toui admin API key page](https://toui.io/admin)
- [toui MCP server](https://mcp.toui.io)
- [toui REST shorten endpoint](https://toui.io/api/v1/shorten)
- [toui REST stats endpoint](https://toui.io/api/v1/urls/{code}/stats)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with short URL values, JSON examples, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP output can include short_url, code, and qr_url; REST output can include short_url, short_code, and stats JSON.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
