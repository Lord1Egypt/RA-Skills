## Description: <br>
Extracts sales data from report images using OCR, parses structured JSON with a MiniMax-compatible API, and exports results to Excel spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoutianwang](https://clawhub.ai/user/zhoutianwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to process sales report images, extract standard sales fields, and produce JSON or Excel outputs for review and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sales report contents are sent to a MiniMax-compatible API for parsing. <br>
Mitigation: Use only data approved for that service and configure the API endpoint according to organizational data-handling requirements. <br>
Risk: API keys can be exposed through command history or shared terminal sessions when passed as command-line arguments. <br>
Mitigation: Run in a controlled environment and avoid storing or sharing shell history that contains secrets. <br>
Risk: OCR text and generated spreadsheets may include sensitive business data and can appear in logs or terminal output. <br>
Mitigation: Restrict access to run logs, JSON outputs, and Excel files; delete intermediate files when they are no longer needed. <br>
Risk: Unpinned dependencies may change behavior or introduce supply-chain risk. <br>
Mitigation: Install in a virtual environment and pin and review dependency versions before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhoutianwang/sales-report-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python commands; generated JSON and Excel files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include OCR text in terminal logs, structured sales-data JSON, and .xlsx spreadsheets.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
