## Description: <br>
Standardizes Chinese banking bid-response Word and Markdown documents with Word Heading 1-5 and Normal styles, GB/T 9704-compatible formatting, section renumbering, review, conversion, and validation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyonghui0810](https://clawhub.ai/user/wuyonghui0810) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Banking proposal teams, bid writers, and developers use this skill to standardize Chinese bid-response documents, review formatting compliance, renumber sections, convert Markdown drafts to Word documents, and validate numbering patterns before submission. <br>

### Deployment Geography for Use: <br>
Chinese mainland <br>

## Known Risks and Mitigations: <br>
Risk: Formatting commands can overwrite the selected output path or produce unintended document changes. <br>
Mitigation: Run review or dry-run first on important files and keep backups before applying formatting changes. <br>
Risk: Bid and proposal documents may contain confidential business information. <br>
Mitigation: Process documents in a trusted local workspace and avoid sharing or committing sensitive input files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuyonghui0810/vkey-bid-standardizer) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Standard profile configuration](artifact/vkey_bid_standardizer/profiles/standard.json) <br>
- [Bid blank Markdown template](artifact/templates/bid_blank.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands; generated artifacts are Word documents, Markdown-derived Word documents, or JSON review reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes user-supplied local Word or Markdown files through configurable document-standardization profiles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
