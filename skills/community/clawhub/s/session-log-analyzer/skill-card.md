## Description: <br>
Analyze agent session logs and generate PDF reports with Notion sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to summarize agent session logs into PDF reports and optionally sync report excerpts to a Notion database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs and generated reports can contain sensitive operational details or errors. <br>
Mitigation: Review and redact reports before sharing or syncing them outside the local environment. <br>
Risk: Optional Notion sync sends report excerpts to a configured Notion database using sensitive credentials. <br>
Mitigation: Use a least-privilege Notion integration scoped to the target reports database and protect the Notion API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/session-log-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Shell commands, Configuration, API Calls] <br>
**Output Format:** [PDF report, terminal status text, and optional Notion page] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyzes JSONL session logs and, when configured, syncs the first 2000 characters of extracted report text to Notion.] <br>

## Skill Version(s): <br>
99.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
