## Description:

Executes spec-plan.md implementation plans in order, verifies each task, updates checklist progress, and reports completion or blockers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill in OpenClaw SDD workspaces to execute implementation plans from spec-plan.md files, run verification steps, and resume incomplete task checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can resume execution from checked plan items without fresh confirmation.

Mitigation: Manually inspect any partially completed spec-plan.md before resuming and confirm the remaining steps still match the intended work.

Risk: Caller-supplied plan paths and weak scoping may cause work to run outside the intended SDD workspace.

Mitigation: Use trusted spec-plan.md files inside the intended SDD workspace and run the skill in a sandbox or limited-permission workspace when possible.

Risk: Plan execution may edit files and run verification commands.

Mitigation: Review the plan before installation or execution, and monitor completed task summaries and blocker reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/skills/sdd-executing-plans)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status updates with inline commands, checklist changes, and concise execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify plan files as tasks and checks are completed; blocked tasks include a concise failure summary.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
