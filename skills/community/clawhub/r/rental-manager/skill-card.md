## Description: <br>
Rental Manager helps manage rental bookkeeping for Quebec, Levis, and Longueuil properties, including income and expense records, receipt uploads, T776 tax preparation, and LOC tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clairproqc-star](https://clawhub.ai/user/clairproqc-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Property owners or rental managers use this skill to keep rental income, expenses, receipts, tax categories, and LOC activity organized for the listed Quebec rental properties. <br>

### Deployment Geography for Use: <br>
Canada (Quebec) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move and rename Google Drive files and update Google Sheets through the user's configured Google account. <br>
Mitigation: Use it only with the intended Google account and confirm the property, receipt file, filename, and target sheet row before allowing Drive or Sheets changes. <br>
Risk: The skill contains fixed Google Sheet IDs and Drive folder IDs for specific rental properties. <br>
Mitigation: Install it only if those property records and folders are yours or expected, and update the reference file before use if any ID is stale. <br>


## Reference(s): <br>
- [Rental Properties Reference](references/properties.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clairproqc-star/rental-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Google Drive and Google Sheets actions executed through the gog CLI when receipt handling is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gog to be installed and authenticated to the intended Google account before Drive or Sheets changes are made.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
