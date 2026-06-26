## Description: <br>
Processes receipt photos and PDFs, extracts vendor, date, amount, and currency, converts expenses to EUR, uploads receipts to Google Drive, and logs them to Google Sheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marinhobot](https://clawhub.ai/user/marinhobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, and small businesses in Spain use this skill to turn receipt photos, PDFs, or text descriptions into EUR-normalized expense records, Drive copies, and quarterly summaries for tax-accountant workflows. <br>

### Deployment Geography for Use: <br>
Spain <br>

## Known Risks and Mitigations: <br>
Risk: Receipt images and expense metadata may contain sensitive financial or personal information. <br>
Mitigation: Use a dedicated private Google Drive folder and Google Sheet, authenticate gog yourself, and review receipts for sensitive information before processing. <br>
Risk: Local CSV logs can expose expense metadata if stored in shared, synced, or committed directories. <br>
Mitigation: Set RECEIPT_LOG_FILE outside shared or committed paths and keep receipt logs excluded from source control. <br>
Risk: Uploads and sheet appends create copies of receipt data on Google services. <br>
Mitigation: Confirm the Google account, Drive folder ID, and Sheet ID before running upload or logging commands. <br>


## Reference(s): <br>
- [Receipt Snap ClawHub page](https://clawhub.ai/marinhobot/receipt-snap-spain) <br>
- [marinhobot ClawHub publisher profile](https://clawhub.ai/user/marinhobot) <br>
- [gog CLI](https://github.com/faradayhq/gog) <br>
- [Open Exchange Rate API endpoint used by the skill](https://open.er-api.com/v6/latest/{currency}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration steps, and receipt-processing confirmations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the bundled Python script may create or update Google Drive files, Google Sheet rows, and a local CSV receipt log.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
