## Description: <br>
Queries a database API, analyzes selected table data, and generates a multi-section Word analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rm-ra](https://clawhub.ai/user/rm-ra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query authorized database tables, summarize incident-style records, and produce a Word report with counts, categories, dates, organizations, contact fields, conclusions, and raw rows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query sensitive database records, including police-style incident data. <br>
Mitigation: Use only an authorized, preferably read-only database endpoint and limit queries to approved tables and fields. <br>
Risk: The examples use broad SQL patterns such as SELECT * that may expose unnecessary sensitive columns. <br>
Mitigation: Replace broad queries with explicit field lists and filters before running the skill. <br>
Risk: The analysis script includes hard-coded sample incident data and writes raw rows into the generated report. <br>
Mitigation: Replace sample data with user-approved query input and redact personal identifiers before export. <br>
Risk: The script persists the report to a fixed Word document path. <br>
Mitigation: Choose an explicit output location and retention policy before generating reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rm-ra/sql-doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and Python code references; generated runtime artifact is a Word document.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report output to a fixed .docx path unless the script is changed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
