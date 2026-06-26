## Description: <br>
Autonomous development loops with iteration, backpressure gates, and completion criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richginsberg](https://clawhub.ai/user/richginsberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run bounded autonomous coding loops for multi-iteration feature work, validation, progress tracking, and structured completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous loops can edit and commit project files. <br>
Mitigation: Use a feature branch or sandbox, keep confirmation checkpoints enabled, and review plans, progress logs, diffs, and commits before pushing or deploying. <br>
Risk: Long-running or overlapping sessions can cause stale status, file conflicts, or unbounded iteration. <br>
Mitigation: Set maximum iteration and timeout limits, require progress logging, verify completion signals, and avoid overlapping sessions on the same codebase. <br>
Risk: Generated implementation work can fail tests, lint, typecheck, build, or subjective quality gates. <br>
Mitigation: Run the configured validation gates and require failures to be fixed before marking work complete or committing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/richginsberg/ralph-mode) <br>
- [Backpressure Gates Reference](references/backpressure.md) <br>
- [Code Patterns Reference](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project planning, progress, operations, source, and test files during an autonomous development loop.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
