## Description: <br>
Look up real-estate listings, property details, market reports, and saved homes or searches on Redfin via MCP, using redfin-mcp with the fetchproxy extension active. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query Redfin listings, property records, market reports, mortgage calculations, and signed-in saved Redfin homes or searches from an agent through MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP acts through the user's signed-in Redfin browser tab and can access saved homes and saved searches. <br>
Mitigation: Install only when that session access is acceptable, and keep the browser extension limited to trusted local use. <br>
Risk: The skill relies on Redfin web behavior and private endpoints rather than a public consumer API. <br>
Mitigation: Use it for normal read-only lookups, avoid bulk scraping or commercial extraction, and expect Redfin session or challenge behavior to affect availability. <br>
Risk: The fetchproxy extension is required to bridge requests through Chrome. <br>
Mitigation: Review the fetchproxy trust model and load the extension only from a source the user trusts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chrischall/redfin-mcp) <br>
- [redfin-mcp npm package](https://www.npmjs.com/package/redfin-mcp) <br>
- [redfin-mcp project link listed in artifact](https://github.com/chrischall/redfin-mcp) <br>
- [fetchproxy extension project link listed in artifact](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON and bash snippets for setup; MCP tool results as text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Redfin lookups and local mortgage calculations; saved-home and saved-search tools depend on a signed-in Redfin browser session.] <br>

## Skill Version(s): <br>
0.9.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
