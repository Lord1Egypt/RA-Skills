## Description: <br>
Exports WeChat Channels customer data reports by calling Da-Mai API endpoints for short video, live video, private message, and heating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or operators in an authorized Da-Mai/OpenClaw environment use this skill to export customer-specific WeChat Channels reports for downstream analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can export internal customer WeChat data, including private-message data. <br>
Mitigation: Run it only in an authorized Da-Mai/OpenClaw environment for customers and data categories the operator is explicitly allowed to access. <br>
Risk: Authorization, privacy, and retention controls are not clearly documented in the artifact. <br>
Mitigation: Add authentication and authorization checks, define retention or secure deletion for exported files, and review private-message exports before operational use. <br>
Risk: Debug output can expose request URLs and customer identifiers. <br>
Mitigation: Redact logged URLs and sanitize filenames or report contents before sharing logs or generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/wechat-data-exporter) <br>
- [Publisher profile](https://clawhub.ai/user/ahsbnb) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Excel files and a JSON report path emitted in terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes exported data under the OpenClaw workspace data directory and prints REPORT_PATH for downstream tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
