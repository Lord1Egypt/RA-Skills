## Description: <br>
Processes uploaded hot-news Excel files by parsing worksheets, saving structured JSON, and producing categorized Markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horizoncove](https://clawhub.ai/user/horizoncove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to process uploaded hotspot-news Excel workbooks, extract worksheet-level categories, and generate concise daily news summaries with a saved JSON record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes a local parser script for uploaded Excel content. <br>
Mitigation: Install or run it only after reviewing and trusting /workspace/scripts/read_hotnews.py and the uploaded workbook source. <br>
Risk: Parsed Excel contents may be persisted under /workspace/data and logs may be written under /workspace/logs. <br>
Mitigation: Keep only necessary generated JSON and log files, and delete them when they are no longer needed. <br>
Risk: The documented cron entry enables recurring background processing. <br>
Mitigation: Disable or omit the cron configuration unless daily automated processing is intentional. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/horizoncove/yuheng-hotnews-excel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with categorized bullet lists, plus a saved JSON data file and optional shell or cron commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save complete parsed data under /workspace/data and append cron output under /workspace/logs when recurring processing is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
