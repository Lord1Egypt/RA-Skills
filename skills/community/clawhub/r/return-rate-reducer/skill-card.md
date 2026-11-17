## Description:

Reduce e-commerce return rates through data-driven root-cause analysis, product-page fixes, and policy optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, merchandising teams, CX teams, and analysts use this skill to diagnose high return rates, identify top return drivers, and prioritize product-page, policy, and measurement fixes across retail categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returns CSVs, product-page files, and generated reports may contain sensitive business data.

Mitigation: Treat inputs and generated Markdown as business data, and review reports before sharing them outside the intended team.

Risk: Return-rate calculations can be misleading if the total order count is missing or inaccurate.

Mitigation: Provide the total order count explicitly when using the analyzer so rates are calculated against the correct denominator.

Risk: Generated Markdown reports from untrusted CSV content may be unsafe in permissive Markdown viewers.

Mitigation: Review generated Markdown before rendering or publishing it, especially when source CSVs come from untrusted locations.

## Reference(s):

- [Return Reduction Playbook](artifact/references/return_reduction_playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/rijoyai/skills/return-rate-reducer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports, tables, prioritized recommendations, and local script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May analyze user-provided returns CSVs and product-page Markdown; accurate return-rate calculations require explicit total order counts.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
