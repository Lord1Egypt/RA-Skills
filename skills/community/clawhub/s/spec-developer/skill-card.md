## Description:

Automates a spec-driven development workflow with commands to draft specs, plan tasks, and execute implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soponcd](https://clawhub.ai/user/soponcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to manage a spec-driven workflow: drafting feature specifications, converting approved specs into tracked tasks, and executing implementation work against those specs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The execution workflow can modify project planning files, code, tests, and implementation status.

Mitigation: Review generated specs and task updates before execution, and inspect code changes and test results before accepting them.

Risk: The skill may run the repository's native test script during implementation.

Mitigation: Run it only in repositories where invoking the native test command is expected and safe for the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soponcd/skills/spec-developer)
- [Skill homepage](https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/spec-developer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with command examples, generated spec files, task-list updates, code changes, tests, and shell command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify repository planning files, implementation code, tests, and status markers as part of the requested spec workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
