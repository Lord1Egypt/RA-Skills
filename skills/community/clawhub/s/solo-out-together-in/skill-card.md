## Description:

Helps travelers post a PowPop solo-out invitation and find potential companions by nearby destinations, nearby departures, or posts mentioning their destination; requires the PowPop MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

Individual travelers use this skill to post a route and date on PowPop and discover potential companions through public posts near their origin or destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip origin, destination, and timing may be published to PowPop, and order details are written to a local orders.json file.

Mitigation: Review each invitation draft before approving publication, and authorize the PowPop MCP connection only if you are comfortable with the server and local state write.

Risk: The security verdict is benign, but scanner coverage was partial and confidence is medium.

Mitigation: Review the PowPop MCP connection and local orders.json write before installing, as the security guidance recommends.

## Reference(s):

- [PowPop MCP server](https://global.powpow.online/api/mcp)
- [ClawHub skill page](https://clawhub.ai/durenzidu/skills/solo-out-together-in)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Invitation drafts, candidate summaries, and setup guidance; publishing requires user approval.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
