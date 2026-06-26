## Description: <br>
Rube lets an agent call Rube tools for recipe search, execution, scheduling, connection management, remote bash and workbench operations, tool search, schema retrieval, and recipe management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Rube automation tools, discover app tools, manage connections, execute recipes and tools, and process larger results in a remote sandbox. It is intended for workflows that need authenticated access to connected apps and should be reviewed before installation because it can run remote commands and scheduled automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports an embedded bearer token in the release. <br>
Mitigation: Use only a version that removes the embedded token, rotates the exposed credential, and requires each installer to provide their own scoped credential. <br>
Risk: The security summary reports broad remote automation, shell, workbench, API, scheduling, and memory capabilities. <br>
Mitigation: Require explicit user approval before remote bash, direct API calls, bulk execution, recipe execution, or recurring schedules, and document what data is sent to Rube and connected apps. <br>


## Reference(s): <br>
- [Rube MCP](https://rube.app/mcp) <br>
- [ClawHub Rube Release](https://clawhub.ai/robertstarry-gif/rube) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return authentication links, remote sandbox outputs, recipe metadata, tool schemas, and connected-app results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
