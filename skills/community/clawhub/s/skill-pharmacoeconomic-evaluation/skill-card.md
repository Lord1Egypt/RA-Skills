## Description:

This skill provides comprehensive guidance and tools for conducting pharmacoeconomic evaluations including cost-effectiveness analysis (CEA), cost-utility analysis (CUA), cost-benefit analysis (CBA), sensitivity analysis, and decision-analytic model construction (Markov, decision tree, DES, PSM). Follows ISPOR Good Practices for Outcomes Research Reports. Use this skill for HTA projects, drug pricing, reimbursement decisions, and health economic research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlb1201](https://clawhub.ai/user/tlb1201)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and health economics analysts can use this skill to plan pharmacoeconomic evaluations, calculate ICERs and QALYs, run sensitivity analyses, and structure decision-analytic models for HTA, pricing, reimbursement, and health economic research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions include an unpinned placeholder npx command.

Mitigation: Review before installing and prefer manual installation from this reviewed package or a pinned, verified release.

Risk: The skill may overstate analytical capabilities or produce misleading pharmacoeconomic guidance if used without expert review.

Mitigation: Treat calculators as basic aids and independently verify methods, assumptions, parameter sources, and results.

Risk: Economic conclusions depend on jurisdiction-specific thresholds, currencies, and dependency versions.

Mitigation: Explicitly set the jurisdiction, willingness-to-pay threshold, currency, and dependency versions for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tlb1201/skills/skill-pharmacoeconomic-evaluation)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Cost-effectiveness analysis script](artifact/scripts/cost_effectiveness_analysis.py)
- [Monte Carlo simulation script](artifact/scripts/monte_carlo_simulation.py)
- [Budget impact analysis script](artifact/scripts/budget_impact_analysis.py)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python code examples and reusable script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires users to supply jurisdiction, willingness-to-pay threshold, currency, parameter sources, and dependency versions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
