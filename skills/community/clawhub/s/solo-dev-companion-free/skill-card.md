## Description: <br>
独立开发者TDD工作流引擎，自动执行实施计划任务、提交代码并更新进度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, solo founders, and TDD learners use this skill to execute planned development tasks from docs/plan, run a red-green-refactor workflow, update task progress, and create traceable git commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to run local development commands, edit repository files, and create git commits. <br>
Mitigation: Review generated diffs and commits before pushing or deploying changes. <br>
Risk: Broad activation wording can cause the agent to apply the workflow in situations where the user expected lighter guidance. <br>
Mitigation: Invoke the skill only for planned development tasks and confirm the target plan or task before allowing file edits or shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/solo-dev-companion-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces repository edits, task status updates, and git commit guidance when used by an agent with local command and file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
