## Description: <br>
Twitter API Alternative — Search 1B+ tweets with natural language queries, boolean filters, and one-click CSV exports up to 64K rows; look up profiles, find users by topic, and track conversations through Xpoz MCP without a Twitter developer account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atyachin](https://clawhub.ai/user/atyachin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to search Twitter/X content, inspect profiles and relationships, track conversations, and export social data to CSV through Xpoz MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an npm-installed MCP helper and network access to Xpoz's hosted MCP service. <br>
Mitigation: Review the npm package provenance before installation and only enable the Xpoz MCP connection in environments where hosted social-data processing is acceptable. <br>
Risk: Using the skill may send Xpoz-related queries, results, and an Xpoz API token to Xpoz's hosted service. <br>
Mitigation: Use scoped or revocable credentials where possible and avoid sending data that should not leave the execution environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atyachin/twitter-api-alternative) <br>
- [Publisher profile](https://clawhub.ai/user/atyachin) <br>
- [Xpoz](https://xpoz.ai) <br>
- [xpoz-setup skill](https://clawhub.ai/skills/xpoz-setup) <br>
- [xpoz-social-search skill](https://clawhub.ai/skills/xpoz-social-search) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides use of mcporter commands against Xpoz MCP tools; search operations may return operation IDs and CSV download URLs.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
