## Description: <br>
Automate repetitive computer tasks including file operations, data processing, web scraping, and API integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to automate repetitive file, data conversion, API sync, web monitoring, scheduling, and e-commerce workflows with configurable tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation runner can move or overwrite files when executing file organization and conversion tasks. <br>
Mitigation: Use --dry-run first, review exact source and destination paths, avoid broad or sensitive folders, and require confirmation before moving or overwriting files. <br>
Risk: API, e-commerce, email alert, and scheduled workflows can affect external systems or repeat unintended actions. <br>
Mitigation: Do not connect real endpoints, credentials, stores, alerts, or scheduled jobs until endpoints, credentials, rate limits, and rollback plans are explicit. <br>
Risk: The skill is broad and was flagged suspicious by ClawScan because it combines file operations with API and scheduled workflow guidance. <br>
Mitigation: Supervise executions closely, inspect task configuration before use, and keep credentials in environment variables rather than committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinanping-CPU/yinan-task-automator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task execution may create log files and can move, overwrite, or write files when run outside dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
