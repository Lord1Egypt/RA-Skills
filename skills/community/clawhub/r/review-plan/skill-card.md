## Description:

Review implementation plans for parallelization, TDD, types, libraries, and security before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review implementation plans before execution, checking parallelization, TDD discipline, type/API fit, library practices, and security or edge-case coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a user-provided plan, inspects relevant code, loads applicable review guidance, and writes a review Markdown file beside the plan.

Mitigation: Run it only in workspaces where the agent is allowed to inspect the referenced plan and code, and review the generated Markdown before using it to change an implementation plan.

Risk: A review workflow could be mistaken for permission to execute the implementation plan.

Mitigation: The workflow is intended to stop after writing the review and ask for the user's next choice; it should not execute the plan automatically.

Risk: Incorrect or misleading findings could affect implementation decisions.

Mitigation: The skill requires same-turn quotes from the plan or code before issuing findings, then saves a consolidated report for human review.

## Reference(s):

- [Review Plan on ClawHub](https://clawhub.ai/anderskev/skills/review-plan)

## Skill Output:

**Output Type(s):** [markdown, guidance, files]

**Output Format:** [Markdown review report with a concise next-step prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a review Markdown file beside the reviewed plan and does not execute the implementation plan automatically.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
