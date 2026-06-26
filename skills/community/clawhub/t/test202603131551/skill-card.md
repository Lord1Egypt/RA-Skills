## Description: <br>
Retrieve real-time commodity price quotes using Octagon MCP for current prices, day ranges, moving averages, and commodity market comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdm1136](https://clawhub.ai/user/wdm1136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and interpret real-time commodity quote data through the Octagon MCP server. It supports price checks, trend analysis, day-range review, moving-average comparison, and commodity comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Octagon API key and MCP configuration, which can expose credentials if stored or shared carelessly. <br>
Mitigation: Store the API key securely, avoid committing MCP configuration files, and rotate the key if it may have been exposed. <br>
Risk: Commodity quote interpretation can be mistaken for financial or trading advice. <br>
Mitigation: Treat the output as market information only and have users apply appropriate financial review before making trading decisions. <br>
Risk: The skill depends on running the Octagon MCP server through npx. <br>
Mitigation: Install only when the publisher and Octagon MCP dependency are trusted in the deployment environment. <br>


## Reference(s): <br>
- [Interpreting Commodities Quote Results](references/interpreting-results.md) <br>
- [Octagon MCP Setup](references/mcp-setup.md) <br>
- [Octagon Docs](https://docs.octagonagents.com) <br>
- [Octagon MCP GitHub](https://github.com/OctagonAI/octagon-mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/wdm1136/test202603131551) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Octagon MCP server configuration and an Octagon API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
