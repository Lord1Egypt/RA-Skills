## Description: <br>
Recognizes receipt photos, categorizes expenses, saves them to expenses.csv, and generates monthly spending reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nick4man](https://clawhub.ai/user/nick4man) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn receipt images into categorized expense records and monthly spending summaries. It is intended for personal or household expense tracking workflows that store results in a workspace CSV file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Nextcloud helper contains plaintext credentials and under-documented remote storage access. <br>
Mitigation: Do not use the helper as-is; remove embedded credentials, rotate the credential if it is real, and configure storage access through reviewed secrets management. <br>
Risk: Receipt photos and expenses.csv can contain sensitive spending history. <br>
Mitigation: Process only receipts the user is comfortable sending to the configured model provider and protect or delete the retained CSV according to the user's data retention needs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nick4man/receipt-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON extraction records, CSV expense rows, and Python or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses receipt images as input and appends extracted Date, Item, Category, and Price records to expenses.csv.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
