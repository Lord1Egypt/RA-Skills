## Description:

Generates a daily 21:30 fixed-income-plus product review report covering 87 products, full data dashboards, top and bottom 3 attribution analysis, and track rankings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wesdaliang](https://clawhub.ai/user/wesdaliang)

### License/Terms of Use:

MIT-0

## Use Case:

Investment analysts and reporting agents use this skill to query Wind data for a fixed-income-plus product universe, rank products by track, and prepare a daily Markdown review with attribution notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent every-60-second cron job may automatically post financial reports to an unspecified chat channel.

Mitigation: Verify the cron job ID, payload, destination channel, and deletion controls before enabling automatic posting.

Risk: The workflow references global memory as a possible product-list source, which can introduce unreviewed or stale data.

Mitigation: Prefer the packaged product list or an approved authoritative source, and remove the MEMORY.md dependency if the packaged list is sufficient.

Risk: Wind API quota or timeout limits can lead to incomplete data collection for the 87-product report.

Mitigation: Confirm Wind API quota impact, batch queries by track or data type, and require completeness checks before publishing.

## Reference(s):

- [Product Codes](references/product_codes.md)
- [Wind Functions](references/wind_functions.md)
- [ClawHub Skill Page](https://clawhub.ai/wesdaliang/skills/xqant-daily-gushouplus-report)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, attribution notes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires complete 87-product Wind data, strict product-code validation, and report tables that omit product codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
