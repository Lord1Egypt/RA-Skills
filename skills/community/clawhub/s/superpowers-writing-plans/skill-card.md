## Description: <br>
Use when you have a spec or requirements for a multi-step task, before touching code - guides writing comprehensive implementation plans with bite-sized tasks, TDD, and DRY/YAGNI principles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill before implementation to convert a multi-step specification into a concrete, test-driven implementation plan. The plan is expected to identify files, task-sized steps, tests, verification commands, and commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans can include git commands, commits, merges, and execution handoffs that affect a repository. <br>
Mitigation: Review the specific commands and approve commits, merges, or delegated execution before running them. <br>
Risk: The skill can reference other skills for subagent execution or branch cleanup. <br>
Mitigation: Review any referenced subagent or cleanup skills separately before using them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown implementation plan with code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans are intended to be reviewed before any generated commands, commits, merges, or delegated execution are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
