## Description: <br>
Team Tasks.Skip coordinates multi-agent development workflows through shared JSON task files, including linear pipelines, DAG dependency workflows, and debate-style cross-review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdp1117](https://clawhub.ai/user/zdp1117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate work across code, test, documentation, and monitoring agents while tracking assignments, status, logs, dependency outputs, and collected results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions, logs, dependency outputs, or result summaries may expose secrets, customer data, private paths, or proprietary project details. <br>
Mitigation: Use the skill only with trusted agents, redact sensitive inputs before dispatch, and keep the task data directory private. <br>
Risk: Hardcoded Telegram-backed session and group identifiers may route project context or agent results to unintended destinations. <br>
Mitigation: Verify or replace the Telegram session and group IDs before use, and disable relay behavior when the destination cannot be confirmed. <br>


## Reference(s): <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code Agent Teams documentation](https://docs.anthropic.com/en/docs/claude-code/agent-teams) <br>
- [Agent Teams Official Docs](docs/AGENT_TEAMS_OFFICIAL_DOCS.md) <br>
- [Gap Analysis](docs/GAP_ANALYSIS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON task data, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local JSON task files; may include project context, task descriptions, logs, dependency outputs, and result summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
