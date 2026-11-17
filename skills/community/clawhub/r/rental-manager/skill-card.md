## Description:

Rental bookkeeping for Quebec, Levis, and Longueuil properties, including income and expense records, receipt uploads to Google Drive, T776 preparation, and LOC tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clairproqc-star](https://clawhub.ai/user/clairproqc-star)

### License/Terms of Use:

MIT-0

## Use Case:

Property owners or managers use this skill to maintain rental bookkeeping records for Quebec-area properties, attach receipts in Google Drive, prepare T776 tax summaries, and track LOC drawdowns and interest.

### Deployment Geography for Use:

Canada (Quebec)

## Known Risks and Mitigations:

Risk: The skill can make persistent Google Drive and Sheets changes, including moving or renaming files and updating spreadsheet links.

Mitigation: Use a Google account limited to the intended rental folders and sheets, and require confirmation before receipt uploads, Drive renames or moves, and spreadsheet updates.

Risk: A supplied file ID could point outside the expected receipt staging or upload location.

Mitigation: Validate file IDs against a trusted upload or staging location before moving or renaming Drive files.

Risk: Receipt links could be attached to the wrong spreadsheet row if the index is stale or incorrect.

Mitigation: Check the spreadsheet index and target tab before updating the File Link column.

## Reference(s):

- [Rental Properties Reference (2026)](references/properties.md)
- [ClawHub Rental Manager Skill](https://clawhub.ai/clairproqc-star/skills/rental-manager)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance and JSON-style status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can result in persistent Google Drive file changes and Google Sheets updates when connected to the required gog command-line tool.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
