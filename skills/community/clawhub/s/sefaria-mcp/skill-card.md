## Description:

Access Jewish texts, commentaries, cross-references, and daily study materials from Sefaria through an MCP-compatible agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeperl](https://clawhub.ai/user/abeperl)

### License/Terms of Use:

MIT

## Use Case:

Developers and users of MCP-compatible assistants use this skill to search, read, and explore Jewish texts, commentaries, calendars, book metadata, and related source sheets from Sefaria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path can fetch the latest npm package at run time, which may differ from the reviewed artifact.

Mitigation: Install or run an exact pinned version or integrity-checked package, keep dependencies updated, and run the MCP server with limited filesystem and environment access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeperl/skills/sefaria-mcp)
- [Sefaria](https://www.sefaria.org)
- [npm package](https://www.npmjs.com/package/sefaria-mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain text MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include Hebrew and English text, search snippets, commentary and cross-reference summaries, calendar items, source sheet links, and error messages.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
