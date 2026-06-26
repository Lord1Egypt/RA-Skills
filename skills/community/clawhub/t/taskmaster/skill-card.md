## Description: <br>
Project manager and task delegation system for breaking down complex work, assigning AI models by task complexity, spawning sub-agents, tracking progress, and managing token budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlwrow](https://clawhub.ai/user/jlwrow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI workflow operators use this skill to decompose multi-step projects, select cost-appropriate models, prepare OpenClaw sub-agent sessions, and monitor estimated or actual token spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated sub-agent commands may launch unintended delegated work if accepted without review. <br>
Mitigation: Review each generated sessions_spawn payload before running it, especially the task text, model, timeout, label, and cleanup settings. <br>
Risk: Task descriptions and retained sessions may contain sensitive project details. <br>
Mitigation: Avoid putting secrets in task descriptions and delete or rotate kept sessions when task history should not persist. <br>
Risk: Local cost history may persist operational task metadata. <br>
Mitigation: Delete or rotate taskmaster-costs.json when cost logs should not be retained. <br>
Risk: Delegated work can exceed intended spend if budgets are not set clearly. <br>
Mitigation: Set explicit budgets and review estimated and actual token costs during execution. <br>


## Reference(s): <br>
- [Model Selection Rules](references/model-selection-rules.md) <br>
- [Task Templates](references/task-templates.md) <br>
- [Token Tracking Integration](TOKEN_TRACKING_README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python code examples, JSON spawn-command payloads, and local JSON cost records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces model-selection recommendations, budget estimates, session-spawn inputs, progress status, and token-cost logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
