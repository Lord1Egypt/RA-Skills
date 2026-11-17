## Description:

Vendor Compliance 1099 helps accounting firms pull full-year QBO General Ledger data, aggregate vendor payments, apply IRS 1099 thresholds and classifications, track W-9/TIN status, and produce an 8-tab Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External accounting and tax preparer users use this skill for year-end 1099 compliance runs, W-9 tracking, IRS threshold checks, and vendor payment review for U.S. entities.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The workflow handles sensitive accounting and tax records in generated workbooks and local cache files.

Mitigation: Keep .cache/vendor-compliance-1099/ and generated workbooks out of source control and shared folders, and handle them as sensitive client tax records.

Risk: The workflow reads full-year QBO General Ledger data for a client.

Mitigation: Install and run it only where QBO access is appropriate for the client and configured as read-only.

Risk: Dependency setup can affect repeatability of financial compliance runs.

Mitigation: Use a pinned dependency set in a virtual environment before running the pipeline.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/vendor-compliance-1099)
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash command examples and generated Excel workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces VendorCompliance_1099_{slug}_{year}.xlsx and local JSON cache files; requires QBO General Ledger access and openpyxl.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
