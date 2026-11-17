## Description:

Calculates month-accurate Social Security benefit factors, break-even ages, earnings-test effects, and longevity-based comparisons for different claiming ages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People nearing Social Security eligibility, couples coordinating survivor benefits, and financial professionals use it to compare claiming ages and break-even outcomes using birth year, PIA, earnings, and longevity assumptions.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Nonzero discount-rate comparisons may be misleading because annual rates can be treated as monthly rates.

Mitigation: Keep the discount at 0 unless rate handling has been verified, and confirm benefit details and current earnings-test limits with the Social Security Administration before relying on the results.

## Reference(s):

- [Claiming Strategy Reference Guide](references/claiming-strategy-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Plain-text tables, break-even ages, and longevity-based verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
