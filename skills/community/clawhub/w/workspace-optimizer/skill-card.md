## Description: <br>
Audit, optimize, and maintain an OpenClaw agent workspace through health checks, skill audits, memory cleanup review, and performance tuning guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentricai-owner](https://clawhub.ai/user/agentricai-owner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit OpenClaw workspace health, review installed skills, identify stale memory or cron-job state, and prepare cleanup actions for review before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup recommendations could remove useful skills, memory files, or cron jobs if applied without review. <br>
Mitigation: Require the agent to show the exact proposed changes, make backups before pruning memory or editing MEMORY.md, and get explicit confirmation before uninstalling skills or disabling cron jobs. <br>
Risk: Workspace maintenance commands may produce misleading or incomplete results when dependency or cron-job history is not checked. <br>
Mitigation: Review skill dependencies and cron-job run history before acting, and prefer archiving old memory files over deletion. <br>


## Reference(s): <br>
- [Workspace Optimizer ClawHub Page](https://clawhub.ai/agentricai-owner/skills/workspace-optimizer) <br>
- [AgentricAI-Owner Publisher Profile](https://clawhub.ai/user/agentricai-owner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit checklists, remediation suggestions, and commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
