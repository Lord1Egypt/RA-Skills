## Description:

需求调度官 helps users capture requirements as cards, manage backlog state, and dispatch confirmed work to background subagents for parallel implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystar513](https://clawhub.ai/user/luckystar513)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to discuss new requirements, record them as Markdown cards, inspect backlog and scheduling status, and move confirmed work through dispatch and acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A project-controlled .wdp-prd pointer can direct writes and background task state to an unintended requirements directory.

Mitigation: Before write-capable commands, verify that .wdp-prd resolves to the intended <PRD_ROOT>/<project-slug>/ directory.

Risk: Dispatch can start background agents that modify code before review and merge gates complete.

Mitigation: Dispatch only confirmed requirements, inspect returned implementation reports, and keep acceptance gated on tests, code review, and explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckystar513/skills/wdp-prd-zh)
- [Requirement card template](artifact/references/card-template.md)
- [Test scenarios](artifact/references/test-scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown requirement cards, backlog tables, scheduling reports, command guidance, and implementation review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update requirement cards, execution-plan.md, and archived implementation plans under the configured PRD root.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
