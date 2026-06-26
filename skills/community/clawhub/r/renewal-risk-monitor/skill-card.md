## Description: <br>
Identifies renewal risk signals and separates recoverable issues from high-probability churn signs for renewal, risk, and customer-success workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success and renewal teams use this skill to turn customer usage, feedback, and interaction history into a structured renewal-risk review. It highlights risk signals, recoverable items, high-risk factors, suggested actions, time windows, escalation criteria, and missing information for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer renewal inputs may contain sensitive customer, personal, or commercial data. <br>
Mitigation: Redact sensitive customer or personal data where possible before use, and keep processing limited to explicit local input files. <br>
Risk: The generated renewal-risk assessment could be mistaken for a final business decision. <br>
Mitigation: Treat the output as a review draft and require human confirmation before making renewal, escalation, or account-action decisions. <br>
Risk: The local script can write reports to a user-selected output path. <br>
Mitigation: Review the output path before writing and use dry-run or stdout when a persisted report is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/renewal-risk-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](artifact/README.md) <br>
- [Output Template](artifact/resources/template.md) <br>
- [Structured Specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown by default, with optional JSON report output from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a user-selected local output file; otherwise prints the review draft to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
