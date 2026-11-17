## Description:

Tvs Analyze helps developers explain project structure, dependencies, business logic, code behavior, issues, and improvement opportunities in clear Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand unfamiliar codebases, explain specific code paths, map dependencies and calls, and summarize risks or improvement opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional dependency-graph command may run local Node tooling against the user's project.

Mitigation: Run it only in a trusted project after reviewing the referenced script and project dependencies.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style explanatory text with optional ASCII diagrams and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language explanations; optional local dependency-graph command for trusted projects]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
