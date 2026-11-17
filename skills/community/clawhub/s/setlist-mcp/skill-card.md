## Description:

Look up concert setlists and live-music history via setlist.fm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer user questions about concert setlists, tour histories, venues, artists, dates, and live-performance records through the setlist.fm MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned npm package can change the MCP server code between installs.

Mitigation: Pin setlist-mcp to a reviewed package version or commit before deployment.

Risk: SETLIST_API_KEY can be exposed if it is committed to source control or placed in an overly broad MCP configuration.

Mitigation: Store the API key outside committed files and prefer project-level MCP configuration unless global availability is intentional.

Risk: setlist.fm data use is governed by API terms, including source attribution and commercial-use requirements.

Mitigation: Cite setlist.fm result URLs in user-facing answers and confirm that the deployment has any required setlist.fm permission for commercial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/setlist-mcp)
- [setlist-mcp npm package](https://www.npmjs.com/package/setlist-mcp)
- [setlist.fm API terms](https://www.setlist.fm/help/api-terms)
- [setlist.fm API key settings](https://www.setlist.fm/settings/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and source-linked setlist answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only setlist.fm lookups; responses should cite setlist.fm result URLs and keep API keys out of outputs.]

## Skill Version(s):

0.7.4 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
