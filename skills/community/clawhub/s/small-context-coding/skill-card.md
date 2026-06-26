## Description: <br>
Efficient coding workflow for small-context models working on medium or large codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ambitioncn](https://clawhub.ai/user/ambitioncn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure coding, debugging, refactoring, and analysis work when context is limited. It guides the agent to keep concise file-based state, split work into small verified steps, and use sub-agents only for bounded subproblems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create persistent notes in the repository that may contain private task details. <br>
Mitigation: Confirm the notes location before use and keep generated notes out of version control when they contain sensitive information. <br>
Risk: Helper scripts may create files or run local workflow checks in the workspace. <br>
Mitigation: Require explicit user approval before setup commands, helper scripts, or file modifications are run. <br>
Risk: The activation scope is broad for general coding work. <br>
Mitigation: Use the skill only for coding tasks that benefit from file-based planning, checkpointing, or bounded sub-agent delegation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ambitioncn/small-context-coding) <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Sub-agent Patterns](references/subagent-patterns.md) <br>
- [Templates](references/templates.md) <br>
- [Verification Defaults](references/verification-defaults.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated note or brief files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent task notes and sub-agent brief files in the user's repository when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
