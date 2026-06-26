## Description: <br>
Generates natural Chinese daily, weekly, monthly, and annual work reports from keywords or casual notes, using prior saved reports to build higher-level summaries when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwu2495](https://clawhub.ai/user/jiuwu2495) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to turn casual Chinese notes or keywords into daily, weekly, monthly, or annual work summaries. It is designed for work-report drafting, including rollups from previously saved reports when those files are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and reuses prior reports stored under .workbuddy/reports/. <br>
Mitigation: Avoid storing confidential details in that folder unless it is excluded from commits, sync, and shared workspaces. <br>
Risk: Generated reports may be saved as workspace files and later reused in higher-level summaries. <br>
Mitigation: Review the generated report before saving and remove sensitive or inaccurate content from stored reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuwu2495/work-report-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jiuwu2495) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Chinese Markdown work reports with concise guidance and optional file-save shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save daily, weekly, monthly, and annual reports under .workbuddy/reports/ after user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
