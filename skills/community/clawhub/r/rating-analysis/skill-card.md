## Description:

Analyzes an Amazon ASIN’s star-rating distribution and changes over time to help identify possible causes of rating declines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product operators use the skill to inspect an ASIN’s star distribution and rating trends, and to investigate when negative reviews cluster. It requires an ARI API key to access account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis or collection may consume ARI credits without fresh approval, including after an unanswered quote or during an operation described as a free preview.

Mitigation: Set the ARI account to ask before every charge and verify the setting. Use the dedicated quote command for pricing; do not rely on omitting --confirm to prevent charges.

Risk: An existing recurring collection schedule can continue to incur charges.

Mitigation: Review existing schedules before use and choose manual collection for a one-time request.

## Reference(s):

- [ARI API and command reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Concise analysis and reports, with star distributions and time trends where data is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conclusions depend on the available review sample and time coverage.]

## Skill Version(s):

1.5.3 (source: release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
