## Description:

Query and update setlist.fm from a shell without running the setlist-mcp server — search/read concert setlists, artists, venues, cities, and users via plain curl against the public REST API (an x-api-key header), and toggle "I was there" attendance on a setlist via the authenticated website, using an fpx-captured session cookie. Use when you want setlist.fm data or want to mark/unmark attendance without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and setlist.fm users can search and read concert, artist, venue, city, and user data, then optionally mark or unmark a setlist as attended from shell workflows without running the setlist-mcp server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The attendance workflow exposes signed-in setlist.fm session cookies to the local CLI.

Mitigation: Protect cookies like passwords, approve only the setlist.fm pairing, and revoke pairing when it is no longer needed.

Risk: The security review covers the bundled instructions, not installed third-party binaries.

Mitigation: Verify the extension download before installing it.

Risk: The attendance action is a toggle and can leave the account in the opposite state if the current state is misread.

Mitigation: Inspect the current state and dry-run the proposed change, then re-read the page to verify the result.

Risk: The free setlist.fm API key is for non-commercial use only.

Mitigation: Follow the API terms and obtain suitable authorization before commercial use.

## Reference(s):

- [REST API endpoint guide](references/rest-api.md)
- [Attendance update walkthrough](references/attendance-write.md)
- [setlist.fm REST API](https://api.setlist.fm/rest)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [fetchproxy extension README](https://github.com/chrischall/fetchproxy#extension)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include curl requests, response projections, and attendance-state checks.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
