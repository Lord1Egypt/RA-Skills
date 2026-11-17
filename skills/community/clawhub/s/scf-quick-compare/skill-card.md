## Description:

Period-over-period variance analysis on the Statement of Cash Flows pulled from QuickBooks Online, producing a four-tab Excel workbook with summary, detail, flagged variances, and change-data-capture log outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting teams use this skill to compare QuickBooks Online Statement of Cash Flows periods during monthly close, YTD review, or cash-swing investigation. It highlights material operating, investing, and financing cash-flow changes and records line-item changes across runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workbooks and local CDC cache files may contain sensitive client financial data.

Mitigation: Run only in an environment approved for client financial data, keep outputs out of shared or synced locations unless approved, and treat the local cache as confidential.

Risk: The workflow depends on QuickBooks Online credentials and a Python Excel dependency.

Mitigation: Use a managed or pinned Python environment for openpyxl and ensure QBO credentials are configured only in the intended runtime environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and generated Excel workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a four-tab workbook with Summary, Detail, Flags, and CDC Log sheets; local cache data should be handled as confidential financial information.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
