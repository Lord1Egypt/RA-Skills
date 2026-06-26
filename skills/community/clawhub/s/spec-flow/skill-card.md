## Description: <br>
Spec Flow guides AI coding agents through proposal, requirements, design, task breakdown, and implementation phases while creating `.spec-flow/` Markdown documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoVic](https://clawhub.ai/user/echoVic) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure complex feature work before implementation. It helps agents create proposal, requirements, design, and task documents, then proceed through user-approved implementation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated specifications can encode incomplete or incorrect requirements that later guide implementation. <br>
Mitigation: Review proposal, requirements, design, and tasks before approving the next phase or starting implementation. <br>
Risk: Fast or batch execution modes reduce the amount of step-by-step user review before changes are made. <br>
Mitigation: Use the default step-by-step mode for important changes and reserve accelerated modes for well-understood work. <br>
Risk: Helper scripts create local `.spec-flow/` files and update task state based on provided feature names and paths. <br>
Mitigation: Run helper scripts only with trusted feature names and review generated files before relying on them. <br>


## Reference(s): <br>
- [Spec-Driven Development Workflow](references/workflow.md) <br>
- [EARS Requirements Format](references/ears-format.md) <br>
- [Task Decomposition Best Practices](references/task-decomposition.md) <br>
- [Execution Modes](references/execution-modes.md) <br>
- [Interaction Rules](references/interaction-rules.md) <br>
- [Example: User Authentication Feature](references/examples/feature-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown planning files with shell command guidance and task status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local `.spec-flow/` proposal, requirements, design, and task documents; generated Markdown is Chinese by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
