## Description: <br>
Executes a spec-plan.md implementation plan by completing tasks in order, validating each step, and retrying failed checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to resume or execute SDD implementation plans from spec-plan.md files, update task checkboxes, run validation steps, and stop with a concise summary when blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit project files and run validation commands while carrying out a selected plan. <br>
Mitigation: Review the selected plan and its checkbox state before starting or resuming execution. <br>
Risk: Repeated fix-and-retry behavior can compound an incorrect plan or failing validation step. <br>
Mitigation: Inspect changed files and the final blocked or completed summary before accepting the result. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mahingbun-dev/sdd-executing-plans) <br>
- [Publisher profile](https://clawhub.ai/user/mahingbun-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status updates, project file changes, validation command results, and final execution summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update the selected spec-plan.md checklist and project files while executing the plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
