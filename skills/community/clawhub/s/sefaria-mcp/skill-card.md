## Description: <br>
Access Jewish texts, commentaries, and daily study materials from Torah, Talmud, and related collections through the Sefaria MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeperl](https://clawhub.ai/user/abeperl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MCP users use this skill to install and configure a Sefaria MCP server for retrieving Jewish texts, commentaries, cross-references, parsha information, learning calendars, book metadata, and related topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a third-party npm package. <br>
Mitigation: Confirm trust in the npm package and maintainer before installation. <br>
Risk: The documented npx command can run an unpinned package version. <br>
Mitigation: Pin a known package version when reproducibility or change control matters. <br>
Risk: Queries may be handled by the MCP server and upstream Sefaria service. <br>
Mitigation: Avoid sending private or sensitive study queries unless that handling is acceptable. <br>


## Reference(s): <br>
- [Sefaria](https://www.sefaria.org) <br>
- [sefaria-mcp-server npm package](https://www.npmjs.com/package/sefaria-mcp-server) <br>
- [Sefaria MCP Server ClawHub page](https://clawhub.ai/abeperl/sefaria-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides MCP installation commands, configuration snippets, tool descriptions, and example prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
