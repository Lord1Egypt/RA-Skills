## Description: <br>
Look up real-estate listings, property details, Zestimates, saved searches and homes, and market reports on Zillow via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query Zillow property listings, property records, Zestimates, saved Zillow activity, market reports, and mortgage calculations through an MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query Zillow through the user's signed-in browser session, including saved homes and saved searches when requested. <br>
Mitigation: Install only when that access is acceptable, keep browser sessions scoped to the intended account, and avoid requesting saved Zillow activity unless needed. <br>
Risk: The Zillow MCP server and fetchproxy extension are external third-party packages used to broker browser-session requests. <br>
Mitigation: Review the zillow-mcp and fetchproxy packages before use and keep them updated through trusted package sources. <br>
Risk: Broad or automated Zillow querying could conflict with Zillow's terms or expose personal real-estate activity. <br>
Mitigation: Use the skill for limited, user-directed read-only queries and avoid broad scraping or redistribution of signed-in Zillow data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/zillow-mcp) <br>
- [zillow-mcp npm package](https://www.npmjs.com/package/zillow-mcp) <br>
- [zillow-mcp source reference from artifact](https://github.com/chrischall/zillow-mcp) <br>
- [fetchproxy source reference from artifact](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and MCP tool descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only Zillow query guidance and MCP setup instructions; saved-home and saved-search tools require a signed-in Zillow browser session.] <br>

## Skill Version(s): <br>
0.10.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
