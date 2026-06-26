## Description: <br>
Intelligent task management and execution coordination officer. Automatically generates task lists, intelligently decomposes complex tasks, matches AI agents, makes priority decisions, and monitors progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break complex goals into structured task plans, match work to suitable agents, set execution priority, and monitor task progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled helper scripts create or update local task JSON files, so an unintended output path could overwrite existing workspace data. <br>
Mitigation: Run the scripts in a project workspace and choose explicit output paths for files that are safe to create or update. <br>
Risk: Task decomposition, agent matching, priority scoring, and retry suggestions are heuristic and may produce unsuitable execution plans for high-impact work. <br>
Mitigation: Review generated plans, dependencies, priorities, and agent assignments before delegating or executing tasks. <br>


## Reference(s): <br>
- [Agent Matching Strategy](references/agent_matching.md) <br>
- [Workflow Patterns](references/workflow_patterns.md) <br>
- [Task Template Library](references/task_templates.md) <br>
- [ClawHub release page](https://clawhub.ai/openlark/task-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON examples and shell commands; helper scripts produce JSON task files and text progress reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local task JSON files when the bundled helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
