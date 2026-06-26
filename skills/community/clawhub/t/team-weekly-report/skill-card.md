## Description: <br>
Collects team weekly report images, extracts work items, groups them by department management and project management, compares current work against last week's plans, and generates a plain-text team weekly report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gotoloops](https://clawhub.ai/user/gotoloops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team leads use this skill to collect weekly status updates from report images, organize them into department and project views, compare them with the previous week's plans, and prepare a concise team weekly report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weekly reports may include names, work details, plans, and hours that are saved locally under memory/weekly-reports. <br>
Mitigation: Use the skill only where local storage of that report content is acceptable, and delete old weekly JSON files when retention or privacy requirements call for it. <br>
Risk: OCR extraction, category assignment, or week-over-week comparison can be inaccurate when source images are unclear or work items are ambiguous. <br>
Mitigation: Review collected entries and generated summaries before sharing or relying on the report. <br>


## Reference(s): <br>
- [Report template](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Plain text weekly report with local JSON weekly-report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores weekly report data locally in memory/weekly-reports and summarizes only missing or newly added items in the comparison section.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
