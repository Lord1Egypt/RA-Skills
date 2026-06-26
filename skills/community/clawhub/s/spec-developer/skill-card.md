## Description: <br>
Automates spec-driven development workflows with commands for drafting specs, planning tasks, and executing implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soponcd](https://clawhub.ai/user/soponcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft feature specs, convert spec task breakdowns into a project task list, and execute implementation work from trusted spec files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify project files and run a fixed local test script when invoked. <br>
Mitigation: Use version control, run it only on trusted specs, and review diffs and test output before committing changes. <br>
Risk: Planning commands can append milestones and renumber task identifiers in specs/tasks.md. <br>
Mitigation: Review task-list changes and task numbering after /spec-plan and /spec-execute before accepting the update. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/soponcd/spec-developer) <br>
- [Skill homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/spec-developer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with repository file edits and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update spec files, task lists, implementation files, tests, and task status markers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
