## Description: <br>
Creates and edits WeCom documents and smart sheets through mcporter and a configured WeCom document MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boge-net](https://clawhub.ai/user/boge-net) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and employees use this skill to create WeCom documents and smart sheets, configure the required mcporter bridge, and write structured document or table content through the WeCom document MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic document requests may be routed to WeCom in the active environment. <br>
Mitigation: Install and enable the skill only where WeCom should be the default document platform, and confirm routing expectations for sensitive workflows. <br>
Risk: The skill depends on mcporter and a configured wecom-doc MCP server that may access business content. <br>
Mitigation: Verify the mcporter package, MCP server configuration, and WeCom/OpenClaw settings are trusted before processing sensitive content. <br>
Risk: Document edit operations may overwrite the whole skill-created document instead of appending. <br>
Mitigation: Review existing content or keep a backup before edit operations that replace document content. <br>


## Reference(s): <br>
- [WeCom document API reference](references/doc-api.md) <br>
- [ClawHub release page](https://clawhub.ai/boge-net/wecom-ccuniverse-leo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke mcporter to create or edit WeCom documents and smart sheets after required configuration is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
