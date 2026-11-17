## Description:

Automated abstract screening tool for systematic literature reviews with PRISMA workflow support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, systematic-review teams, and developers use this skill to screen academic abstracts against configurable inclusion and exclusion criteria, then generate reviewable inclusion, exclusion, conflict, PRISMA, and audit-log outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency file lists unconstrained yaml and dataclasses packages, which can create unsafe or incompatible installs.

Mitigation: Install in an isolated virtual environment after replacing yaml with a pinned PyYAML version and removing or constraining dataclasses.

Risk: CSV report handling and user-supplied reference data may create safety or data-handling risks.

Mitigation: Prefer JSON output for untrusted reference data, inspect generated files before sharing, and keep input and output paths workspace-scoped.

Risk: Automated abstract screening can make incorrect inclusion or exclusion recommendations.

Mitigation: Treat results as recommendations only, confirm language restrictions and confidence thresholds, and require human review for final study decisions.

## Reference(s):

- [Criteria Template](references/criteria_template.yaml)
- [Sample References](references/sample_references.csv)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts may be CSV or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces included, excluded, conflict, PRISMA data, and screening log outputs when the packaged script is run.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md Version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
