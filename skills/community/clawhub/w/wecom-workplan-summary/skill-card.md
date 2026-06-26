## Description: <br>
Summarizes weekly or monthly team work-plan records from pasted table data or an authorized WeCom smart sheet into concise natural-language reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team leads use this skill to summarize team work-plan records for weekly or monthly review. It converts structured plan entries into person-by-person summaries with goal alignment, suggestions, and missing-submission notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a fixed WeCom smart sheet containing team work-plan records. <br>
Mitigation: Install and run it only when authorized to access that sheet and process those records. <br>
Risk: In pasted-data mode, work-plan data may be written temporarily to /tmp/workplan_paste.tsv. <br>
Mitigation: Delete the temporary file after use or use a private temporary path in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/wecom-workplan-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with supporting shell commands and structured text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read an authorized WeCom smart sheet or process pasted TSV/CSV work-plan data before producing the final report.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
