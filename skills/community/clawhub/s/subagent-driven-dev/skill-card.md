## Description: <br>
Use when executing implementation plans with independent tasks in the current session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[user-wangjun](https://clawhub.ai/user/user-wangjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to execute an existing implementation plan as a sequence of mostly independent tasks, with implementer, spec-review, and code-quality-review subagent passes for each task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can cause an agent to make code changes, run tests, and create commits. <br>
Mitigation: Use the skill on a branch and review diffs and commits before pushing or deploying. <br>
Risk: The artifact includes Chinese escalation examples that may confuse teams expecting only English prompts. <br>
Mitigation: Clarify language expectations before use or adapt the prompt examples for the team's operating language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/user-wangjun/subagent-driven-dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown instructions and prompt templates for agent task execution and review] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce code changes, tests, commits, review findings, and task-status updates through the agent workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
