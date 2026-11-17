## Description:

Query thumbtack.com from a shell — search local service pros by trade and zip, and read pro profiles with ratings, reviews, credentials, business hours and pricing. Uses plain curl against Thumbtack's SSR pages and its anonymous GraphQL endpoint; no API key, no login, no browser extension. Use when you want Thumbtack data without an MCP server, in a script, or one-shot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use shell commands to search public Thumbtack service listings by trade and ZIP code, then inspect provider profiles and reviews. This supports one-off lookups and scripts that need local service provider information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipes can overwrite existing local intermediate JSON files.

Mitigation: Run recipes in a fresh temporary directory.

Risk: Searches send the selected trade and ZIP code to Thumbtack.

Mitigation: Use only a trade and ZIP code you intend to share; login credentials are not needed.

## Reference(s):

- [Thumbtack](https://www.thumbtack.com/)
- [Discovery recipes](references/discovery.md)
- [ClawHub release page](https://clawhub.ai/chrischall/skills/thumbtack-mcp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with curl, Node.js, and jq examples; extracted listing and profile data as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookup results for public service listings, provider profiles, and reviews.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
