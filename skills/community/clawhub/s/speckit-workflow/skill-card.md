## Description: <br>
Complete Spec-Driven Development (SDD) orchestrator for OpenClaw. Initializes SpecKit and manages the full engineering lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinayakv22](https://clawhub.ai/user/vinayakv22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill with OpenClaw to run a Spec-Driven Development workflow that creates project principles, specifications, clarification questions, plans, task lists, consistency analysis, and implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create branches, commit changes, and push repository updates when automated Git operations are enabled. <br>
Mitigation: Install only in repositories you control, answer No unless automated Git operations are intended, and review diffs before publishing. <br>
Risk: Bundled shell helpers use unsafe dynamic evaluation of branch or path data. <br>
Mitigation: Avoid using the workflow on untrusted repositories or crafted branch names until the eval-based helpers are fixed. <br>
Risk: Generated agent-context files may affect future agent behavior. <br>
Mitigation: Inspect generated agent-context files before keeping or using them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vinayakv22/speckit-workflow) <br>
- [Publisher profile](https://clawhub.ai/user/vinayakv22) <br>
- [github/spec-kit](https://github.com/github/spec-kit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, generated project files, shell command guidance, and repository changes when explicitly allowed by the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update SpecKit artifacts such as constitution.md, spec.md, plan.md, tasks.md, checklists, and agent-context files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
