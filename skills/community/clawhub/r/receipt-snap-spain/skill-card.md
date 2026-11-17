## Description:

Receipt Snap processes receipt photos, PDFs, and text descriptions by extracting expense details, converting non-EUR amounts, saving receipt files to Google Drive, and logging rows to Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marinhobot](https://clawhub.ai/user/marinhobot)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as freelancers and small businesses in Spain use this skill to organize expense receipts for tax reporting. It helps an agent collect receipt data, convert currencies, upload receipt files, maintain a Google Sheets log, and prepare quarterly summaries.

### Deployment Geography for Use:

Spain

## Known Risks and Mitigations:

Risk: Receipt files and expense metadata are stored in user-configured Google Drive, Google Sheets, and a local CSV log.

Mitigation: Use only a trusted gog-authenticated Google account, verify the configured folder and sheet IDs, and protect or disable the local log on shared machines.

Risk: Receipt extraction, categorization, and quarterly summaries may be incomplete or incorrect for tax filing.

Mitigation: Review extracted vendor, date, amount, currency, category, and summary totals before sharing records with a tax accountant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marinhobot/skills/receipt-snap-spain)
- [Publisher profile](https://clawhub.ai/user/marinhobot)
- [gog CLI](https://github.com/faradayhq/gog)
- [Exchange rate API endpoint](https://open.er-api.com/v6/latest/{currency})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CSV/Google Sheets row data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local CSV receipt logs and Google Drive/Sheets records when the user runs the helper script with configured credentials.]

## Skill Version(s):

1.0.6 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
