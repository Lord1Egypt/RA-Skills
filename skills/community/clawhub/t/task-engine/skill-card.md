## Description: <br>
Multi-agent task orchestration engine with state machine tracking. Use when complex multi-step projects need automated monitoring, multi-agent collaboration, and Discord-based progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron-G](https://clawhub.ai/user/zeron-G) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create, dispatch, monitor, and recover multi-step work across multiple agents. It is suited to projects that need state-machine tracking, heartbeat checks, JSON status output, and Discord-formatted progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented destructive reset guidance could remove live task data if run in a real workspace. <br>
Mitigation: Use an isolated `TASK_ENGINE_TASKS_DIR` for testing and do not run destructive reset commands against live task directories. <br>
Risk: Task titles, descriptions, notes, and acceptance criteria may be sent into downstream agent prompts or Discord-formatted summaries. <br>
Mitigation: Keep secrets and untrusted instructions out of task text, review task content before dispatch, and confirm Discord settings before sharing generated summaries externally. <br>


## Reference(s): <br>
- [Agent Capabilities Reference](references/agent-capabilities.md) <br>
- [State Transitions Reference](references/state-transitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local task JSON, recovery commands, state transition guidance, and Discord-formatted notification text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
