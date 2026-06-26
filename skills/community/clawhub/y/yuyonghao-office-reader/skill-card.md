## Description: <br>
Office Reader helps an agent read local Word, Excel, PowerPoint, PDF, Markdown, text, CSV, JSON, YAML, and HTML files and return parsed contents or summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using agents to inspect local Office and document files can ask the agent to extract readable text, tabular previews, or summaries from selected files. The skill is useful for reviewing document contents in an agent session while keeping file selection under user control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local document contents may appear in the agent chat. <br>
Mitigation: Confirm file paths before opening private files and avoid reading sensitive documents unless the user intends their contents to be processed in the session. <br>
Risk: The artifact references an office-reader.ps1 script and Python dependencies that are not included in this package. <br>
Mitigation: Verify any separate script and install dependencies from trusted sources before executing document-reading commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-office-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown extracted from local files, with PowerShell command examples when script use is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a file path, output format, and maximum line count; artifact documentation describes a default 1000-line output cap.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
