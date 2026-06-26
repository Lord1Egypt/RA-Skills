## Description: <br>
Installs the Solo Factory toolkit, including 23 startup workflow skills and optional solograph MCP setup for code intelligence, knowledge-base search, and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and startup builders use this skill to install the Solo Factory skill collection across supported AI agents and optionally configure solograph MCP for local code, session, and search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk installation can modify multiple AI-agent environments and add a large toolkit at once. <br>
Mitigation: Use a scoped install path, inspect the referenced contents first, and confirm the intended target agents before running installation commands. <br>
Risk: Optional plugin and MCP setup can add persistent behavior, hooks, agents, or auto-start services. <br>
Mitigation: Skip MCP unless local code or session search is needed, and identify uninstall or disable steps before using the plugin path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fortunto2/solo-factory) <br>
- [Solo Factory GitHub repository](https://github.com/fortunto2/solo-factory) <br>
- [solograph MCP server](https://github.com/fortunto2/solograph) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask whether to configure the optional MCP server.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
