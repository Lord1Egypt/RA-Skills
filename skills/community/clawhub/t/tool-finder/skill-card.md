## Description: <br>
Tool Finder helps agents search ClawHub skills and Smithery MCP servers, rank and label results, and provide install-oriented guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lironghai](https://clawhub.ai/user/lironghai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant ClawHub skills or Smithery MCP servers and to get command-line guidance for searching or installing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic invocation can make this skill a default marketplace search workflow. <br>
Mitigation: Install it only when that default behavior is desired, and review any AGENTS.md or TOOLS.md additions before making them persistent. <br>
Risk: Install commands can install third-party skills non-interactively. <br>
Mitigation: Confirm the exact package name and source before running install commands, and prefer a manual or interactive install flow for third-party skills. <br>
Risk: Search results and recommendations can be incomplete or affected by rate limits. <br>
Mitigation: Use exact search when the name is known, check verbose warnings, and verify important results on ClawHub or Smithery before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lironghai/tool-finder) <br>
- [Publisher profile](https://clawhub.ai/user/lironghai) <br>
- [ClawHub](https://clawhub.ai) <br>
- [Smithery API](https://api.smithery.ai) <br>
- [Required tools metadata](artifact/SKILL.md) <br>
- [Setup guide](artifact/SETUP_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and install guidance may depend on ClawHub, Smithery, Node.js, curl, jq, and network availability.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
