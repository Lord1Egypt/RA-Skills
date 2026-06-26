## Description: <br>
Wire one site-scoped read-only MCP sidecar to a local Campus Copilot snapshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local agent operators use this skill to connect a single site-scoped, read-only MCP sidecar to a Campus Copilot snapshot for inspecting site records without live browser interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local agent runtime may be able to read or retain private campus data from the selected snapshot. <br>
Mitigation: Use only trusted MCP consumers and point the sidecar at the specific snapshot and site intended for sharing. <br>
Risk: Responses may be over-scoped if the agent treats snapshot data as live campus state. <br>
Mitigation: Keep claims snapshot-scoped and read-only, and avoid using this skill for posting, replying, submitting, or live browser control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/site-mcp-consumer) <br>
- [Publisher profile](https://clawhub.ai/user/xiaojiou176) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline command and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only, snapshot-scoped local MCP setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
