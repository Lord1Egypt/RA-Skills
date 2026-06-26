## Description: <br>
Tracks personal expenses from natural-language entries, automatically categorizes spending, checks budgets, answers monthly spending questions, and generates monthly reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baoxinwen](https://clawhub.ai/user/baoxinwen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to record personal spending, query totals by month or category, monitor a monthly budget, and generate HTML or CSV spending reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal financial records stored in local JSON, HTML, and CSV files. <br>
Mitigation: Treat generated data and reports as sensitive records, restrict file access, and keep a user-controlled backup before relying on the data. <br>
Risk: The artifact describes automatic monthly report delivery and a fixed backup path. <br>
Mitigation: Review and change the backup location before installation, and enable scheduled report delivery only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baoxinwen/spending-log) <br>
- [Publisher profile](https://clawhub.ai/user/baoxinwen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Plain text or Markdown responses with Python script commands, plus generated HTML and CSV report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local JSON expense records and can generate report files for delivery through OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
