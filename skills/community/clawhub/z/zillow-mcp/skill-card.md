## Description:

Look up real-estate listings, property details, Zestimates, saved searches, saved homes, and market reports on Zillow via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Zillow property listings, estimates, saved Zillow activity, and market reports from an agent through the zillow-mcp server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party code and a browser extension against a signed-in Zillow session.

Mitigation: Review before installing, use a dedicated Chrome profile for Zillow, and pin the MCP package and fetchproxy source to reviewed versions or commits.

Risk: Signed-in Zillow activity may expose saved homes, saved searches, or other account-linked data to the agent.

Mitigation: Avoid staying signed in unless the user intends the agent to access saved Zillow homes or searches.

Risk: Zillow does not publish a public consumer API, and the skill depends on private web app endpoints through a browser session.

Mitigation: Use at the user's discretion and review Zillow access behavior before relying on results in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/zillow-mcp)
- [zillow-mcp npm package](https://www.npmjs.com/package/zillow-mcp)
- [zillow-mcp source](https://github.com/chrischall/zillow-mcp)
- [fetchproxy source](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Zillow listing details, property records, Zestimate history, saved-search results, saved-home results, market reports, and mortgage breakdowns.]

## Skill Version(s):

0.10.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
