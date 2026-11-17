## Description:

Clarifies ambiguous development requirements into implementable, verifiable agreements by checking source evidence and asking targeted questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlykan](https://clawhub.ai/user/wlykan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product owners, and implementation agents use this skill to clarify scope, business rules, inputs, outputs, and acceptance criteria before implementation. It is most useful when requirements are ambiguous, conflicting, or blocked by decisions that source evidence alone cannot resolve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect relevant project files while clarifying requirements.

Mitigation: Limit the task scope when needed and review the cited evidence boundaries before relying on the conclusions.

Risk: Requirement handoff output can be mistaken for completed implementation or verified test results.

Mitigation: Treat clarified rules and acceptance scenarios as implementation guidance until the requested changes are separately implemented and verified.

Risk: The skill may respond in Chinese by default.

Mitigation: Ask for another language when the project team or review workflow requires it.

## Reference(s):

- [OpenSpec handoff rules](references/openspec-handoff.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with structured sections and targeted Q&A]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source-attributed facts, confirmed rules, acceptance scenarios, pending questions, and handoff guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
