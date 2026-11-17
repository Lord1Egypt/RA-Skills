## Description:

Yanjiatuan Task Dispatch is a Chinese-language skill that decomposes investment-research requests into role-based assignments, progress tracking, and output summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators can use this skill to turn Chinese-language investment-research requests into coordinated assignments for fundamental, industry, technical, sentiment, and risk-review roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates task assignments for investment research but does not complete or validate the underlying analysis.

Mitigation: Review the generated dispatch plan and require downstream analysts or agents to substantiate any investment conclusions before use.

Risk: The documentation and generated output are primarily Chinese-language.

Mitigation: Use Chinese-capable reviewers or translation before relying on the dispatch output in non-Chinese workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Text or JSON task-dispatch summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local task identifiers, role assignments, pending statuses, workflow text, and next-step guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
