## Description: <br>
Read your Workday HR data, including tasks, pay, benefits, and compensation, via MCP through your own signed-in session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to configure and use a read-only Workday MCP server that retrieves their own Workday tasks and HR data through an existing signed-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive Workday HR information through an active browser session. <br>
Mitigation: Install only when comfortable granting that access, use it only with your own account, and keep the workflow read-only. <br>
Risk: Use may conflict with an employer's acceptable-use rules for Workday access. <br>
Mitigation: Check employer policy before use and avoid using the skill for data or accounts outside your authorization. <br>
Risk: The setup depends on the workday-mcp package and fetchproxy browser extension. <br>
Mitigation: Confirm the package and extension source before installation. <br>


## Reference(s): <br>
- [Workday MCP package](https://www.npmjs.com/package/workday-mcp) <br>
- [Fetchproxy extension setup](https://github.com/chrischall/fetchproxy) <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/workday-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, JSON] <br>
**Output Format:** [Markdown instructions with JSON configuration and shell command snippets; MCP tools return structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Workday tenant, an active signed-in Workday browser session, and the fetchproxy extension.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
