## Description: <br>
Execution companion for spec-workflow: state navigation, task tracking via tasks.md, incremental delivery, and session recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naozixu](https://clawhub.ai/user/naozixu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill after spec-workflow has produced a plan and tasks.md tracker, so implementation can proceed one task at a time with explicit state tracking, verification, review, and recovery behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct file edits, tests, and commits in a repository as part of its execution workflow. <br>
Mitigation: Confirm the active phase and task before execution, review generated specs and tasks, and treat code edits or commits as user-directed project changes. <br>
Risk: Using the skill without a valid spec-workflow plan or well-formed tasks.md can cause the agent to execute work without reliable state tracking. <br>
Mitigation: Require a valid tasks.md containing task entries with Scope and Verification fields before starting execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naozixu/spec-executor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with tracker updates, review notes, diffs, command suggestions, and implementation changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on a valid spec-workflow tasks.md file with task scope and verification fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
