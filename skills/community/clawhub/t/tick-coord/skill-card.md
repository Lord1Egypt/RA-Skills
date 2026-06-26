## Description: <br>
Multi-agent task coordination via Git-backed Markdown (tick-md). Use when coordinating work across avatars or agents, managing tasks, tracking dependencies, or running multi-agent workflows with TICK.md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoReuMD](https://clawhub.ai/user/CryptoReuMD) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and multi-agent operators use this skill to coordinate work through TICK.md task files, command-line workflows, MCP tools, dependency tracking, agent handoffs, and status reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project task records may contain sensitive details and can be exposed through a network dashboard or remote sync. <br>
Mitigation: Use localhost-only dashboard access, stop the background server after inspection, avoid public or shared networks, and review task contents before Git push or Convex sync. <br>
Risk: Agents can edit TICK.md task records as part of normal coordination workflows. <br>
Mitigation: Review task changes before syncing or committing, and validate task structure after bulk edits or multi-agent handoffs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/CryptoReuMD/tick-coord) <br>
- [tick-md CLI npm package](https://npmjs.com/package/tick-md) <br>
- [tick-mcp-server npm package](https://npmjs.com/package/tick-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and task-management examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local TICK.md task records and suggest Git, CLI, MCP, dashboard, or sync commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
