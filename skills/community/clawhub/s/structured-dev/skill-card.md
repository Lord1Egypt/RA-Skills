## Description: <br>
Structured Dev guides agents through a Research, Plan, Annotate, Implement workflow for code changes, requiring written review checkpoints before implementation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lskun](https://clawhub.ai/user/lskun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to make coding agents research the existing system, write reviewable plans, process annotations, and then implement approved work with progress tracked in project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow creates .dev planning files and may later guide code edits in the active project. <br>
Mitigation: Use it only on the intended project and branch, then review .dev/research.md, .dev/plan.md, diffs, and command output before approving implementation. <br>
Risk: A flawed research or plan phase can preserve incorrect architecture assumptions into implementation. <br>
Mitigation: Require human review of the research and plan documents before saying to implement, and send the agent back through annotation when assumptions are wrong. <br>
Risk: The workflow can describe spawning another coding agent or creating a GitHub/GitLab merge request. <br>
Mitigation: Require explicit confirmation before spawning another agent or creating any merge request. <br>


## Reference(s): <br>
- [Workflow Guide](references/workflow-guide.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans, progress updates, code edits, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates .dev planning files; may guide implementation after explicit user approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
