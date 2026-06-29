## Description: <br>
Subagent Prompt produces a comprehensive handoff prompt that lets a fresh agent session orchestrate sub-agent execution of planned work with per-task verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to turn a discussed work plan into a self-contained prompt for a new session that dispatches one sub-agent per task and requires concrete verification before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated handoff prompt can direct multiple sub-agents to act on source files, so vague source material or weak verification steps could lead to incorrect execution. <br>
Mitigation: Review the source artifacts, task decomposition, per-task checks, and final integration command before running the prompt in a new session. <br>
Risk: The skill assumes the target session supports sub-agents and can access the absolute paths named in the prompt. <br>
Mitigation: Use it only in a compatible agent environment and confirm the referenced paths and required permissions before dispatching work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/subagent-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown fenced prompt with task lists, paths, verification commands, and failure-handling policy] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated prompt is intended for a fresh agent session that supports sub-agents and can access the named absolute paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
