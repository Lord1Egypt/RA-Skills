## Description: <br>
MCP server that tracks Claude Code subagent performance in real time, detects silent failures, token waste from idle loops, and duplicate task spawns, and reports fleet-wide health scores and actionable alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinas90](https://clawhub.ai/user/abhinas90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this MCP server with Claude Code to register subagents, monitor progress, detect stuck or duplicate work, and review fleet health and token-waste estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subagent task names and monitoring metadata are retained locally under ~/.claude. <br>
Mitigation: Avoid putting secrets or sensitive customer details in task names or descriptions, and delete ~/.claude/subagent-health-state.json when retained state should be cleared. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abhinas90/subagent-health-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/abhinas90) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON MCP tool responses and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local monitoring state under ~/.claude/subagent-health-state.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
