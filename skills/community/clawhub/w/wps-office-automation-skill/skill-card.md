## Description: <br>
Automates local processing of documents, spreadsheets, presentations, and PDFs for generation, polishing, contract review, data analysis, charting, conversion, extraction, merging, and splitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyuanhua](https://clawhub.ai/user/zyuanhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and office users use this skill to automate local document, spreadsheet, presentation, and PDF workflows without external API keys. Typical tasks include drafting official documents, polishing text, reviewing contracts, cleaning and analyzing spreadsheets, generating charts and presentations, and converting or restructuring PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local office files and can be given broad file paths. <br>
Mitigation: Restrict input and output paths to reviewed workspace locations, and require user review before processing arbitrary paths. <br>
Risk: The changelog includes an upgrade cleanup command that deletes environment files. <br>
Mitigation: Run cleanup commands only after confirming backups exist and the files are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zyuanhua/wps-office-automation-skill) <br>
- [README](artifact/README.md) <br>
- [Deployment guide](artifact/DEPLOYMENT.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [JSON response with status, message, structured data, and optional base64-encoded file data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated file names and base64 payloads for office documents, spreadsheets, presentations, or PDFs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact files report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
