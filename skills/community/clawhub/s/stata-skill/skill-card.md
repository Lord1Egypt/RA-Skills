## Description: <br>
The most stable way to execute Stata commands, install ado packages, read help documents, and analyze data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SepineTam](https://clawhub.ai/user/SepineTam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to automate Stata workflows, including running do-files, installing ado packages, reading Stata help, inspecting datasets, and reviewing execution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute Stata do-files, so reviewed analysis code may still run commands that affect local files or produce misleading results. <br>
Mitigation: Review do-files before execution and approve the intended analysis steps and file locations. <br>
Risk: The skill can install ado packages from SSC, GitHub, or Net sources. <br>
Mitigation: Approve package names and sources before installation and prefer trusted package sources. <br>
Risk: Stata logs and analyzed datasets may contain sensitive or confidential data. <br>
Mitigation: Handle datasets and logs according to the user's data policy and avoid sharing logs unless their contents have been reviewed. <br>


## Reference(s): <br>
- [Stata-MCP Documentation](https://docs.statamcp.com) <br>
- [OpenClaw Skill Installation](https://docs.statamcp.com/skills/openclaw) <br>
- [Stata-MCP FAQ](https://docs.statamcp.com/faq) <br>
- [Stata-MCP GitHub Repository](https://github.com/statamcp/stata-mcp) <br>
- [Publisher Profile](https://clawhub.ai/user/SepineTam) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Stata and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated do-files, Stata logs, dataset summaries, and ado package names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
