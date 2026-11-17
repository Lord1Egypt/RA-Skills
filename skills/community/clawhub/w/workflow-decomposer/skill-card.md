## Description:

Workflow Decomposer breaks complex tasks into clear executable steps, selects suitable models for each step, tracks workflow progress, and provides blocker diagnosis with solution options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpj18337105261](https://clawhub.ai/user/lpj18337105261)

### License/Terms of Use:


## Use Case:

Developers, operators, and agent users use this skill to turn complex work requests into sequenced plans with visible progress, per-step model assignments, and recovery guidance when a task stalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage use of specific model families even when they are unavailable or not approved in the deployment environment.

Mitigation: Review model assignments before execution and map suggested models to approved local equivalents.

Risk: Generated workflow plans can be incorrect, incomplete, or misleading for complex tasks.

Mitigation: Review decomposition steps, dependencies, and completion criteria before letting an agent execute the plan.

Risk: Optional progress tracking may create local workflow-state.json files containing task details.

Mitigation: Store workflow state only in approved workspaces and remove it when it is no longer needed.

Risk: The skill may produce Chinese-language output that some operators cannot review effectively.

Mitigation: Request output in the operator's preferred review language before executing or approving a workflow plan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lpj18337105261/skills/workflow-decomposer)
- [Model Capabilities Reference](references/model-capabilities.md)
- [Model Selection Guide](references/model-selection.md)
- [Model-Specific Prompt Guide](references/model-prompt-guide.md)
- [Workflow Decomposition Template](references/workflow-template.md)
- [Workflow Templates](references/workflow-templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional JSON workflow state and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workflow-state.json files when progress tracking scripts are used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
