## Description: <br>
Test-driven development workflow enforcing 80%+ code coverage with unit, integration, and E2E tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute test-driven feature work, bug fixes, and refactors with RED-GREEN-REFACTOR gates, coverage checks, and git checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository npm scripts can run project-defined commands during test and coverage steps. <br>
Mitigation: Review the repository's npm test and coverage scripts before using the workflow on an important codebase. <br>
Risk: Integration and E2E tests may touch real services or data if the repository is not configured for test isolation. <br>
Mitigation: Use test environments or mocked services for integration and E2E runs. <br>
Risk: Git checkpoint commits may affect the working branch history. <br>
Mitigation: Run checkpoint commits on an appropriate branch for the feature, bug fix, or refactor. <br>


## Reference(s): <br>
- [TDD Workflow on ClawHub](https://clawhub.ai/djc00p/tdd-workflow) <br>
- [Workflow Steps](references/workflow-steps.md) <br>
- [Patterns and Best Practices](references/patterns-and-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; expects npm and git when executing test and checkpoint steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
