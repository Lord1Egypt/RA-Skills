## Description: <br>
Look up concert setlists and live-music history via setlist.fm for artist, venue, city, date, tour, and live performance questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and use a read-only MCP server for setlist.fm lookups, including artist setlists, venue histories, tour searches, and concert disambiguation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [setlist-mcp npm package](https://www.npmjs.com/package/setlist-mcp) <br>
- [setlist.fm API key settings](https://www.setlist.fm/settings/api) <br>
- [setlist.fm API terms](https://www.setlist.fm/help/api-terms) <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/setlist-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SETLIST_API_KEY; setlist.fm results should include source links and respect API-key, caching, and commercial-use requirements.] <br>

## Skill Version(s): <br>
0.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
