## Description: <br>
Systematic task implementation using TDD, phase checkpoints, and structured commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to implement planned work with test-first development, quality gates, checkpoint approvals, and traceable commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may lead an agent to run normal project commands such as tests, package tooling, and Git operations. <br>
Mitigation: Review proposed commands and commits before execution, especially in projects with sensitive branches, deployment hooks, or generated artifacts. <br>
Risk: Strict phase checkpoints and coverage targets can slow small fixes or projects without established test infrastructure. <br>
Mitigation: Use the skill for planned implementation work and adapt checkpoint scope explicitly when the project lacks tests or the change is trivial. <br>


## Reference(s): <br>
- [TDD Quick Reference](references/tdd-quick-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wpank/workflow-patterns) <br>
- [Publisher Profile](https://clawhub.ai/user/wpank) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes TDD lifecycle steps, checkpoint checklists, quality gates, and commit message patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
