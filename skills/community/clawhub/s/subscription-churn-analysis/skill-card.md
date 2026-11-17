## Description:

Scores US subscription accounts against churn risk criteria and groups the accounts most likely to leave by reason and renewal date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US SaaS customer success leads, founders, and revenue operations teams use the skill to assess account churn risk and organize retention follow-up by driver and renewal timing.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The scoring logic can produce unreliable churn rankings.

Mitigation: Do not rely on generated scores for customer-retention decisions until input mappings, missing-data handling, grouping, and renewal ordering are corrected and validated.

Risk: The optional Windows app is a separate download and requires a separate trust decision.

Mitigation: The Python workflow does not require the Windows app; only download or run it if you independently decide to trust it.

## Reference(s):

- [US subscription churn analysis](references/churn-analysis.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV, Code]

**Output Format:** [Markdown churn analysis and scores, using a CSV account template and a Python scoring script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account-level risk scores, risk drivers, reason groupings, renewal timing, and data gaps; generated rankings are unreliable until the scoring logic is corrected and validated.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
