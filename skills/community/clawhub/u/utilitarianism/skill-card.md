## Description:

Activate when users need to evaluate a policy, product, or organizational decision affecting multiple parties, compare benefits and harms, or conduct cost-benefit or ethical trade-off analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external decision-makers can use this skill to map affected parties, estimate welfare impacts, examine aggregation assumptions, and compare the net effects of choices. It is intended for multi-party decisions and cost-benefit or ethical trade-off analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Numerical examples or welfare assumptions may lead to misleading conclusions if treated as settled facts.

Mitigation: Verify figures, conversion rates, and assumptions; state uncertainty and test how sensitive the conclusion is to the most contested assumption.

Risk: Aggregating total welfare can obscure severe harms to a smaller affected group or unaddressed rights constraints.

Mitigation: Map cost-bearing and underrepresented parties, identify rights constraints, and report the option with the best minimum welfare alongside the aggregate result.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/deciqai/skills/utilitarianism)
- [Primary sources and further reading](artifact/references/sources.md)
- [EPA Clean Air Act benefits and costs](https://www.epa.gov/clean-air-act-overview/benefits-and-costs-clean-air-act)
- [Bentham, An Introduction to the Principles of Morals and Legislation](https://archive.org/details/anintroductiont01bentgoog)
- [Mill, Utilitarianism](https://archive.org/details/utilitarianism00mill)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with a structured Utilitarian Welfare Map]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maps affected parties and welfare impacts, states aggregation assumptions, ranks options, and identifies a contested assumption for sensitivity analysis.]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
