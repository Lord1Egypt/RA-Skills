## Description:

Before committing scarce time, people, or money, name the best forgone use of those resources and the value delta of the chosen path versus that alternative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and agents use this skill to evaluate scarce time, budget, people, or attention by comparing a chosen commitment with the best forgone alternative. It is intended for prioritization, build-versus-buy, investment, and other non-trivial resource-allocation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence how an agent frames resource-allocation decisions, which may lead to misleading prioritization if alternatives or value estimates are incomplete.

Mitigation: Require a concrete next-best use of the same resources, separate best forgone value from value delta, and check the strongest countercase before deciding.

Risk: Using the full analysis on trivial, mandatory, or cheaply reversible work can waste time or create false rigor.

Mitigation: Apply the documented over-application guard: skip full accounting for mandatory or trivial work and evaluate only current-state forward-looking tradeoffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-opportunity-cost)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown or structured text decision analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a concise opportunity-cost comparison with alternatives, best forgone value, value delta, permanent versus temporary losses, decision, and countercase.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
