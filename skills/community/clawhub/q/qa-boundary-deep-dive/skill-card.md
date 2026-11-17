## Description:

Helps QA teams identify and prioritize edge cases across input, state, time, and resource boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to find testable boundary cases in a scenario tree, assign risk-based test depth, and link each case to an expected result and scenario ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real customer, identity, payment, or production data may be exposed when supplying test scenarios.

Mitigation: Use synthetic or masked examples instead of pasting sensitive production data.

Risk: The suggested unpinned installation command may install the publisher's broader skill suite.

Mitigation: Review and trust the publisher and the full suite before choosing to run the installation command.

## Reference(s):

- [Boundary analysis table template](assets/boundary-table.md)
- [Four-dimension boundary reference](references/four-dimensions.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-boundary-deep-dive)

## Skill Output:

**Output Type(s):** [Markdown, QA test guidance]

**Output Format:** [Markdown boundary-analysis table and dimension-specific checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven table columns; unique boundary IDs, risk levels, test depth, expected results, linked scenario IDs, and reasons for uncovered dimensions.]

## Skill Version(s):

1.8.0 (source: skill metadata and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
