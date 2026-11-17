## Description:

Finds regressions that a code change may cause outside the edited lines by tracing affected callers, shared state, contracts, and test coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to trace the blast radius of code changes, identify concrete regression scenarios, and prove or clear them with observed test runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to read broadly across a repository and run tests while tracing regression impact.

Mitigation: Review the requested scope and command plan before use in sensitive repositories.

Risk: Broad natural-language triggers may activate the skill when a related but different workflow was intended.

Mitigation: Use explicit wording when requesting or declining a regression hunt.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown report with cited file references, command summaries, and categorized regression findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports confirmed, suspected, and cleared regression scenarios with coverage details and targeted next-step offers.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
