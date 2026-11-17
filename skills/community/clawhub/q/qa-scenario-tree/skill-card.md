## Description:

Turns decomposed requirements into traceable main, alternate, exception, and data-flow test scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA practitioners use this skill to turn a requirements breakdown into a scenario tree covering normal, alternate, exception, and data-flow paths, with each scenario linked to its requirement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scenario examples may expose customer, identity, payment, or production data.

Mitigation: Use synthetic or masked data rather than real customer information or financial records.

Risk: The optional command to install the broader skill set uses an unpinned package source.

Mitigation: Review the source and use a pinned version or trusted release before installing.

## Reference(s):

- [Scenario tree and description template](assets/scenario-template.md)
- [Scenario types and construction guidance](references/scenario-types.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-scenario-tree)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown scenario tree and scenario descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unique SC- IDs linked to REQ- IDs; notes uncovered paths and reasons; does not produce detailed test cases.]

## Skill Version(s):

1.8.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
