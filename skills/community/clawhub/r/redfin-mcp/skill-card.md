## Description:

Look up real-estate listings, property details, market reports, and your saved homes/searches on Redfin via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Redfin listing data, property details, market reports, mortgage estimates, and their saved Redfin homes or searches through an MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can execute unpinned third-party code through npx and a cloned fetchproxy repository.

Mitigation: Review the package and repository before installation, and pin the npm package and fetchproxy repository to reviewed versions or commits.

Risk: Saved-home and saved-search tools operate through a signed-in Redfin browser session.

Mitigation: Use a browser profile and environment where exposing Redfin saved homes, searches, and session-scoped data to the MCP server and extension path is acceptable.

Risk: Redfin does not publish a public consumer API for the private endpoints used by the skill.

Mitigation: Use at the user's discretion, review Redfin terms and site behavior before deployment, and expect endpoint or challenge changes to affect reliability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/redfin-mcp)
- [redfin-mcp npm package](https://www.npmjs.com/package/redfin-mcp)
- [redfin-mcp source repository](https://github.com/chrischall/redfin-mcp)
- [fetchproxy source repository](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with MCP tool results, JSON configuration snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Redfin lookup and calculation results; saved-home and saved-search tools require an authenticated Redfin browser session.]

## Skill Version(s):

0.9.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
